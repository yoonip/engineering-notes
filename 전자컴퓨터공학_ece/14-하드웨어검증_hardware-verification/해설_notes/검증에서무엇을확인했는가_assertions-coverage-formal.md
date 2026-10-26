# Assertion·coverage·formal의 검증 범위

[Hardware verification](../README.md) · [참조 모델](../../../예제_examples/확장기초_extended/hardware/models.py) · [검산](../../../예제_examples/확장기초_extended/hardware/test_models.py)

## 한국어

### 정답 확인과 지나간 길의 기록

문을 백 번 열었다는 기록과, 문이 잠겼을 때 열리지 않는다는 확인은 다릅니다. 검증에서도 assertion은 지켜야 할 조건을, coverage는 관찰하거나 도달한 상황을 기록합니다. Simulation은 선택한 자극과 시간 동안의 동작을 실행하고, formal은 명시한 모델·초기상태·가정 안에서 가능한 동작을 논리적으로 탐색합니다. 세 가지는 서로를 대체하는 점수표가 아닙니다. [YosysHQ SBY](https://symbiyosys.readthedocs.io/en/latest/verilog.html), [Siemens의 coverage 구분](https://blogs.sw.siemens.com/verificationhorizons/2019/06/03/the-beginning-of-the-end-for-coverage/)

| 항목 | 확인하는 내용 | 남는 한계 |
|---|---|---|
| Assertion | 정한 조건의 위반 여부 | 조건 자체가 빠지거나 틀릴 수 있음 |
| Code coverage | 실행한 구문과 분기 | 실행한 계산의 정답 여부는 별개 |
| Functional coverage | 관찰한 명세상의 상황과 조합 | 정의하지 않은 bin은 보이지 않음 |
| Formal cover | 가정 아래 해당 상태에 도달하는 경로의 존재 여부 | 그 경로가 모든 동작의 안전성을 뜻하지 않음 |

### 상태와 전이를 먼저 정하기

깊이 D의 버퍼 점유량 $`n_t`$를 예로 들겠습니다. 같은 에지의 입력은 갱신 전 점유량으로 판단하고, full에서 쓰기를 거부하며 empty에서 읽기를 거부합니다. 요청 $`w_t,r_t\in\{0,1\}`$에 대해

$$a_t=w_t\land(n_t<D),\quad b_t=r_t\land(n_t>0),\qquad
n_{t+1}=n_t+a_t-b_t.$$

초기상태는 $`n_0=0`$입니다. 내부에서는 동시 읽기·쓰기가 점유량을 유지하지만, empty에서 동시 요청은 쓰기만, full에서는 읽기만 수락됩니다. 다른 FIFO 계약에서는 이 경계 동작이 달라질 수 있습니다.

불변식 $`0\le n_t\le D`$는 귀납으로 검토할 수 있습니다. 시작값이 범위 안에 있고, 내부 상태에서는 변화량이 −1·0·1입니다. 0에서는 감소가, D에서는 증가가 차단되므로 다음 상태도 범위 안입니다. 하지만 이것만으로 데이터 순서·중복·유실을 검증하지는 못합니다. 같은 점유량을 유지하면서 데이터를 뒤바꾸는 구현도 있기 때문입니다.

### 시간 속성과 가정의 역할

Ready/valid의 예로, reset이 해제된 상태에서 `valid && !ready`였다면 다음 샘플에서도 valid와 payload가 유지되어야 한다는 조건을 다음처럼 쓸 수 있습니다.

```systemverilog
// stall된 데이터는 다음 샘플까지 유지합니다.
assert property (@(posedge clk) disable iff (!rst_n)
    valid && !ready |=> valid && $stable(data));
```

이는 SVA 표기 예입니다. DUT reset의 동기·비동기 방식은 별도로 정하며, `disable iff`는 속성 검사를 중단하는 조건이지 DUT 회로의 reset 구현을 바꾸는 문법이 아닙니다. 샘플링·NBA 갱신 시점과 도구의 지원 문법도 확인해야 합니다. SBY의 기본 frontend가 모든 SVA를 지원한다고 가정하지 않고, 지원되는 immediate assertion과 `$past` 또는 해당 frontend의 SVA 범위를 선택합니다. [SBY의 지원 문법·시간 연산](https://symbiyosys.readthedocs.io/en/latest/verilog.html)

`assume`은 환경이 허용하는 입력을 제한합니다. 출력이 항상 올바르다고 가정해 버리면 원하는 결론을 미리 넣은 셈입니다. `cover`로 reset 이후 쓰기·stall·읽기 등 중요한 전제 상황에 실제 경로가 있는지 확인하면, 전제가 한 번도 발생하지 않아 implication이 통과하는 vacuity를 찾는 데 도움이 됩니다.

### 유한 길이 통과와 증명의 차이

깊이 k까지 bounded model checking이 반례를 찾지 못했다고 해서 k 이후도 안전하다는 뜻은 아닙니다. 완전한 유한 상태 탐색이나 올바른 귀납 증명처럼 전체 범위를 덮는 근거가 더 필요합니다. `UNKNOWN`이나 timeout도 통과로 바꾸어 적지 않습니다. Induction이 실패할 때의 임의 상태는 실제 reset에서 도달 불가능할 수도 있으므로 반례 종류를 구분합니다. [YosysHQ의 BMC·prove·cover 정의](https://symbiyosys.readthedocs.io/en/latest/verilog.html)

`counter_next`와 `reachable_counter`는 별도의 Python 상태 모델입니다. 검산은 D=1…16의 모든 유효 상태와 네 요청 조합을 확인하고, BFS로 reset에서의 도달 집합을 구합니다. 경계에서 잘못 증가하는 변이도 불변식을 깨는지 검사합니다. 이것은 작게 완전히 정의한 전이계의 계산이며 실제 RTL solver 실행 결과가 아닙니다.

실제 검증 흐름은 명세에서 속성·coverage 항목을 만들고, reset·입력 프로토콜 가정을 문서화한 뒤 simulation scoreboard와 assertion을 함께 실행합니다. Formal에서는 초기상태, clock 모델과 속성 범위를 고정하고 BMC의 깊이, induction 결과, cover trace를 각각 저장합니다. Coverage의 미도달 항목은 명세상 불가능한지, 환경이 과도하게 제한되었는지, 자극이 부족한지 나누어 검토합니다. 한 가지 100% 수치가 전체 기능의 정당성을 뜻하지 않습니다.

## English

### Correctness checks and records of exercised behavior

Opening a door a hundred times differs from checking that it remains closed when locked. Assertions state requirements; coverage records observed or reachable situations. Simulation executes selected stimuli over a selected duration. Formal verification explores behavior within an explicit model, initial-state set and assumptions. These are complementary forms of evidence. [YosysHQ SBY](https://symbiyosys.readthedocs.io/en/latest/verilog.html), [Siemens coverage discussion](https://blogs.sw.siemens.com/verificationhorizons/2019/06/03/the-beginning-of-the-end-for-coverage/)

Code coverage describes exercised implementation constructs, not their correctness. Functional coverage describes situations and combinations defined in a verification plan; absent bins remain invisible. Formal cover asks whether a path reaches a condition under the assumptions, rather than proving every behavior safe. Assertions themselves may also be incomplete or incorrect.

### Define the transition relation first

For a depth-D buffer, let $`n_t`$ be occupancy, and accept operations using pre-edge state. Reject writes at full and reads at empty:

$$a_t=w_t\land(n_t<D),\quad b_t=r_t\land(n_t>0),\quad
n_{t+1}=n_t+a_t-b_t,\qquad n_0=0.$$

Simultaneous requests preserve interior occupancy, but accept only the write at empty and only the read at full. Another FIFO contract may use different boundary semantics.

The invariant $`0\le n_t\le D`$ follows inductively: reset establishes it; interior steps change occupancy by at most one; decrement at zero and increment at D are blocked. Occupancy alone does not establish data ordering or absence of duplication and loss. An implementation could reorder data while preserving the count.

### Temporal properties and assumptions

The SVA example above expresses that a stalled `valid && !ready` transfer retains valid and payload at the next sample, unless reset disables the property. `disable iff` controls property evaluation; it does not decide whether the DUT reset circuitry is synchronous or asynchronous. Sampling and nonblocking-update semantics matter. A chosen frontend must support the syntax: SBY's basic frontend should not be assumed to implement every SVA construct. Supported immediate assertions and `$past`, or a documented SVA frontend, are alternatives. [SBY semantics](https://symbiyosys.readthedocs.io/en/latest/verilog.html)

An assumption limits legal environmental inputs. Assuming the desired output behavior would simply insert the conclusion. Covering meaningful antecedents—writes, stalls and reads after reset—helps expose vacuity, where an implication passes because its premise never occurs.

### A bounded pass is not automatically a proof

No counterexample within k steps does not establish safety after k. Complete finite-state exploration or a valid induction argument can supply broader evidence. `UNKNOWN` and timeouts are not passes. An induction counterexample may start from a state unreachable after reset and must be distinguished from a reachable counterexample. [SBY BMC/prove/cover definitions](https://symbiyosys.readthedocs.io/en/latest/verilog.html)

`counter_next` and `reachable_counter` implement a separate Python transition system. Tests examine every valid state and all four request combinations for D=1…16, calculate reset reachability by BFS, and show that an incorrect boundary increment violates the invariant. This is analysis of the defined model, not a reported RTL solver execution.

For actual verification, derive properties and coverage from requirements, document reset and input-protocol assumptions, and run a simulation scoreboard with assertions. Formal runs must record initial states, clock model, property scope, BMC depth, induction result and cover traces separately. Investigate an uncovered item as impossible behavior, excessive environmental restriction, or missing stimulus. One 100% metric cannot establish complete functional correctness.

## 출처 대조 / Source cross-check

YosysHQ의 속성·탐색 의미와 Siemens의 code/functional coverage 활용을 독립적으로 읽고 구분했습니다. 예제의 귀납식과 Python 전이계는 위 계약에서 유도했습니다. / YosysHQ's property semantics and Siemens's coverage discussion were read independently; the example's induction argument follows the explicit contract. 확인 / checked: 2026-10-19.
