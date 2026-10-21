# 상태 비트 소거와 완료 버퍼 소유권 / W1C acknowledgment and completed-buffer ownership

인터럽트 처리 함수가 실행됐다는 사실만으로 필요한 사건을 모두 처리했다고 말할 수는 없습니다. 상태 비트를 잘못 소거해 다른 원인을 지우거나, 완료 버퍼를 소비자가 읽기 전에 재사용할 수 있기 때문입니다. 이 사례는 W1C 레지스터의 소거 의미와 DMA 완료 뒤 버퍼 인계 계약을 서로 다른 호스트 모형으로 확인합니다.

[실행 코드](../예제_examples/실무검증_practical-validation/interrupt_dma/models.py), [검사와 자체 입력](../예제_examples/실무검증_practical-validation/interrupt_dma/README.md), [실행 기록](검증기록_evidence/인터럽트DMA캐시모델검증_20261021.md)을 연결했습니다. 실제 레지스터를 읽거나 MCU의 ISR·DMA를 실행한 결과는 아닙니다. 잘못된 경로도 재현을 위해 의도적으로 넣었습니다.

## 1. W1C의 1은 “새 값 1”이 아닙니다

W1C는 write one to clear의 줄임말입니다. 해당 위치에 1을 쓰면 상태를 소거하고 0을 쓰면 그 위치의 상태를 그대로 두는 규약입니다. 일반 RAM처럼 쓴 값 전체를 저장하는 대상이 아닙니다. 같은 C 대입 문법을 사용하더라도 주변장치가 그 쓰기를 해석하는 방식이 다릅니다.

ST RM0368 Rev 6의 STM32F401 EXTI pending register `EXTI_PR`를 예로 들 수 있습니다. 이 pending 비트는 해당 위치에 1을 써서 소거하는 규약입니다. 따라서 처리한 비트만 1인 mask를 써야 합니다. 아래 C 형태는 그 차이를 설명하는 예이며 이 Python 실행에서 빌드하거나 MMIO로 실행한 코드는 아닙니다. 이 F401의 W1C 예와 별도 글의 Cortex-M7 캐시 예는 서로 다른 대상입니다. [STM32F401 공식 RM0368 §10.3.6, 211쪽](https://www.st.com/resource/en/reference_manual/DM00096844.pdf)

```c
EXTI->PR |= (1u << 1); // 잘못된 일반화: 읽은 pending의 다른 1도 다시 써서 함께 소거합니다.
EXTI->PR = (1u << 1);  // 해당 규약에서 비트 1만 처리했다면 그 mask만 씁니다.
```

`->`는 포인터가 가리키는 구조체의 멤버 접근, `<<`는 비트 이동, `|=`는 읽은 값과 비트 OR를 한 뒤 다시 쓰는 복합 대입입니다. `volatile`을 붙여도 이 읽기·OR·쓰기의 의미가 원하는 소거 mask로 바뀌지는 않습니다. 인터럽트를 잠깐 막더라도 이미 남아 있는 다른 pending 비트를 잘못 쓰는 문제는 사라지지 않습니다.

모든 상태 레지스터에 이 규칙을 적용해서는 안 됩니다. DMA처럼 status와 interrupt flag clear 레지스터를 분리한 장치에서는 실제 ISR·IFCR의 접근 속성과 비트 정의를 읽어야 합니다. read-to-clear·write-zero-to-clear·reserved bit가 섞인 대상도 서로 다릅니다. EXTI의 코드를 DMA 레지스터에 이름만 바꾸어 넣는 절차가 아닙니다.

## 2. 다른 원인이 사라지는 입력을 만듭니다

자체 8비트 모형에서 pending은 `00001010`, 즉 비트 1과 3이 켜진 상태입니다. 이번 처리 범위는 비트 1뿐이므로 mask는 `00000010`입니다.

| 경로 | 레지스터에 쓰는 모형 값 | 남은 pending |
| --- | --- | --- |
| 읽기·OR·쓰기 | `00001010` | `00000000` |
| 처리한 mask만 쓰기 | `00000010` | `00001000` |

첫 경로는 비트 3의 원인을 처리하지 않았는데도 소거합니다. 다음 처리 함수가 pending을 읽으면 그 원인이 보이지 않습니다. 소거 후의 값이 0이라서 “처리가 잘 끝났다”고 판정하면 오히려 잘못된 경로를 통과시킵니다. 필요한 조건은 처리한 비트가 사라지는 것과 처리하지 않은 비트가 남는 것입니다.

```python
written = pending | handled_mask if rmw else handled_mask
# 조건 표현식은 rmw일 때 OR 값, 아니면 처리 mask 자체를 선택합니다.
after = pending & ~written & 255
# &는 비트 AND, ~는 비트 반전이며 마지막 255로 8비트 범위에 한정합니다.
```

검사 코드의 oracle은 위의 AND 식을 한 번 더 계산하지 않습니다. 켜진 비트 위치의 집합에서 처리한 위치의 집합을 빼고 남은 위치를 숫자로 만듭니다. pending 0~255와 mask 0~255의 65,536조합을 비교했습니다. 이 수는 8비트의 정적 조합 수이며 실제 IRQ 발생 횟수나 전체 MCU 상태 공간이 아닙니다.

이 모형은 읽기와 쓰기 사이에 새 사건이 생기는 경우, 같은 비트가 여러 사건을 하나로 합치는 경우를 다루지 않습니다. 올바른 mask를 쓰는 것만으로 이미 한 비트에 합쳐진 여러 사건의 개수를 복원할 수는 없습니다. 사건 수가 필요하면 주변장치 FIFO·카운터·시퀀스 등 다른 증거가 필요합니다.

## 3. 완료 비트 소거와 데이터 반환도 다릅니다

두 번째 모형은 A/B 두 버퍼를 사용합니다. DMA가 A에 값 17을 채웠고 완료를 관측한 뒤 CPU 소비자가 A를 인수합니다. 그동안 B에는 값 18이 들어와 READY 상태입니다. 이때 새 입력 19를 A로 받기 시작하면 A의 CPU 소비자가 기대한 17이 19로 바뀝니다.

| 버퍼 상태 | 누가 무엇을 할 수 있는지 정한 자체 계약 |
| --- | --- |
| FREE | 새 DMA 전송에 할당할 수 있습니다. |
| DMA | 전송 중이므로 CPU가 payload를 소비하지 않습니다. |
| READY | 완료를 관측했고 소비자에게 인계할 차례입니다. |
| CPU | 소비자가 읽는 중이며 아직 재사용할 수 없습니다. |

완료 IRQ는 DMA가 쓰기를 끝냈다는 증거 중 하나일 수 있지만, CPU 소비까지 끝냈다는 뜻은 아닙니다. IRQ 비트를 소거했다고 버퍼가 FREE가 되는 것도 아닙니다. 버퍼 반환은 소비자가 처리를 끝내고 실행하는 별도 계약입니다.

잘못된 경로는 상태를 무시해 CPU 소유 A에 새 값 19를 씁니다. 수정 경로는 새 전송을 시작하기 전에 할당을 거부합니다. B도 아직 READY이므로 무조건 B로 바꿀 수도 없습니다. 이 결과는 실제 순환 DMA를 진행 도중 안전하게 중단했다는 뜻이 아닙니다. 새 전송 시작 전의 backpressure·할당 거부 정책을 표현한 것입니다.

## 4. 로컬에서 얻은 값

2026-10-21 Windows x86-64·Python 3.12.14에서 표준 라이브러리로 실행했습니다. W1C 수정 경로는 처리한 비트 1만 소거해 pending 8을 남겼습니다. 읽기·수정·쓰기 경로는 pending 0이었습니다.

| 버퍼 경로 | A 재사용 허용 | CPU가 읽은 값 | B의 미소비 값 |
| --- | --- | --- | --- |
| 소유권 무시 | true | 19 | 18 |
| FREE일 때만 할당 | false | 17 | 18 |

CPU와 DMA의 캐시 일관성을 이 모형에서는 문제 삼지 않았습니다. 메모리를 모두 최신으로 읽더라도 읽어야 할 프레임 17을 다른 주체가 19로 덮어쓰면 잘못된 결과입니다. 따라서 캐시 clean/invalidate와 버퍼 소유권은 별도로 검사해야 합니다. [캐시와 RAM의 데이터 불일치](캐시와RAM의데이터불일치_dma-cache-lines.md)에서 그 차이를 이어 볼 수 있습니다.

검출기는 pending/mask 요청값 자체와 남아야 할 원인을 검사하고, A 재사용 허용 여부와 A/B의 기대 값을 따로 확인합니다. `--inject w1c-rmw`, `--inject allow-owned-reuse` 실행은 각각 `ContractError`·종료 코드 1로 거부되었습니다. 정상 모델 실행은 종료 코드 0입니다.

```powershell
python -B verify.py --output C:/temp/irq-owner-new
python -B verify.py --inject allow-owned-reuse --output C:/temp/irq-owner-fault-new
```

명령은 [코드 폴더](../예제_examples/실무검증_practical-validation/interrupt_dma/README.md)에서 실행하며 새 출력 경로를 사용합니다. JSON에는 입력·소스 해시·환경과 단계별 버퍼 상태를 남깁니다.

## 5. 실제 타깃에서 추가로 확인할 항목

주변장치의 상태 snapshot, 처리한 원인 mask, 실제 clear 쓰기값, 오류·완료의 우선순위, 해당 버퍼 ID·세대·할당/완료/소비/반환 시각을 연결합니다. 동일 비트 재발과 새 버퍼 완료를 구별할 수 있는지도 확인합니다. IRQ 처리와 task 처리 사이의 큐가 가득 차면 완료 버퍼를 덮거나 조용히 FREE로 만들지 않고 명시적인 손실·흐름 제어 정책으로 처리해야 합니다.

실제 DMA의 종료·중단·double-buffer 전환 조건, FIFO 비움, 주변장치의 마지막 쓰기 완료와 오류 후 재초기화는 대상 문서와 드라이버 규약을 따라야 합니다. 이 예제에는 그런 상태 기계나 NVIC·버스 시뮬레이션이 없습니다. 시편에서 “인터럽트가 한 번 왔다”는 관측과 데이터가 올바르게 인계됐다는 관측을 구별하기 위한 모형입니다.

## 확인 문제

1. pending=10, 처리 mask=2인 W1C에 `pending | mask`를 쓰면 왜 잘못됩니까?
2. DMA 완료 비트를 소거했으면 CPU가 보던 A를 즉시 새 전송에 써도 됩니까?
3. A가 CPU 소유, B가 READY이면 이 모형의 수정 경로는 입력 19를 어디에 받습니까?

답: 1. 처리하지 않은 비트 3에도 1을 써서 소거합니다. 2. 아닙니다. 완료 관측과 CPU 소비 후 반환은 다릅니다. 3. 새 전송 할당을 거부합니다. 실제 제품에서는 유실·재시도·추가 버퍼·흐름 제어 정책을 정해야 합니다.

## English

The static eight-bit W1C model exposes an RMW acknowledgment that clears an unhandled cause. A bit-set oracle checks 65,536 pending/mask combinations. A separate two-buffer trace shows A being overwritten with 19 while its CPU consumer still expects 17; the corrected policy refuses a new allocation. No register, IRQ, DMA, same-bit event accumulation, or live transfer stop is executed.

## 출처와 실제 열람 범위

- [ST RM0368 Rev 6, 2025-01](https://www.st.com/resource/en/reference_manual/DM00096844.pdf): §10.3.6 EXTI_PR의 W1C 규약과 §9.5.1~9.5.4 DMA 상태/flag clear 레지스터의 구분을 읽었습니다. STM32F401의 레지스터 규약을 확인한 것이며 Cortex-M7 캐시가 있는 기종이라는 뜻은 아닙니다.
- [Arm Cortex-M7 Devices Generic User Guide, DUI 0646B](https://documentation-service.arm.com/static/61efd6602dd99944d051417b?token=): CPU와 외부 master의 데이터 관찰이 별도라는 배경을 읽었습니다. 이 버퍼 상태 기계는 매뉴얼에서 가져온 드라이버가 아니라 직접 만든 예제입니다.
