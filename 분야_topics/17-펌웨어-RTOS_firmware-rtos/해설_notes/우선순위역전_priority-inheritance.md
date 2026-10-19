# RTOS의 우선순위 역전: 누가 mutex를 놓을 수 있을까

[분야 안내](../README.md) · [실행 예제](../../../예제_examples/심화_advanced/systems/advanced_models.py) · [독립 테스트](../../../예제_examples/심화_advanced/systems/test_advanced_models.py) · [실행 안내](../../../예제_examples/심화_advanced/systems/README.md)

## 한국어

### 높은 우선순위도 자원을 기다릴 수 있다

높은 우선순위 task H가 실행되지 않는다고 해서 scheduler가 잘못된 것은 아니다. 필요한 mutex를 낮은 우선순위 task L이 보유하면 H는 기다린다. 그 사이 중간 우선순위 task M이 L을 계속 선점하면 H는 자신보다 낮은 M의 실행 때문에 간접적으로 늦어진다. 이를 priority inversion이라고 한다. H가 기다리는 이유는 mutex인데, 실제 지연에는 그 mutex와 상관없는 M이 끼어든 셈이다.

L이 임계 구역을 마치도록 H의 우선순위를 잠시 빌려 주는 방식이 priority inheritance다. Linux RT-mutex 설명과 Zephyr mutex 문서는 같은 의존 관계를 설명하지만 구현의 세부 우선순위 규칙은 각 kernel의 계약을 따라야 한다. 이 예제에서는 숫자가 클수록 우선순위가 높다. Zephyr의 실제 숫자 방향과 그대로 대응시키지 않는다. [Linux RT-mutex design](https://docs.kernel.org/locking/rt-mutex-design.html), [Zephyr mutexes](https://docs.zephyrproject.org/latest/kernel/services/synchronization/mutexes.html)

### 의존 관계를 따라 우선순위를 전파한다

task의 본래 우선순위를 $`p_0(t)`$, 유효 우선순위를 $`p(t)`$라 하자. task t가 가진 mutex를 기다리는 task 집합을 W라고 하면 모델의 조건은

```math
p(t)=\max\left(p_0(t),\max_{w\in W}p(w)\right).
```

대기자가 또 다른 mutex의 소유자일 수 있으므로 전파는 한 번으로 끝나지 않는다. H가 M의 lock을 기다리고 M이 L의 lock을 기다리면 H의 우선순위가 L까지 이어져야 한다. `inherited_priorities()`는 변화가 없어질 때까지 이 관계를 반복한다. 유효 값은 주어진 유한한 기본 우선순위 집합에서만 증가하므로 고정점에 도달한다. 큰 task 집합을 위한 최적 kernel 알고리즘이 아니라 의존성을 보는 작은 모델이다.

### 같은 작업량으로 간섭을 비교한다

demo의 시작 상태는 L이 mutex를 보유한 채 CPU 3 tick을 더 써야 하고, M은 독립 작업 4 tick, H는 그 mutex가 풀린 뒤 1 tick이 필요하다고 정의한다. 모두 이미 준비되었으며 H는 lock 대기 상태다. inheritance가 없으면 순서는 `MMMMLLLH`라서 H는 8번째 tick에 끝난다. 있으면 L이 먼저 3 tick을 마쳐 `LLLHMMMM`이 되고 H는 4번째 tick에 끝난다. CPU 작업 총량은 둘 다 8 tick이다.

이 숫자는 특정 보드나 RTOS의 응답 시간 측정이 아니다. context switch, interrupt, lock 획득 자체의 시간과 task release jitter를 0으로 둔 구성 예시다. 여기서 줄어든 것은 관계없는 M의 간섭이며 L의 임계 구역 시간은 여전히 H를 block한다. 실제 deadline 보장은 최악 실행 시간과 다른 task 간섭까지 포함한 분석이 필요하다.

### inheritance가 해결하지 않는 문제

서로의 mutex를 기다리는 cycle은 deadlock이다. 우선순위를 높여도 어느 task도 진행하지 못하면 해결되지 않는다. lock 순서를 정하거나 다른 자원 획득 규약이 필요하다. mutex를 가진 채 긴 I/O를 기다리는 문제, 장시간 임계 구역, interrupt가 사용할 수 없는 API도 별도다. semaphore가 소유자를 갖지 않는 구성에서는 mutex와 같은 inheritance 규약을 기대할 수 없다.

테스트는 위 실행 순서를 정확히 비교하고 H→M→L 두 단계 상속을 확인한다. 기본 우선순위 사전을 바꾸지 않는지도 검사한다. 실제 RTOS의 unlock 때 우선순위 복원, 여러 mutex 보유, 재귀 mutex와 priority ceiling 설정은 구현마다 조건이 있으므로 문서의 구체적 규약과 trace를 함께 읽어야 한다. Python 결과는 우선순위 의존 모델의 검증이지 target scheduler의 timing 증명이 아니다.

저장소 루트에서 실행한다. 첫 명령은 입력과 계산 결과를 출력하고, 두 번째 명령은 이 디렉터리의 전체 테스트를 실행한다.

```sh
python "예제_examples/심화_advanced/systems/demo.py" rtos
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## English

### High-priority work can still wait for a resource

A high-priority task H can legitimately block on a mutex held by low-priority L. If medium-priority M then preempts L, H is indirectly delayed by unrelated lower-priority work. This is priority inversion: the resource dependency is on L, but M increases the delay.

Priority inheritance temporarily lends the waiter's priority to the owner so the owner can release the resource. Linux RT-mutex and Zephyr describe this dependency, while their detailed kernel rules remain implementation-specific. In this model, larger numbers mean higher priorities; that convention must not be copied directly into Zephyr priority numbering. [Linux RT-mutex design](https://docs.kernel.org/locking/rt-mutex-design.html), [Zephyr mutexes](https://docs.zephyrproject.org/latest/kernel/services/synchronization/mutexes.html)

### Propagate priority through dependencies

Let $`p_0(t)`$ be base priority, $`p(t)`$ effective priority, and W the tasks waiting on mutexes owned by t:

```math
p(t)=\max\left(p_0(t),\max_{w\in W}p(w)\right).
```

A waiter can itself own another mutex. If H waits for M's lock and M waits for L's, H's priority must propagate to L. `inherited_priorities()` iterates until no effective priority changes. Values increase only within the finite set of supplied base priorities, so it reaches a fixed point. This is a small dependency model rather than an optimized kernel implementation.

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

## 출처 / Sources

- [Linux: RT-mutex implementation design](https://docs.kernel.org/locking/rt-mutex-design.html): 우선순위 역전·상속 chain / inversion and inheritance chains
- [Zephyr: Mutexes](https://docs.zephyrproject.org/latest/kernel/services/synchronization/mutexes.html): 소유권·priority inheritance·설정 조건 / ownership and inheritance configuration
