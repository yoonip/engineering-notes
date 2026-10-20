# 생산 묶음 단위 분할과 평가 누출 | Group holdouts and leakage in repeated measurements

같은 생산 묶음의 측정값을 여러 행으로 만들었을 때, 행을 무작위로 나누면 다른 행이라는 이유만으로 독립 평가가 되지는 않습니다. 이미 본 묶음의 비슷한 측정값을 맞히는 일과 처음 보는 묶음을 판단하는 일은 다릅니다. 이 사례는 실제 학습 코드를 두 분할에 적용해 그 차이를 드러냅니다.

[`group_evaluation.py`](../예제_examples/실무검증_practical-validation/ai/group_evaluation.py)는 직접 생성한 40개 group, group당 8회 관측, 총 320행을 사용합니다. 여섯 sensor 축은 단위 없는 합성 값입니다. 기업 공정 자료나 실제 모델의 100% 성능을 나타내는 데이터가 아닙니다.

## 오류를 재현할 수 있도록 자료를 만듭니다

각 group에는 고유한 여섯 값의 중심을 정하고 아주 작은 잡음을 더해 8행을 만듭니다. 중심은 서로 달라 같은 group끼리는 매우 가깝습니다. 정답 class는 group 단위로 임의 배정합니다. 새로운 group의 중심으로 class를 알 수 있는 공통 규칙은 넣지 않았습니다.

이 구조는 “이미 본 묶음의 지문”을 기억하면 높은 점수가 나오는 상황을 분리하기 위한 것입니다. group 번호 자체는 모델 특성에 넣지 않습니다. 식별자 열을 지웠다고 반복 측정의 닮음까지 사라지는 것은 아니라는 점을 보여 줍니다. 실제로 group 효과가 있느냐는 별도 자료와 도메인 지식으로 판단해야 합니다.

모델은 StandardScaler와 1-nearest-neighbor 분류기입니다. nearest neighbor는 학습 자료 중 가장 가까운 관측의 class를 참고하는 방식입니다. k=1은 이웃 하나를 사용한다는 뜻입니다. 여기서는 평가 결과를 보고 k를 고르지 않고 처음부터 1로 고정했습니다. 각 분할의 scaler와 모델은 그 분할의 학습 행에만 fit합니다.

## 두 실험의 행 수를 같게 두고 평가 단위를 바꿉니다

| 항목 | 행 무작위 분할 | group 분리 |
| --- | ---: | ---: |
| 학습 행 | 240 | 240 |
| 평가 행 | 80 | 80 |
| 학습 group 수 | 40 | 30 |
| 평가 group 수 | 35 | 10 |
| 학습·평가에 공통인 group | 35 | 0 |
| 실제 합성 자료 정확도 | 80/80 = 100% | 16/80 = 20% |

행 분할의 평가 group 35개는 모두 학습에도 있습니다. 매우 가까운 같은 묶음의 행이 이웃으로 선택되어 전부 맞았습니다. 이 숫자를 “새 생산 묶음에서 100%”라고 부르면 평가 질문이 바뀝니다. 기존 group의 후속 관측을 예측하는 요구라면 다른 의미가 있을 수 있으므로, 행 분할 자체를 언제나 금지하기보다 실제 배포 대상을 먼저 정합니다.

group 분리의 평가 10개는 모두 처음 보는 묶음입니다. 이번 seed에서는 20%였지만, 새로운 group에서의 보편적인 정확도가 20%라고 추정하려는 실험은 아닙니다. group class를 임의로 배정한 합성 자료에서, 같은 묶음의 지문 기억이 새로운 묶음의 규칙 학습과 다르다는 것을 보인 대조입니다. 80행이 독립된 80개 생산 묶음인 것처럼 불확실성을 계산해서도 안 됩니다.

## 실패가 보이도록 분할 조건을 검사합니다

```python
overlap = set(groups[train_ids]) & set(groups[test_ids])  # &는 두 집합의 교집합입니다.
if overlap:                                             # 빈 집합이 아니면 공유 group이 있습니다.
    raise ValueError("overlapping groups")              # 새 group 평가 조건을 거절합니다.
```

`groups[train_ids]`는 NumPy의 인덱스 배열로 학습 행의 group을 고르는 연산입니다. `set()`이 반복 ID를 하나로 모으므로 행 개수 대신 공유 group을 찾습니다. 코드의 `require_group_separation()`에 행 분할을 넣으면 ValueError가 나고 group 분할은 통과합니다.

기존 제조 프로젝트도 [MaterialID 단위 분할](../프로젝트_projects/st-awfd-anomaly-triage/st_awfd_pipeline.py)과 교집합 검사를 사용합니다. 이 글은 그 소스를 새로 수정한 기록이 아닙니다. 같은 요구를 작은 입력에서 눈으로 확인할 수 있게 만든 별도 오류 대조입니다.

GroupShuffleSplit의 `test_size=0.25`는 행의 25%가 아니라 고유 group의 25%를 고릅니다. 이번에는 모든 group이 8행이므로 평가 행도 80개가 됐습니다. group별 길이가 다르면 행의 비율은 달라집니다. 환자·장비·사용자·촬영 세션·문서 원본 등에서도 적절한 묶음 단위를 정의한 뒤 같은 질문을 적용할 수 있습니다.

## 전처리에서 들어오는 평가 정보도 따로 확인합니다

분할이 맞아도 전체 자료로 평균과 표준편차를 맞추면 평가 자료가 학습 변환에 영향을 줍니다. 이를 검사하기 위해 학습 행은 그대로 두고 평가 행의 여섯 값에만 100을 더했습니다. 이것은 실제 설비 drift의 재현이 아니라 정보가 흘러가는 경로를 확인하는 극단적인 진단 입력입니다.

| 통계 계산 방법 | 평가 입력만 바꾼 뒤 평균의 최대 변화 |
| --- | ---: |
| 학습 집합에서 저장한 scaler로 predict | 0 |
| 학습·평가 전체 행에 다시 fit | 약 25 |

전체 320행 중 평가 80행을 100씩 올렸으므로 전체 평균 변화는 `100×80/320=25`입니다. 실제 관측은 부동소수점 표현으로 약 25.00000000000001이었습니다. 이미 fit한 Pipeline의 평균은 바뀌지 않았습니다. 이 검사는 평균이 평가 입력에 의존하는지 확인하며, 그 의존이 언제나 정확도를 높인다는 실험은 아닙니다.

해결 순서는 예측 대상을 정의하고, group·시간·장비 등의 경계로 먼저 나눈 뒤, 학습 부분에서만 전처리를 맞추는 것입니다. Pipeline은 변환과 모델을 묶어 이 순서를 지키는 데 쓰지만, 잘못 만든 train/test 인덱스를 자동으로 올바르게 바꾸지는 않습니다. 전처리 누출과 group 혼입은 별개의 검사입니다.

## 정확도 외에 남길 관측

결과에는 실제 class를 행, 예측 class를 열로 한 혼동행렬을 저장합니다. group 분리 결과는 `[[8,40],[24,8]]`입니다. 맞은 수는 대각선의 `8+8=16`, 전체는 80입니다. 행 분할은 `[[40,0],[0,40]]`입니다. 두 결과 모두 분할 인덱스·group 목록·정답·예측과 함께 저장하므로, 높은 점수의 계산과 평가 단위를 다시 확인할 수 있습니다.

실제 과제에서 문턱·모델·특성·전처리 중 어떤 선택을 평가 자료를 보고 바꿨는지도 남겨야 합니다. 같은 holdout을 반복해서 보고 최선의 설정을 고르면 이름이 test여도 선택 과정에 들어갑니다. 이 사례는 한 설정·한 group 분할의 원인 확인에 한정하며, 시간 경과·새 공장·새 설비·다중 seed를 통한 일반화 평가를 대신하지 않습니다.

## 실행과 결과

[AI 실행 환경](../예제_examples/실무검증_practical-validation/ai/README.md)을 준비하고 저장소 루트에서 실행합니다. 각 실행은 새 폴더에 입력 JSON·인덱스·예측·환경·소스 해시·검사 결과를 씁니다.

```text
python -B 예제_examples/실무검증_practical-validation/ai/group_evaluation.py --out /new/path/group-evaluation
```

2026-10-21에 Python 3.12.14·NumPy 2.5.4·scikit-learn 1.9.1로 실행해 여섯 대조 조건을 통과했습니다. 공유 group 거절, 수정한 분할의 교집합 0, 같은 group 기억, 새 group 점수 차이, 고정 scaler의 평균 보존, 전체 fit의 평가값 참조를 각각 확인합니다. 실행 상세는 [검증 기록](검증기록_evidence/AI배포와그룹평가검증_20261021.md)에 있습니다.

## 확인 문제

1. 학습과 평가의 행 번호가 다르면 생산 묶음도 독립입니까?
2. group 크기가 다를 때 `test_size=0.25`이면 평가 행도 항상 25%입니까?
3. group을 정확히 나눈 뒤 전체 자료에 scaler를 fit해도 됩니까?

답: 1번은 아닙니다. group ID의 교집합을 확인해야 합니다. 2번은 아닙니다. group 수 기준입니다. 3번은 안 됩니다. 평가값이 학습 변환의 통계에 영향을 줍니다. 이 사례에서는 평가 부분만 +100했을 때 전체 평균이 +25 변했습니다.

## 근거와 관련 글

- scikit-learn 1.9.1, [GroupShuffleSplit](https://scikit-learn.org/1.9/modules/generated/sklearn.model_selection.GroupShuffleSplit.html), group 단위 분할과 비율의 정의.
- [Nearest Neighbors §Classification](https://scikit-learn.org/1.9/modules/neighbors.html#classification), 이웃을 이용한 분류. 2026-10-21 열람했습니다.
- [Common pitfalls §12.2](https://scikit-learn.org/1.9/common_pitfalls.html#data-leakage), 학습 자료만으로 전처리 적합.
- [배포의 전처리·특성 계약](AI배포의전처리와특성순서_ai-preprocessing-contract.md), [기존 제조 시계열 사례](제조시계열의인과경계_causal-trace-validation.md).

## English

Forty synthetic groups each contain eight near-duplicate measurements. A fixed 1-NN pipeline scores 80/80 under a row split with 35 overlapping groups, versus 16/80 on ten unseen groups. The point is the changed evaluation unit, not an estimate of manufacturing accuracy. A separate perturbation shows that full-dataset scaling reads test values while a stored training scaler remains unchanged. Inputs, split indices and predictions are saved for replay.
