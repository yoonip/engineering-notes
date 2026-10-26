# 불량 비율과 경보의 정밀도 / Defect prevalence and alert precision

[사례 목차](README.md) · [실행 코드](../예제_examples/실무검증_practical-validation/ai_prevalence/README.md) · [검증 기록](검증기록_evidence/기저율과경보업무량검사_20261021.md) · [평가지표와 불확실성](../전자컴퓨터공학_ece/46-AI응용에이전트평가_ai-agents-evaluation/해설_notes/평가지표와불확실성_metrics-uncertainty.md)

## 문제: 정확도 90%인데 경보를 대부분 잘못 울립니다

검사할 제품 100개 중 불량이 50개인 시험 자료와, 100개 중 불량이 1개인 배포 자료는 경보의 의미가 다를 수 있습니다. 같은 비율로 불량을 찾고 정상품을 잘못 경보하더라도, 정상품이 훨씬 많으면 경보함에 쌓이는 오경보가 많아집니다. 이 글은 두 합성 점수 목록을 실제로 집계해 그 차이를 확인합니다.

기저율(base rate)은 해당 집합에서 대상이 원래 얼마나 자주 나타나는지입니다. 여기서는 전체 제품 중 실제 불량의 비율입니다. Precision은 기계의 소수점 정밀도가 아니라, 경보를 낸 것 중 실제 불량인 비율을 뜻합니다. Cohort는 이번에 함께 평가한 표본 집합입니다. 실제 공장·의료 표본이 아니라 직접 정한 ID·점수·정답 1,200행을 사용합니다.

정답 1은 불량, 0은 정상입니다. 점수 0.8 또는 0.2를 각 행에 정하고 평가 전에 threshold 0.5를 고정합니다. `score >= threshold`일 때 경보를 냅니다. 학습·확률 보정·기존 모델 변경은 하지 않습니다.

## 분모가 다른 다섯 질문

TP는 불량에 경보를 낸 건수, FN은 불량인데 놓친 건수, FP는 정상에 잘못 경보를 낸 건수, TN은 정상에 경보를 내지 않은 건수입니다. 양성은 여기서 경보 대상인 불량 class이며, 긍정적 평가나 좋은 제품이라는 뜻이 아닙니다.

| 질문 | 계산 | 분모의 대상 |
| --- | --- | --- |
| 전체에서 맞춘 비율 accuracy | `(TP + TN) / N` | 제품 전체입니다. |
| 불량에서 찾아낸 비율 recall·TPR | `TP / (TP + FN)` | 실제 불량 전체입니다. |
| 정상에서 잘못 울린 비율 FPR | `FP / (FP + TN)` | 실제 정상 전체입니다. |
| 경보에서 실제 불량인 비율 precision | `TP / (TP + FP)` | 경보 전체입니다. |
| 원래 불량 비율 prevalence | `(TP + FN) / N` | 제품 전체입니다. |

FPR 10%와 “경보의 10%가 오경보”는 같은 말이 아닙니다. 전자는 정상 제품을 분모로 하고, 후자는 경보를 분모로 하므로 후자의 비율은 `1 - precision`입니다. 정의는 [Google 지표 설명](https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall)과 [scikit-learn 1.6.1의 이진 분류 설명](https://scikit-learn.org/1.6/modules/model_evaluation.html#binary-classification)을 대조했습니다.

## 고정 예제와 실행 관측

아래 계수는 검증기에 직접 적은 독립 기대값입니다. fixture에는 이 계수만 저장한 것이 아니라 각 ID의 점수·정답을 한 행씩 저장했습니다. 검증기는 평가 함수가 만든 결과를 기대값으로 재사용하지 않습니다.

| 집합 | N | TP | FN | FP | TN | 실제 불량 비율 | 경보 |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| A | 200 | 90 | 10 | 10 | 90 | `100/200 = 1/2` | 100 |
| B | 1,000 | 9 | 1 | 99 | 891 | `10/1000 = 1/100` | 108 |

| 지표 | A | B |
| --- | --- | --- |
| recall·TPR | `90/100 = 0.9` | `9/10 = 0.9` |
| FPR | `10/100 = 0.1` | `99/990 = 0.1` |
| accuracy | `180/200 = 0.9` | `900/1000 = 0.9` |
| precision | `90/100 = 0.9` | `9/108 = 1/12 ≈ 0.08333` |
| 경보 비율 | `100/200 = 0.5` | `108/1000 = 0.108` |

A에서는 경보 100개를 보면 불량 90개를 찾습니다. B에서는 경보 108개를 봐도 불량은 9개이며 정상품 99개가 함께 들어옵니다. B의 경보 중 오경보 비율은 `99/108 = 11/12`, 약 91.67%입니다. 표본 수가 다르므로 “경보 100개 대 108개”와 “제품당 경보 비율 50% 대 10.8%”를 함께 봐야 합니다. 실제 작업 시간은 측정하지 않았으며, 검토자가 경보 하나씩 본다는 가정에서 경보 건수가 검토 항목 수가 됩니다.

두 집합의 accuracy가 같은 것은 이번에 TPR와 TNR을 모두 0.9로 선택했기 때문입니다. TNR은 정상에서 정상으로 판단한 비율 `1-FPR`입니다. 일반적으로 `accuracy = TPR × p + TNR × (1-p)`이며 p는 실제 불량 비율입니다. TPR와 TNR이 서로 다르면 p만 바뀌어도 accuracy가 바뀝니다.

## 기저율이 precision으로 들어가는 과정

표본 전체를 1로 놓고 실제 불량 비율을 p라고 합니다. 불량 중 경보 비율이 r이면 전체 중 TP 비율은 `r × p`입니다. 정상 비율은 `1-p`이고 그중 경보 비율이 f이면 FP 비율은 `f × (1-p)`입니다. 따라서 다음 식을 얻습니다.

```text
precision = TP 비율 / 전체 경보 비율
          = (r × p) / (r × p + f × (1-p))
A: (0.9 × 0.5)  / (0.9 × 0.5  + 0.1 × 0.5)  = 0.9
B: (0.9 × 0.01) / (0.9 × 0.01 + 0.1 × 0.99) = 1/12
```

이것은 혼동행렬을 표본 수로 나눈 자체 계산입니다. “배포처가 바뀌어도 r·f가 유지됩니다”를 측정한 법칙이 아닙니다. 이번 합성 자료는 class별 점수 분포를 같게 두고 불량 비율만 바꿨습니다. 실제 새 공장에서는 조명·설비·재료·라벨 기준이 함께 바뀌어 r·f도 달라질 수 있습니다. 정답 없는 입력에서 p를 이 식으로 자동 추정하는 코드도 없습니다.

## 자체 비용: 합계와 표본당 값을 함께 봅니다

직접 정한 손실 단위로 FP 한 건은 1, FN 한 건은 20을 부과합니다. TP·TN의 비용은 0으로 둡니다. 다음 수치는 실제 금액·산업 안전 위험·검토 인건비가 아닙니다. 실제 경보 검토 인건비를 계산하려면 TP 검토 시간, 항목별 난도, 인력 한도도 따로 넣어야 합니다.

| 집합 | 계산 `FP × 1 + FN × 20` | 합계 | 표본당 비용 |
| --- | --- | ---: | --- |
| A | `10 + 10 × 20` | 210 | `210/200 = 1.05` |
| B | `99 + 1 × 20` | 119 | `119/1000 = 0.119` |

B의 precision은 더 낮지만 자체 비용 합계도 더 낮습니다. 서로 모순되지 않습니다. B는 제품 수가 다섯 배이고 불량 자체는 열 배 적어 놓친 불량이 한 건뿐이기 때문입니다. 이 두 집합만 보고 어떤 제품·공장·AI가 더 우수하다고 판단하지 않습니다. 실제 목표가 누락 방지인지, 오경보 검토 감소인지부터 정하고 비교 모집단과 단위를 맞춰야 합니다.

## 점수 0.8은 불량 확률 80%가 아닙니다

점수는 행을 경보 여부로 나누기 위한 직접 구성한 수입니다. 이번 자료에서 높은 점수 0.8을 받은 행의 실제 양성 비율은 A에서 90%, B에서 약 8.33%이며 80%가 아닙니다. [scikit-learn 1.1.3 calibration 문서](https://scikit-learn.org/1.1/modules/calibration.html)의 도입과 calibration curve 설명을 확인했습니다. 확률 보정은 점수와 실제 빈도의 대응을 별도 자료에서 평가·학습하는 문제입니다. 이번 코드는 보정·확률 추론·표본 오차 구간을 계산하지 않습니다.

## 정답을 모르는 경우와 분모 0

`label=null`은 모르는 정답이고 `label=0`은 정상이라는 확인입니다. 모른다고 정상으로 채우면 오경보·정상 판정 계수가 만들어집니다. API는 하나라도 label이 없으면 집합 전체의 confusion·precision·recall·FPR·accuracy·prevalence·비용을 `None`으로 남기고 `METRICS_NOT_ESTABLISHED`를 반환합니다. 알려진 행만 골라 전체 자료를 대표한다고 보고하지 않는 정책입니다. 경보 수, 전체 행 수, 알려진 정답 수는 여전히 셀 수 있습니다. 정답을 모두 알게 되면 같은 고정 기준으로 별도 평가할 수 있습니다.

정답이 모두 있어도 경보가 없으면 precision의 분모는 0입니다. 실제 불량이 없으면 recall, 정상품이 없으면 FPR의 분모가 0입니다. 이때 해당 지표의 `value=None`과 원래 분자·분모를 기록합니다. 0%나 100%로 바꾸어 쓰지 않습니다. 빈 집합은 성능 미확정 상태이며 `alarm_rate`도 `0/0`, 값은 `None`입니다.

## 평가 정답으로 threshold를 다시 고르는 오류

정상 API는 `selection="fixed-before-evaluation"`만 받습니다. 이 선언은 실제 사용 이력을 인증하지 않으므로, caller가 이미 정답을 보고 기준을 바꿨다면 문자열만 바꿔도 누출이 없어지지는 않습니다. 기준 선택과 최종 평가 자료를 실제로 분리해야 합니다. [scikit-learn 1.5.2 threshold 문서](https://scikit-learn.org/1.5/modules/classification_threshold.html)의 내부 교차검증 주의와 수동 고정 절을 읽었으며, 여기서는 기준 선택 기능 자체를 정상 경로에 두지 않았습니다.

두 점수 0.8·0.2만 있는 A·B에서는 0.5를 0.8로 바꿔도 `>=` 판정이 같을 수 있습니다. 그래서 별도 네 행 `(점수, 정답) = (0.9,1), (0.49,1), (0.6,0), (0.1,0)`을 검사합니다. 고정 0.5에서는 TP·FN·FP·TN이 각각 1이고 비용은 21입니다. 잘못된 경로가 평가 정답을 보고 0.49를 고르면 TP 2·FN 0·FP 1·TN 1로 바뀌어 비용은 1입니다. 같은 자료의 정답으로 고른 결과를 손대지 않은 평가 성능으로 보고하는 것이 오류입니다. 정상 경로는 해당 호출을 `EVALUATION_LABEL_TUNING_FORBIDDEN`으로 거부합니다.

## 짧은 코드와 문법

아래 코드는 B의 독립 계산이며 `model.py`의 결과를 다시 입력해 기대값으로 쓰지 않습니다.

```python
from fractions import Fraction  # from/import는 표준 모듈에서 정확한 유리수 형 Fraction을 가져옵니다.
tp, fn, fp, tn = 9, 1, 99, 891  # 여러 변수에 정수를 한 번에 대입하며 B의 기대 계수입니다.
precision = Fraction(tp, tp + fp)  # ()로 생성하고 +로 경보 전체 108을 계산합니다.
recall = Fraction(tp, tp + fn)  # 실제 불량 10을 분모로 하여 9/10을 만듭니다.
fpr = Fraction(fp, fp + tn)  # 실제 정상 990을 분모로 하여 1/10을 만듭니다.
cost = fp + 20 * fn  # *는 곱셈이며 자체 비용 119를 계산합니다.
print(precision, recall, fpr, cost)  # print()가 1/12 9/10 1/10 119를 출력합니다.
```

모르는 label과 0을 구별하는 핵심은 다음과 같습니다.

```python
def has_missing(rows):  # def는 함수 정의이며 rows는 호출자가 넘기는 행 리스트입니다.
    for row in rows:  # for/in은 리스트의 행을 차례로 하나씩 읽습니다.
        if row["label"] is None:  # []는 사전 항목 접근, is None은 모르는 값을 정확히 확인합니다.
            return True  # return은 함수를 끝내고 참을 반환하며 label 0을 미상으로 취급하지 않습니다.
    return False  # 모든 행을 확인해도 미상 값이 없으면 거짓을 반환합니다.
```

`{}`는 키와 값을 연결하는 사전, `[]`는 행 목록 또는 항목 접근, `()`는 함수 호출에 쓰입니다. `None`은 아직 값이 없다는 Python 값이며 0과 다릅니다. Python의 bool은 int의 하위 형이므로 입력에서는 `type(label) is int`로 True·False를 class 정수로 받지 않습니다. 중복 키는 JSON을 사전으로 바꾸는 순간 별도 훅에서 거부하고, 행 ID는 `set`으로 중복을 확인합니다.

## 오류 재현과 확인 범위

네 변이는 원래 기대값을 유지한 채 다른 계산을 실행합니다. 전체 행 수로 precision을 나누면 A가 `9/20`으로 바뀌고, A의 precision 캐시를 B에 복사하면 B가 `9/10`으로 잘못 표시됩니다. 미상 label을 정상으로 바꾸면 성능 미확정 상태를 깨며, 평가 정답 기반 재선정은 금지한 호출을 허용합니다.

정상 기본·`-O`에서 각각 168개 검사와 87개 계약 거부가 통과했습니다. 네 변이의 두 모드 8회는 모두 exit 1로 실패했고, 기존 출력 재사용 2회와 잘못된 fixture 3회는 exit 2였습니다. ID 누락·중복, 집합 중복·겹침, schema 키 누락·추가, bool·NaN·범위 밖 점수·다른 class, 분모 0과 경계 점수도 실제 검사했습니다. 원시 관측과 최종 소스 해시는 [검증 기록](검증기록_evidence/기저율과경보업무량검사_20261021.md)에 연결했습니다.

이 실행은 확정된 합성 계수의 산술·정책 검사입니다. 표본 대표성, 정답 신뢰성, 공장 drift, 모델 학습, 확률 보정, 실제 업무 처리량·임상 효과·안전 성능은 입증하지 않습니다. 기존 학습·holdout·checkpoint는 변경하지 않았습니다.

## 확인 문제

1. B에서 FPR가 10%인데 경보 중 오경보가 약 91.67%인 이유는 무엇입니까? FPR의 분모는 정상품 990개이고 후자의 분모는 경보 108개이기 때문입니다.
2. B의 자체 비용이 119로 더 작으면 같은 기준의 AI가 더 좋아진 것입니까? 아닙니다. 표본 크기·실제 불량 비율이 다르고 r·f는 같은 값으로 정했습니다. 합계만으로 비교할 수 없습니다.
3. 경보는 108개지만 정답을 아직 모른다면 precision은 얼마입니까? 이 코드에서는 미확정입니다. 108은 점수에서 계산할 수 있지만 TP·FP는 정답 없이 알 수 없습니다.

## English

The executable example evaluates explicit synthetic score/label lists, not an estimator or a deployed factory system. At a fixed inclusive threshold of 0.5, cohort A has TP/FN/FP/TN = 90/10/10/90 and cohort B has 9/1/99/891. Both have TPR 0.9, FPR 0.1, and accuracy 0.9, while precision changes from 90/100 to 9/108. Accuracy is constant here because TPR and TNR are both 0.9; this is not a general invariance under a change in prevalence.

The derivation holds class-conditional score distributions fixed by construction. It does not establish that they remain fixed in a new factory. Scores 0.8 and 0.2 are synthetic decision scores, not calibrated probabilities. The deliberately assigned loss `FP + 20*FN` is 210 and 119, or 1.05 and 0.119 per sample. It is not monetary, labor, clinical, or safety evidence.

Any unknown label makes all label-dependent cohort metrics and losses unestablished; observable alert counts are retained. A zero denominator gives a `None` value with the original numerator and denominator. Normal evaluation rejects threshold selection from evaluation answers. A separate four-row error contrast changes the threshold from 0.5 to 0.49 and apparent loss from 21 to 1, illustrating why reusing evaluation labels is a contract violation. Normal and optimized runs passed 168 checks each; all four implementation mutations were detected in both modes.
