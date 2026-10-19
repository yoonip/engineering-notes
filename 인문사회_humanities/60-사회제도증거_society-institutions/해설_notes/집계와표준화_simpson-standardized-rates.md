# 전체 비율이 층별 비교를 뒤집을 때: Simpson 역설과 표준화

[분야 목차](../README.md) · [구현](../../../예제_examples/심화_advanced/math_reasoning/models.py) · [검증](../../../예제_examples/심화_advanced/math_reasoning/test_models.py)

## 한국어

### 1. 비율에는 분모의 구성이 들어 있습니다

두 집단의 성공률을 비교할 때 전체 숫자만 보면, 집단마다 어려운 사례와 쉬운 사례가 얼마나 섞였는지 놓칠 수 있습니다. 각 조건에서 A의 성공률이 더 높아도, A가 어려운 사례를 훨씬 많이 맡았다면 전체에서는 낮게 보일 수 있습니다. 계산이 모순된 것이 아니라 서로 다른 가중평균을 비교한 결과입니다.

[Penn State STAT 100의 Simpson 역설 설명](https://online.stat.psu.edu/stat100/Lesson06)과 [STAT 507의 직접 표준화 설명, §4.4](https://online.stat.psu.edu/stat507/Lesson04)을 대조했습니다. 여기서는 계산을 분명히 보이기 위해 만든 사례 수를 사용합니다. 이 표는 실제 기관의 평가 자료나 시험 기출문제가 아닙니다.

### 2. 전체 비율을 조건부 비율로 분해합니다

집단을 $`G`$, 결과를 $`Y`$, 사례의 층을 $`Z`$라 하겠습니다. 전체 확률 법칙으로

```math
P(Y=1\mid G=g)
=\sum_z P(Y=1\mid G=g,Z=z)P(Z=z\mid G=g).
```

즉 전체 비율은 층별 성공률 $`r_{gz}`$에 그 집단의 구성비 $`w_{gz}`$를 곱해 더한 값입니다. A와 B를 비교할 때 성공률뿐 아니라 가중치도 달라진다는 점이 핵심입니다.

| 사례 층 / Stratum | A 성공 / 전체 | B 성공 / 전체 | 층별 차이 A−B |
| --- | ---: | ---: | ---: |
| 쉬운 사례 / Easier | 9 / 10 = 0.90 | 80 / 100 = 0.80 | +0.10 |
| 어려운 사례 / Harder | 20 / 100 = 0.20 | 1 / 10 = 0.10 | +0.10 |
| 전체 / Combined | 29 / 110 ≈ 0.2636 | 81 / 110 ≈ 0.7364 | 약 −0.4727 |

A의 쉬운 사례 비중은 1/11이고 B는 10/11입니다. 따라서 전체에서는 B의 쉬운 사례가 큰 가중치를 받습니다. 서로 다른 구성의 집단을 통째로 비교한 것이 각 층의 비교와 반대 방향이 된 이유입니다.

### 3. 같은 모집단 구성으로 맞추어 계산합니다

직접 표준화는 두 집단에 같은 가중치 $`w_z`$를 적용합니다.

```math
R_g^{std}=\sum_z w_z r_{gz},\qquad
\Delta^{std}=\sum_z w_z(r_{Az}-r_{Bz}),
\qquad w_z\ge0,\quad\sum_z w_z=1.
```

예제에서는 두 층을 절반씩 놓으면 A는 $`0.5(0.9)+0.5(0.2)=0.55`$, B는 $`0.5(0.8)+0.5(0.1)=0.45`$입니다. 차이는 +0.10입니다. 실제 평가에서 절반씩 두는 것이 항상 맞는 것은 아닙니다. 기준 모집단의 구성을 무엇으로 정했는지에 따라 목표 질문이 달라지므로, 가중치를 결과와 함께 공개해야 합니다.

두 집단 모두 같은 층의 관측이 있어야 층별 비율을 계산할 수 있습니다. 표본이 0인 층을 조용히 제외하면 기준 모집단이 바뀝니다. 표본이 적은 층에서는 표준화된 점추정이 가능해도 불확실성이 클 수 있습니다. 가중평균 하나만으로 표본 오차까지 사라지지는 않습니다.

### 4. 공정한 비교와 인과효과는 다른 질문입니다

구성을 맞춘 비율은 기술적 비교를 더 분명하게 하지만, 집단 차이가 특정 정책이나 처치 때문에 생겼다는 결론은 추가 가정이 필요합니다. 보정 변수가 원인보다 앞선 공통 원인인지, 결과 이후의 변수인지, 선택 과정과 연결된 변수인지 확인해야 합니다. 관측 가능한 변수를 무조건 더 넣는 것이 해결책은 아닙니다.

[Hernán의 인과 추론 조건 설명](https://doi.org/10.1177/0962280211398037)과 대조하면, 잠재결과를 쓰는 표준적인 인과 해석에서는 consistency, 조건부 교환가능성, positivity 같은 조건이 필요합니다. 예컨대 어떤 층에서 A에 속할 가능성이 아예 없으면, 그 층에서 A의 효과를 관측값만으로 비교하기 어렵습니다. 이 글의 코드는 층별 집계와 공통 가중치를 계산할 뿐, 이런 가정이 현실에서 성립하는지 판정하지 않습니다.

### 5. 구현과 검증

`standardized_rates`는 성공·전체 수와 가중치를 받아 원시 비율과 표준화 비율을 함께 반환합니다. 비율 계산은 `Fraction`을 사용해 이 예의 유리수를 정확히 유지합니다. 소수 가중치도 정확하게 의도하려면 `Fraction(1, 3)`처럼 전달하거나 문자열을 거쳐 구성합니다. 부동소수점 1/3을 넘기면 그 부동소수점 값 자체를 정확히 표현하게 됩니다.

```bash
python 예제_examples/심화_advanced/math_reasoning/demo.py
```

출력은 A의 원시 비율 `29/110`, 표준화 비율 `11/20`, B의 원시 비율 `81/110`, 표준화 비율 `9/20`을 보여줍니다. 테스트는 집계 방향의 반전, 표준화 차이 `1/10`, 공통 모집단을 복제한 독립 계산, 누락된 층·0 표본·잘못된 가중치의 거부를 확인합니다. 층 수를 $`s`$라 하면 집계 연산은 $`O(s)`$이며 입력에 없는 층을 임의로 채우지 않습니다.

## English

### 1. A rate also describes its denominator

An aggregate comparison can hide how easy and difficult cases are distributed. Group A can have a higher success rate in every stratum but a lower overall rate if it receives many more difficult cases. This compares different weighted averages rather than contradictory arithmetic. [Penn State STAT 100](https://online.stat.psu.edu/stat100/Lesson06) explains Simpson's paradox, and [STAT 507 §4.4](https://online.stat.psu.edu/stat507/Lesson04) describes direct standardization. The counts above are constructed arithmetic examples, not actual institutional evaluations or exam questions.

### 2. Deriving the mixture

The law of total probability gives $`P(Y=1\mid G=g)=\sum_zP(Y=1\mid G=g,Z=z)P(Z=z\mid G=g)`$. Overall rate is stratum-specific rate times that group's composition weight. Both the rates and the weights may change between groups.

In the table, A exceeds B by 0.10 in each stratum, yet its aggregate rate is $`29/110`$ versus $`81/110`$. Easy cases have weight 1/11 for A and 10/11 for B, explaining the reversal. Direct standardization replaces those unequal weights with common $`w_z`$, producing $`R_g^{std}=\sum_z w_zr_{gz}`$ and difference $`\sum_z w_z(r_{Az}-r_{Bz})`$. Equal weights give 0.55 for A and 0.45 for B. Equal weights are an example choice, not a universal evaluation standard; the target population and weights must be specified.

Both groups require observations in each weighted stratum. Silently removing empty strata changes the target population. Sparse strata can also make standardized estimates uncertain. Weighting does not remove sampling uncertainty.

### 3. Description and causation

Matching composition clarifies a descriptive comparison but does not by itself establish a causal effect. Adjustment depends on whether a variable is a preceding common cause, a consequence, or part of selection; adding every measured variable is not a general solution. A potential-outcome interpretation typically requires consistency, conditional exchangeability and positivity ([Hernán, 2012](https://doi.org/10.1177/0962280211398037)). An unobserved group in a target stratum cannot be compared directly from these counts. The implementation calculates mixtures and common weights rather than deciding whether causal assumptions hold.

### 4. Execution and validation

`standardized_rates` returns crude and standardized rates using exact `Fraction` arithmetic. Rational weights such as one third should be supplied as `Fraction(1,3)` or an intended decimal string; passing a binary float preserves that float's value instead. The command returns A rates `29/110` and `11/20`, and B rates `81/110` and `9/20`.

Tests verify the reversal, the standardized difference of `1/10`, an independent replicated-population calculation, and rejection of missing strata, zero denominators and invalid weights. Arithmetic work scales linearly with the number of strata; absent data are never invented. Inference about uncertainty or causation requires the corresponding sampling model and substantive assumptions.

## 출처 / Sources

층별·전체 비율의 구분과 표준화의 의미를 대학 자료로 대조하고, 예제의 모든 비율을 정확한 유리수로 검산했습니다. / University references support the comparison and standardization definitions; every example rate is checked with exact rational arithmetic. 확인 / checked: 2026-10-19.
