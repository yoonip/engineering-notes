# 작업 진행을 확인하는 워치독과 리셋 기록 / Watchdog health gates and reset records

워치독 feed 함수가 주기적으로 호출돼도 주요 작업은 멈춰 있을 수 있습니다. timer interrupt나 높은 우선순위 task가 feed만 계속하면 데이터 수집·제어의 정지를 가리기 때문입니다. 이 사례는 완료 checkpoint를 소비하는 health gate, 순환 tick, feed 허용 창, 부팅 직후 원인 기록과 반복 재부팅 정책을 한 흐름으로 읽습니다.

[모형 코드](../예제_examples/실무검증_practical-validation/watchdog_reset/models.py), [입력과 실행 방법](../예제_examples/실무검증_practical-validation/watchdog_reset/README.md), [검사 코드](../예제_examples/실무검증_practical-validation/watchdog_reset/verify.py), [실행 기록](검증기록_evidence/워치독진행상태와리셋검사_20261021.md)을 연결했습니다. 2026-10-21 Python 호스트 실행이며 MCU·실제 워치독·RTOS를 실행하지 않았습니다. 오류 경로는 교육용으로 직접 구성했습니다.

## 1. “호출됐다”와 “일이 끝났다”를 구분합니다

checkpoint는 task가 의미 있는 작업 단계를 끝냈다는 보고입니다. 예를 들어 수집 task는 DMA 완료를 관측하고 프레임 길이를 검사한 뒤, 제어 task는 유효 입력으로 계산하고 출력 인계까지 끝낸 뒤 보고할 수 있습니다. 실제 의미는 제품의 정상 동작 계약에 맞게 정해야 합니다. 무한 loop의 시작이나 timer ISR에서 카운터만 올리면 보고 수는 증가해도 작업 진행을 증명하지 못합니다.

모형의 control과 acquire는 sequence를 갖습니다. sequence는 완료 checkpoint마다 1씩 증가하는 수입니다. 감독자는 마지막 성공한 feed에서 각 task의 sequence를 accepted로 저장합니다. 다음 feed에는 모든 task가 accepted보다 새 sequence를 제시하고, 마지막 checkpoint의 나이가 10 tick 이하여야 합니다. 이때 epoch는 한 번의 성공한 feed가 진행 보고를 소비한 구간을 뜻합니다.

```python
def task_ok(sequence, accepted, age, fresh_limit):  # def는 이름과 인수를 받는 함수를 정의합니다.
    return sequence > accepted and age <= fresh_limit  # and는 두 조건을 모두 요구합니다.
```

나이만 확인하면 1 tick 전에 보고한 같은 checkpoint를 여러 번 재사용할 수 있습니다. sequence만 확인하면 오래전에 끝난 작업을 현재의 건강 상태로 받아들일 수 있습니다. 두 조건은 서로 다른 오류를 막습니다. 한 task의 보고가 다른 task를 대신하지 않도록 `all(...)`로 전체 등록 task를 확인합니다. 빈 task 목록은 거부해 빈 목록의 `all`이 참이 되는 것도 막습니다.

## 2. 멈춘 수집 작업을 가리는 실제 입력

자체 시간은 절대 tick 250에서 시작하며 저장 tick은 8비트라 255 뒤 0이 됩니다. 두 task는 252에 각각 한 번 보고합니다. 그 뒤 control은 257·261·265·269에 계속 보고하지만 acquire는 멈춥니다. 감독 poll은 254·258·262·266·270에 있습니다.

| 절대 시간·저장 tick | gate가 보는 상태 | 진행 확인 경로 | 무조건 주기 feed |
| --- | --- | --- | --- |
| 254·254 | 두 task 모두 새 보고·나이 2입니다. | feed하고 두 보고를 소비합니다. | feed합니다. |
| 258·2 | acquire의 sequence가 그대로입니다. | 기다리며 feed하지 않습니다. | feed합니다. |
| 262·6 | acquire 나이는 10으로 아직 freshness 경계입니다. | 새 epoch 보고가 없어 feed하지 않습니다. | feed합니다. |
| 266·10 | 마지막 허용 feed 254 뒤 12 tick입니다. | `reset_late`를 보고합니다. | 계속 feed합니다. |

실제 출력에서 진행 확인 경로의 feed 목록은 `[254]`, reset_at은 266이었습니다. 주기 feed 경로는 `[254, 258, 262, 266, 270]`이고 이 입력 구간에는 reset이 없었습니다. acquire가 살아났다는 결과가 아니라 supervisor가 계속 feed해 정지를 가린 결과입니다.

이 모형은 poll에서 창을 평가합니다. 정확히 deadline=266에 poll을 둔 입력이므로 reset_at=266이며, poll이 늦거나 멈춘 사이에 비동기 하드웨어가 언제 리셋하는지 실행한 타이머가 아닙니다. progress 사건은 그 자체로 timeout을 평가하지 않습니다. 실제 워치독의 독립 동작은 대상의 클록·설정과 보드 시험으로 확인해야 합니다.

## 3. tick 순환과 feed 창의 경계

feed를 너무 늦게 하는 오류뿐 아니라 너무 빨리 하는 오류도 분리합니다. 모형은 이전 feed로부터 4 이상 12 미만 tick에서만 feed를 허용합니다. 이는 `[4, 12)`라는 자체 계약입니다. 4는 포함하고 12는 포함하지 않습니다.

```python
age = (now - before) % 256  # %는 나머지이며 8비트 순환 뒤의 경과량을 구합니다.
expired = age >= 12  # >=는 같은 값도 포함하므로 경과 12부터 만료입니다.
early = age < 4  # <는 경과 4를 포함하지 않습니다.
```

| 시작 tick | 현재 tick | 실제로 진행한 tick | feed 요청의 기대 결과 |
| --- | --- | ---: | --- |
| 250 | 253 | 3 | 너무 빨라 reset_early입니다. |
| 250 | 254 | 4 | feed입니다. |
| 250 | 5 | 11 | feed입니다. |
| 250 | 6 | 12 | reset_late입니다. |

`deadline=(250+12)%256=6`을 만든 뒤 `now >= deadline`만 비교하면 now=254에서 이미 만료됐다고 오판합니다. 숫자의 대소와 시간 순서가 순환 경계에서 달라지기 때문입니다. 코드의 오류 주입 `raw-deadline`이 이 경우를 만듭니다.

두 tick만으로 무한한 과거를 복원할 수는 없습니다. 이 모형은 비교하는 실제 차이가 128 미만이라고 전제하고 계산된 차이 128 이상을 거부합니다. 한 바퀴 이상 지나 같은 tick이 됐는지까지 검출하는 기능은 아닙니다. 고정 폭 C 카운터로 옮길 때에는 정수 승격·형 변환과 실제 tick 폭도 별도로 정해야 합니다. Python의 `%256`을 C의 어떤 정수식과도 무조건 같다고 가정하지 않습니다.

실제 STM32F401 WWDG는 별도 7비트 downcounter와 window 레지스터를 사용합니다. ST RM0368 Rev 6 §16.3~16.5의 reload·만료·클록·debug 조건을 확인했습니다. 이 글의 숫자 4·12는 WWDG 레지스터값이나 밀리초가 아니며 하드웨어의 경계 등호와 prescaler 위상을 그대로 구현한 값도 아닙니다. [ST 공식 RM0368](https://www.st.com/resource/en/reference_manual/rm0368-stm32f401xbc-and-stm32f401xde-advanced-armbased-32bit-mcus-stmicroelectronics.pdf)

## 4. 원인을 먼저 저장한 다음 지웁니다

리셋 뒤 첫 로그가 “reset” 한 단어면 timeout이 재발했는지, 소프트웨어 리셋인지, 전원 관련 원인인지 구분하기 어렵습니다. sticky flag는 소거하기 전까지 남는 상태 표시입니다. 여러 비트가 함께 있으면 그 조합을 보존하며 마지막 원인 하나의 시간 순서를 임의로 추정하지 않습니다.

모형의 비트는 watchdog=1, software=2, power=4입니다. 실제 RCC 위치가 아닌 작은 자체 값입니다. power와 watchdog을 함께 latch한 snapshot은 raw=5, causes=`["watchdog", "power"]`입니다. 먼저 clear하면 raw=0, causes=`[]`가 되어 원인이 사라집니다. 먼저 읽고 clear한 뒤 다시 읽은 값 0은 정상입니다. 두 번째 읽기만 진단 자료로 쓰면 안 됩니다.

```python
saved = latch.flags  # .은 객체의 속성을 읽으며 원시 조합을 먼저 보존합니다.
latch.flags = 0  # =는 대입이며 보존한 뒤 모형 상태를 소거합니다.
```

ST RM0368 §6.3.18의 RCC_CSR와 HAL F4 v1.8.3의 clear 매크로도 원인 조회·소거의 구분을 확인하는 자료입니다. 실제 코드에서는 초기화 함수나 bootloader가 먼저 지우지 않는지 확인하고 가장 이른 신뢰 가능한 경로에서 snapshot을 넘깁니다. 해당 raw 값과 firmware ID·부팅 횟수·마지막 task checkpoint를 연결하면 재발 여부를 좁힐 수 있습니다. [HAL RCC v1.8.3](https://github.com/STMicroelectronics/stm32f4xx-hal-driver/blob/v1.8.3/Inc/stm32f4xx_hal_rcc.h)

## 5. 재부팅이 반복되면 같은 시작을 반복하지 않습니다

watchdog이 재부팅시켰어도 같은 고장 입력과 초기화 경로로 바로 돌아가면 boot loop가 됩니다. 자체 정책은 연속 watchdog 부팅 1·2회에는 normal, 3회째에는 recovery를 선택합니다. recovery는 정상 작업을 자동 재시작하지 않는 정책 표시이며 실제 bootloader나 안전 출력 제어를 실행한 기능은 아닙니다.

| 입력 부팅·사건 | 실패 연속값 | 모형 결정 |
| --- | ---: | --- |
| watchdog, watchdog, watchdog | 1, 2, 3 | normal, normal, recovery |
| power 부팅 | 0 | normal |
| watchdog 부팅 | 1 | normal |
| 안정 운전 checkpoint | 0 | stable |
| 다음 watchdog 부팅 | 1 | normal |

실패값이 보존된다는 가정이 필요합니다. 실제 일반 RAM이 모든 리셋·전원 상실에서 남는다는 뜻은 아닙니다. retained RAM·backup register·flash 중 저장 수단을 정하면 초기화·원자적 쓰기·CRC·마모·전원 상실을 따로 시험해야 합니다. stable checkpoint도 부팅 함수 진입 직후가 아니라 정상 업무를 확인한 지점이어야 합니다.

워치독을 켜 둔 채 오래 기다리는 backoff를 무조건 넣지 않습니다. 실제 장치에서 시작 뒤 끌 수 없는 워치독과 boot chain의 제한을 확인하고 recovery 경로에서도 무엇을 건강 상태로 간주해 feed할지 정해야 합니다. 이 모형은 그런 시간을 측정하거나 flash update 절차를 검증하지 않습니다.

## 6. 성공 문구만 확인하지 않습니다

기대 feed·리셋 시각·창 경계·부팅 결정은 [fixture](../예제_examples/실무검증_practical-validation/watchdog_reset/fixtures.json)의 literal 값과 비교합니다. tick 기대값은 현재값을 한 칸씩 전진시키는 별도 oracle로 비교해 256개 시작×128개 경과=32,768조합을 확인했습니다. 결과가 보고한 deadline을 다시 기대 deadline으로 사용하는 검사가 아닙니다.

기본 실행과 Python `-O` 실행은 모두 종료 0이고 검사 결과가 같았습니다. `periodic-feed`, `raw-deadline`, `clear-before-capture`, `always-restart` 네 mutation은 두 실행 모드에서 모두 종료 1로 거부됐습니다. 내부 오류 대조 6개와 잘못된 입력 7개도 확인했습니다. 기존 결과 경로 재사용은 종료 2와 함께 거부했고 결과 SHA-256이 유지됐습니다.

```powershell
python -X utf8 -B verify.py --output C:/temp/watchdog-run-new
python -X utf8 -B -O verify.py --inject periodic-feed --output C:/temp/watchdog-fault-new
```

명령은 코드 폴더에서 실행합니다. JSON의 입력·소스 해시·환경·명령 인수로 어떤 파일을 실행했는지 연결합니다. 검출 건수는 실제 장비 고장 수나 안전 인증의 coverage가 아닙니다. 타깃에서는 가장 긴 정상 처리, startup·sleep·클록 오차·interrupt masking·debug freeze·reset 후 retention 조건을 별도로 확인해야 합니다.

## 확인 문제

1. 수집 task가 멈췄는데 timer ISR의 feed가 계속되면 무엇을 놓칩니까?
2. tick=250에서 12 뒤 deadline=6을 만든 다음 now=254와 단순 대소 비교하면 왜 틀립니까?
3. raw reset flags를 지운 뒤 원인을 읽고 부팅 실패값도 매번 0으로 만들면 어떤 두 가지 증거를 잃습니까?

답: 1. 실제 업무 진행 정지를 놓칩니다. 의미 있는 checkpoint와 task별 epoch를 확인해야 합니다. 2. 순환 뒤의 작은 숫자 6과 아직 순환 전인 254의 크기가 시간 순서와 다릅니다. 선언한 비교 범위 안에서 경과량을 구합니다. 3. 이번 원시 원인 조합과 연속 실패 이력을 잃어 같은 boot loop를 반복할 수 있습니다.

## English

Periodic feeding can hide a stalled acquisition task while the supervisor remains active. This host model requires fresh progress from every task in each accepted feed epoch. It checks explicit wraparound/window boundaries, captures sticky reset causes before clearing them, and selects recovery after three consecutive watchdog boots. Literal expected results, advancing-clock checks, normal/optimized runs and four failing mutations are recorded. Reset timing is evaluated at scripted polls; no asynchronous watchdog, MCU reset or persistent storage is executed.
