# 보이지 않는 내부 상태를 검사하기: scan, ATPG와 fault coverage

[Test와 제조](../README.md) · [참조 모델](../../../예제_examples/확장기초_extended/hardware/models.py) · [검산](../../../예제_examples/확장기초_extended/hardware/test_models.py)

## 한국어

### 기능 검증과 제조 검사는 출발점이 다르다

기능 검증은 설계가 명세를 따르는지 묻는다. 제조 검사는 만들어진 개별 chip에 결함이 있는지 판단할 자극과 관측 경로가 필요하다. DFT(design for test)는 내부 상태에 값을 넣고 결과를 꺼내기 쉽게 회로를 준비한다. Scan, memory BIST, boundary scan은 서로 다른 대상을 다루는 대표적인 방법이다. [Synopsys DFT 설명](https://www.synopsys.com/glossary/what-is-design-for-test.html)

Scan flip-flop은 보통 functional data와 serial scan data 중 하나를 선택한다. Shift mode에서 여러 flop을 chain으로 연결해 내부 상태를 주입하고, capture mode에서 기능 논리의 반응을 잡은 뒤 다시 shift하여 관측한다. Scan chain이 잘 연결되었는지 확인하는 검사와 조합논리의 fault를 검출하는 ATPG pattern 검증도 구분한다. [Cadence의 ATPG 흐름](https://community.cadence.com/cadence_blogs_8/b/di/posts/training-insight-dive-into-atpg-flow-with-cadence-modus-dft-software-solution)

### 실제 결함을 단순한 fault로 모델링하기

Single stuck-at 모델은 한 지점이 항상 0 또는 항상 1이라고 가정한다. 실제 short·open·저항성 결함을 모두 정확히 나타내는 물리 모델은 아니다. 어떤 fault를 검출하려면 정상 회로와 고장 회로의 관측 출력이 달라야 한다. 입력 x와 fault f에 대해

$$detect(x,f)=[y_{good}(x)\ne y_f(x)].$$

이를 위해 fault 지점에서 정상값을 stuck 값의 반대로 만드는 activation과, 그 차이를 출력이나 scan cell까지 전달하는 propagation이 필요하다.

예제로 $n=a\land b$, $y=n\lor c$를 보자. n stuck-at-0을 활성화하려면 a=b=1이어야 하고, OR 출력까지 차이를 보내려면 c=0이어야 한다. 따라서 입력 (1,1,0)이 검출한다. n stuck-at-1은 n의 정상값이 0이고 c=0일 때 드러난다. c=1이면 y가 항상 1이 되어 내부 차이를 가린다. 단순히 모든 입력을 0과 1로 한 번씩 바꾸는 것만으로 충분하지 않은 이유다.

### Coverage의 분모를 먼저 읽기

이 글의 toy model은 a,b,c,n,y 다섯 지점의 stuck-at-0/1, 총 10개를 fault list로 정한다. Branch별 fault나 cell 내부 결함은 넣지 않고 fault collapsing도 하지 않는다. Pattern 집합 P의 검출 집합은

$$D(P)=\bigcup_{x\in P}\{f:detect(x,f)\},\qquad FC(P)=|D(P)|/10.$$

검출된 fault 수, 전체 modeled 수, 증명된 untestable 수, 미해결·중단 수를 따로 기록한다. Tool이 test coverage 또는 efficiency에서 untestable을 분모에서 제외하는 경우도 있으므로 용어만 보고 수치를 비교하지 않는다. 이 글에서는 예를 들어 $N_{det}/(N_{modeled}-N_{proven\,untestable})$처럼 정의를 명시해야 그 비율을 해석할 수 있다고 본다. ATPG가 시간을 다 썼다는 사실은 untestable의 증명이 아니다.

100% stuck-at coverage는 이 fault list에 대한 결과다. Transition, path-delay, bridging, cell-aware fault, analog 특성은 별도 대상이다. 설계 자체의 기능 오류가 모두 사라졌거나 제조 불량이 전혀 없다는 선언도 아니다. [Synopsys의 fault-model 구분](https://www.synopsys.com/glossary/what-is-design-for-test.html)

### Shift 시간과 capture 조건

길이 L인 단일 chain에 P pattern, pattern당 c번 capture를 가정하자. 이전 응답 shift-out과 다음 pattern shift-in을 겹치면 첫 load와 마지막 unload를 포함한 대략의 시간은

$$T\approx\frac{(P+1)L}{f_{shift}}+\frac{Pc}{f_{capture}}.$$

모든 제어 overhead를 뺀 단순 식이다. 여러 chain은 대체로 가장 긴 chain, compression은 별도 controller·입출력 구조가 영향을 준다. Transition fault의 at-speed capture 조건을 shift clock 주파수만으로 충족했다고 볼 수 없다. Test mode의 switching power와 clock/reset 제어도 확인한다.

### 구현과 검증

`logic_output`은 위 2-gate 회로의 정상·single fault 출력을 계산한다. `detected_faults`는 패턴별 차이의 합집합을 구한다. 검산은 n fault의 activation/propagation 조건을 직접 쓴 식과 비교하고, 8개 입력 전체가 10개 fault를 검출하는지 확인한다. 가능한 pattern 부분집합도 전부 비교해 이 모델의 최소 완전 집합 크기가 4임을 확인한다. 이것은 작은 완전 열거이지 대규모 ATPG 알고리즘의 성능 수치가 아니다.

`scan_shift`는 q0가 scan-in에 가까운 chain의 bit 이동·직렬 출력 순서를 검사한다. 실제 EDA 절차에서는 scan library와 netlist를 읽고 test mode·clock·reset을 설정한 뒤 test-structure DRC, chain 확인, fault list 생성, ATPG, fault simulation, pattern simulation을 순서대로 수행한다. Untestable 근거와 excluded/aborted fault, pattern 수와 test power를 함께 남긴다. Python 결과는 scan insertion·Modus·ATE 실행이나 실물 수율 측정이 아니다.

## English

### Functional verification and manufacturing test ask different questions

Functional verification checks a design against requirements. Manufacturing test needs controllable stimuli and observable responses to assess defects in individual fabricated chips. DFT prepares those paths. Scan, memory BIST and boundary scan address different targets. [Synopsys DFT](https://www.synopsys.com/glossary/what-is-design-for-test.html)

A scan flop commonly selects functional or serial data. Shift mode loads internal state through chains; capture mode records functional response; further shifting observes it. Chain connectivity checks differ from verifying ATPG patterns for logic faults. [Cadence ATPG flow](https://community.cadence.com/cadence_blogs_8/b/di/posts/training-insight-dive-into-atpg-flow-with-cadence-modus-dft-software-solution)

### Abstract defects as faults

A single stuck-at fault forces one site to 0 or 1. It is not a complete physical description of shorts, opens or resistive defects. Detection requires $detect(x,f)=[y_{good}(x)\ne y_f(x)]$: activate a difference at the fault site and propagate it to an observable output or scan cell.

For $n=a\land b$, $y=n\lor c$, detecting n stuck-at-0 requires a=b=1 to activate the fault and c=0 to propagate it, giving (1,1,0). Detecting n stuck-at-1 requires normal n=0 and c=0. Setting c=1 masks the difference. Merely toggling each input both ways does not ensure detection.

### Read the denominator before comparing coverage

The toy model defines stuck-at-0/1 at a,b,c,n,y: ten uncollapsed faults, excluding separate branches and cell-internal defects. For pattern set P,

$$D(P)=\bigcup_{x\in P}\{f:detect(x,f)\},\qquad FC=|D(P)|/10.$$

Keep detected, total modeled, proven-untestable and unresolved/aborted counts separate. Some reports exclude untestable faults when defining test coverage or efficiency, so compare explicit formulas rather than labels. A ratio such as $N_{det}/(N_{modeled}-N_{proven\,untestable})$ needs that definition stated. ATPG timeout is not proof of untestability.

100% stuck-at coverage concerns the selected list. Transition, path-delay, bridging, cell-aware faults and analog properties require other models. It also does not prove complete functional correctness or zero manufacturing defects. [Synopsys fault-model distinctions](https://www.synopsys.com/glossary/what-is-design-for-test.html)

### Shift and capture costs

For one chain of length L, P patterns and c capture clocks per pattern, overlapping previous-response unload with next-pattern load gives approximately

$$T\approx(P+1)L/f_{shift}+Pc/f_{capture},$$

including initial load and final unload but omitting control overhead. Multiple chains depend on the longest chain, and compression adds controller and I/O structure. A high shift frequency does not establish transition-test at-speed capture. Test-mode switching power and clock/reset control also matter.

### Implementation and verification

`logic_output` evaluates the stated circuit with one fault; `detected_faults` unions pattern detections. Tests independently compare n-fault activation/propagation conditions, verify complete detection by all eight inputs and enumerate every pattern subset to establish a minimum complete set size of four for this model. This is small exhaustive enumeration, not large-scale ATPG performance.

`scan_shift` checks serial order with q0 nearest scan-in. Actual EDA validation reads scan libraries/netlists, defines test modes/clocks/resets, runs test-structure DRC and chain checks, builds the fault list, then performs ATPG, fault simulation and pattern simulation. Preserve untestable evidence, excluded/aborted counts, pattern count and test power. Python results are not scan insertion, Modus/ATE execution or measured manufacturing yield.

## 출처 대조 / Source cross-check

Synopsys의 DFT·fault 모델 범위와 Cadence의 test-model/구조 확인/ATPG 절차를 대조했다. Toy fault list와 최소 집합은 직접 열거했다. / Synopsys's DFT definitions were cross-checked against Cadence's ATPG procedure; the toy fault list was independently enumerated. 확인 / checked: 2026-10-19.
