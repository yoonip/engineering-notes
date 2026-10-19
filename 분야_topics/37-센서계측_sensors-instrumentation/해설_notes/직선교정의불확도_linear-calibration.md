# 직선 교정의 불확도: 기울기와 절편을 함께 다루기

[센서·계측 목차](../README.md) · [교정 모델](../../../예제_examples/심화_advanced/hardware/models.py) · [검산](../../../예제_examples/심화_advanced/hardware/test_models.py)

## 한국어

### 눈금을 고친 뒤에도 남는 오차

센서가 실제 값보다 조금 크게, 일정한 offset을 더해 출력한다고 하겠습니다. 여러 기준값을 넣어 직선을 맞추면 기울기와 offset을 보정할 수 있습니다. 하지만 맞춘 직선도 유한한 관측에서 추정한 것입니다. 보정식 하나만 저장하고 그 불확도를 지우면 측정의 의미를 잃습니다. 특히 기울기와 절편은 독립이 아닐 수 있습니다.

[NIST Dataplot calibration](https://www.itl.nist.gov/div898/software/dataplot/refman1/auxillar/calibrat.htm)은 반응값에서 입력값을 거꾸로 추정하는 inverse calibration을 설명합니다. [JCGM 100:2008 §5](https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf)의 공분산을 포함한 불확도 전파와 대조합니다. 여기의 reference 값은 예시 숫자이며 실제 계측기를 교정한 기록은 아닙니다.

### ordinary least squares가 맞는 조건

기준 입력 xi의 불확도는 y의 noise에 비해 무시할 만큼 작다고 가정합니다. 출력 모델은 $`y_i=ax_i+b+\epsilon_i`$, 각 ε는 독립이고 평균 0, 같은 분산입니다. 이 가정에서 ordinary least squares를 씁니다. x도 유의한 오차가 있거나 y분산이 위치마다 다르면 errors-in-variables 또는 가중 회귀 등 다른 모델이 필요합니다.

```math
S_{xx}=\sum_i(x_i-\bar x)^2,\quad
S_{xy}=\sum_i(x_i-\bar x)(y_i-\bar y),
\qquad \hat a=S_{xy}/S_{xx},\quad \hat b=\bar y-\hat a\bar x.
```

잔차 제곱합을 최소화해 a와 b로 편미분하면 잔차 합과 x×잔차 합이 각각 0이라는 normal equation을 얻습니다. 이를 풀면 위 식이 나옵니다. n>2, Sxx>0이어야 분산을 추정할 수 있습니다.

```math
s^2=\frac{\sum_i(y_i-\hat a x_i-\hat b)^2}{n-2},\quad
u_a^2=\frac{s^2}{S_{xx}},\quad
u_b^2=s^2\left(\frac1n+\frac{\bar x^2}{S_{xx}}\right),\quad
u_{ab}=-\frac{\bar x s^2}{S_{xx}}.
```

기울기 단위는 y/x, 절편은 y, 공분산은 y²/x입니다. 공분산 부호는 x의 원점 선택에도 영향을 받습니다. 이를 빼고 각 항만 더하면 같은 직선을 다른 좌표로 표현했을 때 불확도가 달라지는 오류가 생길 수 있습니다.

### 새 측정값을 역변환하기

새 reading y가 교정 자료와 독립이고 그 표준불확도가 uy라면 $`\hat x=(y-\hat b)/\hat a`$입니다. a가 0이 아니고 상대 불확도가 작아 1차 선형화가 적절하다고 두면 sensitivity는 다음과 같습니다.

```math
\frac{\partial x}{\partial y}=\frac1a,\quad
\frac{\partial x}{\partial b}=-\frac1a,\quad
\frac{\partial x}{\partial a}=-\frac{x}{a},
\qquad
u_x^2=\frac{u_y^2+u_b^2+x^2u_a^2+2xu_{ab}}{a^2}.
```

공분산의 계수는 두 sensitivity의 곱 $`(-x/a)(-1/a)=x/a^2`$에서 +2x/a²가 됩니다. x나 a가 음수일 수도 있으므로 각 sensitivity의 부호가 항상 음수인 것은 아닙니다. 평균 기준 위치 xbar에서는 분자의 parameter 항이 s²/n으로 줄고, 입력 분산에 주는 기여는 s²/(n a²)입니다. 범위 바깥으로 extrapolate하면 기울기 불확도의 기여가 커집니다. uy가 이미 포함한 repeatability를 다시 s²로 더하지 않도록, 새 reading의 uncertainty와 parameter uncertainty를 분리합니다.

### 실행과 독립 검산

```bash
python demo.py --case calibration
python -m unittest -v test_models.HardwareModels.test_calibration_normal_equations test_models.HardwareModels.test_calibration_inverse_and_covariance
```

예제는 x=[0,1,2,3,4], y=[1,3.1,4.9,7.2,8.8]에 직선을 맞춥니다. 잔차 합과 x가중 잔차 합이 0인지 확인하고, fitted x=2에서 역변환이 2인지 확인합니다. 중앙점 분자의 parameter 항을 s²/n과 별도로 대조하고 끝점의 uncertainty가 더 큰지도 확인합니다.

실제 교정은 기준기의 추적성·불확도, 온도, drift, hysteresis, 범위별 비선형성과 독립 check standard를 포함합니다. 1차 전파가 불안정한 거의 0인 slope나 큰 불확도에는 Monte Carlo·inverse prediction interval 등 별도 분석이 필요합니다. 표준불확도 u는 자동으로 95% 구간이 아니며 coverage factor와 자유도를 따로 정해야 합니다. 이 코드는 OLS와 1차 propagation을 검산한 것이고 공인 교정 성적서를 대신하지 않습니다.

### 다섯 관측값으로 계수를 직접 계산합니다

다음은 위에 제시한 예시 데이터의 산술을 풀어 쓴 것이며 실제 장비의 교정 기록이 아닙니다. x̄=2, ȳ=5이고 Sxx=10, Sxy=19.7입니다. 따라서 a=1.97, b=1.06이며 맞춘 직선은 y=1.97x+1.06입니다. 각 잔차는 「관측값−직선 예측값」으로 계산합니다.

| 기준 x | 관측 y | 직선 예측 | 잔차 |
|---|---|---|---|
| 0 | 1.0 | 1.06 | −0.06 |
| 1 | 3.1 | 3.03 | 0.07 |
| 2 | 4.9 | 5.00 | −0.10 |
| 3 | 7.2 | 6.97 | 0.23 |
| 4 | 8.8 | 8.94 | −0.14 |

잔차 제곱합은 0.091이고 잔차 자유도는 n−2=3입니다. 두 계수를 같은 다섯 관측에서 추정했기 때문에 n으로 나누지 않습니다. s²=0.0303333, u_a²=0.00303333, u_b²=0.0182, u_ab=−0.00606667입니다. 여기의 값은 반올림했으므로 표시된 마지막 자리에서 합이 정확히 같지 않을 수 있습니다.

### 새 출력 5.00을 입력으로 되돌립니다

교정 데이터와 독립인 새 출력 y=5.00의 표준불확도를 u_y=0.10이라고 가정하겠습니다. 역변환한 입력은 x=(5.00−1.06)/1.97=2입니다. 중앙점에서 공분산을 포함한 계수 항은 다음과 같습니다.

```math
u_b^2+x^2u_a^2+2xu_{ab}
=0.0182+4(0.00303333)+4(-0.00606667)
\simeq0.00606667.
u_x=\frac{\sqrt{0.10^2+0.00606667}}{1.97}
\simeq0.06434.
```

공분산을 임의로 버리면 약 0.10194가 되어 같은 자료와 다른 결과를 얻습니다. 「불확도는 무조건 큰 쪽으로 더하면 된다」는 규칙으로 바꾸기보다, 같은 직선을 나타내는 계수의 관계를 보존해야 합니다. 중앙점의 0.00606667은 s²/n과도 같습니다.

같은 u_y 가정에서 맞춘 출력 y=1.06, 8.94에 해당하는 x=0, 4의 u_x는 각각 약 0.08524입니다. x=6까지 외삽하면 약 0.12902이지만, 실제 센서가 그 범위에서도 직선이라는 근거는 따로 필요합니다. 계산식이 숫자를 출력한다는 사실은 외삽의 타당성 증거가 아닙니다.

### 교정 뒤의 확인값과 드리프트

새 기준 입력 x=2를 독립적으로 다시 가했는데 출력이 5.30이라면 기존 식의 역변환값은 약 2.1523입니다. 이 차이는 온도·드리프트·기준기·반복 변동 등을 조사할 신호가 될 수 있습니다. 위의 단순 u_x만으로 즉시 합격·불합격을 결정하지 않습니다. 확인 기준기의 불확도와 허용 한계, 적용할 판정 규칙이 필요합니다. 오차가 보일 때마다 같은 확인값을 교정 데이터에 넣으면 독립 확인의 역할을 잃습니다.

### 스스로 확인해 보세요

1. 잔차 분산을 추정할 때 0.091을 5 대신 3으로 나누는 이유는 무엇인가요?
2. x=2에서 공분산을 포함한 계수 항은 s², s²/n 중 무엇과 같나요?
3. x=6의 불확도를 계산할 수 있으면 센서가 그 범위에서도 직선임을 확인한 것인가요?

<details>
<summary>정답과 해설</summary>

1. 다섯 관측으로 기울기와 절편 두 개를 추정하여 잔차 자유도가 3이기 때문입니다. 앞의 독립·등분산 선형 모형을 전제로 합니다.
2. s²/n입니다. 이 항은 출력 쪽 계수 불확도이며 입력 분산에 기여할 때에는 a²으로 더 나눕니다.
3. 아닙니다. 범위 밖의 비선형성이나 환경 변화를 포함한 근거가 필요합니다. 식의 외삽과 물리적 검증을 구분합니다.

</details>

## English

### Correction does not remove uncertainty

A line can correct sensor gain and offset, but that line is estimated from finite data. Retaining only the correction coefficients discards uncertainty in the calibration itself. Slope and intercept can also be correlated.

[NIST Dataplot's calibration documentation](https://www.itl.nist.gov/div898/software/dataplot/refman1/auxillar/calibrat.htm) describes inverse estimation. [JCGM 100:2008, section 5](https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf) provides covariance-aware uncertainty propagation. The data here are constructed examples, not an instrument calibration record.

### Deriving the fit and coefficient covariance

Assume reference x uncertainty is negligible relative to y noise, with $`y_i=ax_i+b+\epsilon_i`$ and independent, zero-mean, equal-variance errors. Ordinary least squares is appropriate under these assumptions. Significant x error or unequal output variance needs another regression model.

Setting derivatives of the residual sum of squares to zero gives zero residual sum and zero x-weighted residual sum. Solving yields the displayed slope Sxy/Sxx and intercept ybar−a xbar. With n>2 and Sxx>0, residual variance is SSE/(n−2). The displayed formulas give slope variance, intercept variance and covariance. Their units are consistent with slope y/x, intercept y and covariance y²/x.

The covariance depends on the choice of x origin. Dropping it can make uncertainty change incorrectly under a coordinate shift representing the same calibration line.

### Inverting a new independent reading

For new reading y independent of the fitted data, estimate x=(y−b)/a. Assume nonzero slope and uncertainty small enough for first-order linearization. Sensitivities are 1/a with respect to y, −1/a with respect to b and −x/a with respect to a. The resulting variance is the displayed $`(u_y^2+u_b^2+x^2u_a^2+2xu_{ab})/a^2`$. The covariance coefficient follows from the product $`(-x/a)(-1/a)=x/a^2`$; the individual sensitivities need not both be negative when x or a can be negative.

At x=xbar, the numerator's parameter term reduces to s²/n, contributing s²/(n a²) to input variance. Farther from the calibration center, slope uncertainty contributes more strongly. Do not add residual repeatability twice if it is already included in the uncertainty of the new reading. Parameter uncertainty and new-reading uncertainty are distinct inputs.

### Executable checks and limits

The commands above fit the five-point example, check both normal equations, recover x=2 from its fitted response and independently verify the midpoint variance reduction. Endpoint uncertainty must exceed midpoint uncertainty for the same reading uncertainty.

Physical calibration also requires reference traceability and uncertainty, temperature, drift, hysteresis, range-dependent nonlinearity and independent check standards. Near-zero slopes or large uncertainties can invalidate first-order propagation and require another interval or Monte Carlo treatment. A standard uncertainty is not automatically a 95% interval; coverage factor and degrees of freedom need separate treatment. This code verifies OLS and linearized propagation, not an accredited calibration certificate.

## 출처 / Sources

- NIST, *Dataplot CALIBRATION*: inverse calibration and calibration versus prediction uncertainty.
- BIPM/JCGM, *JCGM 100:2008*: first-order covariance-aware uncertainty propagation. Links appear above.
