# 개수는 맞는데 순서는 틀렸다: 작은 모델의 전수검사

[하드웨어 검증 목차](../README.md) · [전이 모델](../../../예제_examples/심화_advanced/hardware/models.py) · [검산](../../../예제_examples/심화_advanced/hardware/test_models.py)

## 한국어

### 검사 항목도 틀릴 수 있다

줄에 두 명이 서 있는데 앞뒤가 바뀌어도 인원수는 두 명이다. FIFO도 마찬가지다. occupancy가 범위 안이라는 assertion은 overflow를 찾는 데 유용하지만 데이터 순서가 맞다는 보장은 아니다. 검증을 설계할 때는 “오류가 없는 결과”뿐 아니라 “어떤 오류를 실제로 잡을 수 있는가”도 확인해야 한다.

이 글은 용량 2, 데이터 1비트, 하나의 동기 clock이라는 작은 queue를 전수 탐색한다. 목적은 모델의 상태·입력·환경 가정과 property의 관계를 드러내는 것이다. assertion·assumption·cover의 역할은 [YosysHQ SBY 문서](https://symbiyosys.readthedocs.io/en/latest/verilog.html), coverage만으로 완료를 단정할 수 없는 이유는 [Siemens Verification Horizons](https://blogs.sw.siemens.com/verificationhorizons/2019/06/03/the-beginning-of-the-end-for-coverage/)와 대조한다.

### 상태와 전이를 먼저 정확히 정의한다

상태는 앞에서부터 순서대로 저장한 tuple이다. 가능한 상태는 빈 tuple 1개, 길이 1의 2개, 길이 2의 4개다.

```math
|S|=1+2+2^2=7.
```

매 cycle 입력은 valid, data, ready다. 세 입력을 각각 1비트로 훑으면 상태 하나당 8가지다. input ready는 갱신 전 occupancy가 2보다 작은지로 결정한다. output valid도 갱신 전 상태가 비어 있지 않은지로 결정한다. 이 queue는 full 상태에서 pop과 동시에 새 push를 받아 throughput을 높이는 bypass 최적화를 포함하지 않는다.

```math
p_{in}=valid\land(n\lt2),\qquad p_{out}=ready\land(n>0),
\qquad n'=n+p_{in}-p_{out}.
```

허용 범위는 $`0\le n'\le2`$다. pop이면 이전 맨 앞 데이터를 꺼내고, push이면 나머지 뒤에 새 데이터를 붙인다. empty 상태에서 valid와 ready가 동시에 1이어도 새 데이터가 같은 cycle에 output으로 바로 통과하지 않는다. 이 의미를 모호하게 두면 모델과 RTL이 다른 queue를 검사하게 된다.

### breadth-first search로 확인하는 범위

초기 상태를 empty로 두고 모든 입력 조합의 다음 상태를 큐에 넣는다. 아직 보지 않은 상태만 다시 확장하면 7개 상태와 총 56개 상태·입력 전이를 방문한다. 모든 reachable 상태의 모든 후속 전이를 확인하므로, 이 유한 모델의 occupancy safety는 임의 길이 실행에 대해 닫혀 있다. 단순히 56 cycle의 한 trace를 돌린 것과는 다르다.

하지만 데이터가 32비트인 실제 FIFO로 자동 확대되지는 않는다. 데이터 독립성이나 추상화의 타당성을 별도로 증명해야 한다. 또 ready가 영원히 0이면 데이터가 영원히 남아도 safety 위반은 아니다. “언젠가 나온다”는 liveness에는 소비자가 결국 ready를 낸다는 fairness 같은 환경 조건이 필요하다. assumption을 지나치게 강하게 두면 실제 문제가 검사 대상에서 사라진다.

### 의도적으로 순서를 망가뜨려 보기

`mutant=True`는 새 데이터를 뒤 대신 앞에 넣는다. 0을 push한 뒤 1을 push하면 올바른 상태는 (0,1), 변형 상태는 (1,0)이다. occupancy는 둘 다 2이며 갱신식도 맞다. 다음 pop에서 출력은 각각 0과 1이므로 순서 property가 차이를 잡는다. occupancy property가 실패하지 않는다는 사실은 그 property의 한계를 보여 준다.

| property | 잡는 오류 | 남는 빈틈 |
|---|---|---|
| occupancy 범위 | 넘침·음수 개수 | 순서·데이터 변조 |
| 개수 보존 | push/pop 회계 오류 | 같은 개수의 데이터 교체 |
| accepted stream과 consumed stream 비교 | 손실·중복·순서 오류 | 환경에 막힌 영구 대기 |
| 환경 조건을 포함한 liveness | 영구 대기 | 조건이 실제 시스템과 맞는지 |

### 실행과 RTL 적용

```bash
python demo.py --case modelcheck
python -m unittest -v test_models.HardwareModels.test_queue_complete_state_space test_models.HardwareModels.test_queue_mutant_escapes_occupancy
```

실행 결과는 7개 상태, 56개 전이와 mutation 반례다. Python tuple 모델의 전수검사이며 RTL solver proof는 실행하지 않았다. 실제 RTL에 적용할 때는 reset 의미, simultaneous push/pop 정책, 데이터·valid 안정 조건을 일치시키고 accepted stream을 기록하는 scoreboard를 둔다. formal 도구에서는 초기화와 `$past` 유효 시점도 구분한다. bounded check의 통과, `UNKNOWN`, 도달 가능한 cover, induction proof는 서로 다른 결과다. 이 차이를 숨기지 않아야 검증 결과가 다음 설계 단계에서도 의미를 갖는다.

## English

### A property can miss a real bug

Reversing two people in a queue leaves its headcount unchanged. Likewise, a legal FIFO occupancy does not guarantee correct data order. Verification should establish not only that a result passes but also which faults its properties can actually detect.

The example exhaustively explores a two-entry queue with one-bit data and a single synchronous clock. [YosysHQ SBY documentation](https://symbiyosys.readthedocs.io/en/latest/verilog.html) distinguishes assertion, assumption and cover. [Siemens Verification Horizons](https://blogs.sw.siemens.com/verificationhorizons/2019/06/03/the-beginning-of-the-end-for-coverage/) provides an independent perspective on the limitations of coverage-based completion claims.

### State and transition semantics

A tuple records stored data in output order. There are seven states: one empty state, two one-element states and four two-element states. Each state has eight combinations of valid, data and ready. Input acceptance requires valid and pre-edge occupancy below two. Output acceptance requires ready and a nonempty pre-edge state. The occupancy relation is $`n'=n+p_{in}-p_{out}`$.

This model does not optimize full-state throughput by accepting a new element concurrently with a pop. It also has no empty-state combinational bypass. If empty with valid and ready both asserted, the new data is stored and does not immediately exit. These details are part of the specification, not incidental implementation choices.

### What exhaustive exploration establishes

Breadth-first search starts at empty, expands every input combination and processes each newly discovered state once. It reaches all seven states and checks 56 state/input transitions. Because every successor is checked in this finite closed transition system, occupancy safety holds for arbitrarily long executions of this model. This is stronger than one trace lasting 56 cycles.

It does not automatically establish the same property for a 32-bit RTL FIFO. Data independence or abstraction must be justified separately. Nor does safety imply eventual delivery: a consumer may keep ready low forever. Liveness needs suitable environmental fairness, and overrestrictive assumptions can remove the very bug being investigated.

### A mutation that occupancy cannot detect

The mutant inserts new data at the front rather than the back. Pushing zero and then one produces (0,1) in the reference and (1,0) in the mutant. Both have occupancy two and satisfy the same count update. Their next outputs differ, exposing the need for a data-order property.

Occupancy bounds detect overflow and underflow. Count conservation detects incorrect push/pop accounting. Comparing accepted and consumed streams detects loss, duplication and reordering. Liveness under an appropriate environment addresses permanent waiting. Each property leaves a different boundary to examine.

### Running and applying the result

The commands above report seven states, 56 transitions and the mutation counterexample. This is exhaustive checking of the Python tuple model, not an executed RTL solver proof. For RTL, align reset behavior, simultaneous-transfer policy and data/valid stability rules, then use a scoreboard that records accepted data. Formal assertions also need correct initialization and a valid first use of `$past`. A bounded pass, an `UNKNOWN` result, a reached cover and an inductive proof mean different things and must remain distinguishable.

## 출처 / Sources

- YosysHQ, *SBY Formal extensions to Verilog*: assumptions, assertions, cover, bounded/inductive results and past-state initialization.
- Siemens, *The Beginning of the End for Coverage*: coverage limitations. Source links appear above.
