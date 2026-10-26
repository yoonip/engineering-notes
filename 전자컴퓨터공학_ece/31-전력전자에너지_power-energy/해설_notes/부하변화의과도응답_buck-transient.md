# 부하가 갑자기 바뀔 때: buck의 평균 과도모델

[전력·에너지 목차](../README.md) · [수치 모델](../../../예제_examples/심화_advanced/hardware/models.py) · [검산](../../../예제_examples/심화_advanced/hardware/test_models.py)

## 한국어

### 전압은 그대로인데 필요한 전류가 두 배가 되면

출력에 달린 저항이 절반으로 줄면 같은 전압을 유지하려면 두 배 전류가 필요합니다. 하지만 인덕터 전류는 순식간에 바뀌지 않습니다. 부족한 전류를 커패시터가 먼저 내주면서 전압이 내려갑니다. 이후 인덕터 전류와 커패시터 전압이 함께 변합니다. 이 과정을 보면 정상상태의 D=Vout/Vin 식만으로는 부하 변화 때의 전압 오차를 설명할 수 없는 이유가 드러납니다.

[TI SLVA057](https://www.ti.com/lit/an/slva057/slva057.pdf)의 buck power-stage·평균화 모델과 [ADI MAXREFDES1269](https://www.analog.com/media/en/reference-design-documentation/reference-designs/maxrefdes1269.pdf)의 출력 부품·부하 요구를 대조합니다. 아래 모델은 이상 소자, 일정 Vin, 고정 duty D, 저항성 부하, CCM 평균화입니다. controller가 duty를 바꾸는 closed-loop 응답은 포함하지 않습니다.

### 두 저장소의 상태방정식

스위칭 한 주기의 평균 인덕터 전압은 D Vin−v입니다. 커패시터 전류는 인덕터 전류 i에서 부하 전류 v/R을 뺀 값입니다.

```math
L\frac{di}{dt}=DV_{in}-v,\qquad
C\frac{dv}{dt}=i-\frac{v}{R}.
```

단위는 L[H], C[F], i[A], v[V], R[Ω], t[s]입니다. 고정 duty의 평형 전압은 $`v_e=DV_{in}`$, 전류는 $`i_e=v_e/R`$입니다. Rold에서 Rnew로 순간 변화해도 i와 v는 연속이므로 초기값은 이전 평형에서 가져옵니다. 변화 직후 전압 기울기는 다음과 같습니다.

```math
\dot v(0^+)=\frac{v_e/R_{old}-v_e/R_{new}}{C}.
```

새 평형에서 벗어난 양을 $`\delta i=i-i_e`$, $`\delta v=v-v_e`$라 쓰고 두 식을 결합하면 다음의 2차 ODE가 됩니다.

```math
\delta\ddot v+\frac{1}{R_{new}C}\delta\dot v+\frac{1}{LC}\delta v=0.
```

$`\alpha=1/(2R_{new}C)`$, $`\omega_d=\sqrt{1/(LC)-\alpha^2}`$가 실수인 저감쇠 조건에서, 처음 전압 편차가 0이면 해는 다음과 같습니다.

```math
\delta v(t)=\frac{\dot v(0^+)}{\omega_d}
e^{-\alpha t}\sin(\omega_dt).
```

임계감쇠·과감쇠에서는 이 sin 식을 쓰지 않고 다른 해를 쓰거나 상태방정식을 직접 적분합니다.

### 12 V에서 6 V를 만드는 수치 예

Vin=12 V, D=0.5, L=100 μH, C=100 μF, Rold=12 Ω, Rnew=6 Ω이면 전류 초기값은 0.5 A, 새 평형은 1 A입니다. $`\dot v(0^+)=-5000\ \mathrm{V/s}`$라서 처음에는 전압이 떨어집니다. 이상적인 고정 duty 모델의 최종 전압은 다시 6 V지만 실제 converter에서는 손실과 제어기 동작 때문에 결과가 달라집니다.

독립적인 물리 검산으로 편차 에너지를 쓸 수 있습니다.

```math
E_\delta=\frac12 L(\delta i)^2+\frac12 C(\delta v)^2,
\qquad \frac{dE_\delta}{dt}=-\frac{(\delta v)^2}{R_{new}}\le0.
```

이는 새 평형 기준 편차 에너지의 감소식입니다. 실제 인덕터·커패시터 총 에너지가 부하 변화 뒤 항상 감소한다는 주장이 아닙니다.

### 구현과 검증 범위

```bash
python demo.py --case buck
python -m unittest -v test_models.HardwareModels.test_buck_analytic_rk4 test_models.HardwareModels.test_buck_initial_slope_and_energy
```

`buck_load_step()`은 i와 v를 RK4로 적분합니다. 별도 해석식과 0·0.1·0.5·2 ms에서 비교하고, 최초 기울기와 편차 에너지 미분을 확인합니다. 시간 간격은 LC 고유시간과 감쇠시간에 비해 충분히 작아야 하며, step을 줄여 수렴을 확인하는 절차가 필요합니다.

실제 PWM의 CCM 조건은 평균 전류가 양수인지만으로 결정되지 않습니다. ripple 최저값, 최소 on/off time, diode 동작과 동기 정류기의 reverse-current 정책을 확인합니다. ESR·DCR·스위치 손실, control compensation과 입력 필터를 추가한 모델로 transient·loop 안정성을 함께 봅니다. 여기의 평균모델 계산은 switching simulation이나 보드 load-step 측정이 아닙니다.

## English

### When the load suddenly demands more current

Halving the output resistance doubles the current required at the same voltage. Inductor current cannot change instantaneously, so the capacitor initially supplies the deficit and its voltage falls. Both stored states then evolve. The steady conversion ratio alone cannot describe this transient.

The stage equations are checked against [TI SLVA057](https://www.ti.com/lit/an/slva057/slva057.pdf); [ADI MAXREFDES1269](https://www.analog.com/media/en/reference-design-documentation/reference-designs/maxrefdes1269.pdf) provides an independent output-component and load-design context. Assume ideal components, fixed input and duty, resistive load and a CCM averaged model. Closed-loop duty adjustment is excluded.

### Deriving the state and voltage equations

Averaging the inductor voltage gives $`L\dot i=DV_{in}-v`$. Capacitor current gives $`C\dot v=i-v/R`$. The units are H, F, A, V, Ω and seconds. Equilibrium is ve=DVin and ie=ve/R. At a resistance step, current and capacitor voltage remain continuous, taking their old equilibrium values. The initial voltage slope is $`(v_e/R_{old}-v_e/R_{new})/C`$.

Subtracting the new equilibrium and combining the state equations yields the displayed second-order equation for delta-v. For underdamping, alpha=1/(2Rnew C) and omega_d=sqrt(1/(LC)−alpha²). With zero initial voltage deviation, its exact response is the displayed exponentially decaying sine multiplied by the initial slope divided by omega_d. Critically and overdamped cases require their corresponding solutions or direct integration.

### Example and energy check

Vin=12 V, D=0.5, L=100 μH and C=100 μF give 6 V equilibrium. A 12 Ω to 6 Ω step changes equilibrium current from 0.5 A to 1 A and produces initial slope −5000 V/s. The ideal fixed-duty model eventually returns to 6 V; losses and control action can alter a real converter's result.

An independent check uses equilibrium-deviation energy $`E_\delta=L\delta i^2/2+C\delta v^2/2`$. Substitution of the state equations gives $`\dot E_\delta=-\delta v^2/R_{new}\le0`$. This is not a claim that total physical stored energy must always decrease after a load change.

### Implementation and physical limits

The commands above integrate i and v with RK4, compare voltage with the analytic solution at 0, 0.1, 0.5 and 2 ms, and verify initial slope and energy derivative. Numerical steps must resolve both natural and damping time scales; step refinement checks convergence.

Positive average current alone does not establish switching-level CCM. Inspect ripple minima, minimum on/off times, diode behavior and synchronous reverse-current policy. Include ESR, DCR, switch losses, compensation and input filtering before interpreting a physical transient or loop margin. These are averaged Python-model results, not switching simulation or a measured board load step.

## 출처 / Sources

- Texas Instruments, *SLVA057 Understanding Buck Power Stages* (March 1999), §§2.1·3.1: operating modes and the averaged power-stage model.
- Analog Devices, *MAXREFDES1269*, Rev. 0 (August 2020), Step 6: output-capacitor sizing for load steps and ripple. Links appear above.
