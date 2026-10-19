# 확률, 평균, 추정의 불확실성 | Probability, means, and uncertainty in estimation

[수식을 코드로](../README.md) · [실행 코드와 검사](../../../examples/foundations/math_physics/README.md)

## 한국어

### 한 번의 측정과 평균은 다른 질문에 답한다

같은 전압을 여러 번 읽어도 값은 조금씩 달라진다. 한 번의 측정값이 얼마나 흔들리는지와, 여러 번 평균 낸 값이 얼마나 불확실한지는 다르다. 전자는 표준편차, 후자는 평균의 표준오차로 구분할 수 있다. 표준편차가 큰 센서도 독립적인 반복 측정을 모으면 평균의 흔들림은 줄일 수 있다. 그러나 모든 측정에 같은 오프셋이 있다면 평균도 그만큼 치우친다.

확률변수 $X$는 측정 전에 결과를 수로 표현하는 모델이고, 관측값 $x$는 실제로 얻은 한 값이다. 이산 확률변수의 기댓값과 분산은

$$\mu=E[X]=\sum_x xp(x),\qquad \sigma^2=E[(X-\mu)^2].$$

연속형에서는 합 대신 확률밀도에 대한 적분을 쓴다. $X$가 V 단위라면 평균과 표준편차는 V, 분산은 V²다. 이 글은 유한한 평균과 분산을 가진 같은 분포의 독립 표본을 기본 모델로 삼는다. 추정량과 표본분포의 구분은 [MIT 18.05 통계 자료](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/mit18_05_s22_statistics.pdf)에서 확인할 수 있다.

### 왜 평균의 흔들림은 제곱근으로 줄어드는가

$\bar X=(X_1+\cdots+X_n)/n$의 기댓값은 $\mu$다. 독립이면 공분산이 0이므로

$$\operatorname{Var}(\bar X)=\frac{1}{n^2}\sum_i\operatorname{Var}(X_i)
=\frac{\sigma^2}{n},\qquad \operatorname{SE}(\bar X)=\frac{\sigma}{\sqrt n}.$$

표본을 4배 모아야 표준오차가 절반이 된다. 단순히 데이터를 복사해 개수를 늘리는 것은 독립 표본을 추가하는 일이 아니다. 상관이 있으면 정확한 분산식에 $2\sum_{i<j}\operatorname{cov}(X_i,X_j)/n^2$가 추가된다. 시간 순서가 있는 센서 데이터에서는 드리프트와 자기상관부터 확인한다. [NIST TN 1297 Appendix A](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-law-propagation-uncertainty)의 독립 반복 측정 공식도 같은 관계를 사용한다.

모집단 분산을 모를 때의 표본분산은

$$s^2=\frac{1}{n-1}\sum_i(x_i-\bar x)^2,\qquad \widehat{\operatorname{SE}}=s/\sqrt n.$$

분모가 $n-1$인 이유는 평균 하나를 데이터로 추정하면서 잔차 합이 0이라는 제약 하나가 생기기 때문이다. 독립·동일 분포, 유한 분산 조건에서 $E[s^2]=\sigma^2$다. 이것이 $s$ 자체까지 불편 추정량이라는 뜻은 아니다.

### 신뢰구간은 계산 절차의 성질이다

독립 정규 표본이고 모집단 표준편차 $\sigma$를 안다면

$$\bar x\pm z_{1-\alpha/2}\frac{\sigma}{\sqrt n}$$

은 평균의 $100(1-\alpha)$ % 신뢰구간이다. 정규 표본에서 $\sigma$를 표본의 $s$로 추정했다면 $z$ 대신 자유도 $n-1$의 Student $t$ 분위수를 사용한다. 정규성이 없으면 이 결과는 일반적으로 정확한 유한 표본 결과가 아니며, 적절한 중심극한 근사나 분포에 맞는 방법이 필요하다. 이 구분은 [NIST의 알려진 분산 구간](https://itl.nist.gov/div898/handbook/prc/section1/prc14.htm)과 [평균의 t 구간](https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm)을 대조했다.

95 %는 같은 조건에서 표본을 다시 뽑고 같은 계산을 반복했을 때 구간이 모평균을 포함하는 장기 비율이다. 이미 계산한 특정 구간에 참평균이 95 % 확률로 들어 있다는 빈도주의 해석은 하지 않는다. 개별 측정값 95 %가 이 구간 안에 있다는 뜻도 아니다.

### 안정적인 구현과 확인

분산을 `평균(x*x) - 평균(x)**2`로 계산하면 큰 수 둘을 빼면서 정밀도를 잃을 수 있다. 구현은 Welford 갱신을 쓴다. 표본 $x$가 추가되면 $\delta=x-\bar x_{old}$, $\bar x_{new}=\bar x_{old}+\delta/n$, $M_{2,new}=M_{2,old}+\delta(x-\bar x_{new})$다. 한 번 순회하고 상태 세 개만 유지해 시간 $O(n)$, 추가 메모리 $O(1)$이다. 갱신식과 상쇄 오차는 [Chan, Golub, LeVeque (1983), §§1–2](https://math.pku.edu.cn/teachers/litj/notes/numer_anal/AmerStat_37_242_Chan_Variance.pdf)와 대조했다.

```python
from math import sqrt
from models import mean_variance, normal_mean_interval

# 생성기에도 한 번의 순회만 필요하다.
n, mean, variance = mean_variance(iter([1.01, 0.99, 1.02, 0.98]))
estimated_se = sqrt(variance / n)
# 이 예의 sigma=0.02는 알려진 모집단 표준편차라는 별도 가정이다.
interval = normal_mean_interval(mean, sigma=0.02, count=n)
print(mean, estimated_se, interval)
```

`normal_mean_interval`은 알려진 $\sigma$의 정규 모델만 구현한다. 표본 표준편차를 그대로 넣어 소표본 t 구간인 것처럼 사용하지 않는다. 검사는 표준 라이브러리의 평균·분산, 알려진 정규 분위수, 표본 수 4배에서 구간 폭 절반, 상수 표본, 잘못된 입력을 확인한다. 고정 시드의 2,000개 정규 모의 표본으로 구간 포함 비율도 검사하지만, 이 빈도 검사가 모든 분포에서 95 %를 보장하지는 않는다. 실제 데이터에서는 표본 수, 수집 조건, 이상값 처리, 드리프트 여부를 함께 기록한다.

## English

### A reading and an average answer different questions

Repeated readings of a constant voltage vary. The spread of individual readings differs from uncertainty in their average. Standard deviation describes the former, while the standard error of the mean describes the latter. Independent repetitions can reduce variation in the average, but do not remove a shared offset.

A random variable $X$ models an outcome before it is observed; $x$ is one realized value. For a discrete variable, $\mu=E[X]=\sum_x xp(x)$ and $\sigma^2=E[(X-\mu)^2]$. Continuous distributions use integrals against a density. If $X$ is measured in V, its mean and standard deviation are in V and variance in V². The basic model here assumes independent observations from the same distribution with finite mean and variance. [MIT 18.05 statistics readings](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/mit18_05_s22_statistics.pdf) distinguish estimators from their sampling distributions.

### Deriving the square-root rule

For $\bar X=\sum_iX_i/n$, $E[\bar X]=\mu$. Independence removes cross-covariances, yielding $\operatorname{Var}(\bar X)=\sigma^2/n$ and $\operatorname{SE}(\bar X)=\sigma/\sqrt n$. Four times as many samples halves standard error. Copying existing observations does not add independent information. Correlation adds $2\sum_{i<j}\operatorname{cov}(X_i,X_j)/n^2$ to the variance, so sensor time series need checks for drift and autocorrelation. The independent-repeat formula in [NIST TN 1297 Appendix A](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-law-propagation-uncertainty) uses the same relationship.

When variance is unknown, $s^2=\sum_i(x_i-\bar x)^2/(n-1)$ and estimated standard error is $s/\sqrt n$. Estimating a mean imposes the constraint that residuals sum to zero, leaving $n-1$ degrees of freedom. For independent identically distributed observations with finite variance, $E[s^2]=\sigma^2$. This does not make $s$ itself unbiased.

### Interpreting confidence intervals

For independent normal observations with known population standard deviation, the mean interval is $\bar x\pm z_{1-\alpha/2}\sigma/\sqrt n$. For normal data with unknown standard deviation estimated by $s$, use a Student $t$ quantile with $n-1$ degrees of freedom. Without normality, these are not generally exact finite-sample results; an appropriate asymptotic approximation or distribution-specific method is needed. See NIST on [known-variance intervals](https://itl.nist.gov/div898/handbook/prc/section1/prc14.htm) and [t intervals](https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm).

A 95 % confidence level describes the long-run coverage of a repeated sampling procedure. It is not a frequentist probability assigned to the fixed true mean being inside one already computed interval. Nor does it mean that 95 % of individual readings fall there.

### Implementation and verification

Computing variance as `mean(x*x) - mean(x)**2` can lose precision by subtracting large similar numbers. The implementation uses Welford updates: $\delta=x-\bar x_{old}$, $\bar x_{new}=\bar x_{old}+\delta/n$, and $M_{2,new}=M_{2,old}+\delta(x-\bar x_{new})$. One pass takes $O(n)$ time and $O(1)$ additional storage. Updating formulas and cancellation are discussed in [Chan, Golub, and LeVeque (1983), §§1–2](https://math.pku.edu.cn/teachers/litj/notes/numer_anal/AmerStat_37_242_Chan_Variance.pdf).

The example estimates mean, variance, and standard error from four readings. Its interval separately assumes that the population standard deviation is known to be 0.02; it does not substitute the sample standard deviation and call the result a small-sample t interval. Tests compare standard-library statistics, a known normal quantile, the fourfold-sample width rule, constant data, and invalid inputs. A seeded simulation checks coverage over 2,000 normal samples. That check does not establish coverage for arbitrary distributions. Real reports also record sample size, acquisition conditions, treatment of unusual observations, and drift checks.

## 출처 / Sources

- MIT 18.05 statistics readings: 추정량·표본분산·정규 표본 신뢰구간 / estimators, sample variance, and normal-data intervals.
- NIST TN 1297 Appendix A: 평균의 표준불확도 / standard uncertainty of an average.
- NIST statistical handbook, sections 7.1.4 and 1.3.5.2: 알려진 분산·추정 분산의 구분과 신뢰구간 해석 / known versus estimated variance and interval interpretation.
- Chan, Golub, LeVeque, The American Statistician 37(3), 242–247 (1983), DOI 10.1080/00031305.1983.10483115: 분산 계산의 갱신식과 반올림 오차 / updating variance and roundoff error.

계산 예와 모의 표본은 실제 측정 데이터가 아니다. / Calculation examples and simulated samples are not experimental measurements.
