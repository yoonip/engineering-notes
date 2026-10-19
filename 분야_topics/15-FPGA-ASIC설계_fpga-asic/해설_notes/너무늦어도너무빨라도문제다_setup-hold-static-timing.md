# 너무 늦어도, 너무 빨라도 문제다: setup·hold와 STA

[FPGA와 ASIC](../README.md) · [참조 모델](../../../예제_examples/확장기초_extended/hardware/models.py) · [검산](../../../예제_examples/확장기초_extended/hardware/test_models.py)

## 한국어

### 데이터가 도착해야 하는 시간 창

플립플롭은 clock edge의 전후에 입력이 안정되어 있어야 한다. Setup은 edge 전에, hold는 edge 뒤에 필요한 안정 시간이다. 가장 늦게 오는 새 데이터만 보면 setup을, 가장 빨리 바뀌는 데이터를 보면 hold를 놓칠 수 있다. Clock-to-Q와 조합논리에도 최대·최소 지연이 필요하다. [MIT 6.004 Sequential Logic](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/pages/c5/c5s1/)

STA(static timing analysis)는 경로와 timing model, clock·I/O 제약으로 도착 시간과 요구 시간을 계산한다. 특정 입력 파형만 실행하는 기능 simulation과 다른 분석이다. 기능이 맞는 회로도 느릴 수 있고, timing slack이 양수여도 기능 자체가 틀릴 수 있다.

### 같은 clock의 인접 상승 에지에서 유도하기

여기서는 edge-triggered register 두 개, 같은 주기 T, setup의 다음 주기 capture와 hold의 같은 주기 capture만 다룬다. Launch clock 지연을 $L$, capture clock 지연을 $C$, skew를 $S=C-L$로 정의한다. 모든 시간은 같은 단위다.

Setup의 가장 늦은 데이터는 $L+t_{cq,max}+d_{max}$에 도착한다. 다음 capture edge는 $T+C$이고, 그보다 $t_{su}+U_{su}$ 일찍 안정되어야 한다. 따라서

$$slack_{su}=T+S-t_{cq,max}-d_{max}-t_{su}-U_{su}.$$

Hold에서는 새 데이터가 $L+t_{cq,min}+d_{min}$보다 일찍 바뀌지 않는다고 모델링한다. 같은 capture edge 뒤 $t_h+U_h$까지 이전 값이 필요하므로

$$slack_h=t_{cq,min}+d_{min}-S-t_h-U_h.$$

0 이상의 slack은 이 모델과 제약에서 여유가 있다는 뜻이다. 양의 skew는 capture clock을 늦춰 setup 여유를 늘리지만 hold 여유는 줄인다. 실제 도구의 공통 clock 경로 보정과 corner별 지연은 이 단순 상수식보다 자세하다. [AMD UG1388 timing slack](https://docs.amd.com/r/en-US/ug1388-acap-system-integration-validation-methodology/Reviewing-Timing-Slack)

| 예제의 시간(ns) | 값 |
|---|---|
| T, L, C | 10, 1.2, 1.7 |
| 최대 clock-to-Q, data delay, setup, uncertainty | 0.8, 7.0, 0.6, 0.1 |
| 최소 clock-to-Q, data delay, hold, uncertainty | 0.2, 0.5, 0.2, 0.1 |

Setup slack은 2.0 ns, hold slack은 −0.1 ns다. 주기를 20 ns로 늘리면 setup은 좋아져도 같은 에지 hold 식에는 T가 없어 −0.1 ns가 남는다. 단순히 clock을 느리게 하는 것이 hold 수정을 보장하지 않는 이유다.

### 제약이 빠진 경로는 통과한 경로가 아니다

Clock 정의, generated clock 관계, 입력 최대·최소 지연, 출력 요구 시간, clock uncertainty가 분석 범위를 만든다. Unconstrained endpoint가 있다는 것은 필요한 조건이 검토되지 않았을 수 있다는 뜻이다. False path나 multicycle은 실제 동작 계약에 근거해야 한다. Slack을 양수로 만들 목적으로 예외를 추가하면 분석 대상만 숨길 수 있다.

여러 주기·위상·서로 다른 clock에서는 tool이 setup과 대응 hold edge 관계를 따로 탐색한다. 위 두 식을 모든 관계에 그대로 대입하지 않는다. 비동기 CDC, metastability, reset recovery/removal은 별도로 분석하며 timing exception이 동기화 회로를 만들어 주지는 않는다. [AMD UG906 hold 관계](https://docs.amd.com/r/en-US/ug906-vivado-design-analysis/Hold/Removal-Relationship)

### 구현과 검증, 수정의 방향

`timing_slack`은 명시한 단일 clock·인접 edge 모델만 계산한다. 검산은 절대 도착 시간과 요구 시간을 따로 만들어 차를 구하고, capture clock을 0.3 ns 늦추면 setup이 0.3 ns 늘고 hold가 그만큼 줄어드는지 확인한다. 주기만 늘렸을 때 hold가 그대로인지도 검사한다.

실제 FPGA에서는 primary/generated clock과 min/max I/O 제약을 작성한 뒤, 제약 누락 보고와 clock interaction을 먼저 읽는다. Synthesis, placement, routing 이후의 setup·hold 경로를 corner별로 비교하며 시작점·끝점, launch/capture edge, cell/net delay, uncertainty를 확인한다. Setup 문제는 논리 깊이·배선·fanout을 줄이거나 pipeline을 추가하는 방향, hold 문제는 최소 데이터 지연과 clock skew를 조정하는 방향으로 접근한다. 한쪽 수정이 다른 쪽을 해칠 수 있어 양쪽을 다시 본다.

Python의 양수 slack은 실제 배치·배선 STA 결과가 아니다. 보드의 전원·신호 품질, clock jitter와 모델 밖의 현상도 이 계산 하나로 보증할 수 없다.

## English

### A window in which data must remain stable

A flip-flop requires stable input before an active clock edge for setup and after it for hold. Looking only at the latest arrival can miss hold; looking only at the earliest transition can miss setup. Both registers and combinational logic need minimum and maximum delays. [MIT 6.004](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/pages/c5/c5s1/)

STA calculates arrival and required times from paths, timing models, and clock/I/O constraints. It differs from functional simulation of selected waveforms. Functionally correct logic may be too slow, while positive timing slack does not establish functional correctness.

### Derivation for adjacent edges of one clock

Assume two edge-triggered registers with period T, next-cycle setup capture and same-cycle hold capture. Let launch and capture clock delays be $L,C$, and define skew $S=C-L$. Latest data arrives at $L+t_{cq,max}+d_{max}$; setup requires stability by $T+C-t_{su}-U_{su}$:

$$slack_{su}=T+S-t_{cq,max}-d_{max}-t_{su}-U_{su}.$$

Earliest new-data arrival is $L+t_{cq,min}+d_{min}$, while hold requires the previous value until $C+t_h+U_h$:

$$slack_h=t_{cq,min}+d_{min}-S-t_h-U_h.$$

Nonnegative slack means margin within this model and its constraints. Positive skew improves setup but worsens hold. Real engines include more detailed corner-dependent timing and common-clock-path corrections. [AMD UG1388](https://docs.amd.com/r/en-US/ug1388-acap-system-integration-validation-methodology/Reviewing-Timing-Slack)

For T=10 ns, L=1.2 ns, C=1.7 ns, maximum clock-to-Q/data/setup/uncertainty of 0.8/7.0/0.6/0.1 ns, setup slack is 2.0 ns. Minimum clock-to-Q/data/hold/uncertainty of 0.2/0.5/0.2/0.1 ns gives hold slack −0.1 ns. Increasing T to 20 ns improves setup but leaves this same-edge hold violation unchanged, explaining why lowering frequency does not generally repair hold.

### An unconstrained path has not passed

Primary/generated clocks, minimum and maximum I/O delays, output requirements and clock uncertainty determine what is analyzed. Unconstrained endpoints may indicate missing checks. False-path and multicycle exceptions need a real behavioral basis; adding them merely to improve slack can hide a requirement.

Multiple phases, periods and clocks require explicit setup and corresponding hold edge relationships; the two simplified formulas cannot be applied blindly. CDC, metastability and asynchronous reset recovery/removal require separate treatment. A timing exception does not create a synchronizer. [AMD UG906](https://docs.amd.com/r/en-US/ug906-vivado-design-analysis/Hold/Removal-Relationship)

### Implementation, verification and repair

`timing_slack` implements the stated one-clock model. Tests independently construct absolute arrival and required events, check that delaying the capture clock by 0.3 ns improves setup and worsens hold by 0.3 ns, and verify that a period change alone leaves same-edge hold unchanged.

In an FPGA flow, define clocks and min/max I/O timing, then inspect missing constraints and clock interactions. Compare setup and hold after synthesis, placement and routing across corners, including endpoints, launch/capture edges, cell/net delays and uncertainty. Setup improvements may reduce logic depth, routing and fanout or add a pipeline. Hold repair addresses minimum data delay and skew. Recheck both because improving one can hurt the other.

Positive slack from Python is not a routed-design STA result. This calculation also does not establish board-level power integrity, signal quality, clock jitter performance or behavior outside its timing model.

## 출처 대조 / Source cross-check

MIT의 안정 시간·최대/최소 지연 유도와 AMD의 skew 부호·setup/hold 식을 대조했다. / MIT's timing-window derivation was cross-checked against AMD's skew convention and slack equations. 확인 / checked: 2026-10-19.
