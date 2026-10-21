# 제조 시계열 예측의 미래 정보 경계 / Causal boundaries in manufacturing trace prediction

ST-AWFD 공정 이상 탐지 프로젝트에서는 시점 t의 예측이 t 이후 센서값을 참조하는지 확인해야 합니다. attention 마스크만 확인해서는 입력 임베딩의 미래 참조를 놓칠 수 있습니다. 이 사례는 전처리·모델·저장 추론·보고서의 경계를 코드로 읽고, 합성 자료에 미래 변화를 넣어 관측한 결과를 연결합니다.

2026-10-21에 수행한 것은 로컬 CPU 회귀 검사입니다. 기존 공개 D2 실험 요약과 이번 합성 검사를 구별합니다. 현재 소스 폴더에는 D2 원본·학습 가중치·원래 점수 CSV가 없으므로 과거 GPU 학습을 재현했다고 표시하지 않습니다. 실행 환경·대조 코드·관측값은 [인과 마스크 검증 기록](검증기록_evidence/인과마스크검증_20261021.md)에 있습니다.

## 요구: 예측에 허용하는 정보와 점수에 쓰는 관측을 나눕니다

입력은 lot별 공정 파형입니다. [프로젝트 설명](../프로젝트_projects/st-awfd-anomaly-triage/README.md)은 Step 1의 익명 센서 20개를 상대 시점 64개로 맞추고, 정상 lot로 학습한 뒤 이상 검토 순위를 정하는 과제를 기록합니다. 여기서 lot는 생산 묶음의 식별 단위이며 wafer나 die 수와 같다고 바꾸지 않습니다.

모델은 시점 t에서 1·2·4·8 시점 뒤 값의 평균과 불확실성을 예측합니다. 이때 허용하는 입력은 현재까지의 값입니다. 이후 실제 값이 관측되면 예측과 비교해 Gaussian 음의 로그우도인 NLL을 계산합니다. NLL은 관측값이 예측 분포에서 얼마나 이례적인지 점수화하는 방식이며 불량 확률 그 자체는 아닙니다. 미래 값을 정답으로 평가하는 일과 예측의 입력으로 미리 제공하는 일은 다른 경계입니다.

## 구조: 합성곱과 attention을 함께 제한합니다

[st_awfd_model.py](../프로젝트_projects/st-awfd-anomaly-triage/st_awfd_model.py)의 `StrictCausalConvEmbedding`은 폭 5인 합성곱 앞에 왼쪽 패딩 4개만 넣습니다. 따라서 출력 t의 국소 입력은 t−4부터 t까지입니다. 자동 양쪽 패딩을 끄고, 시점별 feature 축에 LayerNorm을 적용합니다. 임베딩이 이 조건을 지켜야 뒤의 마스크도 의미가 있습니다.

`CausalMultiHorizonGPT.forward`는 `torch.triu(..., diagonal=1)`로 대각선 위를 True로 만든 Boolean 마스크를 전달합니다. 현재 토큰은 현재·과거를 참조하고 미래 토큰은 참조하지 못합니다. [PyTorch 2.10의 마스크 설명](https://docs.pytorch.org/docs/2.10/generated/torch.nn.Transformer.html)은 이 계열 API에서 True가 attention 참여 금지임을 명시합니다. 다른 attention 함수의 Boolean 의미를 확인 없이 가져오면 방향이 뒤집힐 수 있습니다.

코드는 `TransformerEncoder` 클래스를 사용하지만 마스크를 주어 시간 참조를 제한합니다. 이름에 GPT가 있다는 사실보다 실제 입력 경로와 mask 인자가 근거입니다. 출력은 `[batch, time, horizon, sensor]`의 평균·로그 표준편차입니다. `multi_horizon_loss`는 x[t+h]에 맞추어 끝부분의 유효 길이를 잘라 각 horizon의 NLL을 같은 비중으로 평균합니다. 64시점 입력에서 목표가 있는 길이는 각각 63·62·60·56입니다.

## 대안: 같은 분할의 비교와 같은 예측 과제는 다릅니다

[st_awfd_pipeline.py](../프로젝트_projects/st-awfd-anomaly-triage/st_awfd_pipeline.py)의 CNN autoencoder는 전체 파형을 복원합니다. 양쪽 패딩과 복원 목적을 쓰므로 각 토큰의 미래 예측과 같은 요구를 갖지는 않습니다. 두 모델은 완료된 trace의 이상 검토 과제에서는 비교할 수 있지만, CNN의 복원 오차와 Transformer의 예측 NLL을 같은 단위의 점수로 직접 비교하지 않습니다.

분할 함수는 행을 무작위로 섞는 대신 MaterialID 집합을 나누고 교집합을 검사합니다. 이 코드의 추가 표준화는 학습 정상 집합의 평균·표준편차를 다른 집합에도 고정 적용합니다. Transformer의 `prepare_data`도 같은 함수를 호출합니다. 모델별 임계값은 정상 validation 점수의 상위 분위수로 정합니다. 점수 단위가 다르더라도 각 모델에서 같은 기준을 어떻게 적용했는지 확인할 수 있습니다.

[기존 GPU 요약](../프로젝트_projects/st-awfd-anomaly-triage/evidence/historical-run-summary.json)은 정상 학습 441, validation 111, 평가 정상 237·이상 367 lot를 기록합니다. CNN·Transformer·잔차 공분산 대안의 정상 오경보는 각각 57·76·70개입니다. 모두 이상 recall 100%였지만 정상 오경보는 CNN이 적었습니다. 새 구조를 썼다는 이유로 우월성을 주장할 자료는 아닙니다.

[잔차 공분산 코드](../프로젝트_projects/st-awfd-anomaly-triage/st_awfd_gpt_covariance_audit.py)는 학습 정상 잔차로 reference를 맞추고, 기존 checkpoint를 고정한 채 다른 점수화를 비교합니다. 기존 요약에서 Transformer의 Average Precision은 1.0, 공분산 대안은 약 0.9854입니다. 오경보를 줄인 변화와 순위 성능의 변화를 함께 읽어야 합니다. AP가 1이라고 선택한 임계값의 정상 오경보가 0이라는 뜻도 아닙니다.

## 경계 실패 재현: 검사가 실제 누출에 반응하는지 봅니다

[test_causal_model.py](../프로젝트_projects/st-awfd-anomaly-triage/tests/test_causal_model.py)는 난수로 만든 파형과 학습하지 않은 모델을 사용합니다. `causal_invariance_audit`는 cutoff 뒤 입력에만 3을 더하고 cutoff의 평균·로그 표준편차가 바뀌는지 비교합니다. 임계값은 두 최대 절대 차이 모두 10⁻⁶ 미만입니다. dropout을 끈 평가 모드에서 입력 경계의 불변성을 검사합니다.

이번에는 올바른 모델의 통과 외에 두 실패 조건을 메모리 복사본에만 넣었습니다. 하나는 attention 마스크를 제거하고, 다른 하나는 임베딩을 폭 5·양쪽 패딩 2인 합성곱으로 바꿉니다. 뒤의 attention 마스크를 유지해도 임베딩 t가 t+1·t+2를 먼저 읽으면 누출이 생깁니다. 이는 기존 소스에서 발견한 버그의 수정 이력이 아니라 검사의 감도를 확인하는 의도적 대조입니다.

| 이번 합성 CPU 관측 | 평균의 최대 차이 | 로그 표준편차의 최대 차이 |
|---|---:|---:|
| 원본 구조, cutoff 0·8·24 각각 | 0 | 0 |
| 마스크 제거, cutoff 24 | 0.42551446 | 0.28253430 |
| 대칭 패딩, cutoff 24 | 0.96138346 | 1.36331236 |

두 대조는 모두 불변성 조건을 위반했습니다. 구조를 잘못 바꾸어도 항상 통과하는 검사와 구별되는 관측입니다. 다만 한 난수 표본과 몇 시점의 결과로 모든 입력·정밀도·라이브러리 버전의 성질을 증명한 것은 아닙니다.

## 관측: 저장 추론과 결과 출력도 경계를 갖습니다

[저장 CSV 추론 함수](../프로젝트_projects/st-awfd-anomaly-triage/st_awfd_causal_gpt_multihorizon.py)의 `score_new_csv`는 checkpoint의 구조 표식·horizon을 확인하고 feature·시간·ID 열만 선택합니다. 필수 열·유한한 수치·Step 1 존재·중복 시각을 검사한 뒤 저장된 scaler·가중치·임계값을 재사용합니다. 새 CSV의 정답으로 임계값을 다시 맞추는 경로는 아닙니다.

이번에는 임의 초기화한 상태를 epoch 0의 임시 checkpoint로 저장해 합성 3 lot를 읽었습니다. 직접 점수와 저장 후 점수의 최대 차이는 0이었고, target·is_test 열을 추가한 입력도 같은 결과를 냈습니다. 필수 feature 누락, 중복 시각, NaN, Step 1 없는 lot, 0인 표준편차, 다른 horizon의 여섯 잘못된 fixture는 ValueError로 거부했습니다. 이 결과는 추론 배선의 검사이며 제조 데이터에서 학습한 모델의 정확도가 아닙니다.

임계값 초과와 검토 용량도 나눕니다. 고정 임계값은 정상 reference와 비교하는 규칙이고, 상위 비율은 한 배치에서 사람이 검토할 개수를 정합니다. 합성 3 lot에서 검토 비율 10%는 올림해 1개입니다. 임계값 미만이라도 순위 기준으로 선택될 수 있으므로 두 결과 열의 이름을 구별합니다.

[workbook_export.py](../프로젝트_projects/st-awfd-anomaly-triage/workbook_export.py)는 이미 작성된 CSV를 Excel로 정리하는 보조 단계입니다. 기존 [export 검사](../프로젝트_projects/st-awfd-anomaly-triage/tests/test_workbook_export.py)는 Node 없이 7개 시트를 만들고, 의존성 누락·쓰기 실패 때 `csv_only`와 CSV 보존을 확인합니다. 실제 권한을 바꾼 검사가 아니라 PermissionError를 주입한 검사입니다. 수율 입력이 빈 칸이면 빈 결과를 반환하도록 수식을 확인하며, 실측 수율이나 Excel의 수식 재계산 결과를 만든 검사는 아닙니다.

## 모델 내부 검사와 배포·평가 검사를 연결합니다

미래 입력을 차단해도 특성 순서나 전처리가 달라지면 배포 점수는 틀릴 수 있습니다. [별도 배포 재현](AI배포의전처리와특성순서_ai-preprocessing-contract.md)은 작은 선형 모델을 실제 학습해 열 순서 오류로 2/4 판정, scaler 누락으로 1/4 판정이 바뀌는 결과를 기록합니다. 이 Transformer의 장애를 발견했다는 뜻이 아니라, 모델 구조 밖에도 검사할 계약이 있음을 보여 주는 독립 예제입니다.

평가 집합의 독립성도 다른 검사입니다. [group 분할 재현](생산묶음단위분할과평가누출_ai-group-evaluation.md)은 같은 묶음의 지문이 섞인 행 분할에서 80/80, 새 group만 남긴 분할에서 16/80을 관측했습니다. 동일한 합성 모형·한 seed의 결과이며 실제 제조 정확도가 아닙니다. 인과 마스크 검사, 저장 입력 계약, group 분리, 학습 통계의 고정이 각각 무엇을 막는지 구분해서 확인합니다.

## 재현 명령과 결과 보존

이번 환경은 Windows 11, Python 3.12.14, PyTorch 2.10.0+cpu이며 CPU thread는 1개입니다. 기존 unittest 9개가 통과했습니다. 원본·오류 대조와 저장 추론 검사는 별도 probe로 실행했습니다. 프로젝트 소스·기존 요약 20개 파일의 실행 전후 SHA-256 차이는 0개였습니다.

기존 검사는 프로젝트 폴더에서 다음과 같이 재현할 수 있습니다. 임시 결과·캐시 위치를 별도 폴더로 설정하는 전체 명령과 이번 probe 원문은 [검증 기록](검증기록_evidence/인과마스크검증_20261021.md)에 있습니다.

```powershell
python -B -m unittest discover -s tests -v
```

기본 학습 CLI는 고정된 models/results 경로에 기록하므로 이번에는 호출하지 않았습니다. 새 probe는 프로젝트 밖의 존재하지 않는 출력 폴더만 만들고, 원본 모형은 수정하지 않습니다. 독자는 같은 코드·seed·환경으로 수치와 거부 조건을 대조할 수 있습니다.

## 한계: 모델의 인과 마스크와 실제 공정의 인과는 다릅니다

전처리 `resample_step_one`은 완료된 Step의 최소·최대 시간으로 진행률을 정하고 보간합니다. 이 시점에 전체 trace를 사용하므로 이미 보간된 tensor에서의 미래 차단을 원시 스트림의 실시간 조기 경보로 확대할 수 없습니다. lot 점수도 이후 관측된 정답과 비교한 NLL을 trace 전체에서 모은 값입니다.

기존 기록은 같은 정상 111개를 epoch 선택과 임계값 설정에 다시 사용했고, mixed holdout도 여러 연구 비교에서 반복 관찰했습니다. 새로운 시간·설비·제품의 독립 평가가 필요합니다. 익명 센서의 높은 점수는 조사 단서이며 물리적 고장 원인이나 공정 조치의 효과를 입증하지 않습니다. 이 사례가 보여 주는 것은 정보 경계와 실패 조건을 코드·재실행 기록으로 설명하는 방법이며, 실설비 운용·수율 향상·새 제조 데이터 학습 실적은 아닙니다.

## English

This case checks information boundaries in the existing manufacturing-trace model. Nine existing CPU tests passed, and deliberate in-memory changes to the attention mask or convolution padding broke the expected future-perturbation invariance. An untrained synthetic checkpoint also exercised saved inference and six invalid-input conditions. Historical GPU results remain separate from these fresh software checks. Full-trace preprocessing means that tensor-level causal masking does not establish online early-warning performance on raw sensor streams.
