# RTL에서 layout까지: 서로 다른 검증을 연결하는 EDA 흐름

[EDA와 open hardware](../README.md) · [참조 모델](../../../예제_examples/확장기초_extended/hardware/models.py) · [검산](../../../예제_examples/확장기초_extended/hardware/test_models.py)

## 한국어

### 같은 설계를 서로 다른 모습으로 보기

RTL은 clock에 따라 상태가 어떻게 바뀌는지를 기술하고, netlist는 그 기능을 구현하는 cell과 연결을 나타낸다. Layout은 cell과 배선의 실제 형상이다. 같은 설계의 표현이지만 각 단계에서 확인할 수 있는 오류가 다르다. RTL simulation이 통과했다고 배선 간격이 맞는 것은 아니며, layout의 간격이 맞다고 알고리즘이 맞는 것도 아니다.

OpenROAD Flow Scripts는 Yosys의 논리 합성, OpenROAD의 floorplan부터 routing, KLayout의 GDS merge·DRC·LVS를 연결하는 공개 흐름이다. 개별 OpenROAD application과 전체 flow를 구분해야 한다. [OpenROAD 공식 User Guide](https://openroad-flow-scripts.readthedocs.io/en/latest/user/UserGuide.html)

### 단계마다 필요한 입력과 결과

| 단계 | 대표 입력 | 결과와 확인할 점 |
|---|---|---|
| Elaboration·synthesis | RTL, parameter, clock 제약, cell library | netlist, 추론된 register·memory, latch·폭 문제 |
| Floorplan·placement | netlist, LEF·macro·면적 조건 | cell 위치, congestion·utilization |
| Clock tree·routing | clock 요구, routing layer·규칙 | clock 분배, 배선과 via, 실제 연결 |
| Extraction·STA | parasitic, Liberty, SDC | setup/hold·slew·load·미제약 경로 |
| Physical verification | layout, 공정별 rule deck, 기준 netlist | DRC·LVS·antenna 등 각 검사 결과 |

Liberty는 cell의 논리·timing·전력 특성을, LEF는 배치·배선에 필요한 형상·pin·장애물 등의 추상 정보를 제공한다. SDC는 clock·I/O timing과 예외를 표현한다. SPEF 같은 parasitic 표현은 배선의 R/C를 연결한다. 특정 PDK와 flow에서 어떤 파일과 단위를 쓰는지 일치해야 한다.

### 기능 동등성과 timing은 다른 질문이다

이상적인 1-bit full adder는

$$s=a\oplus b\oplus c_{in},\qquad
c_{out}=ab\lor[c_{in}(a\oplus b)]$$

이고 $s+2c_{out}=a+b+c_{in}$을 만족해야 한다. 입력 세 개의 가능한 8조합을 모두 확인하면 이 조합회로의 truth table을 완전히 대조할 수 있다. 하지만 이 작은 결과를 임의의 sequential RTL과 합성 netlist 전체의 동등성으로 확대할 수는 없다. 실제 equivalence에서는 reset·초기상태·parameter·black box·memory mapping과 비교할 mode를 맞춘다.

Timing에서는 acyclic 조합 경로의 고정 지연 모델을 생각해 보자. 노드 v의 지연 $d_v$와 입력 도착시각 $A_u$에 대해

$$A_v=d_v+\max_{u\in pred(v)}A_u.$$

이는 가장 늦게 오는 입력을 따라가므로 위상 순서로 계산할 수 있다. `dag_arrivals`가 구현한 것은 이 최대 경로 계산이다. 실제 STA의 pin별·rise/fall arc, slew/load 의존성, clock 관계, 최소 지연과 corner 분석은 포함하지 않는다. Synthesis 전 wire 추정값과 routing 후 추출값의 slack은 달라질 수 있다.

### DRC와 LVS는 무엇을 보장하는가

DRC는 지정된 deck으로 폭·간격 등 형상 규칙을 확인한다. LVS는 layout에서 추출한 소자·연결을 기준 회로와 비교한다. KLayout의 LVS 문서에서 말하는 extracted netlist는 기생 R/C를 포함한 post-layout simulation netlist가 아니라 연결·소자 비교용 netlist다. 두 종류의 extraction을 같은 것으로 부르면 검증 단계를 혼동하게 된다. [KLayout LVS overview](https://www.klayout.org/downloads/master/doc-qt5/manual/lvs_overview.html)

DRC 통과는 timing·IR drop·electromigration·기능의 통과가 아니다. LVS 통과도 소자의 실제 속도나 noise margin을 측정한 결과가 아니다. Rule deck의 범위, 제외한 black box, waiver와 미해결 항목을 함께 읽어야 한다. 공개 PDK의 교육용 흐름 결과를 특정 foundry의 signoff 승인으로 바꾸어 표현하지 않는다.

### 구현과 재현 가능한 확인 절차

Python 검산은 gate 식의 full adder를 정수 합산과 8입력 전체에서 비교한다. 별도의 DAG 예에서는 가능한 경로를 직접 나열한 지연 합과 위상 순서 계산을 대조한다. 순서가 잘못된 graph도 거부하는지 검사한다. 이것은 개념 모델의 검증이며 Yosys·OpenROAD·KLayout을 실행한 로그가 아니다.

실제 flow를 실행할 때는 tool version·PDK revision·library corner·RTL hash와 SDC를 고정하고 다음 산출물을 남긴다. 합성 단계의 warning과 구조를 읽고, 기능 simulation 또는 equivalence를 대조한 뒤 placement·clock tree·routing마다 timing·congestion 변화를 확인한다. 추출 후에는 setup과 hold를 필요한 mode/corner에서 실행하고 unconstrained endpoint를 별도 검사한다. 마지막으로 공정에 맞는 DRC/LVS·antenna·power integrity 검사를 각각 수행하고 결과를 같은 revision에 연결한다. GDS 파일이 생성되었다는 사실만으로 모든 검증이 끝나지는 않는다.

## English

### Different representations expose different errors

RTL describes state updates, a netlist describes implementation cells and connectivity, and layout describes physical geometry. They represent one design but expose different failure modes. RTL simulation does not establish spacing compliance, and legal spacing does not establish a correct algorithm.

OpenROAD Flow Scripts integrates Yosys synthesis, OpenROAD floorplanning through routing, and KLayout GDS merge/DRC/LVS. The OpenROAD application and the complete flow are distinct. [Official flow guide](https://openroad-flow-scripts.readthedocs.io/en/latest/user/UserGuide.html)

### Inputs and evidence by stage

Synthesis consumes RTL, parameters, constraints and cell libraries to produce a netlist and inferred structures. Placement adds positions, macro/area constraints and congestion. Clock-tree synthesis and routing construct clock distribution and physical interconnect. Extraction/STA combine parasitics, Liberty and SDC. Physical verification compares layout against process rules and reference circuits.

Liberty carries cell logic/timing/power characterization; LEF abstracts physical information such as pins and obstructions. SDC expresses clocks, I/O timing and exceptions. Parasitic formats such as SPEF provide interconnect R/C. Files, corners and units must agree with the selected PDK and flow.

### Equivalence is distinct from timing

For a one-bit full adder,

$$s=a\oplus b\oplus c_{in},\quad c_{out}=ab\lor[c_{in}(a\oplus b)],\quad
s+2c_{out}=a+b+c_{in}.$$

Exhausting all eight input combinations compares this complete combinational truth table. It does not establish equivalence of arbitrary sequential RTL and a synthesized design. Real equivalence work must align resets, initial-state assumptions, parameters, black boxes, memory mappings and modes.

For an acyclic fixed-delay combinational model, latest arrival satisfies $A_v=d_v+\max_{u\in pred(v)}A_u$. A topological traversal computes it. `dag_arrivals` implements only this maximum-path abstraction, excluding pin-specific rise/fall arcs, slew/load dependencies, clocks, minimum delays and corners. Estimated pre-route wiring and extracted post-route wiring can produce different slack.

### What do DRC and LVS establish?

DRC checks geometric requirements in a selected deck. LVS extracts devices/connectivity from layout and compares them with a reference circuit. KLayout explicitly uses “extracted netlist” in its LVS context for connectivity/device comparison, not a post-layout parasitic R/C simulation netlist. These extraction tasks must be distinguished. [KLayout overview](https://www.klayout.org/downloads/master/doc-qt5/manual/lvs_overview.html)

Passing DRC does not establish timing, IR drop, electromigration or functionality. Passing LVS does not measure device speed or noise margin. Deck scope, black boxes, waivers and unresolved findings matter. A public-PDK educational flow is not automatically foundry signoff approval.

### Implementation and a reproducible validation sequence

Python checks compare gate-level full-adder equations against integer arithmetic for every input. A separate DAG test enumerates all possible paths and compares their delay sums against the topological computation, also rejecting invalid ordering. These are concept-model checks, not Yosys/OpenROAD/KLayout execution logs.

Actual execution fixes tool versions, PDK/library revisions, corners, RTL hash and SDC. Inspect synthesis warnings and inferred structures; compare behavior by simulation or equivalence. Track timing/congestion after placement, clock-tree synthesis and routing. After extraction, check setup/hold across required modes/corners and inspect unconstrained endpoints separately. Run process-appropriate DRC/LVS, antenna and power-integrity checks, tying each result to the same design revision. Producing a GDS file alone does not complete validation.

## 출처 대조 / Source cross-check

OpenROAD의 flow 구성과 독립 도구인 KLayout의 LVS 정의를 대조했다. 논리·graph 예는 직접 계산한 교육 모델이다. / OpenROAD's flow description was cross-checked against KLayout's independent LVS definition; logic and graph examples are derived teaching models. 확인 / checked: 2026-10-19.
