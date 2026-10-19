# SRAM을 읽을 때 저장 노드가 올라가는 이유

[메모리 목차](../README.md) · [읽기 교란 모델](../../../예제_examples/심화_advanced/hardware/models.py) · [검산](../../../예제_examples/심화_advanced/hardware/test_models.py)

## 한국어

### 읽기만 하는데 왜 값이 바뀔 수 있을까

6T SRAM은 서로 물린 두 inverter가 0과 1을 유지한다. 읽을 때는 미리 충전된 bitline을 access transistor로 저장 노드에 연결한다. 낮은 값을 저장한 노드도 완벽한 0 V에 고정되어 있지 않다. bitline 쪽에서 들어오는 전류 때문에 순간적으로 올라갈 수 있다. 그 전압이 반대 inverter의 상태를 바꾸면 read upset이 발생한다.

[UC Berkeley Sriram의 학위논문 §5.3.3](https://people.eecs.berkeley.edu/~tking/theses/bsriram.pdf)은 access와 pull-down의 전압 분배와 read margin을 설명한다. [Berkeley의 dynamic SRAM stability 연구](https://people.eecs.berkeley.edu/~bora/Conferences/2010/VLSI10-Seng.pdf)는 정적 지표와 pulse-duration에 따른 동적 안정성을 구분한다. 아래는 그 원리를 이해하기 위한 저항·용량 근사이며 6T cell 전체의 static noise margin 계산은 아니다.

### 두 저항과 저장 용량으로 단순화하기

bitline은 읽는 동안 VDD로 고정되어 있고, access transistor는 Ra, pull-down은 Rpd라는 일정한 저항으로 근사한다. 낮은 저장 노드의 용량을 C라 하고 처음 전압은 0으로 둔다. 반대 inverter가 아직 전환되지 않았고, wordline이 켜진 이후의 구간을 다룬다.

```math
C\frac{dv}{dt}=\frac{V_{DD}-v}{R_a}-\frac{v}{R_{pd}}.
```

우변 0으로 정리하면 평형 노드 전압을 얻고, v의 계수에서 time constant를 얻는다.

```math
v_\infty=V_{DD}\frac{R_{pd}}{R_a+R_{pd}},\quad
\tau=(R_a\parallel R_{pd})C,\quad
v(t)=v_\infty(1-e^{-t/\tau}).
```

Rpd를 작게, 즉 pull-down을 강하게 만들면 low node가 덜 올라간다. Ra를 작게 만들면 access가 강해져 이 read-disturb 모델에서는 노드가 더 올라간다. 실제 transistor의 strength는 하나의 일정 저항으로 모든 bias에서 표현되지 않으므로, 이 방향성을 정량적인 PDK cell-ratio 규칙으로 바꾸지는 않는다.

### 가정한 trip voltage와 SNM의 차이

VDD=1 V, Ra=20 kΩ, Rpd=10 kΩ, C=1 fF이면 $`v_\infty=1/3`$ V, τ≈6.67 ps다. 가상의 inverter trip voltage를 0.45 V로 정하면 $`0.45-v_\infty\approx0.117`$ V의 간격이 남는다. 이것은 주어진 trip voltage에 대한 divider gap이다.

SNM은 cross-coupled inverter의 VTC를 겹친 butterfly 곡선에서 얻는 정적 안정성 지표다. 여기의 gap을 “SNM=117 mV”라고 부르면 잘못이다. 반대 노드·inverter gain·비선형 feedback이 모두 생략되어 있기 때문이다. 또한 τ가 작아졌다는 사실만으로 동적 read 안정성이 좋아졌다고 결론내릴 수 없다. 평형 전압, feedback, pulse 폭과 실제 disturbance가 함께 중요하다.

| 간단 모델이 알려 주는 것 | 알려 주지 않는 것 |
|---|---|
| KCL과 초기 기울기 | 두 inverter의 전체 VTC |
| Ra/Rpd에 따른 노드 변화 방향 | 공정별 최적 transistor 치수 |
| 일정 bitline에서의 RC 응답 | bitline 방전·sense amplifier offset |
| 가정한 trip까지의 간격 | 정식 read SNM·통계 yield |

### 구현과 검산

```bash
python demo.py --case sram
python -m unittest -v test_models.HardwareModels.test_sram_kcl_and_time_constant test_models.HardwareModels.test_sram_strength_and_ode
```

함수는 `expm1`으로 작은 시간의 응답을 안정적으로 계산한다. 별도 KCL로 평형 전류를 맞추고, t=τ의 1−exp(−1) 비율을 확인한다. 중앙 차분의 기울기를 원래 ODE의 우변과 비교하고, pull-down을 강화했을 때 전압이 낮아지는지도 검사한다. ps 단위의 변화율은 숫자가 매우 크므로 미분 검산은 상대오차를 기준으로 한다.

실제 6T 검증은 PDK transistor 모델과 bitline·wordline 조건으로 read-biased VTC를 구하고, 정적 SNM 및 pulse를 바꾼 transient upset을 각각 평가한다. PVT·mismatch Monte Carlo, half-select, 저전압, sense timing도 필요하다. 공개 코드의 저항값은 교육용 가정이며 실측 transistor 저항이나 tape-out 결과가 아니다.

## English

### Reading can disturb the stored state

A six-transistor SRAM holds complementary states in cross-coupled inverters. Reading connects a precharged bitline through an access transistor. The low storage node is not an ideal voltage source fixed at zero; injected current can raise it. A sufficiently large disturbance can switch the opposite inverter and upset the cell.

[Sriram's Berkeley thesis §5.3.3](https://people.eecs.berkeley.edu/~tking/theses/bsriram.pdf) describes the access/pull-down divider and read margin. [The Berkeley dynamic-stability study](https://people.eecs.berkeley.edu/~bora/Conferences/2010/VLSI10-Seng.pdf) independently distinguishes static metrics from pulse-duration-dependent behavior. The example below is an RC approximation, not a complete six-transistor SNM extraction.

### Deriving the divider and transient

Hold the bitline at VDD, approximate the access device by constant resistance Ra and the pull-down by Rpd, and assign capacitance C to the low node. Initially v=0; the wordline has turned on and the opposite inverter has not switched. KCL gives the displayed first-order equation.

Setting its derivative to zero yields $`v_\infty=V_{DD}R_{pd}/(R_a+R_{pd})`$. The effective resistance is Ra parallel Rpd, so tau=(Ra||Rpd)C and the response is $`v_\infty(1-e^{-t/\tau})`$. A stronger pull-down, represented by smaller Rpd, reduces the voltage rise. A stronger access device increases it in this approximation. Constant resistances cannot represent all transistor biases and are not a quantitative PDK sizing rule.

### A divider gap is not static noise margin

For VDD=1 V, Ra=20 kΩ, Rpd=10 kΩ and C=1 fF, the final node voltage is one third of a volt and tau is about 6.67 ps. Assuming an inverter trip voltage of 0.45 V leaves a divider gap of about 0.117 V. Calling that number an SRAM SNM would be incorrect.

SNM comes from the coupled inverter transfer characteristics, conventionally represented by the butterfly construction. This approximation omits the other node, gain and nonlinear feedback. A shorter RC time constant alone also does not establish better dynamic read stability. Final voltage, feedback, pulse duration and disturbance conditions all matter. The model does not extract bitline discharge, sense-amplifier offset, statistical yield or an optimal cell ratio.

### Implementation and physical verification

The commands above verify equilibrium branch currents, the t=tau response ratio, a central-difference derivative against the original ODE and the expected pull-down-strength trend. `expm1` improves small-time numerical accuracy. Since picosecond slopes are numerically large in V/s, derivative comparison uses relative error.

A physical six-transistor analysis needs PDK devices, read-biased VTCs, separate static SNM and pulse-dependent transient upset checks, PVT and mismatch variation, half-select conditions, low-voltage behavior and sensing timing. The resistor values here are educational assumptions, not extracted device resistances or measured chip results.

## 출처 / Sources

- UC Berkeley, Sriram thesis, §5.3.3: access/pull-down division and read upset.
- Toh et al., *Dynamic SRAM Stability Characterization in 45nm CMOS*, 2010: pulse-dependent stability. Links appear above.
