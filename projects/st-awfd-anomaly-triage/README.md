# ST-AWFD 공정 이상 탐지

공개 반도체 제조 시계열에서 정상 공정의 파형을 학습하고, 이상 징후가 있는 lot의 검토 순위를 계산한다. CNN autoencoder와 strict-causal multi-horizon Transformer를 같은 데이터 분할에서 비교했다. Python 학습·추론 코드, Jupyter notebook, Streamlit 화면과 실험 요약을 담았다.

## 데이터와 모델

[STMicroelectronics ST-AWFD](https://github.com/STMicroelectronics/ST-AWFD)의 D2를 사용했다. 공식 정의에서 MaterialID는 생산 lot이고, `duration_ms`는 정규화된 상대 시간이다. Step 1의 익명 센서 20개를 64개 상대 시점으로 보간했다. 정상 lot 441개로 모델과 scaler를 맞추고, 정상 111개로 epoch와 경보 기준을 정했다. 공개 평가 집합은 정상 237개와 이상 367개다.

CNN denoising autoencoder는 정상 파형을 복원한다. Transformer는 과거 방향 Conv1d embedding과 causal attention으로 1·2·4·8 시점 뒤 센서값의 평균과 불확실성을 예측한다. 관측값의 Gaussian NLL을 이상 점수로 사용한다. 저장 모델 추론은 학습 때 정한 scaler와 경보 기준을 그대로 적용한다.

## 기록된 GPU 실험

RTX 3070 Ti에서 Transformer를 271 epoch 학습했고, 정상 validation NLL이 가장 낮은 241 epoch 모델을 저장했다. 같은 공개 평가 집합의 결과는 다음과 같다.

| 지표 | CNN autoencoder | Transformer | Transformer + 잔차 공분산 |
|---|---:|---:|---:|
| 이상 탐지 recall | 100% | 100% | 100% |
| 정상 오경보 | 57 / 237 | 76 / 237 | 70 / 237 |
| 정상 오경보율 | 24.05% | 32.07% | 29.54% |
| Precision | 86.56% | 82.84% | 83.98% |
| F1 | 0.9279 | 0.9062 | 0.9129 |
| Average Precision | 1.0000 | 1.0000 | 0.9854 |
| 상위 61개 검토 대상 중 이상 | 61 | 61 | 59 |

잔차 공분산 점수는 Transformer의 오경보를 줄이는 대신 순위 성능이 낮아졌다. 이 조건에서 정상 오경보는 CNN이 가장 적었다.

정상 111개를 epoch 선택과 경보 기준 설정에 함께 사용했고, 같은 holdout에서 여러 모델을 비교했다. 결과는 공개 데이터의 탐색 실험이다. 입력은 전체 step을 보간한 trace이므로 모델 내부의 미래 입력 차단 검사와 실시간 원시 데이터 예측은 구분한다. 이 데이터의 정답은 lot의 정상·이상 구분이며, 공정 조치에 따른 최종 die 수율 변화는 포함하지 않는다.

## 파일 구성

| 경로 | 내용 |
|---|---|
| `st_awfd_model.py` | Transformer 구조, Gaussian loss, 고정 모델 추론과 causal 검사 |
| `st_awfd_causal_gpt_multihorizon.py` | Transformer 학습·평가, 저장 checkpoint CSV 추론 |
| `st_awfd_pipeline.py` | D2 처리, CNN autoencoder와 통계 기준선 |
| `st_awfd_gpt_covariance_audit.py` | 저장 Transformer의 잔차 공분산 점수 비교 |
| `workbook_export.py` | 공개 openpyxl 기반 Excel export와 CSV fallback |
| `st_awfd_app.py` | 학습 진행, 모델 비교, CSV 추론 화면 |
| `ST_AWFD_PE_Anomaly_Lab.ipynb` | CNN 학습·평가 |
| `ST_AWFD_Strict_Causal_GPT_실습.ipynb` | Transformer 학습·평가 |
| `ST_AWFD_저장모델_추론.ipynb` | 학습 결과와 무라벨 예제 CSV를 읽는 추론 |
| `evidence/` | 과거 GPU 실험과 공개 준비 과정의 검증 요약 |

## 실행

Python 3.12 이상에서 가상환경을 만든다. [PyTorch 설치 선택기](https://pytorch.org/get-started/locally/)에서 운영체제와 CPU/CUDA 환경에 맞는 PyTorch를 설치한 뒤 나머지 패키지를 설치한다.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

공식 저장소의 `Datasets`에 있는 D2.zip을 `data/st_awfd/D2.zip`에 둔다. 원본 데이터와 학습 가중치는 이 source 폴더에 포함하지 않았다. 학습 명령은 `models/`와 `results/`에 새 결과를 저장한다.

```powershell
# CNN 기준선
python st_awfd_pipeline.py
# Transformer
python st_awfd_causal_gpt_multihorizon.py
# 공개 D2에서 정답 열을 제거한 추론 예제
python prepare_demo_csv.py
# 저장된 Transformer로 추론
python st_awfd_causal_gpt_multihorizon.py --infer-csv results/st_awfd/st_awfd_label_free_demo_input.csv
# 저장된 Transformer의 잔차 공분산 비교
python st_awfd_gpt_covariance_audit.py
# 웹 화면
python -m streamlit run st_awfd_app.py
```

Excel은 openpyxl로 작성한다. export가 불가능하면 저장된 모델·CSV를 유지하고 결과 요약에 `csv_only`를 기록한다.

```powershell
python -m unittest discover -s tests -v
```

2026년 10월 19일에는 공개 데이터와 기존 학습 가중치 없이 CPU 모델의 causal 불변성·Gaussian loss·추론 batch 동등성, Node 없는 Excel 생성, Excel 의존성·쓰기 권한 오류 시 CSV 보존을 검사했다. 전체 GPU 재학습과 공개 D2 전체 실행은 이번 source 정리 과정에서 반복하지 않았다.

## 출처

데이터: [ST-AWFD 공식 저장소](https://github.com/STMicroelectronics/ST-AWFD) · [데이터 라이선스 CC BY-NC-SA 4.0](https://github.com/STMicroelectronics/ST-AWFD/blob/main/LICENSE)

원 논문: [An Ensembled Anomaly Detector for Wafer Fault Detection, Sensors 2021](https://doi.org/10.3390/s21165465)

모델 아이디어: [TRACE-GPT](https://arxiv.org/abs/2309.11427). 이 코드의 다변량·다중 horizon Gaussian 예측 구조는 별도 구현이다.

## English

Anomaly detection and review prioritization for public semiconductor manufacturing traces from ST-AWFD D2. The project compares a CNN denoising autoencoder with a strict-causal multi-horizon Transformer trained on normal production lots.

The recorded RTX 3070 Ti experiment completed 271 epochs and selected epoch 241. Residual covariance scoring reduced the Transformer's false alarms from 76 to 70, with lower ranking performance; the CNN produced 57 false alarms on the same 237 normal holdout lots. This is an exploratory public benchmark, without measured yield improvement from process interventions.

The source includes training and saved-model inference, cleared notebooks, a Streamlit UI, and portable openpyxl export with CSV fallback. A separate CPU check covers model causality and reporting failures. Raw data and trained weights are obtained or generated separately.

