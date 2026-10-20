# DMA 버퍼와 캐시의 경계 / Cortex-M7 Cache Lines and DMA Buffer Ownership

## CPU가 쓴 값과 DMA가 읽은 값

DMA(직접 메모리 접근)는 컨트롤러가 메모리와 주변장치 사이에서 데이터를 옮기는 방식입니다. UART DMA에서 순번 17을 넣었는데 이전 값이 나오는 상황을 가정합니다. 주소·길이·배치·캐시 정책·동시 접근을 나누어 원인을 확인해야 합니다.

아래는 분리 시험을 설계하기 위한 가상 관측표입니다. 실보드에서 얻은 측정값이나 수정 전후의 성과가 아닙니다.

| 관측 항목 | 가정한 기록 | 다음 질문 |
|---|---|---|
| 송신 | CPU가 넣은 순번은 17인데 수신 장치는 16을 받습니다. | CPU가 쓴 값이 DMA가 읽는 메모리에 도달했습니까? |
| 수신 | DMA 완료 표시 뒤에도 CPU가 이전 payload를 읽습니다. | RAM이 갱신된 뒤 오래된 캐시 복사본을 읽었습니까? |
| 상태 변수 | 수신 버퍼를 invalidate한 뒤 완료 flag가 0으로 보입니다. | flag와 RX 버퍼가 같은 cache line을 공유합니까? |

일관성은 여러 주체가 공유 데이터의 변경을 올바르게 관찰하는 성질입니다. write-back 캐시에서는 CPU의 새 값이 dirty 상태로 캐시에 남고 RAM에는 옛 값이 있을 수 있습니다. clean은 dirty 내용을 메모리 쪽에 쓰고, invalidate는 캐시 복사본을 버리는 연산입니다. [ST AN4839 §3.2][an4839]

## 40바이트 버퍼가 두 line에 걸치는 계산

Cortex-M7의 cache line은 32바이트입니다. 유지 연산도 한 바이트만 골라 처리하지 않습니다. 직접 정한 주소 `p=0x2002000D`, 길이 `n=40`을 계산합니다. 특정 보드의 사용 가능 주소라는 뜻은 아닙니다.

| 구간 | 시작 포함 | 끝 미포함 | 크기 |
|---|---|---|---:|
| payload | 0x2002000D | 0x20020035 | 40바이트 |
| 영향을 받는 line 전체 | 0x20020000 | 0x20020040 | 64바이트 |

`lo=floor(p/32)×32`, `hi=ceil((p+n)/32)×32`로 시작을 내리고 끝을 올립니다. 앞 13바이트와 뒤 11바이트도 영향을 받습니다. 이 범위까지 전용으로 예약하거나 다른 객체를 분리해야 합니다. 길이 0은 별도 처리하며 코드에서는 주소 덧셈의 overflow도 확인합니다.

`aligned(32)`인 16바이트 배열도 뒤의 변수와 line을 공유할 수 있습니다. 67바이트 payload의 전용 할당을 `ceil(67/32)×32=96`바이트로 잡으면 padding은 29바이트입니다. 실제 DMA 전송은 67바이트로 둘 수 있습니다. [ST의 공유 line 주의사항][st-faq], [인접 flag 예제][microchip]

## TX: CPU에서 DMA로 넘기기

소유권은 누가 버퍼를 읽거나 바꿀 수 있는지 정한 규칙입니다. DMA가 접근 가능한 cacheable RAM이며 자동 캐시 일관성이 없는 구성을 전제로 합니다.

1. CPU가 TX payload와 DMA가 읽을 descriptor를 완성합니다.
2. `SCB_CleanDCache_by_Addr`로 범위를 반영하고 유지 연산 완료를 보장합니다.
3. DMA를 시작합니다. 완료 전까지 CPU가 전송 내용을 바꾸지 않습니다.
4. controller의 완료 조건을 확인한 뒤 CPU가 버퍼를 재사용합니다.

TX를 읽기만 했다면 사후 invalidate가 항상 필요하지는 않습니다. DMA가 descriptor의 status를 쓰는 부분은 RX 방향으로 따로 다룹니다. TX의 새 dirty 값에 사전 invalidate만 적용하면 그 값을 버릴 수 있습니다.

## RX: DMA가 쓴 뒤 CPU가 읽기

RX는 line 전체를 예약하고 다른 task·ISR·DMA와 겹치지 않게 합니다. 기존 dirty 내용도 보존할 수 있는 순서입니다.

1. CPU 소유 단계에서 `SCB_CleanInvalidateDCache_by_Addr`로 RX 범위를 처리한 뒤 DMA에 넘깁니다.
2. DMA가 쓰는 동안 CPU는 같은 line의 padding까지 포함해 그 공간에 접근하지 않습니다.
3. controller가 정한 status·IRQ 등으로 DMA 쓰기 완료를 확인합니다.
4. `SCB_InvalidateDCache_by_Addr`의 완료를 보장한 뒤 CPU가 읽습니다.

사전 처리는 dirty line이 나중에 RAM으로 밀려나 DMA 결과를 덮는 상황을 막습니다. 사후 invalidate는 DMA 중 생겼을 수 있는 오래된 clean 복사본을 버립니다. Normal memory에서는 추측 읽기를 고려해야 합니다. AN4839의 사전 clean·사후 invalidate, ST FAQ의 사전 invalidate·비접근 조건, Arm 설명을 종합한 절차이며 한 문서의 코드 예제를 그대로 옮긴 것은 아닙니다. [Arm M7 User Guide §2.2.1·§4.8][arm-guide]

전용 line의 기존 내용이 모두 버려도 된다면 사전에 clean 없이 invalidate할 수도 있습니다. 사후 clean 없는 invalidate에는 사전 dirty 상태 제거, DMA 소유 중 CPU의 비접근, DMA 쓰기 완료라는 전제가 필요합니다.

## 공유 line은 사후 clean으로 해결하지 않습니다

자체 예로, 한 line 앞 16바이트는 RX이고 뒤에는 완료 flag가 있다고 가정합니다. RAM flag는 0인데 CPU가 cache flag만 1로 바꾸었습니다. DMA가 RAM의 RX를 갱신한 뒤 invalidate하면 flag=1도 버릴 수 있습니다.

사후 clean+invalidate를 하면 cache의 낡은 RX까지 RAM에 써서 새 데이터를 덮을 수 있습니다. 사전 clean 뒤에도 CPU가 같은 line의 flag를 다시 쓰면 전제가 깨집니다. flag를 분리하고 line 전체의 소유권을 유지해야 합니다.

## barrier·volatile·메모리 배치의 역할

CMSIS_6 v6.3.0의 세 by-address 함수에는 사전 `__DSB()`와 사후 `__DSB()`·`__ISB()`가 있습니다. 실제 프로젝트의 구현과 주변 DMA 설정 순서를 확인해야 하며 같은 barrier를 밖에 무조건 반복할 필요는 없습니다. [고정 판본의 함수 구현][cmsis]

DSB는 앞선 명시적 메모리 접근과 유지 연산의 완료를 보장하고, ISB는 명령 흐름을 동기화합니다. DSB만으로 dirty line을 clean하거나 외부 DMA 완료를 기다리지는 않습니다. volatile도 컴파일러의 접근 처리에 관한 도구이며 cache를 우회하거나 유지 연산을 수행하지 않습니다. [volatile과 메모리 순서의 구분][barrier]

링커 section은 배치, MPU는 접근 권한과 cache 속성을 정합니다. `.dma`라는 section 이름도 자동으로 non-cacheable이 되지는 않습니다. Normal non-cacheable 영역에서도 주소 접근성·순서·완료·소유권은 확인합니다. M7 MPU 영역은 2의 거듭제곱 크기와 그 크기에 맞는 시작 정렬이 필요하므로 96바이트 할당을 곧 96바이트 MPU 영역으로 설정할 수는 없습니다. shareable 속성도 자동 캐시 일관성을 보장하는 말로 사용하지 않습니다.

DTCM 접근 여부도 CPU 이름만으로 결정하지 않습니다. AN4839의 DMA→DTCM 예와 ST FAQ의 H7 경로를 모든 MCU에 옮기지 않고 부품번호·DMA master·bus matrix·주소를 확인합니다.

## 원인을 좁히는 시험과 남길 기록

| 분리 시험 | 고정하거나 바꿀 조건 | 판정과 한계 |
|---|---|---|
| 주소 경로 확인 | linker map의 버퍼 주소를 해당 MCU/DMA의 메모리 경로와 대조합니다. | DMA가 접근하지 못하는 배치는 cache 함수로 해결할 수 없습니다. |
| TX 반영 확인 | payload·전송 길이는 같게 두고 사전 clean 유무를 비교합니다. | CPU 메모리 표시와 수신 바이트를 함께 남깁니다. 한 번 일치했다고 전체 원인을 확정하지 않습니다. |
| RX 격리 확인 | line 정렬·전용 할당과 사전/사후 처리를 적용한 조건을 비교합니다. | 받은 바이트와 인접 guard·flag를 함께 확인합니다. payload만 맞는지 보지 않습니다. |
| cache 비활성 비교 | 같은 입력에서 cache 정책을 바꾼 조건을 따로 기록합니다. | 증상이 사라져도 시간·버스 부하가 함께 바뀌므로 단독 인과 증거는 아닙니다. |

실제 시험에서는 펌웨어·compiler·CMSIS 버전, 부품·DMA, 버퍼 주소·할당/전송 길이, MPU/cache 설정, 소유권 전환, DMA status, 수신 원문·첫 불일치를 남깁니다. 시험 횟수와 재현 조건도 기록합니다.

2026-10-21에 AN4839 Rev 2(2018-03)의 §2~4·개정 이력, Arm DUI 0646B의 관련 절, CMSIS v6.3.0 소스를 확인했습니다. 주소는 직접 계산했으며 실보드 실행·성능·수정 성과는 없습니다.

## 확인 문제

1. `0x2002001F`부터 2바이트를 invalidate하면 영향을 받는 line의 총 크기는 얼마입니까?
2. RX 완료 뒤 clean+invalidate로 바꾸면 공유 line의 flag와 수신 데이터가 모두 안전합니까?
3. CMSIS 유지 함수 뒤에 DSB가 있으므로 DMA 완료 status를 확인하지 않고 RX를 읽어도 됩니까?

<details>
<summary>답과 해설</summary>

1. 64바이트입니다. 두 바이트는 32바이트 경계의 양쪽에 있으므로 두 line에 걸칩니다. 이 범위에 다른 객체가 없는지 확인해야 합니다.
2. 안전하다고 할 수 없습니다. dirty line의 오래된 RX 내용을 RAM에 써서 DMA 결과를 덮을 수 있습니다. 전용 line과 CPU/DMA 소유권을 먼저 정합니다.
3. 안 됩니다. 그 DSB는 CPU의 유지 연산 완료를 보장합니다. 외부 DMA 완료는 controller의 규정된 status·IRQ 등으로 별도 확인해야 합니다.

</details>

## English summary

DMA buffers need exclusive ownership of cache lines. Clean TX before DMA reads it; prepare RX before transfer and invalidate after verified completion. CMSIS v6.3.0 includes barriers. The observations and address examples are educational, with no physical-board measurements.

[an4839]: https://www.st.com/resource/en/application_note/an4839-level-1-cache-on-stm32f7-series-and-stm32h7-series-stmicroelectronics.pdf
[st-faq]: https://community.st.com/stm32-mcus-60/dma-is-not-working-on-stm32h7-devices-97
[microchip]: https://ww1.microchip.com/downloads/en/DeviceDoc/Managing-Cache-Coherency-on-Cortex-M7-Based-MCUs-DS90003195A.pdf
[arm-guide]: https://documentation-service.arm.com/static/61efd6602dd99944d051417b?token=
[cmsis]: https://raw.githubusercontent.com/ARM-software/CMSIS_6/v6.3.0/CMSIS/Core/Include/m-profile/armv7m_cachel1.h
[barrier]: https://documentation-service.arm.com/static/5efefb97dbdee951c1cd5aaf
