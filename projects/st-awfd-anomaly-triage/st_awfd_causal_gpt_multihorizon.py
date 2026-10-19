# -*- coding: utf-8 -*-  # Windows와 Jupyter에서 한국어 주석을 깨지지 않게 읽는다.
# ST-AWFD D2 정상 lot만으로 strict-causal, multi-horizon Transformer를 학습하는 재현 실험이다.  # 이는 공개 abnormal-lot triage benchmark이지 실제 die-yield prediction이 아니다.
# TRACE-GPT 논문 아이디어를 참고하되 미래 누설 없는 causal embedding과 확률적 연속값 예측으로 독립 구현한다.  # TRACE-GPT 공식 코드나 SK hynix 내부 시스템이라고 주장하지 않는다.

from __future__ import annotations  # 현대 타입 표기를 파이썬 런타임에서 즉시 평가하지 않도록 한다.
import copy  # validation loss가 가장 낮은 weight를 안전하게 복사해 되돌린다.
import argparse  # 재학습과 저장 checkpoint 추론을 명령줄에서 명확히 선택한다.
import json  # 설정·학습 결과·한계를 기계가 읽을 수 있는 manifest로 남긴다.
import math  # review queue의 최소 1개 행과 적중률을 계산한다.
import random  # Python 표준 난수 생성기도 seed를 고정해 재현성을 높인다.
from pathlib import Path  # 실행 위치가 아니라 현재 파일 위치에서 프로젝트 경로를 찾는다.
from typing import Any, Callable  # 학습 callback과 JSON형 결과를 명시한다.

import matplotlib  # 터미널에서도 그림을 파일로 저장하는 plotting backend를 설정한다.
matplotlib.use("Agg")  # 화면 창을 띄우지 않고 headless 환경에서 안전하게 그래프를 저장한다.
import matplotlib.pyplot as plt  # 실제 학습 곡선과 score 분포를 결과 그림으로 만든다.
import numpy as np  # 시계열 텐서 전처리와 지표 계산에 사용한다.
import pandas as pd  # 점수표·훈련이력·Excel 결과물을 작성한다.
import torch  # causal Transformer를 GPU/CPU에서 학습하고 추론한다.
from sklearn.metrics import average_precision_score, balanced_accuracy_score, f1_score, precision_score, recall_score, roc_auc_score  # 순위·고정 경계선·불균형 class 지표를 계산한다.
from torch import nn  # PyTorch 신경망 층을 구성한다.
from torch.nn import functional as F  # padding, Gaussian loss와 attention mask 연산을 제공한다.
from torch.utils.data import DataLoader, TensorDataset  # 정상 lot group 묶음을 GPU batch로 공급한다.

from st_awfd_model import CausalMultiHorizonGPT, DROPOUT, D_MODEL, FFN_DIM, HORIZONS, KERNEL_SIZE, LOG_SIGMA_MAX, LOG_SIGMA_MIN, N_HEADS, N_LAYERS, StrictCausalConvEmbedding, causal_invariance_audit, gaussian_nll, multi_horizon_loss, score_signals
from workbook_export import export_strict_workbook, optional_export

import st_awfd_pipeline as baseline  # 공식 split, 고정 64-point resampling, train-only scaling을 재사용한다.

PROJECT_DIR = Path(__file__).resolve().parent  # 이 스크립트가 있는 재현 가능한 project root를 계산한다.
RESULT_DIR = PROJECT_DIR / "results" / "st_awfd" / "causal_gpt_multihorizon"  # 이번 strict-causal 결과를 이전 실험과 구분해 저장한다.
MODEL_DIR = PROJECT_DIR / "models" / "st_awfd"  # 다시 불러올 state dict와 scaler 설정을 보관한다.
SEED = 3070  # 프로젝트의 재현성을 위한 고정 난수 seed다.
MAX_EPOCHS = 320  # 160 epoch 결과에서 정상 validation NLL이 계속 개선돼 학습 상한을 320으로 늘린다.
PATIENCE = 30  # 검증 NLL이 더 나아지지 않는 구간을 기다린 뒤 best checkpoint로 돌아간다.
BATCH_SIZE = 64  # 3070 Ti 8 GB 메모리에서 trace batch를 안정적으로 처리한다.
ALPHA = 0.05  # normal calibration score의 상위 5%를 review 기준 후보로 정한다.
REVIEW_FRACTION = 0.10  # 고정 review capacity 가정에서 상위 10%에 이상이 얼마나 있는지 본다.
LEARNING_RATE = 2e-4  # 다중 horizon 확률학습을 안정적으로 진행할 AdamW step 크기다.
WEIGHT_DECAY = 1e-3  # train-only 모델의 과도한 weight 크기를 억제한다.






def set_seed(seed: int = SEED) -> None:  # 재현성을 위해 Python·NumPy·Torch 난수 상태를 하나로 고정한다.
    random.seed(seed)  # Python 기본 random 호출 결과를 고정한다.
    np.random.seed(seed)  # NumPy data split/array 연산의 난수를 고정한다.
    torch.manual_seed(seed)  # CPU 모델 초기화의 난수 seed를 설정한다.
    if torch.cuda.is_available():  # CUDA GPU가 감지된 경우에만 GPU 난수 상태를 조절한다.
        torch.cuda.manual_seed_all(seed)  # 모든 CUDA device의 난수 상태를 동일하게 시작한다.
    torch.backends.cudnn.deterministic = True  # 결과 재현성이 높은 CuDNN kernel을 선택한다.
    torch.backends.cudnn.benchmark = False  # shape별 비결정성 성능탐색을 막는다.


def prepare_data() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, dict[str, list[float]]]:  # 기존 CNN/GPT와 같은 공식 group split을 불러온다.
    frame = baseline.read_d2_source()  # 공식 공개 D2 source schema를 검증해서 읽는다.
    train_frame, calibration_frame, test_frame, _ = baseline.split_official_normal_reference(frame, seed=SEED)  # 공식 is_test 구분과 MaterialID 단위 normal-only 분할을 재사용한다.
    features = [name for name in frame.columns if name.startswith("feature_")]  # 정답/ID가 아닌 20개 익명 sensor column만 고른다.
    train_raw, _, train_ids, _ = baseline.resample_step_one(train_frame, features)  # train normal의 Step 1 trace를 lot group 단위로 고정 길이화한다.
    calibration_raw, _, calibration_ids, _ = baseline.resample_step_one(calibration_frame, features)  # 별도 normal group은 control limit과 early stopping에만 쓴다.
    test_raw, test_labels, test_ids, _ = baseline.resample_step_one(test_frame, features)  # holdout label은 마지막 성능 감사에만 둔다.
    train, (calibration, test), scaler = baseline.normalize_with_training_normals(train_raw, [calibration_raw, test_raw])  # sensor scale은 training normal에서만 적합한다.
    if np.any(test_labels < 0):  # 공식 holdout 감사 label 누락을 확인한다.
        raise ValueError("공식 holdout target label이 없어 benchmark 감사 지표를 낼 수 없습니다.")  # label 불확실성을 성공 수치로 감추지 않는다.
    return train, calibration, test, test_labels.astype(np.int64), train_ids, calibration_ids, np.asarray(test_ids), scaler  # 분할별 배열, ID, scaler만 전달한다.








def empirical_normal_limit(values: np.ndarray, alpha: float = ALPHA) -> float:  # normal-only calibration quantile을 운영 후보 limit으로 계산한다.
    return float(np.quantile(values, 1.0 - alpha, method="higher"))  # 작은 validation set에서 실제 관측 quantile 경계값을 보수적으로 택한다.


def score_new_csv(csv_path: str | Path, checkpoint_path: str | Path | None = None, review_fraction: float = REVIEW_FRACTION) -> pd.DataFrame:  # 저장된 GPT형 모델로 label 없는 완성 Step 1 trace를 재학습 없이 점수화한다.
    if not 0.01 <= review_fraction <= 0.50:  # 검토 예산을 데이터 label 대신 사용자가 명시하게 한다.
        raise ValueError("review_fraction은 0.01~0.50 사이여야 합니다.")  # 잘못된 queue 크기는 처리 전에 알린다.
    saved_path = Path(checkpoint_path) if checkpoint_path is not None else MODEL_DIR / "st_awfd_strict_causal_multihorizon_gpt.pt"  # 사용자 지정 또는 학습된 기본 weight 파일을 선택한다.
    checkpoint = torch.load(saved_path, map_location="cpu", weights_only=True)  # tensor와 기본 metadata만 허용하는 loader로 자체 생성 checkpoint를 읽는다.
    if tuple(checkpoint["horizons"]) != HORIZONS or not checkpoint.get("causal_embedding", False):  # 다른 구조의 checkpoint를 조용히 잘못 적용하지 않는다.
        raise ValueError("이 추론 함수는 strict-causal h=(1,2,4,8) checkpoint를 필요로 합니다.")  # 구조 mismatch를 명확히 설명한다.
    feature_columns = [f"feature_{index + 1}" for index in range(int(checkpoint["feature_count"]))]  # D2의 고정 sensor 순서를 복원한다.
    incoming = pd.read_csv(csv_path)  # 새로운 raw trace 행을 읽되 target/is_test label은 요구하지 않는다.
    required = {"MaterialID", "StepID", "duration_ms", *feature_columns}  # ID·step·정렬축·센서가 모델 입력 schema의 필수 요소다.
    missing = required.difference(incoming.columns)  # 필요한 필드가 빠졌는지 확인한다.
    if missing:  # 오류 sensor mapping을 파형 변화로 오해하지 않도록 중단한다.
        raise ValueError(f"필수 열 누락: {sorted(missing)}")  # 사용자가 CSV를 고칠 수 있도록 누락 이름을 적는다.
    incoming = incoming.loc[:, ["MaterialID", "StepID", "duration_ms", *feature_columns]].copy()  # target/is_test와 무관하게 label-free inference 입력만 전달한다.
    if incoming["MaterialID"].isna().any():  # 그룹 식별이 없는 행은 임의로 다른 lot에 합치지 않는다.
        raise ValueError("MaterialID 누락 행이 있습니다.")  # trace group을 잃은 입력을 명확히 알린다.
    for column in ["StepID", "duration_ms", *feature_columns]:  # 공정 trace 수치형 필드를 검증한다.
        incoming[column] = pd.to_numeric(incoming[column], errors="raise")  # 문자열의 임의 coercion/결측치 채움으로 이상을 숨기지 않는다.
    if not np.isfinite(incoming[["StepID", "duration_ms", *feature_columns]].to_numpy(dtype=float)).all():  # NaN/무한대는 보간이나 uncertainty score를 망칠 수 있다.
        raise ValueError("trace 수치 열에 NaN/무한대가 있습니다. 원본 데이터 품질을 확인하세요.")  # 알 수 없는 값을 정상으로 만들지 않는다.
    step_rows = incoming.loc[incoming["StepID"] == baseline.STEP_ID]  # 완료된 Step 1만 기존 실험과 같은 방식으로 읽는다.
    missing_step = set(incoming["MaterialID"]).difference(step_rows["MaterialID"])  # 입력 lot 중 Step 1이 없어 조용히 누락될 대상을 찾는다.
    if missing_step:  # 일부 lot을 결과에서 숨기지 않고 batch 검증을 중단한다.
        raise ValueError(f"StepID=1 trace가 없는 MaterialID: {sorted(map(str, missing_step))[:10]}")  # 첫 누락 ID들을 알려 사용자가 원본을 점검하게 한다.
    if step_rows.duplicated(["MaterialID", "duration_ms"]).any():  # 보간축 중복은 측정 중복인지 여부가 불분명하므로 자동 평균하지 않는다.
        raise ValueError("Step 1에서 MaterialID/duration_ms 중복이 있습니다. 원본 trace의 중복 정책을 먼저 정하세요.")  # 현장 데이터 품질 정책이 없는 상황의 조용한 오판을 막는다.
    signals, _, ids, metadata = baseline.resample_step_one(incoming, feature_columns, sequence_length=int(checkpoint["sequence_length"]))  # 전체 step 완료 후 고정 상대진행률 격자로 보간한다.
    means = np.asarray(checkpoint["scaler"]["feature_mean"], dtype=np.float32).reshape(1, -1, 1)  # 정상441 fit 집합에서 저장한 sensor 평균을 그대로 사용한다.
    deviations = np.asarray(checkpoint["scaler"]["feature_std"], dtype=np.float32).reshape(1, -1, 1)  # 새로운 batch로 scaler를 다시 적합하면 drift가 숨겨질 수 있어 고정한다.
    if np.any(deviations <= 0) or not np.isfinite(means).all() or not np.isfinite(deviations).all():  # checkpoint의 수치 reference도 추론 전에 검사한다.
        raise ValueError("checkpoint scaler가 유효하지 않습니다.")  # 잘못된 reference를 학습된 공정 지식으로 취급하지 않는다.
    normalized = ((signals - means) / deviations).astype(np.float32)  # 새 lot에도 동일한 training normal scale을 적용한다.
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # 3070 Ti가 감지되면 실제 추론도 CUDA에서 수행한다.
    model = CausalMultiHorizonGPT(len(feature_columns), int(checkpoint["sequence_length"])).to(device)  # 저장된 구조와 같은 빈 neural network를 준비한다.
    model.load_state_dict(checkpoint["state_dict"], strict=True)  # best241 가중치를 정확하게 복원하고 optimizer나 backward는 실행하지 않는다.
    scores, sensor_scores, horizon_scores = score_signals(model, normalized, device)  # eval/no_grad로 평균·분산 예측과 실측값의 NLL을 계산한다.
    threshold = float(checkpoint["normal_reference_limit"])  # 정상111의 고정 quantile을 사용하며 새 batch label이나 score로 threshold를 맞추지 않는다.
    ranking = np.argsort(-scores, kind="mergesort")  # surprise가 큰 lot을 PE 검토 우선순위 상단에 놓는다.
    ranks = np.empty(len(scores), dtype=np.int64)  # 원래 ID 순서와 대응하는 rank 배열을 준비한다.
    ranks[ranking] = np.arange(1, len(scores) + 1)  # 동점은 안정적인 ID 입력 순서를 사용한다.
    queue_size = max(1, math.ceil(len(scores) * review_fraction))  # capacity 설정은 lot별 abnormal 여부와 별개의 review 예산이다.
    result = pd.DataFrame({"MaterialID": ids, "anomaly_score": scores, "normal_reference_limit": threshold, "above_normal_reference_limit": scores > threshold, "review_rank": ranks, "review_candidate_at_capacity": ranks <= queue_size, "leading_anonymous_feature": [feature_columns[index] for index in sensor_scores.argmax(axis=1)], "largest_surprise_horizon": [HORIZONS[index] for index in horizon_scores.argmax(axis=1)], "step_sample_count": metadata["step_sample_count"].to_numpy()})  # label 없는 다음 조사용 queue를 만든다.
    for index, feature in enumerate(feature_columns):  # 각 익명 channel의 score 기여를 사람이 검토할 수 있도록 공개한다.
        result[f"{feature}_mean_nll"] = sensor_scores[:, index]  # 최댓값 channel이 원인이라는 결론은 포함하지 않는다.
    for index, horizon in enumerate(HORIZONS):  # 각 예측거리의 surprise도 결과표에 보존한다.
        result[f"horizon_{horizon}_mean_nll"] = horizon_scores[:, index]  # 샘플 horizon은 물리적 초/ms를 뜻하지 않는다.
    result = result.sort_values("review_rank").reset_index(drop=True)  # Excel에서 상단부터 바로 검토할 수 있게 정렬한다.
    result.attrs.update({"device": str(device), "device_name": torch.cuda.get_device_name(0) if device.type == "cuda" else "CPU", "selected_epoch": int(checkpoint["best_epoch"]), "checkpoint_path": str(saved_path), "preprocessing_mode": "completed-step relative-time interpolation; network-only tensor causality"})  # notebook/UI가 실제 저장 가중치·장치를 확인하게 한다.
    return result  # 저장은 호출자에게 맡겨 임의의 기존 결과파일을 덮어쓰지 않는다.




def evaluate(labels: np.ndarray, scores: np.ndarray, threshold: float, calibration_scores: np.ndarray) -> dict[str, float | int]:  # 순위·alarm·review capacity를 서로 다른 관점으로 보고한다.
    predicted = scores > threshold  # normal reference에서 미리 고정한 threshold를 test label 없이 적용한다.
    normals = labels == 0  # official mixed holdout의 정상 lot group mask다.
    anomalies = labels == 1  # official mixed holdout의 이상 lot group mask다.
    queue_size = max(1, int(math.ceil(len(scores) * REVIEW_FRACTION)))  # PE 인력 review capacity 가정에서 확인할 lot group 개수다.
    queue = np.argsort(-scores, kind="mergesort")[:queue_size]  # 상위 점수 lot만 고정 크기 queue에 넣는다.
    true_positive = int(np.sum(predicted & anomalies))  # 정상 limit 초과 이상 lot group 수를 계산한다.
    false_positive = int(np.sum(predicted & normals))  # 정상인데 이상 검토를 요구한 건수를 계산한다.
    normal_ci = baseline.wilson_interval(false_positive, int(normals.sum()))  # 표본 변동을 보여주도록 정상 false-alarm rate의 Wilson 95% CI를 계산한다.
    recall_ci = baseline.wilson_interval(true_positive, int(anomalies.sum()))  # 이상 recall의 불확실성을 같은 방식으로 계산한다.
    return {  # xlsx와 JSON에서 모델의 운영 절충을 직접 확인할 수 있게 모든 metric을 명시한다.
        "holdout_average_precision": float(average_precision_score(labels, scores)),  # test prevalence에 민감한 PR ranking summary를 기록한다.
        "holdout_roc_auc": float(roc_auc_score(labels, scores)),  # 양성-음성 쌍 순위의 분리도를 기록한다.
        "holdout_balanced_accuracy_at_normal_limit": float(balanced_accuracy_score(labels, predicted)),  # 두 class recall 평균으로 class imbalance 영향을 줄인다.
        "holdout_f1_at_normal_limit": float(f1_score(labels, predicted, zero_division=0)),  # 고정 control limit에서 precision/recall 절충을 기록한다.
        "holdout_precision_at_normal_limit": float(precision_score(labels, predicted, zero_division=0)),  # 검토 경보 가운데 abnormal label인 비율이다.
        "holdout_anomaly_recall_at_normal_limit": float(recall_score(labels, predicted, zero_division=0)),  # 이상 lot group 중 경보에 걸린 비율이다.
        "holdout_normal_false_alarm_rate": float(np.mean(predicted[normals])),  # 정상 lot group 가운데 불필요하게 경보된 비율이다.
        "holdout_normal_false_alarm_ci95_low": float(normal_ci[0]),  # 정상 false alarm 비율의 Wilson 신뢰구간 하한이다.
        "holdout_normal_false_alarm_ci95_high": float(normal_ci[1]),  # 정상 false alarm 비율의 Wilson 신뢰구간 상한이다.
        "holdout_anomaly_recall_ci95_low": float(recall_ci[0]),  # 이상 recall 비율의 Wilson 신뢰구간 하한이다.
        "holdout_anomaly_recall_ci95_high": float(recall_ci[1]),  # 이상 recall 비율의 Wilson 신뢰구간 상한이다.
        "calibration_normal_false_alarm_rate": float(np.mean(calibration_scores > threshold)),  # 같은 정상 calibration data에서 실제 얻은 FPR이다.
        "normal_reference_target_fpr": float(ALPHA),  # limit 설정 때 사용한 정상 tail budget 가정이다.
        "alert_fraction_at_normal_limit": float(np.mean(predicted)),  # 전체 queue 중 alert로 올린 비율이다.
        "top_review_fraction": float(REVIEW_FRACTION),  # 고정 용량 queue 크기다.
        "top_review_count": queue_size,  # 실제 검토 lot group 수다.
        "top_review_anomaly_recall": float(np.sum(labels[queue]) / max(int(np.sum(anomalies)), 1)),  # 검토 대상 상위 10%에 포함된 전체 이상 비율이다.
        "top_review_precision": float(np.mean(labels[queue])),  # review queue에서 abnormal인 비율이다.
        "threshold": float(threshold),  # calibration normal에서 고정한 decision score 값을 기록한다.
        "holdout_false_alarm_count": false_positive,  # PE review load 해석을 위해 오경보 원시 건수를 함께 적는다.
        "holdout_true_alarm_count": true_positive,  # threshold에서 이상을 포착한 원시 건수를 함께 적는다.
    }  # 추정 수율 향상이나 recipe action 효과를 포함하지 않는다.


def _write_results(model: CausalMultiHorizonGPT, history: list[dict[str, float]], train_ids: np.ndarray, calibration_ids: np.ndarray, test_ids: np.ndarray, train: np.ndarray, calibration: np.ndarray, test: np.ndarray, labels: np.ndarray, scaler: dict[str, list[float]], device: torch.device, best_epoch: int, metrics: dict[str, Any], calibration_scores: np.ndarray, test_scores: np.ndarray, sensor_scores: np.ndarray, horizon_scores: np.ndarray) -> dict[str, Any]:  # 학습·추론 표와 checkpoint를 재실행 가능한 형태로 저장한다.
    RESULT_DIR.mkdir(parents=True, exist_ok=True)  # 이번 실험의 result subfolder를 만든다.
    MODEL_DIR.mkdir(parents=True, exist_ok=True)  # checkpoint 저장 폴더를 준비한다.
    history_frame = pd.DataFrame(history)  # epoch 지표 list를 행 단위 data frame으로 바꾼다.
    history_path = RESULT_DIR / "strict_causal_gpt_training_history.csv"  # epoch 기록을 스프레드시트에서 열 수 있는 CSV 경로다.
    history_frame.to_csv(history_path, index=False, encoding="utf-8-sig")  # train/normal-validation loss를 매 epoch 영구 보관한다.
    threshold = float(metrics["threshold"])  # 같은 고정 calibration limit을 모든 산출물에 쓴다.
    calibration_table = pd.DataFrame({"MaterialID": calibration_ids, "normal_calibration_nll": calibration_scores, "fixed_normal_reference_limit": threshold, "exceeds_limit": calibration_scores > threshold})  # label 없는 정상 calibration 점수와 threshold 검산용 표다.
    calibration_table.to_csv(RESULT_DIR / "normal_calibration_scores.csv", index=False, encoding="utf-8-sig")  # 정상 score 분포를 별도 audit 파일로 내보낸다.
    score_table = pd.DataFrame({"MaterialID": test_ids, "target_for_retrospective_audit_only": labels, "multi_horizon_gaussian_nll": test_scores, "normal_reference_limit": threshold, "exceeds_fixed_limit": test_scores > threshold})  # test label은 audit 파일 하나에서만 모델 예측과 대조한다.
    for channel_index in range(sensor_scores.shape[1]):  # 익명 센서 channel별 기여값을 score table에 덧붙인다.
        score_table[f"feature_{channel_index + 1}_mean_nll"] = sensor_scores[:, channel_index]  # PE는 물리 매핑이 공개되지 않은 feature index를 추가 조사해야 한다.
    for horizon_index, horizon in enumerate(HORIZONS):  # 예측거리별 surprise를 개별 열로 남긴다.
        score_table[f"horizon_{horizon}_mean_nll"] = horizon_scores[:, horizon_index]  # 짧은/긴 time scale 중 어디가 이상 score를 만들었는지 본다.
    score_table["review_rank"] = score_table["multi_horizon_gaussian_nll"].rank(method="first", ascending=False).astype(int)  # 높은 surprise가 빠른 review가 되도록 rank를 만든다.
    score_table.to_csv(RESULT_DIR / "official_holdout_audit_scores.csv", index=False, encoding="utf-8-sig")  # 최종 holdout 사후 감사 결과를 보존한다.
    checkpoint_path = MODEL_DIR / "st_awfd_strict_causal_multihorizon_gpt.pt"  # 엄밀한 causal 구현의 가중치 경로를 정한다.
    torch.save({"state_dict": model.state_dict(), "feature_count": int(train.shape[1]), "sequence_length": int(train.shape[-1]), "horizons": list(HORIZONS), "scaler": scaler, "normal_reference_limit": threshold, "best_epoch": int(best_epoch), "seed": SEED, "architecture": "causal left-padded Conv1d + causal decoder-only Transformer + multi-horizon Gaussian NLL", "causal_embedding": True}, checkpoint_path)  # inference weights와 model/scaler/limit을 함께 저장한다.
    label_free_table = score_table.drop(columns=["target_for_retrospective_audit_only"]).rename(columns={"multi_horizon_gaussian_nll": "anomaly_score", "exceeds_fixed_limit": "above_normal_reference_limit"})  # 새 학습마다 같은 best 가중치의 label-free queue도 갱신한다.
    label_free_table["review_candidate_at_capacity"] = label_free_table["review_rank"] <= max(1, math.ceil(len(test_ids) * REVIEW_FRACTION))  # 사전에 정한 review 예산으로만 후보를 결정한다.
    label_free_table["leading_anonymous_feature"] = [f"feature_{index + 1}" for index in sensor_scores.argmax(axis=1)]  # 물리 의미가 공개되지 않은 기여 channel 번호를 보존한다.
    label_free_table["largest_surprise_horizon"] = [HORIZONS[index] for index in horizon_scores.argmax(axis=1)]  # 상대시점의 forecast 기여를 표시한다.
    label_free_table.sort_values("review_rank").to_csv(RESULT_DIR / "saved_checkpoint_label_free_holdout_queue.csv", index=False, encoding="utf-8-sig")  # Excel 후속조사 source가 이전 모델 점수에 머물지 않게 한다.
    figure, axes = plt.subplots(1, 2, figsize=(14, 5))  # 학습 수렴과 실제 score 분리를 나란히 그린다.
    axes[0].plot(history_frame["epoch"], history_frame["train_multi_horizon_gaussian_nll"], label="Train normal")  # train normal objective가 epoch마다 내려가는지 본다.
    axes[0].plot(history_frame["epoch"], history_frame["validation_multi_horizon_gaussian_nll"], label="Validation normal")  # 독립 정상 validation 목적함수로 best epoch를 결정한다.
    axes[0].axvline(best_epoch, color="black", linestyle="--", label=f"Selected epoch {best_epoch}")  # holdout 결과가 아닌 정상 validation 기준 선택 epoch다.
    axes[0].set_title("Strict-causal multi-horizon training")  # 학습 목표가 causal multi-step likelihood임을 표기한다.
    axes[0].set_xlabel("Epoch")  # 가로축은 optimizer 학습 반복 수다.
    axes[0].set_ylabel("Gaussian negative log-likelihood")  # 서로 달라 직접 비교하면 안 되는 loss 종류를 적는다.
    axes[0].legend()  # train과 validation 선을 구분한다.
    axes[1].hist(test_scores[labels == 0], bins=24, alpha=0.70, label="Official holdout normal")  # holdout 정상 score 분포를 사후 감사용으로 그린다.
    axes[1].hist(test_scores[labels == 1], bins=24, alpha=0.70, label="Official holdout abnormal")  # holdout abnormal score 분포를 사후 감사용으로 그린다.
    axes[1].axvline(threshold, color="black", linestyle="--", label="Normal-only calibration limit")  # test labels를 사용하지 않은 고정 limit을 표시한다.
    axes[1].set_title("Holdout score audit (not yield uplift)")  # score 분리가 fab yield 증가를 의미하지 않음을 그림에서 상기시킨다.
    axes[1].set_xlabel("Mean multi-horizon predictive surprise")  # score는 이상 확률이 아닌 예측 비적합도다.
    axes[1].legend()  # 정상/이상 분포 및 고정 기준선을 식별한다.
    figure.tight_layout()  # label 간 겹침을 줄인다.
    chart_path = RESULT_DIR / "strict_causal_gpt_experiment.png"  # notebook와 app에서 직접 열 그림 경로다.
    figure.savefig(chart_path, dpi=180)  # 고해상도 분석 그림을 저장한다.
    plt.close(figure)  # 반복 실행 시 matplotlib 메모리 누수를 막는다.
    comparison_rows: list[dict[str, Any]] = [{"model": "Strict-causal multi-horizon GPT-style Transformer", **metrics}]  # 신모델의 복합 운영 metric 행으로 비교표를 시작한다.
    cnn_summary = baseline.RESULTS_DIR / "st_awfd_run_summary.json"  # 같은 split에서 앞서 훈련한 CNN의 공식 결과를 불러온다.
    if cnn_summary.exists():  # 결과 파일이 저장된 경우만 비교 행을 추가한다.
        old = json.loads(cnn_summary.read_text(encoding="utf-8"))  # CNN 최종 summary를 읽는다.
        cnn_metrics = old.get("experiment", {}).get("primary_holdout_metrics", {})  # 모델 비교에 필요한 holdout 지표를 선택한다.
        cnn_interval = cnn_metrics.get("test_normal_fpr_wilson_95pct", [None, None])  # CNN의 holdout 정상 오경보 불확실성 구간도 함께 가져온다.
        comparison_rows.insert(0, {"model": "1D CNN denoising autoencoder", "holdout_average_precision": cnn_metrics.get("average_precision"), "holdout_roc_auc": cnn_metrics.get("roc_auc"), "holdout_f1_at_normal_limit": cnn_metrics.get("f1_at_normal_limit"), "holdout_precision_at_normal_limit": cnn_metrics.get("precision_at_normal_limit"), "holdout_anomaly_recall_at_normal_limit": cnn_metrics.get("recall_at_normal_limit"), "holdout_normal_false_alarm_rate": cnn_metrics.get("test_normal_false_alarm_rate"), "holdout_normal_false_alarm_ci95_low": cnn_interval[0], "holdout_normal_false_alarm_ci95_high": cnn_interval[1], "calibration_normal_false_alarm_rate": cnn_metrics.get("calibration_normal_false_alarm_rate"), "top_review_fraction": REVIEW_FRACTION, "top_review_anomaly_recall": cnn_metrics.get("recall_at_review_capacity"), "top_review_precision": cnn_metrics.get("precision_at_review_capacity"), "threshold": cnn_metrics.get("threshold")})  # 동일 group split CNN baseline을 같은 지표 열과 나란히 둔다.
    classical_path = baseline.RESULTS_DIR / "st_awfd_model_comparison.csv"  # 현재 benchmark의 classical detector 결과 파일을 불러온다.
    if classical_path.exists():  # 기존 table이 있으면 그 same-split detector 결과를 포함한다.
        classical_rows = pd.read_csv(classical_path).to_dict(orient="records")  # robust limit, SVM, Isolation Forest, rank fusion 결과를 읽는다.
        for row in classical_rows:  # train/eval 설정이 같은 실험의 detector별 운영 지표를 변환한다.
            if row.get("model") in {"TemporalAutoencoder_GPU", "1D CNN denoising autoencoder"}:  # 기존 CNN은 이미 별도 normalized row로 추가했다.
                continue  # 동일 CNN이 중복으로 표시되지 않게 건너뛴다.
            precision = float(row.get("holdout_precision_at_limit", 0.0))  # anomaly holdout에서 fixed threshold precision을 읽는다.
            recall = float(row.get("holdout_recall_at_limit", 0.0))  # anomaly recall을 읽는다.
            fpr = float(row.get("holdout_test_normal_fpr", 0.0))  # 정상 holdout의 경보 비율을 읽는다.
            f1 = 2.0 * precision * recall / max(precision + recall, 1e-12)  # harmonic mean으로 동일-threshold F1을 계산한다.
            balanced_accuracy = (recall + 1.0 - fpr) / 2.0  # class당 recall을 같은 비중으로 둔 balanced accuracy다.
            comparison_rows.insert(0, {"model": row.get("model"), "holdout_average_precision": row.get("holdout_average_precision"), "holdout_roc_auc": row.get("holdout_roc_auc"), "holdout_f1_at_normal_limit": f1, "holdout_precision_at_normal_limit": precision, "holdout_anomaly_recall_at_normal_limit": recall, "holdout_normal_false_alarm_rate": fpr, "holdout_normal_false_alarm_ci95_low": row.get("holdout_test_normal_fpr_ci_lower"), "holdout_normal_false_alarm_ci95_high": row.get("holdout_test_normal_fpr_ci_upper"), "calibration_normal_false_alarm_rate": row.get("calibration_normal_alarm_rate"), "holdout_balanced_accuracy_at_normal_limit": balanced_accuracy, "top_review_fraction": REVIEW_FRACTION, "top_review_anomaly_recall": row.get("review_queue_recall"), "top_review_precision": row.get("review_queue_precision"), "threshold": row.get("threshold_score"), "holdout_false_alarm_count": row.get("threshold_false_positive"), "holdout_true_alarm_count": row.get("threshold_true_positive")})  # classical baselines의 장단점을 동일 핵심 columns로 비교한다.
    comparison = pd.DataFrame(comparison_rows)  # 모델별 trade-off를 한 dataframe으로 구성한다.
    comparison.to_csv(RESULT_DIR / "model_comparison.csv", index=False, encoding="utf-8-sig")  # Excel 없이도 모델 결과를 불러올 수 있도록 저장한다.
    training_table = pd.DataFrame(history)  # epoch별 loss curve 원천자료를 만든다.
    causality_audit = causal_invariance_audit(model, test[0], device)  # 실제 학습한 가중치로 미래 perturbation 불변성을 검증한다.
    config = {"data": "STMicroelectronics ST-AWFD public D2", "task": "normal-only multi-horizon sequence anomaly triage; not final die-yield prediction", "split": "official normal train=441; normal calibration=111; official mixed holdout=604; MaterialID groupwise", "input": "StepID 1, 20 anonymized features, 64 relative-time interpolated points; train-normal-only standardization", "architecture": {"embedding": "strict left-padded causal Conv1d, kernel=5", "transformer": "decoder-only causal attention; 3 blocks, 4 heads, d_model=64, FFN=128", "forecast_horizons": list(HORIZONS), "distribution": "sensor-specific Gaussian mean + log_sigma", "objective": "equal-weight Gaussian NLL across horizons 1,2,4,8", "anomaly_score": "mean multi-horizon/sensor next-value Gaussian NLL"}, "causality_audit": causality_audit, "training": {"device": str(device), "device_name": torch.cuda.get_device_name(0) if device.type == "cuda" else "CPU", "epochs_completed": len(history), "selected_epoch": best_epoch, "best_normal_validation_nll": float(min(row["validation_multi_horizon_gaussian_nll"] for row in history)), "seed": SEED, "normal_fit_ids": int(len(train_ids)), "normal_calibration_ids": int(len(calibration_ids))}, "metrics": metrics, "limitations": ["D2 labels are abnormal/normal MaterialID groups, not final good-die/tested-die yield.", "The dataset is STMicroelectronics and does not represent SK hynix products/tools or proprietary fab behavior.", "Feature channels are anonymized so physical sensor/root-cause mapping is unavailable.", "The abnormal holdout prevalence is enriched and does not represent a factory alarm prevalence.", "A 5% normal-calibration tail is an experiment control-limit assumption, not an approved factory limit.", "The same 111 normal groups are reused for checkpoint early stopping and threshold calibration; the independent holdout measures this complete procedure, but calibration needs a fresh untouched normal period for deployment.", "The official split is not a future-time, product, tool/chamber or fab transfer validation.", "A high anomaly score is a review hypothesis, not causal evidence or recipe-change authorization.", "No intervention outcome or yield numerator/denominator exists, so true yield uplift is not measured."]}  # 학습·평가·주장 범위를 정리해 실험의 해석 범위를 지킨다.
    summary_path = RESULT_DIR / "strict_causal_gpt_run_summary.json"  # 재현 manifest의 저장 위치다.
    config["unit_definition"] = "MaterialID = production lot in the official ST-AWFD README; counts are lot groups, not verified wafer/die counts."  # 재학습 후에도 공식 표본 단위를 명시한다.
    config["causality_scope"] = "Network-only invariance within already resampled tensors; completed-step interpolation is post-step trace triage, not raw-stream online early warning."  # 전체 step을 보는 전처리와 causal network를 구분한다.
    config["research_evaluation_scope"] = "Holdout labels excluded from fit/calibration; this mixed holdout has been repeatedly reviewed across architecture/score research, so fresh future-time/tool data is needed for confirmatory selection."  # 반복 연구 benchmark를 최종 미사용 test로 포장하지 않는다.
    summary_path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")  # 한국어 한계설명과 숫자를 사람이 읽기 쉽게 기록한다.
    workbook_path, export_status = optional_export(lambda: export_strict_workbook(RESULT_DIR, config))
    config["workbook_export"] = export_status
    summary_path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"summary": config, "summary_path": summary_path, "checkpoint_path": checkpoint_path, "workbook_path": workbook_path, "chart_path": chart_path, "history_path": history_path, "comparison_path": RESULT_DIR / "model_comparison.csv"}  # 앱·노트북이 결과 경로와 metrics를 직접 표시하도록 반환한다.


def run_experiment(progress_callback: Callable[[dict[str, Any]], None] | None = None, max_epochs: int = MAX_EPOCHS, patience: int = PATIENCE) -> dict[str, Any]:  # normal-only 학습부터 calibration과 locked test 감사까지 한 번에 수행한다.
    set_seed(SEED)  # 각 실행에서 model initialization과 batch order를 재현한다.
    train, calibration, test, labels, train_ids, calibration_ids, test_ids, scaler = prepare_data()  # 동일 group split에서 signal과 audit label을 받는다.
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # CUDA가 있으면 사용자 RTX GPU를 우선 사용한다.
    model = CausalMultiHorizonGPT(train.shape[1], train.shape[-1]).to(device)  # feature_count 20, sequence length 64로 모델을 구성한다.
    optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)  # 정상 forecast probability를 최소화하는 optimizer다.
    train_tensor = torch.from_numpy(train).float()  # 정상 train array를 float32 tensor로 바꾼다.
    loader = DataLoader(TensorDataset(train_tensor), batch_size=BATCH_SIZE, shuffle=True, num_workers=0, pin_memory=device.type == "cuda")  # GPU로 옮길 training lot을 섞어 소 batch로 만든다.
    calibration_tensor = torch.from_numpy(calibration).float().to(device)  # 정상 validation trace를 model과 같은 device에 올린다.
    best_state: dict[str, torch.Tensor] | None = None  # 가장 낮은 calibration loss의 가중치를 보관한다.
    best_loss = float("inf")  # 첫 정상 validation epoch가 항상 개선되도록 초깃값을 무한대로 둔다.
    best_epoch = 0  # 아직 검증된 epoch이 없음을 0으로 나타낸다.
    stale = 0  # validation loss가 개선되지 않은 연속 epoch 수를 센다.
    history: list[dict[str, float]] = []  # UI/CLI 그래프에 쓸 epoch별 train/validation 기록이다.
    for epoch in range(1, max_epochs + 1):  # early stopping 상한까지 실제 forward/backward pass를 반복한다.
        model.train()  # dropout과 train mode를 활성화한다.
        total_loss = 0.0  # sample-weighted train objective 누적값이다.
        total_samples = 0  # loss 평균을 계산할 실제 lot group 개수를 센다.
        for (batch,) in loader:  # 각 training batch는 normal lot group trace만 포함한다.
            batch = batch.to(device, non_blocking=True)  # CPU pin memory에서 CUDA로 batch를 비동기 복사한다.
            optimizer.zero_grad(set_to_none=True)  # 과거 gradient 누적을 지우고 불필요한 0 fill을 피한다.
            loss = multi_horizon_loss(model, batch)  # 네 미래거리의 sensor forecast Gaussian NLL을 계산한다.
            loss.backward()  # 목표 예측 확률을 올리도록 gradient를 전파한다.
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)  # 작은 데이터에서 튀는 gradient로 학습이 무너지는 일을 줄인다.
            optimizer.step()  # AdamW로 model parameter 한 step을 갱신한다.
            total_loss += float(loss.detach().cpu()) * len(batch)  # batch size 가중 평균을 계산할 numerator를 누적한다.
            total_samples += len(batch)  # 현재 batch lot group 개수를 누적한다.
        train_loss = total_loss / max(total_samples, 1)  # epoch 전체의 trace 수 가중 train loss를 계산한다.
        model.eval()  # validation에서 dropout을 끈다.
        with torch.no_grad():  # validation은 학습 gradient에 포함되지 않는다.
            validation_loss = float(multi_horizon_loss(model, calibration_tensor).cpu())  # 정상 calibration trace로만 best epoch를 선택한다.
        history.append({"epoch": float(epoch), "train_multi_horizon_gaussian_nll": train_loss, "validation_multi_horizon_gaussian_nll": validation_loss})  # Excel, notebook, 그래프에서 실제 학습 진전을 확인한다.
        if validation_loss < best_loss - 1e-5:  # 작은 noise 개선을 무시하고 명확한 normal validation 개선만 받는다.
            best_loss = validation_loss  # 현재 최선 정상 validation NLL을 기록한다.
            best_state = copy.deepcopy(model.state_dict())  # 후속 epoch update와 분리된 best model snapshot을 만든다.
            best_epoch = epoch  # selection에 사용된 epoch 수를 저장한다.
            stale = 0  # 개선이 있으면 early-stop 기다림을 초기화한다.
        else:  # normal validation objective가 개선되지 않은 epoch다.
            stale += 1  # 연속 미개선 횟수를 더한다.
        if progress_callback is not None:  # Streamlit/Jupyter가 전달한 경우 진행 상황을 실시간으로 보낸다.
            progress_callback({"epoch": epoch, "max_epochs": max_epochs, "train_loss": train_loss, "validation_loss": validation_loss, "best_validation_loss": best_loss, "best_epoch": best_epoch, "patience_left": max(patience - stale, 0), "device": str(device)})  # 사용자에게 loss와 장치를 투명하게 표시한다.
        if stale >= patience:  # 설정한 연속 patience만큼 정상 validation 개선이 없으면 종료한다.
            break  # test set을 보지 않고 early stopping을 수행한다.
    if best_state is None:  # 모델 학습 중 유효한 best snapshot이 하나도 없는지 확인한다.
        raise RuntimeError("정상 validation checkpoint가 없어 실험을 완료할 수 없습니다.")  # 실패를 정상 결과로 위장하지 않는다.
    model.load_state_dict(best_state)  # calibration normal에서 선택된 best model만 추론에 사용한다.
    calibration_scores, _, _ = score_signals(model, calibration, device)  # normal validation에서 고정 operating limit을 계산한다.
    test_scores, sensor_scores, horizon_scores = score_signals(model, test, device)  # official holdout을 gradient 없이 한 번 score한다.
    threshold = empirical_normal_limit(calibration_scores)  # holdout label을 쓰지 않은 정상 전용 95th percentile이다.
    metrics = evaluate(labels, test_scores, threshold, calibration_scores)  # 동일하게 고정한 limit 및 rank·queue 운영 지표를 산출한다.
    output = _write_results(model, history, train_ids, calibration_ids, test_ids, train, calibration, test, labels, scaler, device, best_epoch, metrics, calibration_scores, test_scores, sensor_scores, horizon_scores)  # model·workbook·chart·manifest를 모두 쓴다.
    output["metrics"] = metrics  # 완료된 앱 화면에 지표를 즉시 보여주도록 결과 dictionary에 넣는다.
    output["history"] = history  # Streamlit에서 epoch별 line chart를 그리도록 기록을 전달한다.
    output["device"] = str(device)  # UI와 터미널 요약에 실행 device를 표기한다.
    output["best_epoch"] = best_epoch  # normal validation이 선택한 best epoch를 기록한다.
    return output  # 앱·CLI·노트북 모두 같은 결과 구조를 받아서 사용한다.


if __name__ == "__main__":  # 직접 실행할 때만 재학습 또는 저장 모델 추론을 선택한다.
    parser = argparse.ArgumentParser(description="ST-AWFD GPT형 학습 / 저장 checkpoint CSV 추론")  # 실행 목적과 결과 경로를 명시하는 CLI를 만든다.
    parser.add_argument("--infer-csv", type=Path, help="재학습 없이 점수화할 label-free CSV")  # 미지정 기본 동작은 기존 실제 학습이다.
    parser.add_argument("--output-csv", type=Path, default=RESULT_DIR / "new_batch_review_queue.csv")  # CSV 저장 위치를 사용자가 지정할 수 있다.
    arguments = parser.parse_args()  # 오타/미지원 옵션은 argparse가 사용법과 함께 알린다.
    if arguments.infer_csv is not None:  # 추론 모드는 optimizer와 epoch loop에 들어가지 않는다.
        queue = score_new_csv(arguments.infer_csv)  # 학습된 best checkpoint로 실제 CUDA/CPU inference를 수행한다.
        arguments.output_csv.parent.mkdir(parents=True, exist_ok=True)  # 새 결과용 부모 폴더만 생성한다.
        queue.to_csv(arguments.output_csv, index=False, encoding="utf-8-sig")  # 한국어 Windows Excel에서도 읽히는 UTF-8 CSV를 저장한다.
        print(json.dumps({**queue.attrs, "lot_groups_scored": len(queue), "output_csv": str(arguments.output_csv)}, ensure_ascii=False, indent=2))  # 실행 장치·weight epoch·결과 위치를 눈으로 확인시킨다.
    else:  # 사용자가 inference 옵션을 주지 않았으면 normal-only 실험 전체를 실행한다.
        result = run_experiment(progress_callback=lambda event: print(f"epoch {event['epoch']:03d}/{event['max_epochs']}  train NLL={event['train_loss']:.5f}  normal-val NLL={event['validation_loss']:.5f}  best={event['best_validation_loss']:.5f} @ {event['best_epoch']}  device={event['device']}"))  # 매 epoch 실제 GPU 상태와 train/validation NLL을 보여준다.
        print(json.dumps({"device": result["device"], "best_epoch": result["best_epoch"], "metrics": result["metrics"], "summary_path": str(result["summary_path"]), "workbook_path": str(result["workbook_path"]), "chart_path": str(result["chart_path"])}, indent=2, ensure_ascii=False))  # 완료 지표와 결과 파일 위치를 출력한다.
