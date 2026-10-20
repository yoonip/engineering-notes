# 뮤텍스 대기와 마감시간 / Mutex blocking, priority inheritance, and deadlines

높은 우선순위 작업이 늦어졌다고 그 작업의 우선순위부터 더 올리면 원인을 놓칠 수 있습니다. 작업이 기다리는 자원을 누가 가지고 있는지, 그 소유자가 왜 실행하지 못하는지를 먼저 봐야 합니다. 이 사례는 낮은 우선순위 L이 가진 뮤텍스를 H가 기다리고, 관계없는 중간 우선순위 M이 L을 선점하는 상황을 실행 가능한 모델로 비교합니다.

[모델 코드](../예제_examples/실무검증_practical-validation/rtos/models.py), [독립 검사 코드](../예제_examples/실무검증_practical-validation/rtos/verify.py), [실행 안내](../예제_examples/실무검증_practical-validation/rtos/README.md), [검증 기록](검증기록_evidence/RTOS스케줄과알림검사_20261021.md)을 연결했습니다. 실제 FreeRTOS 커널이나 MCU에서 시간을 측정한 결과가 아니라, 의도적으로 만든 단일 CPU 스케줄 모델입니다.

## 1. 실행 준비와 자원 대기를 구별합니다

태스크는 독립적으로 실행되는 작업 단위입니다. 실행 준비가 된 Ready 상태와 자원을 기다리는 Blocked 상태는 다릅니다. 뮤텍스는 공유 자원을 한 소유자만 사용하도록 하는 잠금입니다. 높은 우선순위라도 필요한 뮤텍스가 다른 태스크에 있으면 그 소유자가 반환할 때까지 기다립니다.

자체 예제의 우선순위는 L=1, M=2, H=3이며 큰 숫자가 높습니다. L은 시각 0에 잠금을 이미 보유합니다. H와 M은 시각 1에 준비됩니다. CPU 일은 아래와 같고, 실행 단위 하나는 실제 FreeRTOS tick이나 1ms를 뜻하지 않습니다.

| 작업 | 필요한 CPU 일 | 자원 관계 |
| --- | --- | --- |
| L | 3단위 | 처음에 뮤텍스를 소유하며 자기 일이 끝나면 반환합니다. |
| M | 8단위 | 해당 뮤텍스를 사용하지 않는 독립 작업입니다. |
| H | 1단위 | 뮤텍스를 획득한 뒤 처리하고 반환합니다. |

시각 0~1에 L이 한 단위를 실행합니다. 시각 1에 H가 준비되지만 잠금을 얻지 못해 기다립니다. M은 실행 가능하므로, 상속이 없으면 L보다 높은 M이 실행됩니다. H가 M을 기다리는 것처럼 보이지만 실제 자원 의존성은 H→L입니다. M의 간섭이 그 대기를 늘리는 현상을 우선순위 역전이라고 합니다.

## 2. 같은 작업량으로 상속을 대조합니다

우선순위 상속은 대기자 H의 높은 우선순위를 소유자 L에게 임시로 빌려 주는 규칙입니다. 실행 가능한 소유자가 자원을 빨리 반환하도록 하는 방법이지, H에게 잠긴 자원을 동시에 쓰도록 허용하는 방법은 아닙니다. FreeRTOS의 뮤텍스와 일반 이진 세마포어는 이 규약이 다릅니다. [FreeRTOS 공식 뮤텍스 설명](https://freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes)

| 경로 | 실제 모델 실행 순서 | H 완료 시각 | H 준비 후 응답시간 | 마감 시각 5 |
| --- | --- | --- | --- | --- |
| 상속 없음 | `LMMMMMMMMLLH` | 12 | 12−1=11 | 넘깁니다. |
| 상속 적용 | `LLLHMMMMMMMM` | 4 | 4−1=3 | 만족합니다. |

상속 적용 시 L은 시각 1~3에 남은 임계 구역 2단위를 끝냅니다. H가 시각 3~4에 실행하고, M은 그 뒤에 실행합니다. 전체 CPU 일은 두 경로 모두 12단위입니다. 줄어든 것은 총 작업량이 아니라 H의 앞에 끼어드는 M의 간섭입니다. H는 여전히 L의 남은 2단위와 자기 1단위가 필요합니다.

이 사례의 마감 시각은 시각 0 기준 5입니다. H가 준비된 시각 1부터 5단위 안에 끝내라는 상대 마감이라면 절대 마감은 6입니다. 완료 시각·응답시간·절대 마감·상대 마감을 섞으면 같은 추적에서도 판정이 달라집니다. 실제 시험 계획에는 기준 시각부터 명시해야 합니다.

## 3. 코드에서 바뀌는 것은 선택에 쓰는 우선순위입니다

```python
effective = base.copy()               # dict 복사로 본래 우선순위를 보존합니다.
if inherit and high_waits:            # and는 두 조건이 모두 참일 때만 참입니다.
    effective["L"] = base["H"]        # []로 소유자의 유효 우선순위를 바꿉니다.
chosen = max(ready, key=lambda name: effective[name])
# max는 비교 값이 가장 큰 항목을 고르고 lambda는 그 비교 값을 만드는 작은 함수입니다.
remaining[chosen] -= 1                # -=는 남은 CPU 일을 하나 줄입니다.
```

`base`는 본래 우선순위이고 `effective`는 이번 선택에서 사용하는 값입니다. L이 뮤텍스를 반환하면 H의 대기 의존성이 사라져 L의 유효 우선순위는 본래 값으로 돌아갑니다. H가 잠금을 얻은 사건도 JSON에 기록합니다. 실제 커널의 자료구조나 API 호출 비용은 이 함수에 구현하지 않았습니다.

다중 잠금의 상속 전파와 복원은 이 단순 규칙보다 복잡합니다. FreeRTOS V11.1.0의 `xTaskPriorityInherit()`와 `xTaskPriorityDisinherit()`를 읽어 소유자 우선순위 변경과 보유 뮤텍스 수에 따른 복원 조건을 확인했습니다. 이번 모델은 뮤텍스가 하나이며 FreeRTOS의 중첩 잠금 처리를 복제하지 않습니다. [버전이 고정된 공식 tasks.c](https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/V11.1.0/tasks.c)

## 4. 시뮬레이터와 다른 방식으로 기대값을 만듭니다

검사 코드의 `priority_oracle()`는 매 시간 Ready 목록을 고르지 않습니다. 현재 가정에서 가능한 연속 작업 블록을 직접 이어 기대 순서와 완료 시각을 계산합니다. L이 1단위면 H가 준비되기 전에 잠금이 풀리므로 상속 유무와 관계없이 `L → H → M`입니다. L이 2단위 이상이면 상속 없는 경로에는 M 전체가 끼고, 상속 경로에는 끼지 않습니다.

L=1~5, M=0~8, H=1~3과 상속 두 값을 조합해 270개를 검사했습니다. 각 조합에서 기대 완료 시각보다 1 작은 마감과 완료 시각과 같은 마감도 비교해 540개 경계 판정을 확인했습니다. 상태 전이를 다른 코드로 한 번 더 베낀 비교보다 오류를 발견하기 쉬운 이유는, 시뮬레이터와 기대값이 계산하는 방법이 다르기 때문입니다. 다만 같은 가정에서 만든 oracle이므로 실제 커널의 정답을 증명하는 것은 아닙니다.

검출기가 느슨하지 않은지도 확인했습니다. 상속을 적용하겠다는 검사에 실제로는 상속을 끈 스케줄을 넣으면 `ContractError`가 발생합니다. `--inject priority-no-inherit` 실행은 종료 코드 1과 `status=failed`를 기록했습니다. 이 의도된 실패를 정상 검사와 같은 통과로 합치지 않습니다.

```powershell
python verify.py --output C:/temp/rtos-priority-new
python verify.py --inject priority-no-inherit --output C:/temp/rtos-priority-fault-new
```

명령은 [코드 폴더](../예제_examples/실무검증_practical-validation/rtos/README.md)에서 실행합니다. 첫 명령의 정상 종료 코드는 0, 두 번째 결함 대조의 기대 종료 코드는 1입니다. 새 폴더마다 소스 해시, 실행 환경과 인수를 남깁니다.

## 5. 실제 API로 옮길 때의 판단

자원 소유권에는 뮤텍스를, 작업 도착 알림에는 큐·세마포어·태스크 알림을 고려합니다. 뮤텍스를 태스크 사이의 단순 깨우기 토큰처럼 사용하면 소유권과 반환 책임이 어긋날 수 있습니다. ISR은 블록해서 뮤텍스를 기다릴 수 없으므로 태스크용 뮤텍스 경로와 ISR용 전달 API를 구분합니다.

다음은 API 선택을 설명하는 별도 C 형태입니다. 이 문서의 Python 검사에서 빌드하거나 실행한 코드는 아닙니다. 잠금 생성·할당 실패, 실제 타임아웃 정책과 태스크 생성은 사용하는 프로젝트에서 정해야 합니다.

```c
if (xSemaphoreTake(bus_mutex, wait_ticks) == pdTRUE) { // 획득 성공인 경우에만 자원을 사용합니다.
    update_shared_state(); // 예제 함수 이름이며 잠금 안의 짧은 상태 변경을 뜻합니다.
    xSemaphoreGive(bus_mutex); // 같은 소유자가 반환합니다. 오류 경로에서도 누락하면 안 됩니다.
} else {
    record_lock_timeout(); // 획득 실패를 데이터 처리 성공으로 기록하지 않습니다.
}
```

I/O 완료나 다른 태스크의 응답을 오랫동안 기다리며 뮤텍스를 잡고 있으면 우선순위를 빌려도 그 외부 대기 자체가 빨라지지 않습니다. 상태를 짧게 갱신한 뒤 잠금을 놓거나, 한 태스크가 장치를 소유하고 요청 큐로 직렬화하는 설계를 비교해야 합니다. 후자도 큐의 대기 순서·길이·긴 요청에 의한 지연을 별도로 분석해야 합니다.

## 6. 현장에서는 무엇을 기록합니까?

H의 준비·잠금 요청·획득·반환·완료 시각과 당시 소유자, 본래/유효 우선순위, L의 잠금 보유 시간, ISR·다른 태스크의 실행을 한 시간축에 둡니다. H의 우선순위만 올려 보는 시험보다, L의 임계 구역을 줄인 비교와 M의 간섭을 통제한 비교가 원인을 분리하기 쉽습니다.

이번 모델에는 타임아웃, 중첩 잠금, 태스크 삭제, 동일 우선순위 라운드로빈, 멀티코어, 실제 tick 경계, 인터럽트 비용이 없습니다. 최악 응답시간 보장은 별도 실행시간 상한과 실제 RTOS 포트의 규약을 포함해야 합니다. 모델의 마감 만족을 제품의 실시간 보장으로 바꾸지 않습니다.

## 확인 문제

1. H는 우선순위가 가장 높은데 왜 M보다 먼저 실행하지 못합니까?
2. 상속 적용으로 전체 CPU 작업량도 12에서 4로 줄었습니까?
3. L의 일 자체가 10단위라면 상속만 켜서 마감 시각 5를 보장할 수 있습니까?

답: 1. L의 자원을 기다리는 Blocked 상태이기 때문입니다. 2. 아닙니다. H의 완료만 시각 4로 앞당겨졌고 M의 일은 뒤에서 실행됩니다. 3. 아닙니다. 소유자의 필요한 일이나 외부 대기를 없애는 규칙은 아닙니다.

## English

The single-CPU model releases H and M at time 1 while L already owns one mutex. With work L=3, M=8 and H=1, inheritance changes H's completion from 12 to 4 while total CPU work remains 12. A separate block-order oracle checks 270 parameter combinations and 540 deadline boundaries. Removing inheritance under an inheritance-required contract causes CLI verification to fail. These are deterministic host-model observations, not FreeRTOS execution or target deadline guarantees.

## 출처와 실제 열람 범위

- [FreeRTOS 공식 뮤텍스 설명](https://freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes): 2026-10-21에 상속·상호 배제·단순화된 상속 범위를 읽었습니다. 본문 접근이 비어 반환되는 경우 공식 [문서 저장소 원문](https://github.com/FreeRTOS/FreeRTOS-Website-Content/blob/main/content/en-us/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes.md)을 대조했습니다. 웹 문서의 현재 내용과 V11.1.0 태그를 구분합니다.
- [FreeRTOS-Kernel V11.1.0 tasks.c](https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/V11.1.0/tasks.c): `xTaskPriorityInherit()`·`xTaskPriorityDisinherit()` 부분을 읽었습니다. 전체 커널 포트 검증이나 바이너리 실행은 하지 않았습니다.
- 시간축·작업량·독립 oracle·마감 조건·결함 주입은 직접 구성한 교육 예제입니다.
