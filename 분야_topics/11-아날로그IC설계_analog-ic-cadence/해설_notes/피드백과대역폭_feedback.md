# 피드백을 걸면 이득과 대역폭은 어떻게 바뀝니까

[아날로그 IC 목차](../README.md) · [실행 코드](../../../예제_examples/심화_advanced/hardware/models.py) · [검산](../../../예제_examples/심화_advanced/hardware/test_models.py)

## 한국어

### 출력의 일부를 돌려주는 이유

자동 온도조절기가 현재 온도를 목표와 비교하듯, 증폭기도 출력 일부를 입력과 비교할 수 있습니다. negative feedback은 오차를 줄이는 방향으로 작동합니다. 하지만 비교 결과가 늦게 돌아오면 보정이 지나쳐 진동할 수 있습니다. 따라서 직류 이득을 원하는 값으로 만드는 문제와, 주파수에 따라 안정적으로 동작하는 문제를 함께 풀어야 합니다.

이 글에서는 선형 소신호 모델, 일정한 실수 feedback factor $`\beta>0`$, 입력·출력 loading이 이미 A에 반영된 단일 루프를 가정합니다. 비선형 slew rate나 출력 포화는 포함하지 않습니다. [ADI MT-033](https://www.analog.com/media/en/training-seminars/tutorials/mt-033.pdf)의 전압 피드백 증폭기 모델과 [TU Delft phase-margin 설명](https://analog-electronics.tudelft.nl/webbook/SED/_build/html/freq_compensation/freq_compensation_Phase_margin_design.html)을 대조해 이득·위상 조건을 구분합니다.

### 폐루프 식을 직접 유도하기

오차 $`e=x-\beta y`$, 출력 $`y=A(s)e`$에서 y를 모으면 다음과 같습니다.

```math
y=A(x-\beta y),\qquad
H(s)=\frac{y}{x}=\frac{A(s)}{1+\beta A(s)},\qquad L(s)=\beta A(s).
```

한 개의 pole을 갖는 open-loop 모델을 대입하면 분모를 곱해 정리할 수 있습니다.

```math
A(s)=\frac{A_0}{1+s/\omega_p},\qquad
H(s)=\frac{A_0}{1+\beta A_0+s/\omega_p}
=\frac{A_0/(1+\beta A_0)}{1+s/[\omega_p(1+\beta A_0)]}.
```

따라서 DC 이득은 $`A_0/(1+\beta A_0)`$, 폐루프 pole은 $`\omega_p(1+\beta A_0)`$입니다. 충분히 큰 loop gain에서 이득은 1/β에 가까워지고 대역폭이 넓어집니다. 이 한 pole 모델에서는 DC 이득과 pole 주파수의 곱이 정확히 $`A_0\omega_p`$입니다. 실제 회로에서 gain-bandwidth를 항상 일정하다고 가정하는 것은 다른 pole·zero와 loading을 무시하는 근사입니다. rad/s와 Hz는 $`\omega=2\pi f`$로 구별합니다.

A0=100000, fp=10 Hz, β=0.1이면 DC 이득은 약 9.9990 V/V, 폐루프 pole은 100010 Hz입니다. 유한한 open-loop gain 때문에 목표 10 V/V보다 조금 작습니다.

### 두 번째 pole과 phase margin

```math
L(j\omega)=\frac{L_0}{(1+j\omega/\omega_1)(1+j\omega/\omega_2)},
\quad |L(j\omega_c)|=1,
\quad PM=180^\circ-\tan^{-1}(\omega_c/\omega_1)-\tan^{-1}(\omega_c/\omega_2).
```

$`\omega_c`$는 loop gain의 0 dB 교차점입니다. 코드에서는 양의 pole 두 개에 의해 크기가 단조 감소하는 성질을 이용해 이분법으로 구합니다. 두 번째 pole이 교차점 가까이 오면 추가 위상 지연 때문에 PM이 작아집니다. 이 단순한 두 pole·양의 DC gain 시스템의 폐루프 분모 계수는 모두 양수여서 안정하지만, 작은 PM에서는 overshoot와 ringing이 커질 수 있습니다. 이 관찰을 임의의 다중 루프·우반평면 pole·시간지연 시스템의 안정성 정리로 확대하지 않습니다. 그런 경우에는 Nyquist 조건과 정확한 loop 정의가 필요합니다.

### 구현과 검증, 실제 회로에 옮기는 조건

```bash
python demo.py --case feedback
python -m unittest -v test_models.HardwareModels.test_feedback_closed_form test_models.HardwareModels.test_feedback_crossover_and_pole_separation
```

`feedback_one_pole()`의 직접 복소수 계산을 유도한 폐루프 식과 여러 주파수에서 비교합니다. `two_pole_margin()`의 교차점에서는 loop 크기가 1인지 확인하고, 다른 조건을 고정한 채 두 번째 pole을 멀리 보냈을 때 PM이 증가하는지도 확인합니다. 같은 함수에서 나온 값끼리의 비교만으로 끝내지 않고, 다르게 정리한 해석식과 물리적으로 예상되는 방향을 사용합니다.

트랜지스터 회로에서는 DC operating point를 먼저 확인하고, 루프를 끊는 위치가 bias와 loading을 바꾸지 않도록 loop injection 방법을 택합니다. Spectre stb 등은 선택한 probe·루프 조건에 따라 해석 의미가 달라지므로 회로와 분석 설정을 함께 기록해야 합니다. 실제 부하 용량·ESR, 출력 전류, PVT, common-mode 범위를 바꿔 loop 응답과 transient 응답을 각각 확인합니다. 여기서는 Python 전달함수만 실행했으며 Spectre 분석이나 보드 안정성을 검증한 것은 아닙니다.

## English

### Why return part of the output?

An amplifier can compare its output with its input much as a thermostat compares temperature with a target. Negative feedback acts to reduce error. Delayed correction, however, can produce excessive correction and oscillatory behavior. DC gain accuracy and frequency-domain stability therefore need separate attention.

The model assumes linear small signals, a constant positive real feedback factor β, and one loop whose amplifier transfer A already includes loading. Slew rate and output saturation are excluded. The model is checked against [ADI MT-033](https://www.analog.com/media/en/training-seminars/tutorials/mt-033.pdf) and [TU Delft's phase-margin treatment](https://analog-electronics.tudelft.nl/webbook/SED/_build/html/freq_compensation/freq_compensation_Phase_margin_design.html).

### Deriving closed-loop gain and bandwidth

Starting with error $`e=x-\beta y`$ and output $`y=Ae`$ yields $`H=A/(1+\beta A)`$ and loop gain $`L=\beta A`$. Substituting the one-pole open-loop model and collecting terms gives the displayed closed-loop expression. Its DC gain is $`A_0/(1+\beta A_0)`$ and its pole is $`\omega_p(1+\beta A_0)`$. Large loop gain brings the DC gain near 1/β while expanding bandwidth.

Within this particular one-pole model, the product of closed-loop DC gain and pole frequency is exactly $`A_0\omega_p`$. Treating gain-bandwidth as constant in a physical circuit is an approximation that can fail with additional poles, zeros or loading. Angular frequency and ordinary frequency differ by $`\omega=2\pi f`$. For A0=100000, fp=10 Hz and β=0.1, the DC gain is about 9.9990 V/V and the closed-loop pole is 100010 Hz. Finite open-loop gain explains the small error from the target gain of ten.

### A second pole and phase margin

For the displayed two-pole loop, the crossover frequency satisfies $`|L(j\omega_c)|=1`$. The phase margin is 180 degrees minus the sum of the two arctangent lags. With two positive poles, magnitude decreases monotonically, so bisection finds the unique crossover when the DC loop gain exceeds one. Moving the second pole toward crossover reduces phase margin.

This particular two-pole closed loop with positive DC gain has positive second-order denominator coefficients and is stable, although a small margin can cause pronounced overshoot and ringing. This is not a general stability theorem for systems with multiple loops, right-half-plane poles or delay. Those require the appropriate Nyquist analysis and a carefully defined loop transfer.

### Implementation, checks and physical use

Run the commands above from the example directory. The tests compare direct complex feedback evaluation with an independently rearranged closed-form transfer at several frequencies. They also require unit loop magnitude at the numerically located crossover and verify increasing phase margin when the second pole is moved away while other parameters remain fixed.

For a transistor circuit, establish its DC operating point first. Loop injection must preserve bias and loading; a Spectre stb result depends on probe placement and the loop being analyzed. Record that setup with the circuit. Examine load capacitance, ESR, output current, PVT and common-mode range, and check transient behavior as well as loop response. The supplied execution evaluates Python transfer functions; it is not a Spectre run or a board stability measurement.

## 출처 / Sources

- Analog Devices, *MT-033*: voltage-feedback gain and bandwidth approximations.
- TU Delft, *Phase margin design*: loop crossover, phase and compensation assumptions. Both sources are linked above.
