# 증거는 믿음을 어떻게 바꿉니까: 모형 비교와 Bayes factor

[분야 목차](../README.md) · [계산 구현](../../../예제_examples/심화_advanced/math_reasoning/models.py) · [검증](../../../예제_examples/심화_advanced/math_reasoning/test_models.py)

## 한국어

### 1. 같은 자료도 어떤 가설을 비교하는지에 따라 달라집니다

새로운 관측은 모든 가설을 같은 정도로 지지하지 않습니다. 어떤 결과가 한 가설 아래에서는 자연스럽지만 다른 가설 아래에서는 드물다면, 그 차이가 비교의 근거가 됩니다. Bayesian epistemology는 믿음의 정도와 증거에 따른 갱신을 확률로 다루는 철학적 접근입니다. 확률을 쓴다는 이유만으로 가설의 목록이나 사전확률까지 자동으로 정당해지는 것은 아닙니다. 다른 인식론적 접근과도 구분해야 합니다. [Stanford Encyclopedia of Philosophy](https://plato.stanford.edu/entries/epistemology-bayesian/)는 이 규범과 사전확률·객관성의 논점을 함께 설명합니다.

이 글에서는 관측을 잘 설명하는 정도, 모형 사전확률, 모형 안의 매개변수 사전분포를 구분해 계산합니다. 예제는 앞면 횟수 자료이지만 실제 동전의 정밀한 물리 모형이나 어느 연구 결론의 진위를 판정하는 도구로 해석하지 않습니다.

### 2. 사후 odds를 단계별로 유도합니다

모형 $`M_0,M_1`$와 관측 $`D`$에 Bayes 정리를 각각 적용합니다. 두 식을 나누면 공통 분모 $`P(D)`$가 없어져

```math
\frac{P(M_0\mid D)}{P(M_1\mid D)}
=\frac{P(D\mid M_0)}{P(D\mid M_1)}
\frac{P(M_0)}{P(M_1)}.
```

첫 비율이 Bayes factor입니다. 이것은 사후확률 자체가 아니라 사전 odds에 곱하는 증거의 배율입니다. 로그로 계산하면 곱셈이 덧셈으로 바뀝니다. 모형 안에 미지의 매개변수가 있으면, 가장 잘 맞는 한 값의 likelihood만 고르지 않고 사전분포 전체에 대해 평균합니다.

```math
P(D\mid M)=\int P(D\mid\theta,M)\,p(\theta\mid M)\,d\theta.
```

이 적분은 데이터에 잘 맞는 값의 범위가 넓은지, 아니면 사전분포에서 아주 좁은 부분만 잘 맞는지도 반영합니다. 이를 모든 상황에서 “단순한 모형이 옳다”는 법칙으로 바꾸면 안 됩니다. 모형·사전분포의 선택에 따라 비교 결과가 달라집니다.

### 3. 고정 모형과 유연한 모형을 비교합니다

$`M_0`$에서는 앞면 확률을 정확히 1/2로 고정합니다. $`M_1`$에서는 앞면 확률 $`\theta`$에 Beta(1,1), 즉 균등 사전분포를 둡니다. 한 모형이 선택되면 시행들은 해당 확률을 조건으로 독립이라고 가정합니다. 전체 $`n`$회 중 앞면 $`h`$회인, 순서까지 특정한 관측열의 likelihood는

```math
P(D\mid M_0)=2^{-n},\qquad
P(D\mid M_1)=\int_0^1\theta^h(1-\theta)^{n-h}d\theta
=\frac{h!(n-h)!}{(n+1)!}.
```

마지막 식은 Beta 함수의 정규화 적분에서 나옵니다. [MIT 18.655 Lecture 3, pp. 10–12](https://ocw.mit.edu/courses/18-655-mathematical-statistics-spring-2016/9c7b5d5cfb5ad8127c4b9c1a0442f29b_MIT18_655S16_LecNote3.pdf)의 Bernoulli–Beta 관계와 대조할 수 있습니다. 모형 $`M_1`$ 안에서 매개변수의 사후분포는 Beta($`h+1,n-h+1`$)이고 평균은 $`(h+1)/(n+2)`$입니다. 이것은 모형의 사후확률 $`P(M_1\mid D)`$와 다른 값입니다.

횟수만 관측했다면 두 모형의 likelihood에 똑같이 $`\binom nh`$가 곱해져 Bayes factor에서는 상쇄됩니다. 순서열 likelihood와 횟수 likelihood를 한쪽에만 섞으면 잘못된 결과가 나옵니다.

### 4. 계산 결과를 읽는 방법

$`n=20,h=10`$이면 $`M_0`$ 쪽 Bayes factor는 약 3.70입니다. 두 모형의 사전확률을 각각 1/2로 두면 $`P(M_0\mid D)\approx0.78724`$가 됩니다. 앞뒤 횟수가 같다는 이유만으로 공정함이 증명된 것은 아닙니다. 고정 1/2 모형과 균등 사전분포의 유연한 모형 사이에서 얻은 상대적인 결과입니다. 두 모형에 들어 있지 않은 시간 변화나 시행 간 의존성은 이 비교로 발견된다고 보장할 수 없습니다.

`bayes_coin_models`는 factorial을 직접 만들지 않고 `lgamma`로 로그 적분값을 구합니다. 로그 odds를 안정적인 두 가지 logistic 식으로 바꾸어 큰 음수에서도 `exp` overflow를 피합니다.

```bash
python 예제_examples/심화_advanced/math_reasoning/demo.py
```

모형 사전확률을 바꾸었을 때 결과가 얼마나 달라지는지 함께 읽어야 합니다. 실제 분석에서는 후보 모형의 적절성, 자료를 보고 모형을 선택한 과정, 의존성, 사후 예측과 민감도 분석도 중요합니다. 큰 Bayes factor 하나가 연구 설계나 측정의 문제를 대신 확인해 주지는 않습니다.

### 5. 독립 검증

테스트는 $`n=0`$부터 15까지 모든 앞면 횟수에서 정확한 유리수 기준을 계산합니다. 균등 사전분포에서 적분 likelihood는 $`1/[(n+1)\binom nh]`$이므로, 로그 감마 구현과 다른 정수 계산 경로로 검증할 수 있습니다. 관측이 없으면 모형 사후확률이 사전확률 그대로인지 확인하고, 100,000회 규모에서는 로그 계산이 유한한지와 확률의 극한을 확인합니다. 이것은 확률 갱신의 구현 검증이며 특정 철학적 입장의 완전한 정당화는 아닙니다.

## English

### 1. Evidence is relative to hypotheses

An observation supports competing hypotheses differently when their predictions differ. Bayesian epistemology studies probabilistic degrees of belief and norms for updating them. Probabilistic consistency does not automatically justify a hypothesis list or its priors, and this is one epistemological approach among others. The [Stanford Encyclopedia of Philosophy](https://plato.stanford.edu/entries/epistemology-bayesian/) discusses both updating and controversies about priors and objectivity.

This calculation distinguishes model priors, parameter priors within a model, and fit to observations. The coin example is a transparent statistical calculation rather than a detailed physical model or an automatic arbiter of scientific truth.

### 2. Deriving model odds and evidence

Apply Bayes' theorem to each model and divide. The common evidence denominator cancels, leaving posterior odds equal to Bayes factor times prior odds. The Bayes factor is the ratio $`P(D\mid M_0)/P(D\mid M_1)`$, not a posterior probability. Unknown parameters are integrated over their prior distribution rather than replaced by their best-fitting value. This average distinguishes broad predictive support from a narrow well-fitting parameter region. It is not an unconditional rule that simpler models are true; choices of models and priors affect the comparison.

### 3. A fixed coin and a flexible coin

$`M_0`$ fixes the head probability at 1/2; $`M_1`$ uses a uniform Beta(1,1) parameter prior. Trials are conditionally independent given the selected model and parameter. For a specified sequence of $`n`$ results with $`h`$ heads, likelihood under $`M_0`$ is $`2^{-n}`$. Integrating $`\theta^h(1-\theta)^{n-h}`$ under $`M_1`$ gives $`h!(n-h)!/(n+1)!`$. This Beta normalization follows the Bernoulli–Beta relationship in [MIT 18.655 Lecture 3, pp. 10–12](https://ocw.mit.edu/courses/18-655-mathematical-statistics-spring-2016/9c7b5d5cfb5ad8127c4b9c1a0442f29b_MIT18_655S16_LecNote3.pdf).

Within $`M_1`$, the parameter posterior is Beta($`h+1,n-h+1`$), with mean $`(h+1)/(n+2)`$. This parameter mean is distinct from the posterior probability of $`M_1`$. If only the count is observed, both likelihoods gain the same binomial coefficient and it cancels from their ratio. Mixing count and sequence likelihoods on only one side is incorrect.

### 4. Computation and interpretation

For ten heads in twenty trials, the Bayes factor favoring $`M_0`$ is about 3.70. Equal model priors give posterior probability approximately 0.78724. Equal head and tail counts do not prove fairness; the result is relative to these two particular models. Time-varying behavior or dependence absent from both models need not be detected.

`bayes_coin_models` uses `lgamma` to compute integrated likelihoods in the log domain and sign-dependent logistic formulas to avoid exponential overflow. Run the command above. Prior sensitivity, model adequacy, data-dependent selection and posterior prediction remain part of a serious analysis; one evidence ratio does not validate experimental design or measurement.

Tests use exact integer/rational likelihoods for every count with zero through fifteen trials: the flexible sequence likelihood is $`1/[(n+1)\binom nh]`$. They also verify unchanged priors without evidence and finite log calculations at 100,000 trials. These checks establish consistency of the implementation, not a complete philosophical justification of Bayesian inference.

## 출처 / Sources

철학적 의미는 Stanford의 논점과, 확률 적분·사후분포는 MIT의 정의와 대조했습니다. 유리수 기준 계산은 별도로 구현했습니다. / Philosophical interpretation and statistical identities were checked separately, with an independent rational reference. 확인 / checked: 2026-10-19.
