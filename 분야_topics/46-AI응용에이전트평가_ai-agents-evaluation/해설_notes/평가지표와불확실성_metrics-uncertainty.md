# Macro·micro 지표와 평가의 불확실성

[지표와 구간 구현](../../../예제_examples/심화_advanced/ai_data/advanced_ai_models.py) · [실행 CLI](../../../예제_examples/심화_advanced/ai_data/demo.py) · [독립 검증](../../../예제_examples/심화_advanced/ai_data/test_advanced_ai.py)

## 같은 정답률에도 다른 모습이 있습니다

사진 열 장 중 아홉 장이 고양이이고 한 장이 강아지라고 하겠습니다. 모든 사진을 고양이라고 답하면 정답률은 90%입니다. 숫자만 보면 좋아 보이지만 강아지는 하나도 찾지 못합니다. 평균을 어떻게 내느냐는 부수적인 표시 방법이 아닙니다. 어떤 실패를 크게 반영할 것인지 정하는 평가 설계입니다.

여기서는 각 표본에 정답과 예측이 하나씩 있는 single-label 다중 분류를 다룹니다. 평가할 클래스 목록은 미리 고정하고 실제 정답·예측을 모두 포함합니다. 여러 정답을 동시에 허용하는 multilabel 분류, ranking, 생성 문장 품질의 평균에는 아래 등식이 그대로 적용되지 않습니다. [Stanford 정보검색 교재의 macro·micro 설명](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-text-classification-1.html), [Google의 분류 평가 설명](https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall)

## 클래스별 집계에서 전체 지표로

클래스 c를 하나 정해 “c인가?”를 이진 질문으로 바꿉니다. TP는 c를 c라고 맞힌 수, FP는 다른 클래스를 c라고 예측한 수, FN은 실제 c를 놓친 수입니다. Precision은 예측한 c 중 맞은 비율이고 recall은 실제 c 중 찾아낸 비율입니다.

```math
P_c=\frac{TP_c}{TP_c+FP_c},\qquad
R_c=\frac{TP_c}{TP_c+FN_c}.
```

두 비율의 조화평균을 통분하면 F1의 계수 형태가 나옵니다.

```math
F1_c=\frac{2P_cR_c}{P_c+R_c}
=\frac{2TP_c}{2TP_c+FP_c+FN_c}.
```

이 식은 분모가 0이 아닐 때 적용됩니다. 예제는 정답에도 예측에도 없는 클래스의 F1을 0으로 정합니다. 그 클래스를 평균에서 제외하는 관례와 값이 달라질 수 있으므로 클래스 목록과 0 분모 처리 규칙도 결과의 일부입니다. 클래스 c가 존재하지만 한 번도 맞히지 못해 분모가 양수이면 F1은 0입니다.

Macro-F1은 각 클래스 F1을 같은 비중으로 평균합니다. Micro-F1은 클래스별 계수를 먼저 합친 뒤 비율을 만듭니다.

```math
F1_{\mathrm{macro}}=\frac1C\sum_c F1_c,\qquad
F1_{\mathrm{micro}}
=\frac{2\sum_cTP_c}{2\sum_cTP_c+\sum_cFP_c+\sum_cFN_c}.
```

Macro-F1은 평균 precision과 평균 recall을 구한 뒤 만든 F1과 일반적으로 다릅니다. 평균과 비선형 비율 계산의 순서를 바꿀 수 없기 때문입니다.

## Micro-F1이 accuracy와 같아지는 조건

위 single-label 조건에서 맞힌 표본은 TP를 하나 만들고, 틀린 표본은 예측 클래스에 FP 하나와 정답 클래스에 FN 하나를 만듭니다. 정답 수를 K, 오답 수를 E라 하면

```math
\sum_cTP_c=K,\qquad \sum_cFP_c=\sum_cFN_c=E,
\qquad F1_{\mathrm{micro}}=\frac{2K}{2K+2E}=\frac{K}{K+E}.
```

따라서 모든 클래스를 포함한 single-label 분류에서 micro-F1은 accuracy입니다. 관심 클래스 일부만 집계하거나 multilabel인 경우까지 넓혀 해석할 수는 없습니다.

CLI의 정답은 A 9개, B 1개이고 예측은 모두 A입니다. 결과를 직접 세면 다음과 같습니다.

| 클래스 | TP | FP | FN | F1 |
|---|---:|---:|---:|---:|
| A | 9 | 1 | 0 | 18/19 |
| B | 0 | 0 | 1 | 0 |
| 전체 | | | | macro = 9/19 ≈ 0.4737, micro = 0.9 |

작은 클래스도 중요한 문제라면 0.9 하나보다 이 표가 실패 형태를 더 잘 보여 줍니다. 반대로 실제 빈도를 반영한 전체 정답률이 목적이라면 macro만으로 판단하는 것도 맞지 않습니다. 지표는 사용 목적과 함께 읽어야 합니다.

## 표본 열 개의 90%는 얼마나 확실합니까

지표가 정확히 계산되었다고 모집단 성능까지 정확히 아는 것은 아닙니다. 고정된 모델을 독립적으로 같은 분포에서 얻은 n개 표본에 평가하고, 각 정답 여부가 성공 확률 p인 Bernoulli라고 모델링하겠습니다. 관측 정답률은 $`\hat p=K/n`$입니다. 같은 환자의 연속 사진이나 같은 문서의 여러 조각을 독립 표본으로 세면 이 가정이 깨질 수 있습니다.

Wilson 구간은 후보 p에 대한 score 부등식을 뒤집어 얻습니다. 정규 근사의 임계값 z에 대해

```math
\frac{(\hat p-p)^2}{p(1-p)/n}\le z^2
\quad\Longrightarrow\quad
(n+z^2)p^2-(2n\hat p+z^2)p+n\hat p^2\le0.
```

이 이차식의 두 근이 구간의 경계입니다. 정리하면

```math
\mathrm{center}=\frac{\hat p+z^2/(2n)}{1+z^2/n},\qquad
\mathrm{half}=\frac{z\sqrt{\hat p(1-\hat p)/n+z^2/(4n^2)}}{1+z^2/n}.
```

95% 근사 구간은 $`z\approx1.959964`$로 center ± half입니다. n=10, K=9를 실제 계산하면 약 [0.59585, 0.98212]입니다. 작은 평가셋의 점 추정 90%와 넓은 구간이 동시에 성립합니다. K=0일 때도 상한은 $`z^2/(n+z^2)`$이며 0으로 붙지 않습니다. [NIST의 Wilson 구간과 score 방법](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm)

빈도주의 신뢰수준은 같은 표본 추출과 계산을 반복했을 때 만들어지는 구간들의 포괄률에 관한 것입니다. 이번 고정된 p가 계산된 구간 안에 있을 확률을 사후확률로 부여한 것이 아닙니다. Wilson은 근사 방법이며 모든 p,n에서 정확히 95%를 보장하지도 않습니다.

## 실행과 독립 검증

```bash
python "예제_examples/심화_advanced/ai_data/demo.py" metrics
python -m unittest discover -s "예제_examples/심화_advanced/ai_data" -p "test_*.py" -v
```

구현은 표본을 한 번 읽어 클래스별 TP·FP·FN을 집계합니다. 표본 수 n, 클래스 수 C에 대해 시간은 O(n+C), 추가 집계 공간은 O(C)입니다. 테스트는 위 열 개 표본의 계수를 손으로 정한 값과 비교합니다. Wilson 경계는 구현의 center·half 공식을 다시 복사하지 않고 원래 score 이차식에 대입해 잔차가 거의 0인지 확인합니다. 성공 0회와 전부 성공인 경계도 검사합니다.

Wilson 구간은 이 문서의 정답 여부에 적용했습니다. F1은 여러 계수의 비선형 함수이므로 F1에 이 구간을 그대로 붙이지 않습니다. 모델 두 개를 같은 표본에서 비교할 때도 결과가 짝지어져 있습니다. 각 모델의 독립 구간 겹침만으로 차이의 유의성을 판정할 수 없습니다. 데이터 그룹, 모델 선택에 사용한 검증셋과 최종 평가셋의 분리, 평가 표본 간 의존성을 먼저 정해야 비교의 의미가 선명해집니다.

## English

### An average chooses which failures matter

If nine of ten images are class A and one is B, predicting A for every image produces 90% accuracy while never recognizing B. Averaging is part of evaluation design: it determines which failures contribute most.

This example covers single-label multiclass classification, with one true and one predicted label per sample. A fixed class list includes every true and predicted label. The identities below do not automatically apply to multilabel tasks, ranking or generated-text quality. [Stanford's classification evaluation chapter](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-text-classification-1.html) and [Google's classification metrics](https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall) provide the reference conventions.

### Derive F1 and its averages

For each class, treat membership as a binary question. TP counts correctly predicted members, FP counts nonmembers predicted as members, and FN counts missed members. Precision is TP/(TP+FP), recall is TP/(TP+FN). Simplifying their harmonic mean gives $`F1_c=2TP_c/(2TP_c+FP_c+FN_c)`$.

The implementation assigns zero when that denominator is zero, including a class absent from both truth and predictions. Excluding such a class would change the macro average, so the class list and zero-denominator convention are part of the reported result. A present class with no correct predictions and a positive denominator has F1 zero.

Macro-F1 averages the class F1 values equally. Micro-F1 sums their TP, FP and FN first and then computes the ratio shown above. Macro-F1 is generally not the F1 calculated from averaged precision and recall: a nonlinear ratio does not commute with averaging.

Under complete single-label classification, every correct sample contributes one TP, and every error contributes one FP and one FN. With K correct and E incorrect samples, micro-F1 is $`2K/(2K+2E)=K/(K+E)`$, which is accuracy. Restricting the measured classes or allowing multiple labels invalidates this particular derivation.

For the executed nine-A/one-B example, class A has TP=9, FP=1, FN=0 and F1=18/19. Class B has TP=0, FP=0, FN=1 and F1=0. Macro-F1 is 9/19, about 0.4737, while micro-F1 and accuracy are 0.9. If rare classes matter, these counts expose a failure hidden by accuracy. If the objective is the overall correctness at the actual class frequency, macro alone is also insufficient; the objective determines which summaries are useful.

### A score is an estimate from samples

Correct arithmetic does not remove sampling uncertainty. Model the correctness indicators of a fixed classifier as independent Bernoulli observations with a common success probability p. Then $`\hat p=K/n`$ estimates p. Multiple frames from one patient or fragments from one document may violate independence.

Wilson's interval inverts the score inequality $`n(\hat p-p)^2\le z^2p(1-p)`$. Expanding produces the quadratic above; its roots are center ± half. With z approximately 1.959964, n=10 and K=9, the executed approximate 95% interval is [0.59585, 0.98212]. A point estimate of 90% can coexist with substantial uncertainty. With no successes, its upper endpoint remains $`z^2/(n+z^2)`$ rather than collapsing to zero. [NIST's proportion interval reference](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm) explains the Wilson construction.

Frequentist confidence refers to coverage by intervals produced over repeated sampling. It does not assign a posterior probability that the fixed p lies inside this particular computed interval. Wilson coverage is approximate, not exactly 95% for every p and n.

### Executed implementation and limits

The commands count TP, FP and FN in one pass, requiring O(n+C) time and O(C) extra counts for n samples and C classes. Tests compare the ten-sample counts with the explicit table. Independently, substituting each Wilson endpoint into the original score quadratic checks near-zero residual; zero-success and all-success endpoints are tested too.

This Wilson interval applies to the Bernoulli correctness indicators, not directly to F1, a nonlinear function of several counts. Two models evaluated on the same samples produce paired results; overlap of separate intervals is not by itself a test of their difference. Grouping dependent samples and separating model-selection data from final evaluation are necessary to interpret the comparison.

## 출처 / Sources

- [Stanford, Introduction to Information Retrieval: Evaluation of text classification](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-text-classification-1.html): class-level counts and macro/micro averaging.
- [Google Machine Learning Crash Course: Accuracy, precision, recall](https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall): metric definitions and imbalanced-class interpretation.
- [NIST Engineering Statistics Handbook: Confidence intervals for a proportion](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm): Wilson score intervals. 확인 / checked: 2026-10-19.
