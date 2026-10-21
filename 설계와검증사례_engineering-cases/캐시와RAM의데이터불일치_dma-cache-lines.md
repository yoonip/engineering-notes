# 캐시와 RAM의 데이터 불일치 / DMA visibility and shared cache-line corruption

CPU 코드가 읽은 값이 맞는데 DMA가 이전 값을 보낼 수 있습니다. 반대로 DMA가 RAM을 갱신했는데 CPU는 캐시의 옛 값을 읽을 수 있습니다. 이 사례는 두 저장 공간을 따로 둔 실행 모델에서 TX·RX·dirty 사본·공유 line의 이웃 데이터 문제를 분리합니다.

[실행 코드](../예제_examples/실무검증_practical-validation/interrupt_dma/models.py), [자체 입력과 검사](../예제_examples/실무검증_practical-validation/interrupt_dma/README.md), [검증 기록](검증기록_evidence/인터럽트DMA캐시모델검증_20261021.md)을 연결했습니다. 실제 Cortex-M7·DMA·캐시 명령·성능을 측정한 것이 아닙니다. 자동 캐시 일관성이 없는 write-back 구성을 이해하기 위한 결정적인 Python 모형입니다.

## 1. 같은 주소의 값이 한 곳에만 있지는 않습니다

RAM은 DMA가 접근하는 메모리이고, 캐시는 CPU가 가까이 두는 복사본입니다. write-back 정책에서는 CPU 쓰기가 캐시에 먼저 반영되고 RAM에는 아직 이전 값이 남을 수 있습니다. dirty는 RAM에 반영되지 않은 CPU 변경이 있다는 표시입니다. CPU 읽기에 최신처럼 보여도 다른 master가 보는 값과 다를 수 있습니다.

clean은 dirty 사본을 메모리 쪽으로 반영하는 유지 연산이고, invalidate는 캐시 사본을 버려 다음 접근에서 다시 읽게 하는 연산입니다. 둘의 목적은 다릅니다. ST AN4839는 DMA에 넘기기 전의 반영과 DMA가 쓴 메모리를 CPU가 읽기 전의 처리를 구분합니다. [AN4839 공식 원문](https://www.st.com/resource/en/application_note/an4839-level-1-cache-on-stm32f7-series-and-stm32h7-series-stmicroelectronics.pdf)

모형은 128바이트 RAM과 32바이트 단위 캐시 복사본을 사용합니다. CPU는 캐시를 통해 읽고 쓰며 DMA는 RAM만 읽고 씁니다. 실제 cache way·교체 정책·store buffer·버스 지연을 구현하지 않았습니다. 코드의 clean은 모형 line 전체를 RAM에 쓰는 추상 동작이며 실제 명령의 버스 동작을 측정한 결과는 아닙니다.

## 2. TX clean 누락과 오래된 RAM 데이터

입력 바이트는 `11 22 33 44`이고 RAM의 초기값은 0입니다. CPU가 이 네 바이트를 캐시에 쓰면 dirty가 됩니다.

| TX 경로 | CPU가 읽는 바이트 | DMA가 RAM에서 읽는 바이트 |
| --- | --- | --- |
| 사전 clean 없음 | `11223344` | `00000000` |
| 사전 clean 적용 | `11223344` | `11223344` |

```python
memory.cpu_write(address, payload)     # CPU 저장으로 캐시를 바꾸고 dirty로 표시합니다.
memory.clean(address, len(payload))    # len은 바이트 수이며 전송 전에 RAM에 반영합니다.
sent = memory.dma_read(address, len(payload))  # DMA가 보는 RAM 값을 따로 읽습니다.
```

`volatile`이나 순서 barrier를 썼다는 사실만으로 캐시의 dirty 값을 자동으로 RAM에 반영했다고 판단하지 않습니다. DMA가 버퍼를 읽는 동안 CPU가 같은 payload를 다시 바꾸면 clean을 한 번 했어도 다른 문제가 생깁니다. [완료 버퍼의 소유권](상태비트소거와완료버퍼소유권_irq-w1c-ownership.md)과 캐시 가시성은 각각의 계약입니다.

## 3. RX에서는 완료 뒤 오래된 사본을 버립니다

RX 입력은 `31 32 33 34`입니다. 모형은 사전 전용 line 처리를 한 뒤 DMA가 쓰기 전에 오래된 clean 복사본이 채워지는 사건을 가정합니다. 그 후 DMA는 RAM을 갱신합니다. 이 채움은 사후 처리를 분리하기 위한 모형 사건이며 실제 speculative read를 관측한 것도, DMA 소유 중 CPU 코드가 버퍼를 읽어도 된다는 뜻도 아닙니다.

| RX 경로 | DMA가 쓴 RAM | CPU가 최종적으로 읽는 값 |
| --- | --- | --- |
| 사후 invalidate 없음 | `31323334` | `00000000` |
| 완료 확인 뒤 invalidate | `31323334` | `31323334` |

사전 처리도 별도의 이유가 있습니다. CPU가 이전 값 `07 07 07 07`을 dirty 사본으로 가지고 있는데 DMA가 RAM에 새 값을 쓰면, 나중에 그 dirty 사본을 clean하거나 내보내면서 새 DMA 결과를 덮을 수 있습니다. 이 오류 경로의 RAM과 CPU 최종값은 모두 `07070707`이었습니다. 반면 DMA에 넘기기 전에 해당 전용 line의 dirty 상태를 정리한 경로는 `31323334`를 유지했습니다.

따라서 “DMA 뒤에는 무조건 clean+invalidate”라는 규칙으로 합치지 않습니다. TX/RX 방향, 사전 dirty 상태, DMA 완료, CPU 비접근과 line 소유권을 나누어 봅니다. DSB가 CPU 유지 연산의 완료를 보장하는 것과 외부 DMA의 전송 완료를 확인하는 것도 별개입니다.

## 4. 16바이트 버퍼도 32바이트 이웃에 영향을 줍니다

가장 작은 공유 line 예제에서는 0~15번 바이트가 RX payload, 16번 바이트가 flag입니다. 모두 같은 0~31번 line에 있습니다. CPU가 flag를 1로 쓰면 그 line은 dirty가 됩니다. 당시 캐시의 RX 사본은 0이고, 그 뒤 DMA가 RAM의 RX 16바이트를 `41`로 채웁니다.

| 완료 뒤 처리 | CPU가 읽는 RX | CPU가 읽는 flag | 잃는 값 |
| --- | --- | --- | --- |
| RX 범위 invalidate | `41` × 16 | 0 | dirty flag=1이 사라집니다. |
| RX 범위 clean 후 invalidate | `00` × 16 | 1 | 옛 RX를 RAM에 써 새 DMA 값을 덮습니다. |
| flag를 다음 line의 32번 위치로 분리 | `41` × 16 | 1 | 이 모형에서는 두 값을 유지합니다. |

invalidate가 요청한 16바이트만 골라 버리는 것이 아니기 때문에 첫 오류가 생깁니다. 두 번째 오류를 피하려고 사후 clean을 추가하면 dirty line에 들어 있던 옛 RX까지 함께 반영합니다. payload만 비교하면 첫 경로를 통과시킬 수 있고, flag만 비교하면 두 번째 경로를 통과시킬 수 있습니다. 검사는 payload와 이웃 상태를 동시에 봐야 합니다.

```python
line["data"][address % LINE] = value  # %는 line 안의 위치를 구하는 나머지 연산입니다.
line["dirty"] = True                # 한 바이트 쓰기도 이 모형에서는 line을 dirty로 만듭니다.
self.lines.pop(base, None)           # pop으로 사본을 버리며 다른 dirty 바이트도 보존하지 않습니다.
```

수정 경로의 핵심은 버퍼 시작 정렬만이 아니라 영향을 받는 line 전체의 격리입니다. 시작만 32바이트 정렬하고 배열을 16바이트만 할당하면 바로 뒤의 다른 변수가 나머지 절반에 들어갈 수 있습니다. 할당 크기·링커 배치·소유권을 함께 정합니다. ST의 [DMA/cache 안내](https://community.st.com/stm32-mcus-60/dma-is-not-working-on-stm32h7-devices-97)도 같은 line의 다른 데이터가 invalidate의 영향을 받을 수 있음을 설명합니다.

## 5. 유지 연산 범위를 계산하고 다른 방법으로 검산합니다

주소를 바이트 기준으로 놓고 `lo=(start//32)*32`, `hi=((start+length+31)//32)*32`로 내림·올림 경계를 구합니다. 길이 0은 빈 범위로 따로 처리합니다. 자체 예제에서 시작 13·길이 40이면 실제 payload는 `[13,53)`, 유지 범위는 `[0,64)`입니다. 시작 31·길이 2도 두 line을 건드립니다.

검사 코드의 oracle은 이 두 경계 식을 다시 사용하지 않습니다. payload에 포함된 각 바이트의 line 주소를 모아 집합으로 만들고, 함수가 만든 line 목록과 비교합니다. 128바이트 메모리 안에서 가능한 시작·길이 8,385조합을 검사했습니다. 이것은 제한된 호스트 주소 공간의 범위 계산이며 실제 주소 덧셈의 overflow·접근 권한·DMA bus matrix를 검증한 결과는 아닙니다.

CMSIS_6 v6.3.0의 by-address 유지 함수는 32바이트 단위와 barrier를 포함합니다. 프로젝트가 사용하는 실제 CMSIS 구현과 인수형·크기 한계도 확인해야 합니다. 모형의 Python 메서드 이름이 실제 `SCB_*` 호출을 실행하는 것은 아닙니다. [고정 판본의 Arm CMSIS 소스](https://github.com/ARM-software/CMSIS_6/blob/v6.3.0/CMSIS/Core/Include/m-profile/armv7m_cachel1.h)

## 6. 검사 결과와 실제 적용의 경계

2026-10-21 Windows x86-64·Python 3.12.14에서 정상 검사와 일곱 가지 의도적인 오류 대조가 기대대로 판정됐습니다. `--inject tx-no-clean`은 TX가 기대 입력을 읽지 못해 종료 코드 1로 실패했습니다. 정상 검사는 종료 코드 0이며 소스·입력 SHA-256과 JSON을 남겼습니다.

```powershell
python -B verify.py --output C:/temp/cache-dma-new
python -B verify.py --inject tx-no-clean --output C:/temp/cache-dma-fault-new
```

명령은 [코드 폴더](../예제_examples/실무검증_practical-validation/interrupt_dma/README.md)에서 실행합니다. 이 결과에는 실제 cache 명령, MPU·DTCM 접근성, 순환 DMA·descriptor 처리, 실시간 지연·전력·동시 실행이 없습니다. 타깃에서는 부품/DMA master·주소·할당/전송 길이·cache 속성·소유권 전환·완료 status·첫 불일치 바이트·이웃 guard를 함께 기록합니다.

## 확인 문제

1. CPU가 TX를 맞게 읽었는데 DMA가 0을 읽었다면 무엇을 나누어 봐야 합니까?
2. 같은 line의 flag를 잃지 않으려고 RX 완료 뒤 clean까지 추가하면 항상 안전합니까?
3. 32바이트 정렬인 16바이트 배열은 line 전체를 독점합니까?

답: 1. CPU 캐시의 값과 DMA가 읽는 RAM, 사전 clean·주소 접근성·소유권을 봅니다. 2. 아닙니다. 캐시의 옛 RX를 새 DMA 결과 위에 쓸 수 있습니다. 3. 아닙니다. 남은 16바이트의 실제 배치도 확인해야 합니다.

## English

The write-back host model separates CPU cache and DMA-visible RAM. It reproduces stale TX, stale post-DMA RX, dirty RX writeback corruption, and both ways a shared line can lose either payload or a neighboring flag. Line isolation preserves both in the fixture. Bytewise range oracles check 8,385 bounded address/length combinations. No MCU cache instruction, speculative read, bus behavior, or physical timing is measured.

## 출처와 실제 열람 범위

- [ST AN4839, Level 1 cache on STM32F7/H7](https://www.st.com/resource/en/application_note/an4839-level-1-cache-on-stm32f7-series-and-stm32h7-series-stmicroelectronics.pdf): cache line·write-back·DMA 전후 가시성 설명을 읽었습니다.
- [Arm DUI 0646B §4.8](https://documentation-service.arm.com/static/61efd6602dd99944d051417b?token=): 외부 master에 변경을 보이는 유지 연산의 의미를 읽었습니다.
- [CMSIS_6 v6.3.0 유지 함수](https://github.com/ARM-software/CMSIS_6/blob/v6.3.0/CMSIS/Core/Include/m-profile/armv7m_cachel1.h): by-address 함수의 범위·DSB/ISB를 대조했습니다. 날짜별 실행 기록에 판본과 한계를 정리했습니다.
- 바이트 배열·flag 위치·모형 사건과 실제 출력은 직접 구성한 교육 예제입니다.
