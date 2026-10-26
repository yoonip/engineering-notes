# 자료를 숫자로 읽기: 기준, 비율, 평균 | Quantitative data reasoning

[추론·적성](../README.md) · [실행 코드](../../예제_examples/추론_reasoning/README.md)

## 한국어

### 계산하기 전에 분모부터 정하기

같은 “5 증가”라도 10에서 15가 되었는지, 100에서 105가 되었는지에 따라 변화의 크기는 다릅니다. 표와 그래프를 읽을 때는 무엇을 세었는지, 어느 기간과 집단인지, 어떤 단위인지, 비율의 분모가 무엇인지를 먼저 고정합니다. 계산이 맞아도 기준 집단이 다르면 비교 결론은 틀릴 수 있습니다. 아래 수치는 개념의 차이를 보여 주기 위한 작은 계산 예입니다.

비율은 두 수의 몫입니다. 부분을 전체로 나눈 구성비라면 단위가 소거되고, 거리/시간 같은 비율은 속도 단위를 가집니다. 비중·증가율·평균은 모양이 비슷해도 분모가 다릅니다.

| 비교 | 계산 | 뜻 |
|---|---|---|
| 20에서 25 | $`25-20=5`$ | 절대 증가 |
| 20에서 25 | $`(25-20)/20=0.25`$ | 기준 20에 대한 25 % 증가 |
| 비중 20 %에서 25 % | $`25-20=5`$ percentage points | 비중의 차이 5 %p |
| 비중 20 %에서 25 % | $`(25-20)/20=25\%`$ | 비중 자체의 상대 증가율 |

양의 기준값 $`a`$에서 $`b`$로 바뀐 상대 변화는 $`r=(b-a)/a`$입니다. 따라서 $`b=a(1+r)`$이고, 두 번 변화하면

$$c=a(1+r_1)(1+r_2),\qquad
r_{total}=r_1+r_2+r_1r_2.$$

20 % 증가한 뒤 20 % 감소하면 $`1.2\times0.8=0.96`$이므로 원래보다 4 % 낮습니다. 기준값 0의 증가율은 이 정의로 계산할 수 없습니다. 음수 기준값도 해석이 달라지므로 이 글의 증가율 구현은 양의 기준만 받습니다. 단위와 수치를 함께 다루는 원칙은 [단위·차원 글](../../전자컴퓨터공학_ece/06-수식과코드_math-to-code/해설_notes/단위차원측정불확도_units-dimensional-analysis-uncertainty.md)과 이어집니다.

### 평균의 평균이 틀리는 이유

크기가 $`n_i`$인 집단의 평균이 $`\bar x_i`$라면 그 집단의 합은 $`n_i\bar x_i`$입니다. 전체 합을 전체 개수로 나누면

$$\bar x=\frac{\sum_i n_i\bar x_i}{\sum_i n_i}.$$

이는 비음수 가중치 $`w_i`$에 대한 가중평균 $`\bar x_w=\sum_iw_ix_i/\sum_iw_i`$입니다. [NIST Dataplot의 weighted mean 정의](https://www.itl.nist.gov/div898/software/dataplot/refman2/ch2/weigmean.pdf)와 대조했습니다. 20개의 평균이 80, 80개의 평균이 50이면 전체 평균은 $`(20\times80+80\times50)/100=56`$이지 65가 아닙니다. 모든 가중치를 같은 양수로 곱해도 평균은 같습니다. 정규화된 가중치가 음수가 아니므로 결과는 입력 최솟값과 최댓값 사이에 있습니다.

합격률·오류율처럼 “건수/대상 수”인 비율을 합치려면 대상 수를 가중치로 씁니다. 두 집단의 구성비가 시기별로 달라지면 각 집단 내 변화와 전체 변화의 방향도 다를 수 있습니다. 합계 행이 서로 배타적인 집단을 합친 것인지, 중복 응답이나 누락이 있는지도 확인합니다. 반올림된 비율에서 원래 건수를 정확히 복원할 수 있다고 가정하지 않습니다.

### 기대값과 조건부 확률

결과 $`x_i`$의 확률이 $`p_i`$이면 $`E[X]=\sum_i p_ix_i`$입니다. 확률이 비음수이고 합이 1이므로 기대값도 확률을 가중치로 한 평균입니다. 이것이 한 번의 결과를 보장하거나 가장 흔한 값이라는 뜻은 아닙니다. 예를 들어 0과 10이 같은 확률이면 기대값은 5이지만 실제 결과는 둘 중 하나입니다. 기댓값과 이산 확률변수의 정의는 [Stanford CS109, Lecture Notes 6](https://web.stanford.edu/class/archive/cs/cs109/cs109.1206/lectureNotes/LN06_random_variables.pdf)을 참고했습니다.

조건부 확률은 기준 집단을 바꿉니다. $`P(E\mid H)`$는 $`H`$인 집단에서 $`E`$인 비율이고 $`P(H\mid E)`$는 $`E`$인 집단에서 $`H`$인 비율입니다. 일반적으로 같지 않습니다. $`P(H\cap E)=P(E\mid H)P(H)`$를 $`P(E)`$로 나누고, 전체 집단을 $`H`$와 $`\neg H`$로 분할하면

$$P(H\mid E)=\frac{P(E\mid H)P(H)}{P(E\mid H)P(H)+P(E\mid\neg H)P(\neg H)},\quad P(E)>0.$$

이것이 이진 Bayes 식입니다. 분모의 두 사건은 겹치지 않으며 전체 $`E`$를 이룹니다. 조건부 확률·전체확률·Bayes 유도는 [Stanford CS109, Lecture Notes 4](https://web.stanford.edu/class/archive/cs/cs109/cs109.1206/lectureNotes/LN04_cond_bayes.pdf)와 대조했습니다.

설명용 모델에서 불량 비율이 1 %, 불량품 경보율이 90 %, 정상품 경보율이 5 %라고 하겠습니다. 10,000개 기준으로 불량품 100개 중 경보 90개, 정상품 9,900개 중 경보 495개입니다. 경보 가운데 불량 비율은 $`90/(90+495)=2/13\approx15.38\%`$입니다. 90 %를 그대로 답하면 처음 불량 비율인 base rate를 빠뜨린 것입니다. 이 식에 독립성 가정은 필요 없으며 입력한 비율들이 같은 모집단·조건을 가리켜야 합니다.

### 구현과 독립 검증

```python
from 예제_examples.추론_reasoning.models import weighted_mean, bayes_binary

# 정수·분수·소수 문자열은 유리수로 정확히 계산한다.
print(weighted_mean([80, 50], [20, 80]))
print(bayes_binary("0.01", "0.9", "0.05"))
```

`Fraction`은 이 작은 예에서 반올림을 뒤로 미룹니다. 소수 `0.1`을 float로 넘기면 이미 이진 근사가 들어 있으므로 정확한 십진값이 필요할 때는 문자열을 씁니다. 가중평균은 한 번의 순회에서 $`O(n)`$개의 유리수 연산과 $`O(1)`$개 누산기를 씁니다. 분자·분모의 비트 길이에 따른 연산 비용은 별도입니다. Bayes도 산술 연산 수는 일정하지만 비트 비용이 무조건 일정한 것은 아닙니다.

검사는 집단별 가중평균을 원래 관측값을 펼친 평균과 비교하고, 가중치 배율 불변성·정확한 소수 입력·비율의 경계값을 확인합니다. Bayes는 독립적으로 센 건수와 비교합니다. 두 집단의 경보율이 같으면 사후확률이 사전확률과 같아지는지도 검사합니다. 잘못된 확률, 가중치 합 0, 확률 0 사건의 조건화는 거부합니다. 입력 자료의 정확성이나 실제 분포는 이 산술 검사가 대신 확인하지 않습니다.

## English

### Fix the denominator before calculating

An increase of five means different things when starting from 10 or 100. Reading a table requires identifying the quantity, period, population, units, and denominator. Correct arithmetic can still support a wrong comparison if populations differ. The numbers here are small conceptual examples.

A ratio divides quantities: a part/whole proportion is dimensionless, while distance/time has speed units. From 20 to 25, the absolute increase is 5 and the relative increase is $`(25-20)/20=25\%`$. A share rising from 20 % to 25 % rises by five percentage points, or 25 % relative to its initial share. These are different statements.

For positive baseline $`a`$, $`r=(b-a)/a`$, so $`b=a(1+r)`$. Consecutive changes give $`c=a(1+r_1)(1+r_2)`$ and $`r_{total}=r_1+r_2+r_1r_2`$. Increasing by 20 % then decreasing by 20 % leaves 96 % of the initial amount. A zero baseline makes this relative change undefined; negative baselines need different interpretation, so this implementation accepts only positive baselines. See the connected [units article](../../전자컴퓨터공학_ece/06-수식과코드_math-to-code/해설_notes/단위차원측정불확도_units-dimensional-analysis-uncertainty.md).

### Deriving weighted means

A group of size $`n_i`$ and mean $`\bar x_i`$ has sum $`n_i\bar x_i`$. Dividing the sum across groups by their total size yields $`\bar x=\sum_i n_i\bar x_i/\sum_i n_i`$. The general nonnegative weighted mean is $`\sum_iw_ix_i/\sum_iw_i`$, as defined by [NIST Dataplot](https://www.itl.nist.gov/div898/software/dataplot/refman2/ch2/weigmean.pdf). Twenty observations averaging 80 and eighty averaging 50 combine to 56, not 65. Common positive rescaling of all weights leaves the result unchanged, and nonnegative normalized weights keep it within the input range.

To pool rates defined as count/eligible population, use the eligible population as weight. Changes in group composition can make aggregate and within-group directions differ. Check whether groups are exclusive, responses overlap, or observations are missing. Rounded percentages do not uniquely recover original counts.

### Expectation and reversed conditioning

For outcomes $`x_i`$ with probabilities $`p_i`$, $`E[X]=\sum_i p_ix_i`$. Nonnegative probabilities summing to one make this a weighted average. Expectation is neither a guaranteed single outcome nor necessarily the most frequent result: equally likely 0 and 10 have expectation 5. See [Stanford CS109 Notes 6](https://web.stanford.edu/class/archive/cs/cs109/cs109.1206/lectureNotes/LN06_random_variables.pdf).

$`P(E\mid H)`$ uses the population satisfying $`H`$, while $`P(H\mid E)`$ uses those satisfying $`E`$. They are not generally equal. Writing $`P(H\cap E)=P(E\mid H)P(H)`$ and partitioning $`E`$ into its $`H`$ and non-$`H`$ parts yields

$$P(H\mid E)=\frac{P(E\mid H)P(H)}{P(E\mid H)P(H)+P(E\mid\neg H)P(\neg H)},\quad P(E)>0.$$

The derivation is cross-checked against [Stanford CS109 Notes 4](https://web.stanford.edu/class/archive/cs/cs109/cs109.1206/lectureNotes/LN04_cond_bayes.pdf). With a hypothetical 1 % defect rate, 90 % alarm rate among defective items and 5 % among nondefective items, 10,000 items contain 90 true and 495 false alarms. The defective fraction among alarms is $`90/585=2/13\approx15.38\%`$. Answering 90 % ignores the base rate. This identity needs no independence assumption, but the input rates must describe the same population and conditions.

### Implementation and verification

The Python example calculates the weighted mean and posterior exactly as rational numbers. `Fraction` postpones rounding. A float such as `0.1` already contains binary approximation; use a string when exact decimal meaning matters. Weighted accumulation takes $`O(n)`$ rational operations and a constant number of accumulators. Big-integer bit costs depend on numerator/denominator size. Bayes uses a fixed number of arithmetic operations, not necessarily constant bit cost.

Tests compare weighted groups with an independently expanded population, check scaling invariance, exact decimal input, and probability boundaries. Bayes is compared with direct event counts; equal alarm rates in both groups must leave posterior equal to prior. Invalid probabilities, zero total weight, and conditioning on a zero-probability event are rejected. Arithmetic verification does not validate the source data or real distribution.

## 출처 / Sources

- [NIST Dataplot: Weighted Mean](https://www.itl.nist.gov/div898/software/dataplot/refman2/ch2/weigmean.pdf) — 가중평균의 분모와 정의 / weighted mean and its denominator.
- [Stanford CS109, Notes 4: Conditional Probability](https://web.stanford.edu/class/archive/cs/cs109/cs109.1206/lectureNotes/LN04_cond_bayes.pdf) — 조건부 확률·전체확률·Bayes / conditioning, total probability, Bayes.
- [Stanford CS109, Notes 6: Random Variables](https://web.stanford.edu/class/archive/cs/cs109/cs109.1206/lectureNotes/LN06_random_variables.pdf) — 이산 기댓값 / discrete expectation.

참고일 / Accessed: 2026-10-19. 집단 크기·경보 수치는 개념 설명용이며 실제 관측 자료가 아닙니다. / Group sizes and alarm counts illustrate concepts and are not experimental observations.
