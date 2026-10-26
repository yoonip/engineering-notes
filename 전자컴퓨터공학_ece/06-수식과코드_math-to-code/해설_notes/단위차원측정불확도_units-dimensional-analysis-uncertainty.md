# 단위, 차원, 측정 불확도 | Units, dimensions, and measurement uncertainty

[수식을 코드로](../README.md) · [모델과 검사 코드](../../../예제_examples/공학기초_foundations/math_physics/README.md)

## 한국어

### 숫자에 의미를 붙이는 일

센서가 `25`를 보냈을 때 이것이 25 °C인지, 25 mV인지, ADC 코드 25인지 알아야 계산을 시작할 수 있습니다. 물리량은 수치와 단위를 함께 가집니다. `1000 mV = 1 V`처럼 단위가 바뀌면 수치도 바뀝니다. 차원은 그보다 큰 분류입니다. 거리의 차원은 길이이고, 속도의 차원은 길이/시간입니다. m와 mm는 단위가 다르지만 차원은 같습니다. SI의 일곱 기본 차원과 유도 단위의 관계는 [BIPM SI Brochure, §2.3.3–2.3.4](https://www.bipm.org/en/publications/si-brochure)에 정리되어 있습니다.

| 물리량 | 정의 예 | SI 단위 | 질량 M·길이 L·시간 T·전류 I로 쓴 차원 |
|---|---|---|---|
| 속도 | $`v=dx/dt`$ | m/s | $`LT^{-1}`$ |
| 힘 | $`F=ma`$ | N | $`MLT^{-2}`$ |
| 에너지 | $`W=\int F\,dx`$ | J | $`ML^2T^{-2}`$ |
| 전력 | $`P=dW/dt`$ | W | $`ML^2T^{-3}`$ |
| 전압 | $`V=P/I`$ | V | $`ML^2T^{-3}I^{-1}`$ |

같은 식에서 더하거나 등호로 연결하는 항은 차원이 같아야 합니다. `거리 + 시간`은 의미가 없습니다. $`x=x_0+vt`$에서는 세 항 모두 길이입니다. 차원이 맞는다고 법칙이 옳다는 뜻은 아닙니다. $`x=x_0+2vt`$도 차원은 맞으므로 계수와 적용 조건은 별도로 검증합니다. 이러한 차원 검사는 [MIT 8.01, Chapter 2](https://ocw.mit.edu/courses/8-01sc-classical-mechanics-fall-2016/mit8_01scs22_chapter2.pdf)와 대조했습니다.

### 식을 무차원으로 바꾸면 보이는 것

감쇠 모델 $`dy/dt=-y/\tau`$에서 $`\tau`$는 시간입니다. $`s=t/\tau`$, $`z=y/y_0`$로 놓으면 $`dz/ds=-z`$가 됩니다. 초기값이 0이 아닐 때 가능한 변환입니다. 이 식은 초와 밀리초를 어느 쪽으로 쓰든 같은 모양입니다. 수치 계산의 핵심 간격도 `dt` 하나가 아니라 $`h/\tau`$입니다. `exp(-t)`처럼 단위가 있는 값을 그대로 지수에 넣지 않고 `exp(-t/tau)`로 비율을 만듭니다. 각도는 rad를 명시해 도와 혼동하지 않으며, 온도 비율이나 열역학식에는 절대온도를 사용합니다. 단순 온도차는 1 K와 1 °C의 크기가 같습니다.

### 오차와 불확도는 구분합니다

오차는 측정값과 기준값 사이의 차입니다. 불확도는 현재 정보로 측정 결과에 부여할 수 있는 값들의 퍼짐을 표현합니다. 참값을 정확히 모르더라도 교정, 반복 측정, 기기 사양 등으로 불확도를 평가할 수 있습니다. 반복 측정이 흔들리는 정도만 줄여도 공통 교정 오프셋이 사라지는 것은 아닙니다.

측정 모델 $`y=f(x_1,\ldots,x_n)`$를 입력 추정값 근처에서 1차 전개하면

```math
\delta y\approx\sum_i c_i\delta x_i,\qquad c_i=\frac{\partial f}{\partial x_i}.
```

양변의 분산을 취하면 공분산 행렬 $`\Sigma`$에 대해

```math
u_c^2(y)\approx \mathbf{c}^T\Sigma\mathbf{c}
=\sum_i c_i^2u_i^2+2\sum_{i\lt j}c_ic_j\mathrm{cov}(x_i,x_j).
```

입력 사이의 공분산이 0이면 교차항이 사라집니다. 독립이면 이 조건을 만족하지만 무상관이 항상 독립을 뜻하지는 않습니다. 비선형성이 크거나 입력이 분모의 0 근처에 있으면 1차 근사가 부적절할 수 있습니다. 이 유도와 조건은 [NIST TN 1297, Appendix A](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-law-propagation-uncertainty)를 기준으로 확인했습니다.

### 저항 측정을 모델로 옮기기

저항 모델 $`R=V/I`$에서 $`c_V=1/I`$, $`c_I=-V/I^2`$입니다. $`V=2.000\ \mathrm V`$, $`I=0.01000\ \mathrm A`$, 표준불확도 $`u_V=0.002\ \mathrm V`$, $`u_I=0.00001\ \mathrm A`$를 넣고 두 입력을 독립으로 가정하면

```math
R=200\ \Omega,\qquad u_R=\sqrt{(0.2)^2+(-0.2)^2}\ \Omega\approx0.283\ \Omega.
```

`±0.283 Ω`는 여기서 표준불확도를 뜻합니다. 이것을 근거 없이 보장 범위나 95 % 구간이라고 부르지 않습니다. 상관계수 $`\rho`$가 있다면 공분산은 $`\rho u_Vu_I`$입니다. 두 측정값에 같은 비율의 스케일 오차가 생기는 경우 저항 비율에서는 그 성분이 상쇄될 수 있습니다.

```python
from models import resistance_uncertainty

# 입력을 V와 A로 통일하고 각 불확도도 같은 단위로 전달한다.
r, u_r = resistance_uncertainty(2.0, 0.01, 0.002, 0.00001)
print(r, u_r)
```

구현은 고정된 입력 두 개를 다루므로 시간·추가 메모리 비용이 $`O(1)`$입니다. 자동 단위 변환기는 아니며 호출자가 SI로 통일합니다. 검사는 독립 입력의 손계산, 양·음 상관의 효과, 0인 전류와 잘못된 입력 거부를 확인합니다. 이 예는 계산식 검증입니다. 실제 저항 측정에서는 리드 저항, 자기 발열, 접촉 상태, 기기의 부담 전압까지 측정 모델에 포함할 필요가 있습니다.

## English

### Giving a number a meaning

A sensor value of `25` could mean 25 °C, 25 mV, or ADC code 25. A physical quantity has both a numerical value and a unit: `1000 mV = 1 V`. A dimension is a broader classification. Metres and millimetres are different units with the same dimension of length; velocity has dimension length/time. The table above gives definitions, SI units, and dimensions of velocity, force, energy, power, and voltage. The seven SI base dimensions and derived units are specified in the [BIPM SI Brochure, §2.3.3–2.3.4](https://www.bipm.org/en/publications/si-brochure).

Terms added together or connected by equality must have matching dimensions. In $`x=x_0+vt`$, every term has dimension length. This check catches incompatible operations, but does not prove a law: $`x=x_0+2vt`$ also passes it. Coefficients and physical assumptions need independent checks. This distinction is consistent with [MIT 8.01, Chapter 2](https://ocw.mit.edu/courses/8-01sc-classical-mechanics-fall-2016/mit8_01scs22_chapter2.pdf).

### Nondimensionalization

For $`dy/dt=-y/\tau`$, define $`s=t/\tau`$ and $`z=y/y_0`$, with nonzero $`y_0`$. Then $`dz/ds=-z`$. The same model works whether time is entered in seconds or milliseconds, provided units agree. The important numerical step is $`h/\tau`$, not the bare value of `dt`. Exponential arguments are dimensionless ratios such as `-t/tau`. Explicit radian notation avoids mixing radians and degrees. Temperature ratios and thermodynamic equations use absolute temperature; temperature differences of 1 K and 1 °C have equal magnitude.

### Error and uncertainty

Error is a difference from a reference value. Measurement uncertainty describes the dispersion of values attributed to the result from available information. Calibration, repeated observations, and instrument specifications can inform it even when the true value is not known exactly. Averaging repeatability noise does not remove a shared calibration offset.

Linearizing $`y=f(x_1,\ldots,x_n)`$ gives $`\delta y\approx\sum_i c_i\delta x_i`$, where $`c_i=\partial f/\partial x_i`$. Taking the variance yields

```math
u_c^2(y)\approx\mathbf{c}^T\Sigma\mathbf{c}
=\sum_i c_i^2u_i^2+2\sum_{i\lt j}c_ic_j\mathrm{cov}(x_i,x_j).
```

The cross terms vanish when the input covariances are zero. Independence is sufficient for this, but uncorrelated inputs are not necessarily independent. Strong nonlinearity or a denominator near zero can invalidate this first-order approximation. [NIST TN 1297, Appendix A](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-law-propagation-uncertainty) provides the propagation law and its assumptions.

### Resistance model, implementation, and checks

For $`R=V/I`$, the sensitivities are $`1/I`$ and $`-V/I^2`$. With $`V=2.000\ \mathrm V`$, $`I=0.01000\ \mathrm A`$, $`u_V=0.002\ \mathrm V`$, and $`u_I=0.00001\ \mathrm A`$, independent inputs give $`R=200\ \Omega`$ and $`u_R=\sqrt{0.2^2+(-0.2)^2}\ \Omega\approx0.283\ \Omega`$. This is a standard uncertainty, not automatically a guaranteed bound or a 95 % interval. For correlation coefficient $`\rho`$, covariance is $`\rho u_Vu_I`$. A shared proportional scale error can cancel in the ratio.

The executable example calls `resistance_uncertainty` with values in V and A. It takes constant time and additional memory. It is not an automatic unit-conversion system: callers normalize units. Tests compare an independent hand calculation, positive and negative correlation, and rejected invalid inputs including zero current. These checks verify the calculation. A physical measurement model may also need lead resistance, self-heating, contact conditions, and instrument burden voltage.

## 출처 / Sources

- BIPM SI Brochure: 차원·단위·물리량 표기 / dimensions, units, and quantity notation.
- MIT 8.01 Chapter 2: 차원 검사의 용도와 한계 / dimensional checks and their limits.
- NIST TN 1297 Appendix A: 공분산을 포함한 1차 불확도 전파 / first-order uncertainty propagation with covariance.

수치 예와 코드는 이 글의 정의에 맞춰 구성했습니다. / Numerical examples and code were constructed for the definitions used here.
