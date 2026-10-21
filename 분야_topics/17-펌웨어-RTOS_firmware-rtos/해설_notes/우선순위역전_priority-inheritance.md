# RTOS의 우선순위 역전: 누가 mutex를 놓을 수 있을까요

[분야 안내](../README.md) · [실행 예제](../../../예제_examples/심화_advanced/systems/advanced_models.py) · [독립 테스트](../../../예제_examples/심화_advanced/systems/test_advanced_models.py) · [실행 안내](../../../예제_examples/심화_advanced/systems/README.md)

## 한국어

### 높은 우선순위도 자원을 기다릴 수 있습니다

높은 우선순위 task H가 실행되지 않는다고 해서 scheduler가 잘못된 것은 아닙니다. 필요한 mutex를 낮은 우선순위 task L이 보유하면 H는 기다립니다. 그 사이 중간 우선순위 task M이 L을 계속 선점하면 H는 자신보다 낮은 M의 실행 때문에 간접적으로 늦어집니다. 이를 priority inversion이라고 합니다. H가 기다리는 이유는 mutex인데, 실제 지연에는 그 mutex와 상관없는 M이 끼어든 셈입니다.

L이 임계 구역을 마치도록 H의 우선순위를 잠시 빌려 주는 방식이 priority inheritance입니다. Linux RT-mutex 설명과 Zephyr mutex 문서는 같은 의존 관계를 설명하지만 구현의 세부 우선순위 규칙은 각 kernel의 계약을 따라야 합니다. 이 예제에서는 숫자가 클수록 우선순위가 높습니다. Zephyr의 실제 숫자 방향과 그대로 대응시키지 않습니다. [Linux RT-mutex design](https://docs.kernel.org/locking/rt-mutex-design.html), [Zephyr mutexes](https://docs.zephyrproject.org/latest/kernel/services/synchronization/mutexes.html)

### 의존 관계를 따라 우선순위를 전파합니다

task의 본래 우선순위를 $`p_0(t)`$, 유효 우선순위를 $`p(t)`$라 하겠습니다. task t가 가진 mutex를 기다리는 task 집합을 W라고 하면 모델의 조건은

```math
p(t)=\max\left(\{p_0(t)\}\cup\{p(w):w\in W\}\right).
```

기본 우선순위를 집합에 넣었으므로 대기자가 없는 `W=∅`에서도 `p(t)=p₀(t)`로 정의됩니다. 대기자가 또 다른 mutex의 소유자일 수 있으므로 전파는 한 번으로 끝나지 않습니다. H가 M의 lock을 기다리고 M이 L의 lock을 기다리면 H의 우선순위가 L까지 이어져야 합니다. `inherited_priorities()`는 기본 우선순위에서 시작하여 변화가 없어질 때까지 이 관계를 반복합니다. 유효 값은 주어진 유한한 기본 우선순위 집합에서만 증가하므로 고정점에 도달합니다. 큰 task 집합을 위한 최적 kernel 알고리즘이 아니라 의존성을 보는 작은 모델입니다. [Linux 6.12 RT-mutex의 Priority adjustments](https://docs.kernel.org/6.12/locking/rt-mutex-design.html#priority-adjustments)는 소유자의 기본 우선순위와 최상위 대기자의 우선순위를 비교하는 규칙을 설명합니다. Linux `prio`의 숫자 방향은 이 모델과 반대입니다.

### 같은 작업량으로 간섭을 비교합니다

demo의 시작 상태는 L이 mutex를 보유한 채 CPU 3 tick을 더 써야 하고, M은 독립 작업 4 tick, H는 그 mutex가 풀린 뒤 1 tick이 필요하다고 정의합니다. 모두 이미 준비되었으며 H는 lock 대기 상태입니다. inheritance가 없으면 순서는 `MMMMLLLH`라서 H는 8번째 tick에 끝납니다. 있으면 L이 먼저 3 tick을 마쳐 `LLLHMMMM`이 되고 H는 4번째 tick에 끝납니다. CPU 작업 총량은 둘 다 8 tick입니다.

이 숫자는 특정 보드나 RTOS의 응답 시간 측정이 아닙니다. context switch, interrupt, lock 획득 자체의 시간과 task release jitter를 0으로 둔 구성 예시입니다. 여기서 줄어든 것은 관계없는 M의 간섭이며 L의 임계 구역 시간은 여전히 H를 block합니다. 실제 deadline 보장은 최악 실행 시간과 다른 task 간섭까지 포함한 분석이 필요합니다.

### inheritance가 해결하지 않는 문제

서로의 mutex를 기다리는 cycle은 deadlock입니다. 우선순위를 높여도 어느 task도 진행하지 못하면 해결되지 않습니다. lock 순서를 정하거나 다른 자원 획득 규약이 필요합니다. mutex를 가진 채 긴 I/O를 기다리는 문제, 장시간 임계 구역, interrupt가 사용할 수 없는 API도 별도입니다. semaphore가 소유자를 갖지 않는 구성에서는 mutex와 같은 inheritance 규약을 기대할 수 없습니다.

테스트는 위 실행 순서를 정확히 비교하고 H→M→L 두 단계 상속을 확인합니다. 기본 우선순위 사전을 바꾸지 않는지도 검사합니다. 실제 RTOS의 unlock 때 우선순위 복원, 여러 mutex 보유, 재귀 mutex와 priority ceiling 설정은 구현마다 조건이 있으므로 문서의 구체적 규약과 trace를 함께 읽어야 합니다. Python 결과는 우선순위 의존 모델의 검증이지 target scheduler의 timing 증명이 아닙니다.

저장소 루트에서 실행합니다. 첫 명령은 입력과 계산 결과를 출력하고, 두 번째 명령은 이 디렉터리의 전체 테스트를 실행합니다.

```sh
python "예제_examples/심화_advanced/systems/demo.py" rtos
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

### FreeRTOS의 자원 소유권과 알림은 나누어 봅니다

위의 고정점 모델은 상속 의존성을 이해하기 위한 모델입니다. 모든 RTOS가 같은 자료구조와 복원 규칙을 쓴다는 뜻은 아닙니다. FreeRTOS V11.1.0의 `xTaskPriorityInherit()`·`xTaskPriorityDisinherit()`에서는 대기자·소유자의 우선순위와 보유 뮤텍스 수를 다룹니다. 중첩 뮤텍스가 남아 있는 상태의 복원을 뮤텍스 하나의 예제로 단정하지 않습니다. [버전이 고정된 공식 tasks.c](https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/V11.1.0/tasks.c)

자체 적용 예로, 낮은 우선순위의 표시 작업이 통신 버스를 잡고 있고 제어 작업이 같은 버스를 기다린다고 하겠습니다. 표시 작업보다 높은 독립 계산 작업이 계속 실행되면 제어 작업의 대기가 늘 수 있습니다. 이때 제어 작업의 우선순위만 더 높여도, 그 작업이 이미 자원 대기 상태라는 사실은 바뀌지 않습니다. 버스 소유자의 임계 구역·실행 가능 상태·상속 적용을 확인해야 합니다.

| 필요한 계약 | 살펴볼 선택 | 확인할 책임 |
| --- | --- | --- |
| 한 태스크가 자원을 소유하고 반환 | 뮤텍스 | 실제 소유자, 모든 오류 경로의 반환, 잠금 보유 시간 |
| 항목을 보관하며 태스크로 전달 | 큐 | 큐 가득 참, payload 수명·복사, 대기와 수신의 연결 |
| 특정 태스크에 작업 도착을 알림 | 태스크 알림 | 같은 인덱스·소거/감소 정책, 별도 payload 보관 |
| ISR에서 태스크로 전달 | 해당 `FromISR` API | 포트의 허용 인터럽트 우선순위와 필요한 문맥 전환 |

상속은 소유자가 CPU를 받아 잠금을 반환하도록 돕습니다. 잠금 안에서 외부 장치 응답을 오래 기다리면 그 물리적인 지연은 없어지지 않습니다. 상태를 짧게 갱신하고 잠금을 놓거나 장치 소유 태스크에 요청을 보내는 설계도 비교할 수 있습니다. 요청 큐를 사용하더라도 긴 요청 앞에 짧은 요청이 밀리는 시간은 남으므로, 설계 선택마다 대기 원인을 다시 분석합니다.

새 [뮤텍스 대기와 마감시간 사례](../../../설계와검증사례_engineering-cases/뮤텍스대기와마감시간_rtos-priority-inversion.md)는 H/M의 준비 시각을 1로 두고 실제 모델의 작업 선택을 기록합니다. L=3·M=8·H=1이면 H의 완료는 상속 없는 경우 12, 있는 경우 4입니다. 270개 작업량 조합과 완료 직전/완료 시각의 540개 마감 경계를 독립적인 작업 블록 기대값과 비교합니다. 이는 앞의 모든 작업이 이미 준비된 3·4·1 예제와 입력 조건이 다릅니다.

자원 대기와 별개로 “큐가 비었으면 잠든다”는 코드에는 검사와 대기 사이의 틈이 생길 수 있습니다. [검사와 대기 사이의 알림 유실 사례](../../../설계와검증사례_engineering-cases/검사와대기사이의알림유실_rtos-lost-wakeup.md)는 그 사이 도착한 단순 resume이 사라지는 경로와 알림을 보관하는 경로를 비교합니다. FreeRTOS V11.1.0의 `ulTaskGenericNotifyTake()`가 확인·대기 등록을 임계 구역에서 연결하는 이유도 함께 읽습니다. 일반 변수에 플래그를 두고 잠들기 직전에 지우는 방법과 같은 계약으로 취급하지 않습니다.

실제 타깃 검증에서는 태스크 준비·잠금 요청·획득·반환·완료 시각, 소유자와 본래/유효 우선순위, ISR 구간을 한 시간축에 남깁니다. 알림에는 payload ID·공개 시각·알림 인덱스·값·대기 진입/복귀·소비를 추가합니다. Python 모형 통과, 커널 코드 열람, 실제 MCU의 지연 측정은 각각 다른 증거로 기록합니다. [공통 실행 방법](../../../예제_examples/실무검증_practical-validation/rtos/README.md)과 [2026-10-21 실행 기록](../../../설계와검증사례_engineering-cases/검증기록_evidence/RTOS스케줄과알림검사_20261021.md)을 연결했습니다.

## English

### High-priority work can still wait for a resource

A high-priority task H can legitimately block on a mutex held by low-priority L. If medium-priority M then preempts L, H is indirectly delayed by unrelated lower-priority work. This is priority inversion: the resource dependency is on L, but M increases the delay.

Priority inheritance temporarily lends the waiter's priority to the owner so the owner can release the resource. Linux RT-mutex and Zephyr describe this dependency, while their detailed kernel rules remain implementation-specific. In this model, larger numbers mean higher priorities; that convention must not be copied directly into Zephyr priority numbering. [Linux RT-mutex design](https://docs.kernel.org/locking/rt-mutex-design.html), [Zephyr mutexes](https://docs.zephyrproject.org/latest/kernel/services/synchronization/mutexes.html)

### Propagate priority through dependencies

Let $`p_0(t)`$ be base priority, $`p(t)`$ effective priority, and W the tasks waiting on mutexes owned by t:

```math
p(t)=\max\left(\{p_0(t)\}\cup\{p(w):w\in W\}\right).
```

Including the base priority makes the set nonempty: with no waiters, `p(t)=p₀(t)`. A waiter can itself own another mutex. If H waits for M's lock and M waits for L's, H's priority must propagate to L. Starting from base priorities, `inherited_priorities()` iterates until no effective priority changes. Values increase only within the finite set of supplied base priorities, so it reaches a fixed point. This is a dependency model rather than an optimized kernel. [Linux 6.12, Priority adjustments](https://docs.kernel.org/6.12/locking/rt-mutex-design.html#priority-adjustments) compares the owner's base priority with its top waiter; Linux `prio` numbering runs in the opposite direction from this model.

### Compare interference at equal total work

The demo starts with L holding a mutex and needing three more CPU ticks, M needing four independent ticks, and H needing one tick after the lock becomes available. All have been released and H is already blocked. Without inheritance the trace is `MMMMLLLH`, completing H at tick eight. With inheritance it is `LLLHMMMM`, completing H at tick four. Both consume eight CPU ticks overall.

These constructed ticks are not board or RTOS response-time measurements. Context switches, interrupts, lock-operation cost, and release jitter are zero in this model. Inheritance removes M's unrelated interference; it does not remove L's critical-section blocking. A real deadline argument needs worst-case execution times and other interference too.

### What inheritance does not solve

A cycle of tasks waiting for each other's mutexes is deadlock. Raising priority cannot make blocked tasks progress. Lock ordering or another resource-acquisition protocol addresses that problem. Long I/O while holding a mutex, oversized critical sections, and APIs unavailable in interrupt context are separate issues. A semaphore without an owner cannot automatically provide the same owner-based inheritance contract.

Tests assert both exact traces and two-stage H→M→L propagation, while checking that base priorities remain unchanged. Unlock restoration, multiple held mutexes, recursive locking, and priority-ceiling configurations need the actual RTOS contract and target traces. Python verification establishes the dependency model, not target scheduler timing.

Run the following commands from the repository root. The first prints the input and computed observations; the second runs the complete test suite in this example directory.

```sh
python "예제_examples/심화_advanced/systems/demo.py" rtos
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

### Resource ownership, notifications, and target evidence

The dependency fixed point above is a teaching model, not every RTOS's implementation. FreeRTOS V11.1.0 has specific owner-priority and held-mutex restoration rules. Ownership, queued payload delivery, notification retention, and ISR-to-task handoff have different contracts. Inheritance cannot remove physical I/O delay while a mutex is held.

The [release-time case study](../../../설계와검증사례_engineering-cases/뮤텍스대기와마감시간_rtos-priority-inversion.md) uses L=3, M=8 and H=1 with H/M released at time 1. A separate block-order oracle checks 270 parameter combinations and 540 deadline boundaries. The [lost-wakeup case](../../../설계와검증사례_engineering-cases/검사와대기사이의알림유실_rtos-lost-wakeup.md) contrasts resume-only signaling with retained notification state. Both are deterministic Python host models.

Target evidence needs release/request/acquisition/release/completion timestamps, mutex ownership, base/effective priorities, and interrupt intervals. Notification traces additionally need payload identity, publication, index/value, wait entry/return, and consumption. Model execution, version-pinned source review, and MCU timing measurements must remain separate evidence. [Code and commands](../../../예제_examples/실무검증_practical-validation/rtos/README.md)

## 출처 / Sources

- [Linux: RT-mutex implementation design](https://docs.kernel.org/locking/rt-mutex-design.html): 우선순위 역전·상속 chain / inversion and inheritance chains
- [Zephyr: Mutexes](https://docs.zephyrproject.org/latest/kernel/services/synchronization/mutexes.html): 소유권·priority inheritance·설정 조건 / ownership and inheritance configuration
- [FreeRTOS-Kernel V11.1.0 tasks.c](https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/V11.1.0/tasks.c): 2026-10-21에 상속·복원 및 알림 확인·대기 등록 부분을 읽었습니다. / Version-pinned inheritance, restoration and notification wait-registration source review.
- [FreeRTOS-Kernel V11.1.0 task.h](https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/V11.1.0/include/task.h): 정지·재개 API의 동기화 한계를 확인했습니다. / Suspend/resume synchronization contract.
