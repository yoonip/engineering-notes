# 불량 비율과 경보의 정밀도 / Defect prevalence and alert precision

[사례 본문](../../../설계와검증사례_engineering-cases/불량비율과경보의정밀도_ai-prevalence-precision.md) · [실행 기록](../../../설계와검증사례_engineering-cases/검증기록_evidence/기저율과경보업무량검사_20261021.md)

두 합성 집합의 고정 점수와 정답을 실제로 집계하는 표준 라이브러리 예제입니다. 두 집합 모두 accuracy 90%, recall 90%, FPR 10%이지만 경보 중 실제 불량의 비율은 90%와 약 8.33%입니다. 모델 학습·확률 보정·공정 측정·기존 checkpoint 변경은 하지 않습니다.

| 파일 | 내용 |
| --- | --- |
| [model.py](model.py) | 입력 계약, 고정 threshold 평가, 분모를 포함한 지표와 자체 비용입니다. |
| [fixtures.json](fixtures.json) | A 200행과 B 1,000행의 ID·점수·정답을 한 행씩 적었습니다. |
| [verify.py](verify.py) | 독립 혼동행렬·분수 리터럴, 무정답 상태, 경계, 입력 거부, 오류 변이를 비교합니다. |

## 실행

Python 3.10 이상과 표준 라이브러리만 사용합니다. 이 폴더에서 실행하며 결과에는 매번 새 폴더를 지정합니다.

```powershell
python -X utf8 -B verify.py --out C:/temp/ai-prevalence-normal-new
python -X utf8 -B -O verify.py --out C:/temp/ai-prevalence-optimized-new
python -X utf8 -B verify.py --mutation precision-uses-all-samples --out C:/temp/ai-prevalence-fault-new
```

정상은 exit 0/PASS, 의도적 변이는 exit 1/ERROR입니다. 기존 결과 폴더나 잘못된 fixture는 exit 2로 거부합니다. 비교는 `assert` 문 대신 실패 목록에 기록하므로 `-O`에서도 남습니다. 2026-10-21 최종 실행에서 정상 두 모드는 각각 168개 검사·87개 계약 거부를 통과했습니다. 네 변이를 두 모드로 실행한 8회는 모두 기대한 오류였으며 출력 재사용 2회와 잘못된 fixture 3회는 exit 2였습니다.

## API와 입력 계약

`load_fixture(path)`는 JSON을 읽고, `evaluate_bundle(document)`는 여러 집합을 평가합니다. 작은 입력은 `evaluate_cohort(cohort, policy, cost)`로 평가할 수 있습니다. 세 인자의 모양은 다음과 같습니다.

```python
from model import evaluate_cohort  # from/import는 같은 폴더의 평가 함수를 가져옵니다.
cohort = {"id": "sample", "rows": [{"id": "x1", "score": 0.8, "label": 1}]}  # {}는 사전, []는 행을 담은 리스트입니다.
policy = {"threshold": 0.5, "selection": "fixed-before-evaluation"}  # 평가 전에 고정한 점수 기준입니다.
cost = {"false_positive": 1, "false_negative": 20}  # 실제 금액이 아닌 자체 손실 가중치입니다.
result = evaluate_cohort(cohort, policy, cost)  # ()로 함수를 호출하고 반환 사전을 저장합니다.
print(result["metrics"]["precision"])  # []로 사전의 항목을 읽으며 분자·분모·값을 함께 출력합니다.
```

`score >= threshold`이면 경보입니다. 두 점수 0.8·0.2는 직접 정했으며 80%·20% 확률이라는 뜻이 아닙니다. 지표는 `{"numerator": 9, "denominator": 108, "value": 0.08333333333333333}`처럼 원래 계수를 남깁니다. 분모가 0이면 `value=None`입니다.

label은 정수 0·1 또는 명시적 `null`만 받습니다. label 키 누락은 잘못된 schema이며 `null`은 정답을 모르는 상태입니다. 한 행이라도 `null`이면 전체 집합의 confusion·metrics·cost는 `None`, 상태는 `METRICS_NOT_ESTABLISHED`입니다. 점수에서 셀 수 있는 경보 수와 알려진 정답 수는 남깁니다. 빈 집합도 같은 상태입니다. 정답이 일부 있는 행만 평가해 전체 성능처럼 보고하지 않습니다.

JSON은 300,000바이트 이하이고 중복 키·NaN·Infinity를 거부합니다. 집합은 1~4개, 집합당 최대 2,000행, 전체 최대 4,000행입니다. 빈 집합은 허용합니다. 집합·행 ID는 1~32자의 ASCII 문자·숫자·밑줄·하이픈입니다. 중복 집합 ID, 집합 내 중복 행 ID, 집합 사이 겹치는 행 ID를 거부합니다. 사전은 정해진 키만 받습니다. 점수와 threshold는 bool을 제외한 유한 수 0~1, 비용은 bool을 제외한 정수 0~1,000,000입니다. 문자열 숫자·다른 class·빠진 ID도 거부합니다.

정상 API의 `selection`은 `fixed-before-evaluation`만 받습니다. 이 필드는 호출자의 선언이며 데이터 사용 이력을 자동 인증하지 않습니다. 평가 정답으로 기준을 다시 고르는 `test-labels`는 거부합니다. `mutation` 인자는 교육용 오류 대조이며 실제 평가 경로에 사용하지 않습니다.

| 오류 변이 | 고정 기대값과 달라지는 내용 |
| --- | --- |
| `precision-uses-all-samples` | 경보 수 대신 전체 행 수로 나눕니다. |
| `copy-validation-precision` | 첫 집합의 precision을 다음 집합에 복사합니다. |
| `missing-label-as-normal` | 모르는 정답을 정상 0으로 가정합니다. |
| `retune-on-test-labels` | 금지한 `test-labels` 호출을 받아 평가 정답으로 기준을 고릅니다. |

## 읽은 자료와 범위

[Google ML Crash Course의 지표 설명](https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall)(2026-01-12 갱신)에서 accuracy·recall·FPR·precision과 분모 0을 읽었습니다. [scikit-learn 1.6.1 지표 문서](https://scikit-learn.org/1.6/modules/model_evaluation.html#precision-recall-and-f-measures), [1.5.2 threshold 문서](https://scikit-learn.org/1.5/modules/classification_threshold.html), [1.1.3 calibration 문서](https://scikit-learn.org/1.1/modules/calibration.html)의 관련 절도 확인했습니다. 이 예제는 해당 라이브러리로 학습하거나 평가한 결과가 아니며 모든 표본과 비용은 자체 구성입니다.

## English

This standard-library evaluator counts 200 explicit synthetic rows in A and 1,000 in B at a fixed inclusive threshold of 0.5. TPR 0.9 and FPR 0.1 are deliberately held constant; precision changes from 90/100 to 9/108. Accuracy stays at 0.9 here because TPR and TNR both equal 0.9, not because accuracy is generally invariant to prevalence. Scores are not calibrated probabilities. An unknown label prevents all cohort-level label-dependent metrics and costs from being established, while observable alert counts remain available. The example performs no training, checkpoint modification, clinical evaluation, factory measurement, or safety-cost estimation.
