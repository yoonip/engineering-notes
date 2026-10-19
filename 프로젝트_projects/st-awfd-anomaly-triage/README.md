# ST-AWFD 공정 이상 탐지

공개 반도체 제조 시계열에서 정상 공정의 파형을 학습하고, 이상 징후가 있는 lot의 검토 순위를 계산합니다. CNN autoencoder와 strict-causal multi-horizon Transformer를 같은 데이터 분할에서 비교했습니다. Python 학습·추론 코드, Jupyter notebook, Streamlit 화면과 실험 요약을 담았습니다.

## 데이터와 모델

[STMicroelectronics ST-AWFD](https://github.com/STMicroelectronics/ST-AWFD)의 D2를 사용했습니다. 공식 정의에서 MaterialID는 생산 lot이고, `duration_ms`는 정규화된 상대 시간입니다. Step 1의 익명 센서 20개를 64개 상대 시점으로 보간했습니다. 정상 lot 441개로 모델과 scaler를 맞추고, 정상 111개로 epoch와 경보 기준을 정했습니다. 공개 평가 집합은 정상 237개와 이상 367개입니다.

CNN denoising autoencoder는 정상 파형을 복원합니다. Transformer는 과거 방향 Conv1d embedding과 causal attention으로 1·2·4·8 시점 뒤 센서값의 평균과 불확실성을 예측합니다. 관측값의 Gaussian NLL을 이상 점수로 사용합니다. 저장 모델 추론은 학습 때 정한 scaler와 경보 기준을 그대로 적용합니다.

## 기록된 GPU 실험

RTX 3070 Ti에서 Transformer를 271 epoch 학습했고, 정상 validation NLL이 가장 낮은 241 epoch 모델을 저장했습니다. 같은 공개 평가 집합의 결과는 다음과 같습니다.

| 지표 | CNN autoencoder | Transformer | Transformer + 잔차 공분산 |
|---|---:|---:|---:|
| 이상 탐지 recall | 100% | 100% | 100% |
| 정상 오경보 | 57 / 237 | 76 / 237 | 70 / 237 |
| 정상 오경보율 | 24.05% | 32.07% | 29.54% |
| Precision | 86.56% | 82.84% | 83.98% |
| F1 | 0.9279 | 0.9062 | 0.9129 |
| Average Precision | 1.0000 | 1.0000 | 0.9854 |
| 상위 61개 검토 대상 중 이상 | 61 | 61 | 59 |

잔차 공분산 점수는 Transformer의 오경보를 줄이는 대신 순위 성능이 낮아졌습니다. 이 조건에서 정상 오경보는 CNN이 가장 적었습니다.

정상 111개를 epoch 선택과 경보 기준 설정에 함께 사용했고, 같은 holdout에서 여러 모델을 비교했습니다. 결과는 공개 데이터의 탐색 실험입니다. 입력은 전체 step을 보간한 trace이므로 모델 내부의 미래 입력 차단 검사와 실시간 원시 데이터 예측은 구분합니다. 이 데이터의 정답은 lot의 정상·이상 구분이며, 공정 조치에 따른 최종 die 수율 변화는 포함하지 않습니다.

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
| `evidence/` | 과거 GPU 실험과 소스 검증 요약 |

## 실행

Python 3.12 이상에서 가상환경을 만듭니다. [PyTorch 설치 선택기](https://pytorch.org/get-started/locally/)에서 운영체제와 CPU/CUDA 환경에 맞는 PyTorch를 설치한 뒤 나머지 패키지를 설치합니다.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

공식 저장소의 `Datasets`에 있는 D2.zip을 `data/st_awfd/D2.zip`에 둡니다. 원본 데이터와 학습 가중치는 이 source 폴더에 포함하지 않았습니다. 학습 명령은 `models/`와 `results/`에 새 결과를 저장합니다.

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

Excel은 openpyxl로 작성합니다. export가 불가능하면 저장된 모델·CSV를 유지하고 결과 요약에 `csv_only`를 기록합니다.

```powershell
python -m unittest discover -s tests -v
```

2026년 10월 19일에는 공개 데이터와 기존 학습 가중치 없이 CPU 모델의 causal 불변성·Gaussian loss·추론 batch 동등성, Node 없는 Excel 생성, Excel 의존성·쓰기 권한 오류 시 CSV 보존을 검사했습니다. 전체 GPU 재학습과 공개 D2 전체 실행은 이 검사에서 반복하지 않았습니다.

## 출처

데이터: [ST-AWFD 공식 저장소](https://github.com/STMicroelectronics/ST-AWFD) · [데이터 라이선스 CC BY-NC-SA 4.0](https://github.com/STMicroelectronics/ST-AWFD/blob/main/LICENSE)

원 논문: [An Ensembled Anomaly Detector for Wafer Fault Detection, Sensors 2021](https://doi.org/10.3390/s21165465)

모델 아이디어: [TRACE-GPT](https://arxiv.org/abs/2309.11427). 이 코드의 다변량·다중 horizon Gaussian 예측 구조는 별도 구현입니다.

## English

The project learns normal waveforms from public semiconductor manufacturing time series and ranks lots for anomaly review. It compares a CNN denoising autoencoder with a strict-causal multi-horizon Transformer on the same split. Source includes training/inference, Jupyter notebooks, a Streamlit UI and experiment summaries.

### Data and models

The data is D2 from [STMicroelectronics ST-AWFD](https://github.com/STMicroelectronics/ST-AWFD). MaterialID denotes a production lot; `duration_ms` is normalized relative time. Twenty anonymized Step-1 sensors are interpolated to 64 relative time points. Models/scalers use 441 normal lots; 111 normal validation lots select epochs and alarm thresholds. The public holdout has 237 normal and 367 anomalous lots.

The CNN reconstructs normal traces. The Transformer uses past-facing Conv1d embeddings and causal attention to predict sensor means/uncertainties at horizons 1, 2, 4 and 8. Gaussian NLL scores observed values; saved-model inference reuses training scalers and thresholds.

### Recorded GPU experiment

Training on an RTX 3070 Ti ran for 271 epochs and selected epoch 241 by normal-validation NLL.

| Metric | CNN autoencoder | Transformer | Transformer + residual covariance |
| --- | ---: | ---: | ---: |
| Anomaly recall | 100% | 100% | 100% |
| Normal false alarms | 57 / 237 | 76 / 237 | 70 / 237 |
| Normal false-alarm rate | 24.05% | 32.07% | 29.54% |
| Precision | 86.56% | 82.84% | 83.98% |
| F1 | 0.9279 | 0.9062 | 0.9129 |
| Average Precision | 1.0000 | 1.0000 | 0.9854 |
| Anomalies among top 61 review items | 61 | 61 | 59 |

Covariance scoring reduced Transformer false alarms while lowering ranking performance; the CNN had the fewest normal false alarms here. The same 111 normal lots select epochs and thresholds, and several models are compared on the same holdout, so these are exploratory benchmark results. Full-step interpolation is separate from the model's internal causal-mask guarantee and does not establish raw-stream online forecasting. Labels describe normal/anomalous lots; no intervention-based die-yield improvement is measured.

### Files and execution

`st_awfd_model.py` defines the Transformer, Gaussian loss, fixed-model inference and causal checks. `st_awfd_causal_gpt_multihorizon.py` trains/evaluates it and runs checkpoint CSV inference. `st_awfd_pipeline.py` processes D2 and implements CNN/statistical baselines; `st_awfd_gpt_covariance_audit.py` compares residual scoring. `workbook_export.py` uses openpyxl with CSV fallback, and `st_awfd_app.py` provides training progress, comparisons and inference. Three notebooks cover CNN, causal Transformer and label-free saved-model inference. `evidence/` stores historical GPU and source-check summaries.

Use Python 3.12+, create a virtual environment and select a suitable CPU/CUDA installation through [PyTorch](https://pytorch.org/get-started/locally/), then install the remaining requirements. Place official `Datasets/D2.zip` at `data/st_awfd/D2.zip`; raw data and trained weights are not bundled. The commands above run baselines, Transformer training, demo CSV generation, saved inference, covariance analysis and Streamlit. New results go in `models/` and `results/`.

Excel export uses openpyxl. If it fails, model/CSV files are retained and the summary records `csv_only`. The October 19, 2026 CPU check covered causal invariance, Gaussian loss, batch-equivalent inference, Excel generation without Node and CSV preservation after missing dependencies or write failures. Full GPU training and D2 execution were not repeated.

### Attribution

Data and terms: [ST-AWFD](https://github.com/STMicroelectronics/ST-AWFD), [CC BY-NC-SA 4.0](https://github.com/STMicroelectronics/ST-AWFD/blob/main/LICENSE). Original paper: [An Ensembled Anomaly Detector for Wafer Fault Detection, Sensors 2021](https://doi.org/10.3390/s21165465). [TRACE-GPT](https://arxiv.org/abs/2309.11427) informs the modeling idea; the multivariate, multi-horizon Gaussian architecture here is a separate implementation.
