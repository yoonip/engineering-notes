# -*- coding: utf-8 -*-  # Windows와 Jupyter에서 한국어 설명을 그대로 읽는다.
# STMicroelectronics ST-AWFD D2를 공식 정상-only train / mixed-test로 재현하는 PE 이상감지 실험이다.  # SK hynix 내부 공정 연결과 자동 recipe 제어는 구현하지 않는다.
# 실행 가능한 Python 행마다 계산 이유와 현업 해석 경계를 설명하는 주석을 둔다.  # 빈 줄만 코드 섹션을 구분한다.

from __future__ import annotations  # 타입 힌트에 쓰인 새 표기법을 실행 시점까지 안전하게 보존한다.
from workbook_export import optional_export

import copy  # 최고 validation loss epoch의 신경망 가중치를 복사한다.
import hashlib  # 입력 공개 원본의 무결성 확인에 SHA-256을 쓴다.
import json  # 실험 설정과 실제 계산 지표를 machine-readable 형식으로 기록한다.
import math  # review queue 행 수와 비율을 계산한다.
import random  # Python 표준 난수 생성기까지 고정해 재현성을 높인다.
import zipfile  # 공식 원본 압축파일 안의 CSV를 중복 압축 해제 없이 읽는다.
from pathlib import Path  # 현재 코드가 어디서 실행되더라도 project 기준 경로를 계산한다.
from typing import Any, Callable  # callback와 결과 데이터 구조를 명확히 표기한다.

import joblib  # 기준 anomaly detector를 pickle 형식으로 저장하고 다시 불러온다.
import matplotlib  # headless 그래프 저장 backend를 설정한다.
matplotlib.use("Agg")  # Streamlit/Jupyter 외 터미널 실행에서도 차트 파일을 만든다.
import matplotlib.pyplot as plt  # 실제 epoch 기록과 anomaly score 분포를 시각화한다.
import numpy as np  # 고정 길이 시계열과 robust 통계 계산을 처리한다.
import pandas as pd  # 공개 sensor CSV와 audit/queue workbook 표를 다룬다.
import torch  # temporal autoencoder 학습과 RTX 3070 Ti inference에 사용한다.
from sklearn.ensemble import IsolationForest  # 정상 reference로부터 멀리 있는 표형 sample을 찾는 비지도 기준선이다.
from sklearn.metrics import average_precision_score, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score  # 희귀 이상 순위와 고정 false-alarm control limit 성능을 계산한다.
from sklearn.model_selection import train_test_split  # 정상 lot group 안에서 validation calibration 표본을 ID 단위로 분리한다.
from sklearn.pipeline import Pipeline  # 기준선 스케일링과 모델을 한 객체로 저장한다.
from sklearn.preprocessing import StandardScaler  # 요약 특징의 스케일을 training-normal subset에서만 적합한다.
from sklearn.svm import OneClassSVM  # normal manifold를 학습하는 고전적 multivariate anomaly 기준선이다.
from torch import nn  # temporal convolutional autoencoder를 정의한다.
from torch.utils.data import DataLoader, TensorDataset  # training wafer를 작은 GPU batch로 넣는다.

PROJECT_DIR = Path(__file__).resolve().parent  # project 경로를 이 모듈 파일에서 계산한다.
DATA_DIR = PROJECT_DIR / "data" / "st_awfd"  # 공개 D1/D2 archive 및 출처 정보를 모아 두는 폴더다.
RESULTS_DIR = PROJECT_DIR / "results" / "st_awfd"  # ST-AWFD 결과를 기존 SECOM 결과와 분리한다.
MODEL_DIR = PROJECT_DIR / "models" / "st_awfd"  # 새로 학습한 모델과 전처리 설정을 저장한다.
RAW_ARCHIVE = DATA_DIR / "D2.zip"  # 모델이 학습하고 평가할 공식 D2 파일의 경로다.
SEED = 3070  # GPU 장치명과 기억하기 쉽게 설정한 난수 seed다.
STEP_ID = 1  # 첫 제조 단계 신호만 입력해 stage-aware 조기 선별 가능성을 검토한다.
SEQUENCE_LENGTH = 64  # variable length lot group trace를 같은 상대시간 격자에 표현한다.
BATCH_SIZE = 64  # 작은 학습집합에서도 GPU 연산 효율과 안정성을 함께 유지한다.
MAX_EPOCHS = 150  # 정상 신호 재구성 학습의 최대 epoch 상한이다.
PATIENCE = 18  # 정상 validation MSE 개선이 멈추면 과적합을 줄이기 위해 조기 종료한다.
CALIBRATION_FPR = 0.05  # 5%는 예제 경보 예산 가정이고 fab의 공식 SPC/FDC limit은 아니다.
REVIEW_FRACTION = 0.10  # 상위 10% review queue는 고정 인력 용량 시나리오로만 표시한다.


class TemporalAutoencoder(nn.Module):  # 정상 waveform을 압축·복원하고 복원 오차를 이상 점수로 쓰는 소형 1D CNN이다.
    def __init__(self, input_channels: int) -> None:  # 실제 sensor 채널 수에 맞춰 입출력 층을 만든다.
        super().__init__()  # PyTorch module의 parameter 추적을 초기화한다.
        self.encoder = nn.Sequential(nn.Conv1d(input_channels, 32, kernel_size=5, padding=2), nn.BatchNorm1d(32), nn.GELU(), nn.Conv1d(32, 16, kernel_size=5, stride=2, padding=2), nn.BatchNorm1d(16), nn.GELU())  # 시간축을 절반으로 줄이며 정상 trace의 compact 표현을 학습한다.
        self.decoder = nn.Sequential(nn.ConvTranspose1d(16, 32, kernel_size=4, stride=2, padding=1), nn.BatchNorm1d(32), nn.GELU(), nn.Conv1d(32, input_channels, kernel_size=5, padding=2))  # 잠재 표현에서 원래 64시점 sensor trace를 복원한다.

    def forward(self, signal: torch.Tensor) -> torch.Tensor:  # sensor×time tensor를 같은 shape의 재구성 signal로 만든다.
        latent = self.encoder(signal)  # 정상 패턴을 압축된 특징으로 표현한다.
        return self.decoder(latent)  # 입력과 같은 차원의 추정 waveform을 반환한다.


def set_reproducibility(seed: int = SEED) -> None:  # 난수 발생기를 설정해 같은 split과 초기화를 재실행한다.
    random.seed(seed)  # 표준 library random 결과를 고정한다.
    np.random.seed(seed)  # NumPy shuffle/interpolation 후처리를 고정한다.
    torch.manual_seed(seed)  # CPU PyTorch model 초기 weights를 고정한다.
    if torch.cuda.is_available():  # CUDA가 설치된 경우만 장치 난수를 설정한다.
        torch.cuda.manual_seed_all(seed)  # GPU 하나 또는 여러 개의 난수 상태를 초기화한다.
    torch.backends.cudnn.deterministic = True  # 결정적인 CuDNN convolution 구현을 선택한다.
    torch.backends.cudnn.benchmark = False  # shape별 비결정적 성능 탐색을 끈다.


def sha256_file(path: Path) -> str:  # 재현 run에 사용한 원본 압축파일을 고유한 지문으로 기록한다.
    digest = hashlib.sha256()  # SHA-256 누산 객체를 만든다.
    with path.open("rb") as file_handle:  # 입력을 바이너리 모드로 연다.
        for block in iter(lambda: file_handle.read(1024 * 1024), b""):  # 큰 원본도 일정한 1 MiB 메모리만 사용해 읽는다.
            digest.update(block)  # 각 원본 block을 해시에 차례로 누적한다.
    return digest.hexdigest()  # 결과 manifest에 기록할 64자리 SHA-256을 반환한다.


def read_d2_source() -> pd.DataFrame:  # ST 공식 D2.zip에서 원본 행렬을 검증해 dataframe으로 읽는다.
    if not RAW_ARCHIVE.exists():  # 데이터 압축파일 누락을 학습 전에 확인한다.
        raise FileNotFoundError(f"공식 ST-AWFD D2.zip이 없습니다: {RAW_ARCHIVE}")  # 사용자가 문제를 바로 고칠 수 있도록 구체적 경로를 표시한다.
    with zipfile.ZipFile(RAW_ARCHIVE) as archive:  # 공식 원본을 read-only로 연다.
        csv_names = [member for member in archive.namelist() if Path(member).name.lower() == "d2.csv"]  # archive 내부의 D2.csv 하나를 찾는다.
        if len(csv_names) != 1:  # 여러 후보나 누락된 이름을 조용히 잘못 읽지 않게 한다.
            raise ValueError(f"D2.zip 안에서 D2.csv 하나를 기대했지만 {csv_names}를 찾았습니다.")  # 원본 archive schema가 달라졌음을 알린다.
        with archive.open(csv_names[0]) as source_stream:  # 압축된 원본 CSV stream을 메모리에서 연다.
            frame = pd.read_csv(source_stream)  # 쉼표 구분 열과 값들을 pandas가 읽는다.
    required = {"MaterialID", "StepID", "duration_ms", "is_test", "target"}  # 분석 단위·공정 단계·시간·공식 split·감사 label을 검증한다.
    missing = required.difference(frame.columns)  # 현재 CSV에서 필수 schema 열이 빠졌는지 찾는다.
    if missing:  # 새로운 schema의 불완전한 데이터로 학습하는 일을 막는다.
        raise ValueError(f"ST-AWFD D2 필수 열이 없습니다: {sorted(missing)}")  # 기대하는 schema 변경을 사용자에게 전달한다.
    feature_columns = [name for name in frame.columns if name.startswith("feature_")]  # 공식 익명 sensor name만 학습 입력 후보로 선택한다.
    if not feature_columns:  # 입력 열이 없으면 MaterialID나 label이 feature로 사용될 위험이 있다.
        raise ValueError("feature_ 접두어의 sensor 열이 없습니다.")  # 정답 열을 잘못 입력하는 일을 막는다.
    frame[feature_columns] = frame[feature_columns].apply(pd.to_numeric, errors="coerce")  # feature가 실제 숫자인지 점검한다.
    if frame[feature_columns].isna().any().any():  # 결측 신호는 모델이나 원천으로부터 명시적 처리 기준이 필요하다.
        raise ValueError("공개 D2 sensor에 결측/비숫자 값이 있어 학습을 중단합니다.")  # 값을 임의로 메우지 않고 source quality를 알린다.
    if frame.groupby("MaterialID")["target"].nunique().gt(1).any():  # 같은 wafer의 여러 time rows에 label이 하나인지 확인한다.
        raise ValueError("동일 MaterialID 안에 target label이 일관되지 않습니다.")  # label 해석이 불분명한 상태로 wafer를 합치지 않는다.
    if frame.groupby("MaterialID")["is_test"].nunique().gt(1).any():  # 공식 train/test가 row 단위로 섞인 wafer가 있는지 검사한다.
        raise ValueError("동일 MaterialID가 공개 is_test 양쪽에 포함되어 group leakage 위험이 있습니다.")  # 동일 lot group 파형이 train과 test에 나뉘지 않게 한다.
    return frame  # schema/label/group 검증이 끝난 원본을 반환한다.


def split_official_normal_reference(frame: pd.DataFrame, seed: int = SEED) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:  # 공식 is_test 구조를 따라 normal reference train/calibration과 mixed test를 나눈다.
    wafer_table = frame.groupby("MaterialID", sort=True).agg(target=("target", "first"), is_test=("is_test", "first")).reset_index()  # 각 lot group ID의 target/split을 한 행으로 만든다.
    train_wafer_table = wafer_table[wafer_table["is_test"] == 0].copy()  # 공개 benchmark의 is_test=0에 속한 historical reference wafer만 선택한다.
    test_wafer_table = wafer_table[wafer_table["is_test"] == 1].copy()  # 공개 benchmark에서 보류한 normal+abnormal wafer를 잠금 holdout으로 둔다.
    train_labels = set(train_wafer_table["target"].unique().tolist())  # 공식 train에 anomaly label이 섞였는지 확인한다.
    if train_labels != {0}:  # normal-only training이라는 dataset protocol이 바뀌었는지 검증한다.
        raise ValueError(f"ST-AWFD D2 is_test=0이 정상-only가 아닙니다: {train_labels}")  # 정상-only 탐지 설정을 잘못 재현하지 않게 중단한다.
    train_ids, calibration_ids = train_test_split(train_wafer_table["MaterialID"].to_numpy(), test_size=0.20, random_state=seed, shuffle=True)  # 정상 reference lot group 안에서 80% 학습/20% control-limit calibration으로 나눈다.
    train_set = set(train_ids.tolist())  # training MaterialID 묶음을 교집합 검사용 set으로 만든다.
    calibration_set = set(calibration_ids.tolist())  # 정상 validation calibration ID 묶음을 별도로 만든다.
    test_set = set(test_wafer_table["MaterialID"].tolist())  # 공개 혼합 holdout의 MaterialID를 독립 집합으로 만든다.
    if train_set & calibration_set or train_set & test_set or calibration_set & test_set:  # 동일 ID가 여러 단계로 새지 않았는지 확인한다.
        raise RuntimeError("MaterialID가 train/calibration/holdout 사이에 겹칩니다.")  # 누출이 발견되면 성공 결과를 내지 않는다.
    train_frame = frame[frame["MaterialID"].isin(train_set)].copy()  # 정상 reference model fit용 trace만 선택한다.
    calibration_frame = frame[frame["MaterialID"].isin(calibration_set)].copy()  # threshold 설정용 정상 trace만 선택한다.
    test_frame = frame[frame["MaterialID"].isin(test_set)].copy()  # test labels는 결과 감사 전까지 학습/threshold 계산에서 쓰지 않는다.
    manifest = wafer_table.copy()  # 각 데이터 개체의 분할과 원본 flag를 보관한다.
    manifest["partition"] = np.where(manifest["MaterialID"].isin(train_set), "train_normal", np.where(manifest["MaterialID"].isin(calibration_set), "normal_calibration", "official_mixed_holdout"))  # 학습·control-limit·final audit 역할을 명확히 표시한다.
    return train_frame, calibration_frame, test_frame, manifest  # 세 집합과 lot group-level split 증적을 넘긴다.


def resample_step_one(frame: pd.DataFrame, feature_columns: list[str], sequence_length: int = SEQUENCE_LENGTH) -> tuple[np.ndarray, np.ndarray, np.ndarray, pd.DataFrame]:  # wafer별 Step 1 파형을 64개의 상대 시간으로 보간한다.
    step_frame = frame[frame["StepID"] == STEP_ID].copy()  # Step 1 신호만 골라서 PE stage-aware 입력으로 한정한다.
    if step_frame.empty:  # 잘못된 데이터 subset/공정 step 설정을 미리 찾는다.
        raise ValueError(f"StepID={STEP_ID} 신호가 비었습니다.")  # 잘못된 선택으로 빈 tensor를 만들지 않는다.
    step_frame = step_frame.sort_values(["MaterialID", "duration_ms"], kind="mergesort")  # 각 lot group 안에서 기록된 상대 시간 순서를 보존한다.
    relative_grid = np.linspace(0.0, 1.0, sequence_length, dtype=np.float32)  # feature별 보간에 공통 상대시간 격자를 만든다.
    signals: list[np.ndarray] = []  # lot group×sensor×time 입력 tensor를 순서대로 쌓는다.
    metadata: list[dict[str, Any]] = []  # lot group id와 실제 관측 sample 수를 별도로 유지한다.
    for wafer_id, wafer_rows in step_frame.groupby("MaterialID", sort=True):  # lot group 단위로 묶어 하나의 곡선이 여러 wafer에 이어지지 않게 한다.
        timestamps = wafer_rows["duration_ms"].to_numpy(dtype=np.float64)  # 공개 상대시간을 실제 순서 축으로 변환한다.
        time_min = float(timestamps.min())  # lot group 관측 step의 시작 timestamp를 구한다.
        time_max = float(timestamps.max())  # lot group 관측 step의 끝 timestamp를 구한다.
        if time_max <= time_min:  # 같은 time 한 점뿐이면 곡선의 모양을 정의할 수 없다.
            raise ValueError(f"MaterialID={wafer_id}에 유효한 Step 1 시간 범위가 없습니다.")  # 잘못된 trace는 추정값으로 채우지 않는다.
        local_axis = ((timestamps - time_min) / (time_max - time_min)).astype(np.float32)  # 정확한 timestamp 단위가 공개되지 않아 lot group-local relative time만 쓴다.
        values = wafer_rows[feature_columns].to_numpy(dtype=np.float32)  # 익명 sensor matrix를 같은 timestamp 순서로 변환한다.
        curve = np.stack([np.interp(relative_grid, local_axis, values[:, channel]).astype(np.float32) for channel in range(len(feature_columns))], axis=0)  # 실제 관측점 사이를 선형 보간해 고정 길이 파형을 만든다.
        signals.append(curve)  # 현재 wafer의 [sensor, time] tensor를 결과에 보존한다.
        metadata.append({"MaterialID": wafer_id, "target_for_audit_only": int(wafer_rows["target"].iloc[0]) if "target" in wafer_rows else None, "source_is_test": int(wafer_rows["is_test"].iloc[0]) if "is_test" in wafer_rows else None, "step_sample_count": int(len(wafer_rows)), "step_duration_normalized": time_max - time_min})  # score-input 정보와 사후 audit 정보를 명확히 나눈다.
    meta = pd.DataFrame(metadata)  # 센서 array 행에 맞는 lot group-level meta table을 만든다.
    targets = meta["target_for_audit_only"].fillna(-1).to_numpy(dtype=np.int64)  # train에는 모두 normal, inference에는 -1이 될 수 있는 audit label 배열을 만든다.
    return np.stack(signals).astype(np.float32), targets, meta["MaterialID"].to_numpy(), meta  # raw waveform과 매칭되는 labels/IDs/quality metadata를 반환한다.


def normalize_with_training_normals(train_array: np.ndarray, other_arrays: list[np.ndarray]) -> tuple[np.ndarray, list[np.ndarray], dict[str, list[float]]]:  # 표준화 평균과 분산을 정상 train wafer에만 맞춘다.
    means = train_array.mean(axis=(0, 2), keepdims=True)  # 정상 학습집합의 sensor별 평균만 산출한다.
    deviations = train_array.std(axis=(0, 2), keepdims=True)  # 정상 학습집합의 sensor별 표준편차만 산출한다.
    deviations = np.where(deviations < 1e-6, 1.0, deviations)  # 일정한 channel은 division by zero 없이 centered 처리한다.
    train_scaled = ((train_array - means) / deviations).astype(np.float32)  # 정상 학습 signal을 training reference 통계로 표준화한다.
    other_scaled = [((values - means) / deviations).astype(np.float32) for values in other_arrays]  # calibration와 test도 고정한 train 통계만 사용한다.
    saved = {"feature_mean": means.reshape(-1).astype(float).tolist(), "feature_std": deviations.reshape(-1).astype(float).tolist()}  # 새로운 CSV 추론에 쓸 scaler 값을 JSON/checkpoint 형태로 만든다.
    return train_scaled, other_scaled, saved  # 학습·validation·test 정규화 파형과 변환 상태를 반환한다.


def summarize_waveforms(signal_array: np.ndarray) -> np.ndarray:  # 고전 model baseline용 waveform 통계를 wafer별 feature vector로 만든다.
    time_grid = np.linspace(0.0, 1.0, signal_array.shape[-1], dtype=np.float32)  # 선형 drift를 계산할 상대시간 지점을 만든다.
    means = signal_array.mean(axis=-1)  # sensor의 step 평균값을 특징으로 쓴다.
    stds = signal_array.std(axis=-1)  # step 내 공정 변동 폭을 특징으로 쓴다.
    minima = signal_array.min(axis=-1)  # 낮은 transient를 포착할 최소값을 보존한다.
    maxima = signal_array.max(axis=-1)  # 높은 transient를 포착할 최대값을 보존한다.
    p10 = np.quantile(signal_array, 0.10, axis=-1)  # 낮은 꼬리 분포값을 robust summary에 포함한다.
    p90 = np.quantile(signal_array, 0.90, axis=-1)  # 높은 꼬리 분포값을 robust summary에 포함한다.
    abs_peak = np.abs(signal_array).max(axis=-1)  # 정규화된 기준으로 가장 큰 excursion을 요약한다.
    start = signal_array[..., 0]  # step 진입 초반의 수준을 기록한다.
    end = signal_array[..., -1]  # step 종료 직전의 수준을 기록한다.
    centered_time = time_grid - time_grid.mean()  # 회귀 절편과 분리할 선형 time coordinate를 만든다.
    slopes = np.einsum("nct,t->nc", signal_array - means[..., None], centered_time) / np.sum(centered_time**2)  # 각 sensor의 전체 step 선형 drift를 추정한다.
    return np.stack([means, stds, minima, maxima, p10, p90, abs_peak, start, end, slopes], axis=-1).reshape(signal_array.shape[0], -1).astype(np.float32)  # 10개 요약 통계를 feature dimension으로 펼친다.


def fit_autoencoder(train_array: np.ndarray, validation_array: np.ndarray, device: torch.device, callback: Callable[[dict[str, Any]], None] | None = None, max_epochs: int = MAX_EPOCHS, patience: int = PATIENCE) -> tuple[TemporalAutoencoder, list[dict[str, float]], int]:  # 정상 wafer만 보고 CNN autoencoder를 학습하고 정상 validation MSE로 epoch을 선택한다.
    model = TemporalAutoencoder(train_array.shape[1]).to(device)  # data sensor channel 수와 일치하는 모델을 선택 장치에 올린다.
    optimizer = torch.optim.AdamW(model.parameters(), lr=8e-4, weight_decay=1e-3)  # validation normal MSE를 줄이는 작은 learning rate와 weight decay를 사용한다.
    loss_function = nn.MSELoss()  # 복원한 sensor trace와 실제 정상 reference trace 사이의 평균제곱오차를 계산한다.
    training_x = torch.from_numpy(train_array).float()  # 정상 waveform을 PyTorch float tensor로 준비한다.
    training_loader = DataLoader(TensorDataset(training_x), batch_size=BATCH_SIZE, shuffle=True, num_workers=0, pin_memory=(device.type == "cuda"))  # lot group 단위 normal trace만 random minibatch로 처리한다.
    calibration_x = torch.from_numpy(validation_array).float().to(device)  # 정상 calibration trace를 GPU에 한 번 올려 매 epoch 검증한다.
    best_validation_mse = float("inf")  # 아직 좋은 모델을 찾지 못한 초기 상태를 표시한다.
    best_weights: dict[str, torch.Tensor] | None = None  # 정상 validation MSE가 최소인 parameter snapshot을 보관한다.
    best_epoch = 0  # 실제 선택한 epoch 번호를 기록한다.
    stale_epochs = 0  # validation MSE 개선이 없는 연속 epoch 수를 센다.
    history: list[dict[str, float]] = []  # 실제 학습 및 정상 validation error만 모은다.
    for epoch in range(1, max_epochs + 1):  # 최대 epoch 내에서 실제 gradient update를 반복한다.
        model.train()  # batch normalization과 학습 모드를 켠다.
        total_loss = 0.0  # wafer별 loss 합계를 초기화한다.
        total_wafers = 0  # 손실 평균 분모를 계산할 lot group 수를 초기화한다.
        for (clean_batch,) in training_loader:  # 정상 lot group waveform batch 하나를 불러온다.
            clean_batch = clean_batch.to(device, non_blocking=True)  # 선택된 장치로 입력을 전송한다.
            noisy_batch = clean_batch + 0.02 * torch.randn_like(clean_batch)  # 작은 sensor noise를 더해 과도한 identity-copy를 줄인다.
            optimizer.zero_grad(set_to_none=True)  # 직전 batch의 gradient를 지우고 메모리 재사용을 돕는다.
            reconstructed = model(noisy_batch)  # 약간 변형된 입력을 정상 형태로 복원하도록 추정한다.
            loss = loss_function(reconstructed, clean_batch)  # 복원값과 변형 전 정상 trace를 비교한다.
            loss.backward()  # reconstruction MSE를 줄이기 위한 gradient를 계산한다.
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=5.0)  # 작은 데이터에서 불안정한 weight update를 제한한다.
            optimizer.step()  # AdamW가 실제 학습 parameter를 한 번 갱신한다.
            total_loss += float(loss.detach().cpu()) * len(clean_batch)  # batch 크기를 반영해 epoch 평균 손실을 누적한다.
            total_wafers += len(clean_batch)  # epoch 전체 lot group 수로 평균을 낼 수 있게 센다.
        model.eval()  # calibration lot group 예측은 dropout 없는 평가 모드에서 수행한다.
        with torch.no_grad():  # validation weight update가 없으므로 gradient 기록을 끈다.
            validation_reconstruction = model(calibration_x)  # 정상 calibration trace를 복원한다.
            validation_mse = float(loss_function(validation_reconstruction, calibration_x).detach().cpu())  # 정상 calibration 집합의 재구성 오차를 계산한다.
        training_mse = total_loss / max(total_wafers, 1)  # wafer별로 가중한 실제 training MSE 평균을 계산한다.
        history.append({"epoch": float(epoch), "train_denoising_mse": training_mse, "validation_normal_mse": validation_mse})  # 보이는 학습 곡선에 실제 observation을 기록한다.
        if validation_mse < best_validation_mse - 1e-7:  # 정상 calibration trace가 전보다 잘 복원되는지 비교한다.
            best_validation_mse = validation_mse  # 현재 검증 점수를 최고 점수로 갱신한다.
            best_weights = copy.deepcopy(model.state_dict())  # 이후 epoch이 덮기 전에 선택 가능한 weights를 복사한다.
            best_epoch = epoch  # 최종 재현에 필요한 선택 epoch을 기억한다.
            stale_epochs = 0  # 정상 validation 개선 시 조기 종료 카운터를 재설정한다.
        else:  # MSE가 개선되지 않은 epoch은 학습 수렴 판정에 반영한다.
            stale_epochs += 1  # validation plateau가 지속된 횟수를 누적한다.
        if callback is not None:  # Streamlit/Jupyter가 실시간 epoch 값을 표시하도록 요청했는지 확인한다.
            callback({"epoch": epoch, "max_epochs": max_epochs, "train_loss": training_mse, "validation_loss": validation_mse, "best_validation_loss": best_validation_mse, "best_epoch": best_epoch, "patience_left": max(patience - stale_epochs, 0), "device": str(device)})  # UI에 실제 계산한 loss와 조기 종료 상태만 전달한다.
        if stale_epochs >= patience:  # 정상 validation 신호 개선이 멈추면 overfit 방지를 위해 학습을 끝낸다.
            break  # 저장한 최고 점수 모델로 돌아갈 것이므로 불필요한 epoch을 수행하지 않는다.
    if best_weights is None:  # 유효한 validation checkpoint가 선택되지 않았는지 검사한다.
        raise RuntimeError("정상 validation MSE 기준으로 모델을 선택하지 못했습니다.")  # 잘못된 학습 결과를 산출물로 저장하지 않는다.
    model.load_state_dict(best_weights)  # test를 한 번도 보고 선택하지 않은 best validation model을 복원한다.
    return model, history, best_epoch  # 모델·실측 학습 이력·선택 epoch을 반환한다.


def reconstruction_scores(model: TemporalAutoencoder, signals: np.ndarray, device: torch.device) -> tuple[np.ndarray, np.ndarray]:  # 복원오차를 lot group score와 sensor contribution으로 나눈다.
    model.eval()  # inference에서는 batch norm을 학습 상태로 바꾸지 않는다.
    with torch.no_grad():  # scoring에 gradient가 필요하지 않아 memory를 절약한다.
        inputs = torch.from_numpy(signals).float().to(device)  # 고정길이 signal batch를 RTX GPU 또는 CPU로 이동한다.
        reconstruction = model(inputs)  # 학습된 정상 manifold로 입력 파형을 재구성한다.
        squared_errors = (reconstruction - inputs).square().detach().cpu().numpy()  # 시간·채널마다 정상 기준과 다른 정도를 절대 제곱 오차로 계산한다.
    return squared_errors.mean(axis=(1, 2)), squared_errors.mean(axis=2)  # lot group 전체 anomaly score와 sensor별 평균 오차를 함께 반환한다.


def calibrate_normal_limit(scores: np.ndarray, target_false_alarm_rate: float = CALIBRATION_FPR) -> float:  # 정상 calibration score 분포의 사전 선택 quantile을 control limit으로 쓴다.
    if not 0.01 <= target_false_alarm_rate <= 0.20:  # 임의로 넓은 영역의 alarm 설정을 막아 1~20% scenario로 제한한다.
        raise ValueError("calibration false-alarm target은 1%~20% 사이에서 지정하세요.")  # 이 비율이 fab의 공식 기준은 아님을 UI 문구와 함께 보여준다.
    return float(np.quantile(scores, 1.0 - target_false_alarm_rate, method="higher"))  # 정상 validation 상위 tail 값을 사용해 사전에 정한 alarm rate를 구현한다.


def wilson_interval(successes: int, observations: int, z_value: float = 1.96) -> list[float]:  # lot group 수가 유한한 false alarm/recall 추정의 95% Wilson 구간을 계산한다.
    if observations <= 0:  # 표본이 없으면 범위를 산출할 분모가 없다.
        return [float("nan"), float("nan")]  # 추측값 대신 unavailable로 남긴다.
    proportion = successes / observations  # 관측 비율을 계산한다.
    denominator = 1.0 + z_value**2 / observations  # Wilson 식의 보정 분모를 계산한다.
    center = (proportion + z_value**2 / (2.0 * observations)) / denominator  # 유한 표본 중심을 보정한다.
    margin = z_value * math.sqrt((proportion * (1.0 - proportion) / observations) + (z_value**2 / (4.0 * observations**2))) / denominator  # 불확실성 구간 반폭을 계산한다.
    return [float(max(center - margin, 0.0)), float(min(center + margin, 1.0))]  # 확률 영역 [0,1]에 잘라 하한과 상한을 반환한다.


def evaluate_anomaly_scores(labels: np.ndarray, scores: np.ndarray, threshold: float, review_fraction: float = REVIEW_FRACTION, calibration_scores: np.ndarray | None = None) -> dict[str, Any]:  # 고정 정상 기준선과 test label 감사 지표를 함께 계산한다.
    predictions = (scores > threshold).astype(np.int64)  # validation normal에서 고정한 control limit 초과 여부를 적용한다.
    tn, fp, fn, tp = confusion_matrix(labels, predictions, labels=[0, 1]).ravel().tolist()  # 정답 label과 alarm flag의 혼동행렬을 계산한다.
    ranking = np.argsort(-scores, kind="mergesort")  # 고정 검토 용량 순위 큐를 안정적으로 만든다.
    queue_size = min(len(labels), max(1, math.ceil(len(labels) * review_fraction)))  # 사용 가능한 PE review 인력의 예시 용량을 lot group 수로 환산한다.
    queue_hits = int(labels[ranking[:queue_size]].sum())  # 상위 review queue 안에 양성 wafer가 몇 개 있는지 사후 감사한다.
    metric = {"n_wafers": int(len(labels)), "n_anomalous": int(labels.sum()), "anomaly_prevalence": float(labels.mean()), "average_precision": float(average_precision_score(labels, scores)), "roc_auc": float(roc_auc_score(labels, scores)), "threshold": float(threshold), "true_positive": int(tp), "false_positive": int(fp), "true_negative": int(tn), "false_negative": int(fn), "recall_at_normal_limit": float(recall_score(labels, predictions, zero_division=0)), "precision_at_normal_limit": float(precision_score(labels, predictions, zero_division=0)), "f1_at_normal_limit": float(f1_score(labels, predictions, zero_division=0)), "test_normal_false_alarm_rate": float(fp / max(tn + fp, 1)), "test_normal_fpr_wilson_95pct": wilson_interval(fp, tn + fp), "anomaly_recall_wilson_95pct": wilson_interval(tp, tp + fn), "test_alert_fraction": float(predictions.mean()), "review_queue_capacity": int(queue_size), "review_queue_true_positives": queue_hits, "recall_at_review_capacity": float(queue_hits / max(int(labels.sum()), 1)), "precision_at_review_capacity": float(queue_hits / queue_size)}  # 검색 순위와 실제 정상 calibration 기준선 결과를 함께 보여준다.
    if calibration_scores is not None:  # 정상 reference calibration에서 기준선을 실제로 맞춘 비율도 함께 감사한다.
        metric["calibration_normal_false_alarm_rate"] = float(np.mean(calibration_scores > threshold))  # quantile 경계 ties를 포함한 실제 validation exceedance를 기록한다.
    return metric  # 모든 지표를 같은 딕셔너리로 반환한다.


def predict_scores(detector: Any, features: np.ndarray, direction: str) -> np.ndarray:  # sklearn detector의 정상도 점수를 이상 순위로 방향 맞춘다.
    if direction == "decision_function":  # OneClassSVM의 높을수록 inlier인 점수를 처리한다.
        return -np.asarray(detector.decision_function(features)).reshape(-1)  # 부호를 뒤집어 높을수록 anomaly가 되게 한다.
    if direction == "score_samples":  # Isolation Forest의 낮은 정상도 점수를 처리한다.
        return -np.asarray(detector.score_samples(features)).reshape(-1)  # 부호 반전으로 높은 anomaly score 규약을 통일한다.
    raise ValueError(f"알 수 없는 이상점수 방향입니다: {direction}")  # 예상한 score type 외에는 뜻을 임의로 추측하지 않는다.


def empirical_cdf(reference_scores: np.ndarray, values: np.ndarray) -> np.ndarray:  # ensemble 구성 detector 점수를 정상 calibration 분포의 percentile로 변환한다.
    ordered_reference = np.sort(np.asarray(reference_scores, dtype=np.float64))  # calibration 정상 score의 순서 통계량을 계산한다.
    return np.searchsorted(ordered_reference, values, side="right").astype(np.float64) / max(len(ordered_reference), 1)  # 모든 test wafer에 같은 calibration reference를 적용한다.


def score_new_csv(csv_path: str | Path, checkpoint_path: str | Path | None = None, review_fraction: float = REVIEW_FRACTION) -> pd.DataFrame:  # 새 label-free fab CSV를 기존 TCN과 고정 기준선으로 점수화한다.
    input_path = Path(csv_path)  # 사용자가 지정한 incoming batch CSV 경로를 정규화한다.
    incoming = pd.read_csv(input_path)  # target/is_test 없이도 읽을 수 있도록 CSV를 로드한다.
    required = {"MaterialID", "StepID", "duration_ms"}  # 새 공정 데이터에 필요한 lot group/step/time 식별 열을 확인한다.
    if not required.issubset(incoming.columns):  # 최소 schema가 빠진 데이터는 잘못된 예측 전에 중단한다.
        raise ValueError(f"CSV에 필요한 열이 없습니다: {sorted(required - set(incoming.columns))}")  # 외부 입력 오류를 구체적으로 표시한다.
    if checkpoint_path is None:  # 경로가 생략됐을 때 현재 project의 학습 결과 모델을 쓴다.
        checkpoint_path = MODEL_DIR / "st_awfd_step1_temporal_autoencoder.pt"  # training pipeline이 저장하는 기본 TCN checkpoint를 선택한다.
    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=True)  # GPU에 종속되지 않는 CPU map에서 모델 metadata를 읽는다.
    feature_columns = checkpoint["feature_columns"]  # 학습 때 쓰던 익명 센서 order를 정확히 복원한다.
    missing_features = set(feature_columns).difference(incoming.columns)  # 모델에 필요한 입력 sensor가 누락됐는지 검사한다.
    if missing_features:  # 센서가 바뀌면 그대로 점수화할 수 없다.
        raise ValueError(f"학습 때와 다른 입력 schema입니다. 빠진 sensor: {sorted(missing_features)}")  # 잘못 정렬된 channel에 모델을 적용하지 않는다.
    signal, _, ids, metadata = resample_step_one(incoming, feature_columns)  # target 없는 incoming row도 한 wafer씩 같은 기준으로 변환한다.
    means = np.asarray(checkpoint["scaling"]["feature_mean"], dtype=np.float32).reshape(1, -1, 1)  # 학습 정상 wafer에서 저장한 channel 평균을 복원한다.
    deviations = np.asarray(checkpoint["scaling"]["feature_std"], dtype=np.float32).reshape(1, -1, 1)  # 학습 정상 wafer에서 저장한 channel 표준편차를 복원한다.
    standardized = ((signal - means) / deviations).astype(np.float32)  # 신규 batch 통계로 다시 맞추지 않고 training reference를 그대로 적용한다.
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # 가능한 경우 inference도 RTX GPU에서 수행한다.
    model = TemporalAutoencoder(len(feature_columns)).to(device)  # checkpoint의 channel 차원과 일치하는 model shell을 만든다.
    model.load_state_dict(checkpoint["state_dict"])  # 실제 저장된 정상 pattern model weight를 불러온다.
    values, _ = reconstruction_scores(model, standardized, device)  # label 없이 복원 기반 anomaly score를 계산한다.
    ranking = np.argsort(-values, kind="mergesort")  # incoming batch 내 상대 우선순위를 결정한다.
    ranks = np.empty(len(values), dtype=np.int64)  # 입력 순서에 맞춰 각 wafer의 review rank를 저장한다.
    ranks[ranking] = np.arange(1, len(values) + 1)  # 점수가 큰 wafer에 낮은 순위 번호를 준다.
    queue_size = max(1, math.ceil(len(values) * review_fraction))  # 사용자가 선택한 batch 검토 용량을 계산한다.
    summary = json.loads((RESULTS_DIR / "st_awfd_run_summary.json").read_text(encoding="utf-8"))  # training run에서 validation-only로 정한 normal reference limit을 읽는다.
    threshold = float(summary["experiment"]["calibration_thresholds"]["TemporalAutoencoder_GPU"])  # 정상 validation 95th percentile threshold를 그대로 적용한다.
    return pd.DataFrame({"MaterialID": ids, "step_id_used": STEP_ID, "anomaly_score": values, "normal_reference_limit": threshold, "above_normal_reference_limit": values > threshold, "review_rank": ranks, "review_candidate_at_capacity": ranks <= queue_size, "step_sample_count": metadata["step_sample_count"].to_numpy(), "step_duration_normalized": metadata["step_duration_normalized"].to_numpy()}).sort_values("review_rank").reset_index(drop=True)  # label-free queue만 외부 응용에 반환한다.


def make_excel_report(summary: dict[str, Any], history: pd.DataFrame, model_table: pd.DataFrame, queue: pd.DataFrame, audit: pd.DataFrame, residual_table: pd.DataFrame, calibration_audit: pd.DataFrame, manifest: pd.DataFrame) -> Path:  # PE가 복원오차 queue와 retrospective audit를 분리해 보는 Excel을 생성한다.
    output = RESULTS_DIR / "ST_AWFD_PE_Anomaly_Triage.xlsx"  # 새 workbook을 이번 실험 output 폴더에 저장한다.
    experiment = summary["experiment"]  # 요약을 만들기 쉽게 실험 설정과 선택 모델을 불러온다.
    overview = pd.DataFrame([{"항목": "공개 데이터", "값": summary["dataset"]["name"]}, {"항목": "공식 원본", "값": summary["dataset"]["source_url"]}, {"항목": "공식 train", "값": f'{summary["dataset"]["official_train_normal_wafers"]}개 wafer, target 0만 포함'}, {"항목": "공식 mixed holdout", "값": f'{summary["dataset"]["official_test_wafers"]}개 wafer, normal {summary["dataset"]["official_test_normal_wafers"]}, anomaly {summary["dataset"]["official_test_anomalous_wafers"]}'}, {"항목": "입력", "값": "StepID=1, 20 anonymized sensors × 64 relative-time bins"}, {"항목": "학습", "값": "normal-only temporal convolutional autoencoder, denoising MSE"}, {"항목": "학습 장치", "값": summary["device"]["device_name"]}, {"항목": "best epoch", "값": experiment["best_epoch"]}, {"항목": "normal reference limit", "값": f'validation normal {experiment["calibration_target_fpr"]:.0%} quantile'}, {"항목": "mixed holdout ROC-AUC", "값": experiment["primary_holdout_metrics"]["roc_auc"]}, {"항목": "mixed holdout AP", "값": experiment["primary_holdout_metrics"]["average_precision"]}, {"항목": "holdout recall at normal limit", "값": experiment["primary_holdout_metrics"]["recall_at_normal_limit"]}, {"항목": "validation normal false-alarm rate", "값": experiment["primary_holdout_metrics"]["calibration_normal_false_alarm_rate"]}, {"항목": "holdout normal false-alarm rate", "값": experiment["primary_holdout_metrics"]["test_normal_false_alarm_rate"]}, {"항목": "normal false-alarm 95% CI", "값": str(experiment["primary_holdout_metrics"]["test_normal_fpr_wilson_95pct"])}, {"항목": "holdout FPR / target", "값": experiment["primary_holdout_metrics"]["test_normal_false_alarm_inflation_vs_target"]}, {"항목": "10% top queue anomaly capture", "값": f'{experiment["primary_holdout_metrics"]["review_queue_true_positives"]} / {experiment["primary_holdout_metrics"]["n_anomalous"]}'}, {"항목": "양산 수율 개선", "값": "미측정; abnormal lot/wafer 검토 후보 순위화만 측정"}, {"항목": "threshold 조건", "값": "5% validation-normal tail 기준 가정; 업체 SPC/FDC limit 아님"}, {"항목": "license", "값": "CC BY-NC-SA 4.0; attribution/non-commercial/share-alike 준수"}])  # 출처와 실제 지표·threshold drift·해석 한계를 첫 탭에 요약한다.
    dictionary = pd.DataFrame([{"필드": "MaterialID", "설명": "ST source의 익명 wafer ID; group 단위 분할/출력 식별에만 사용"}, {"필드": "StepID", "설명": "공정 단계 식별자; early-stage pilot은 StepID=1만 입력"}, {"필드": "duration_ms", "설명": "relative timestamp; 물리적 ms 단위로 해석하지 않음"}, {"필드": "feature_1 … feature_20", "설명": "익명 sensor channel; 공개 전에 z-score된 신호이며 물리량/tool mapping은 비공개"}, {"필드": "is_test", "설명": "공식 split key; source training/calibration/test selection에만 쓰고 모델 입력에서 제외"}, {"필드": "target", "설명": "normal=0/anomaly=1 사후 평가 label; 신경망 학습과 threshold calibration에서는 제외"}, {"필드": "anomaly_score", "설명": "Step 1 정상 waveform reconstruction MSE; 확률이 아니라 정상 reference로부터의 비유사도"}])  # 모델 입력과 label·점수의 의미를 모두 분리해 기록한다.
    source_table = pd.DataFrame([{"자료": "STMicroelectronics ST-AWFD", "URL": "https://github.com/STMicroelectronics/ST-AWFD", "사용": "D2.zip, normal-only training + mixed holdout"}, {"자료": "ST-AWFD original paper", "URL": "https://doi.org/10.3390/s21165465", "사용": "sensor step/wafer structure 및 2021 anomaly detection baseline"}, {"자료": "TRACE-GPT paper", "URL": "https://arxiv.org/abs/2309.11427", "사용": "sequence forecasting error 개념 참조; 본 CNN AE가 TRACE-GPT 재현은 아님"}, {"자료": "KNUAI/forCar", "URL": "https://github.com/KNUAI/forCar", "사용": "ST-AWFD에 적용된 CR AE/LSTM pipeline 직접 검토 후 group/threshold/padding 개선"}, {"자료": "License text", "URL": "https://creativecommons.org/licenses/by-nc-sa/4.0/", "사용": "비상업적 재사용·출처·동일조건 공유 조건"}])  # 논문과 구현 출처, 이 코드의 차용 범위를 밝힌다.
    with pd.ExcelWriter(output, engine="openpyxl") as writer:  # 사용자가 정렬/필터/수식 확장을 할 수 있는 xlsx로 기록한다.
        overview.to_excel(writer, sheet_name="PE 검토 요약", index=False)  # 주 결과와 목표 FPR을 workbook 처음에 둔다.
        model_table.to_excel(writer, sheet_name="모델 비교", index=False)  # CNN AE와 classical detector의 같은 test 비교를 기록한다.
        history.to_excel(writer, sheet_name="실제 epoch 기록", index=False)  # 매 epoch 실측 MSE 두 값을 보존한다.
        queue.to_excel(writer, sheet_name="검토 큐 label 제외", index=False)  # 현장 판단 view에는 target을 숨긴 순위표만 둔다.
        audit.to_excel(writer, sheet_name="공식 test 사후 감사", index=False)  # 실제 label과 confusion outcomes는 분리된 audit에 둔다.
        residual_table.to_excel(writer, sheet_name="Sensor 오차 영향", index=False)  # 재구성 차이가 컸던 익명 channel을 검토 단서로 제공한다.
        calibration_audit.to_excel(writer, sheet_name="기준선 drift 감사", index=False)  # 정상 calibration과 공식 holdout 정상의 분포 이동을 숨기지 않는다.
        manifest.to_excel(writer, sheet_name="Wafer split manifest", index=False)  # MaterialID가 model fit/limit/test 중 어디에 갔는지 보존한다.
        dictionary.to_excel(writer, sheet_name="데이터 사전", index=False)  # ST source 열과 점수의 실제 정의를 설명한다.
        source_table.to_excel(writer, sheet_name="출처와 한계", index=False)  # citation, license, methodological boundary를 기록한다.
        for sheet in writer.book.worksheets:  # 모든 탭에 filter/freeze/열 너비 편의를 설정한다.
            sheet.freeze_panes = "A2"  # 긴 result table에서도 header를 고정한다.
            sheet.auto_filter.ref = sheet.dimensions  # 현장 후보를 sensor/label별로 정렬·필터할 수 있게 한다.
            for column_cells in sheet.columns:  # 데이터 텍스트를 기준으로 열 폭을 계산한다.
                measured_width = max((len(str(cell.value or "")) for cell in column_cells), default=10) + 2  # 각 열의 대표적인 텍스트 폭을 측정한다.
                sheet.column_dimensions[column_cells[0].column_letter].width = min(max(measured_width, 12), 54)  # 너무 좁거나 넓은 열을 제한한다.
            for header in sheet[1]:  # 각 sheet의 첫 행을 헤더 모양으로 구별한다.
                header_font = copy.copy(header.font)  # openpyxl immutable style을 새 객체로 복사해 수정한다.
                header_font.bold = True  # column 이름을 굵게 표시한다.
                header_font.color = "FFFFFF"  # header 글자를 흰색으로 설정한다.
                header.font = header_font  # 변경한 header font를 셀에 다시 할당한다.
                header.fill = __import__("openpyxl").styles.PatternFill("solid", fgColor="255C85")  # 짙은 청색 채우기로 source/output 표의 첫 행을 구분한다.
    return output  # 사용자가 app에서 바로 받을 수 있도록 만든 통합문서 경로를 반환한다.


def run_experiment(project_dir: Path = PROJECT_DIR, calibration_target_fpr: float = CALIBRATION_FPR, review_fraction: float = REVIEW_FRACTION, progress_callback: Callable[[dict[str, Any]], None] | None = None, max_epochs: int = MAX_EPOCHS) -> dict[str, Any]:  # 공식 split 기반 normal-only fit부터 혼합 holdout inference와 Excel 작성까지 수행한다.
    global PROJECT_DIR, DATA_DIR, RESULTS_DIR, MODEL_DIR, RAW_ARCHIVE  # 호출자가 project copy를 지정해도 내부 경로가 해당 copy를 바라보게 한다.
    PROJECT_DIR = Path(project_dir).resolve()  # 최종 project root를 확정한다.
    DATA_DIR = PROJECT_DIR / "data" / "st_awfd"  # 공개 source archive 폴더를 현재 root에 맞춘다.
    RESULTS_DIR = PROJECT_DIR / "results" / "st_awfd"  # 결과 폴더를 현재 root에 맞춘다.
    MODEL_DIR = PROJECT_DIR / "models" / "st_awfd"  # 모델 폴더를 현재 root에 맞춘다.
    RAW_ARCHIVE = DATA_DIR / "D2.zip"  # D2 원본 압축파일을 지정한다.
    if not 0.01 <= review_fraction <= 0.50:  # 운영 review capacity scenario가 너무 작은/큰 값을 갖지 않게 막는다.
        raise ValueError("review_fraction은 0.01~0.50 사이로 지정해야 합니다.")  # 검토 비율이 최적 score threshold는 아니라고 설명한다.
    if not 0.01 <= calibration_target_fpr <= 0.20:  # normal reference false-alarm target을 제한한다.
        raise ValueError("calibration_target_fpr은 0.01~0.20 사이로 지정해야 합니다.")  # 사용자가 생각한 경보예산을 명시적으로 넘겨준다.
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)  # 처음 실행에서 결과 하위 폴더를 만든다.
    MODEL_DIR.mkdir(parents=True, exist_ok=True)  # 처음 실행에서 모델 하위 폴더를 만든다.
    set_reproducibility(SEED)  # CPU/GPU와 Python/NumPy 모델을 동일 seed로 맞춘다.
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # CUDA 3070 Ti가 탐지되면 GPU를 쓰고 그렇지 않으면 CPU로 동작한다.
    device_name = torch.cuda.get_device_name(0) if device.type == "cuda" else "CPU fallback"  # 화면과 JSON에서 실제 학습 장치 이름을 확인하게 한다.
    source = read_d2_source()  # 공식 D2 raw source를 schema 검사 후 읽는다.
    feature_columns = [column for column in source.columns if column.startswith("feature_")]  # anon sensor 열의 공식 순서를 보존한다.
    train_frame, calibration_frame, test_frame, manifest = split_official_normal_reference(source)  # 공개 is_test=0 정상-only train 구조와 heldout을 따른다.
    train_raw, train_labels, train_ids, train_metadata = resample_step_one(train_frame, feature_columns)  # 학습 신호만 먼저 wafer별 고정 길이로 변환한다.
    calibration_raw, calibration_labels, calibration_ids, calibration_metadata = resample_step_one(calibration_frame, feature_columns)  # control limit calibration에 쓸 정상 wafer를 변환한다.
    test_raw, test_labels, test_ids, test_metadata = resample_step_one(test_frame, feature_columns)  # 공식 mixed holdout을 추론용으로 변환한다.
    if np.any(train_labels != 0) or np.any(calibration_labels != 0):  # label은 split 프로토콜 점검에만 쓰고 이상 모델 학습에는 전달하지 않는다.
        raise ValueError("정상 reference train/calibration 집합에 target=1이 포함됐습니다.")  # anomaly contamination이 있을 때 설정값으로 숨기지 않는다.
    train_signal, scaled_others, scaling = normalize_with_training_normals(train_raw, [calibration_raw, test_raw])  # model scaler는 정상 train 구간에서만 추정한다.
    calibration_signal, test_signal = scaled_others  # train scaler를 동일하게 적용한 validation/test signal을 분리한다.
    train_summary = summarize_waveforms(train_signal)  # classical model input은 동일한 relative-time waveform에서 만든다.
    calibration_summary = summarize_waveforms(calibration_signal)  # normal-only calibration features를 만든다.
    test_summary = summarize_waveforms(test_signal)  # mixed holdout features는 score만 계산한다.
    summary_columns = [f"{sensor}_{statistic}" for sensor in feature_columns for statistic in ["mean", "std", "min", "max", "p10", "p90", "abs_peak", "start", "end", "slope"]]  # sensor ID와 시계열 요약 통계의 연결을 보존한다.
    robust_model = StandardScaler()  # one-class 기준선에 적용할 training-normal summary scaler를 만든다.
    robust_train_summary = robust_model.fit_transform(train_summary)  # 정상 train wafer에서만 기준선 통계를 적합한다.
    robust_calibration_summary = robust_model.transform(calibration_summary)  # 정상 validation/test에 같은 변환을 재사용한다.
    robust_test_summary = robust_model.transform(test_summary)  # unseen mixed holdout에 train scaler를 적용한다.
    svm_pipeline = Pipeline([("scale", StandardScaler()), ("ocsvm", OneClassSVM(kernel="rbf", gamma="scale", nu=0.05))])  # robust Z feature를 쓰는 One-Class SVM을 normal-only로 학습한다.
    svm_pipeline.fit(train_summary)  # label을 주지 않고 정상 reference feature distribution만 적합한다.
    forest = IsolationForest(n_estimators=300, max_samples="auto", max_features=1.0, contamination="auto", random_state=SEED, n_jobs=-1)  # 센서 통계 공간에서 정상으로부터 고립되는 point를 찾는다.
    forest.fit(train_summary)  # 정상 학습 sample만 기준으로 isolation tree들을 구축한다.
    robust_calibration_scores = np.max(np.abs(robust_calibration_summary), axis=1)  # calibration normal에서 각 sensor summary의 최대 표준편차 이탈을 계산한다.
    robust_test_scores = np.max(np.abs(robust_test_summary), axis=1)  # mixed holdout에서 동일한 rule의 excursion score를 계산한다.
    svm_calibration_scores = predict_scores(svm_pipeline, calibration_summary, "decision_function")  # 정상 validation의 One-Class SVM anomaly score를 계산한다.
    svm_test_scores = predict_scores(svm_pipeline, test_summary, "decision_function")  # official test의 One-Class SVM anomaly score를 계산한다.
    forest_calibration_scores = predict_scores(forest, calibration_summary, "score_samples")  # 정상 validation의 Isolation Forest anomaly score를 계산한다.
    forest_test_scores = predict_scores(forest, test_summary, "score_samples")  # official test의 Isolation Forest anomaly score를 계산한다.
    autoencoder, history_rows, best_epoch = fit_autoencoder(train_signal, calibration_signal, device, progress_callback, max_epochs=max_epochs)  # 정답 label 없이 정상 파형 재구성 CNN을 실제 GPU에서 epoch 학습한다.
    auto_calibration_scores, calibration_sensor_residuals = reconstruction_scores(autoencoder, calibration_signal, device)  # 정상 validation의 재구성 error를 threshold calibration에 쓴다.
    auto_test_scores, test_sensor_residuals = reconstruction_scores(autoencoder, test_signal, device)  # 공식 mixed holdout waveform을 학습된 encoder-decoder로 추론한다.
    fusion_calibration_scores = np.column_stack([pd.Series(scores).rank(method="average", pct=True).to_numpy() for scores in [robust_calibration_scores, svm_calibration_scores, forest_calibration_scores, auto_calibration_scores]]).mean(axis=1)  # calibration 내부 순위로 detector 점수 스케일을 정규화한다.
    fusion_test_scores = np.column_stack([empirical_cdf(reference, current) for reference, current in zip([robust_calibration_scores, svm_calibration_scores, forest_calibration_scores, auto_calibration_scores], [robust_test_scores, svm_test_scores, forest_test_scores, auto_test_scores])]).mean(axis=1)  # test 점수는 각각 calibration 정상의 ECDF에 넣어 test 자체 순위를 threshold에 잘못 대지 않게 한다.
    calibration_scores = {"RobustSensorLimit": robust_calibration_scores, "OneClassSVM": svm_calibration_scores, "IsolationForest": forest_calibration_scores, "TemporalAutoencoder_GPU": auto_calibration_scores, "RankFusionEnsemble": fusion_calibration_scores}  # 정상 validation만 보고 각 detector limit을 계산할 map을 만든다.
    test_scores = {"RobustSensorLimit": robust_test_scores, "OneClassSVM": svm_test_scores, "IsolationForest": forest_test_scores, "TemporalAutoencoder_GPU": auto_test_scores, "RankFusionEnsemble": fusion_test_scores}  # official test score를 알고리즘 이름과 함께 모은다.
    thresholds = {name: calibrate_normal_limit(scores, calibration_target_fpr) for name, scores in calibration_scores.items()}  # target normal false alarm rate를 정상 validation score quantile로 각 model에 적용한다.
    model_rows: list[dict[str, Any]] = []  # test audit를 비교 가능한 row별 dictionary로 모은다.
    for name, scores in test_scores.items():  # 모든 candidate detector에 동일 평가 함수를 적용한다.
        metric = evaluate_anomaly_scores(test_labels, scores, thresholds[name], review_fraction, calibration_scores[name])  # threshold는 validation에서 잠갔고 test label은 이제 감사 metric에서만 사용한다.
        model_rows.append({"model": name, "calibration_normal_wafers": len(calibration_labels), "threshold_calibration_target_fpr": calibration_target_fpr, "calibration_normal_alarm_rate": metric["calibration_normal_false_alarm_rate"], "threshold_score": thresholds[name], "holdout_wafers": metric["n_wafers"], "holdout_anomalies": metric["n_anomalous"], "holdout_prevalence": metric["anomaly_prevalence"], "holdout_average_precision": metric["average_precision"], "holdout_roc_auc": metric["roc_auc"], "threshold_true_positive": metric["true_positive"], "threshold_false_positive": metric["false_positive"], "threshold_false_negative": metric["false_negative"], "threshold_true_negative": metric["true_negative"], "holdout_precision_at_limit": metric["precision_at_normal_limit"], "holdout_recall_at_limit": metric["recall_at_normal_limit"], "holdout_test_normal_fpr": metric["test_normal_false_alarm_rate"], "holdout_test_normal_fpr_ci_lower": metric["test_normal_fpr_wilson_95pct"][0], "holdout_test_normal_fpr_ci_upper": metric["test_normal_fpr_wilson_95pct"][1], "holdout_alert_fraction": metric["test_alert_fraction"], "review_queue_size_at_capacity": metric["review_queue_capacity"], "review_queue_anomalies_captured": metric["review_queue_true_positives"], "review_queue_recall": metric["recall_at_review_capacity"], "review_queue_precision": metric["precision_at_review_capacity"]})  # calibration·검증·alert rate와 고정용량 queue를 각각 비교한다.
    model_table = pd.DataFrame(model_rows).sort_values("holdout_average_precision", ascending=False).reset_index(drop=True)  # 요약 표는 결과 해석을 돕도록 AP 내림차순 정렬한다.
    primary_name = "TemporalAutoencoder_GPU"  # 우수 결과 사후 선택을 피하고 temporal CNN을 사전에 비교 기준 후보로 고정한다.
    primary_metrics = evaluate_anomaly_scores(test_labels, test_scores[primary_name], thresholds[primary_name], review_fraction, calibration_scores[primary_name])  # 최종 설명할 모델의 test 결과와 calibration 통계를 계산한다.
    primary_metrics["test_normal_false_alarm_inflation_vs_target"] = float(primary_metrics["test_normal_false_alarm_rate"] / calibration_target_fpr)  # 정상 holdout false alarm이 validation 목표보다 몇 배 커졌는지 계산한다.
    calibration_rows: list[dict[str, Any]] = []  # validation normal과 official test normal의 score 분포를 직접 비교한다.
    for name in test_scores:  # 각 detector에 동일 drift audit 통계를 계산한다.
        normal_scores = test_scores[name][test_labels == 0]  # label은 사후 감사에서만 사용해 official test normal group을 확인한다.
        anomaly_values = test_scores[name][test_labels == 1]  # benchmark label을 이용해 anomaly score 분포를 사후 요약한다.
        calibration_rows.append({"model": name, "validation_normal_count": len(calibration_scores[name]), "validation_normal_target_fpr": calibration_target_fpr, "validation_normal_observed_fpr": float(np.mean(calibration_scores[name] > thresholds[name])), "validation_normal_score_q50": float(np.quantile(calibration_scores[name], 0.50)), "validation_normal_score_q95": float(np.quantile(calibration_scores[name], 0.95)), "validation_threshold": thresholds[name], "official_test_normal_count": len(normal_scores), "official_test_normal_score_q50": float(np.quantile(normal_scores, 0.50)), "official_test_normal_score_q95": float(np.quantile(normal_scores, 0.95)), "official_test_normal_exceedance_rate": float(np.mean(normal_scores > thresholds[name])), "official_test_anomaly_count": len(anomaly_values), "official_test_anomaly_score_q50": float(np.quantile(anomaly_values, 0.50)), "official_test_anomaly_score_q95": float(np.quantile(anomaly_values, 0.95)), "interpretation": "retrospective domain-shift audit; test labels were not used to recalibrate threshold"})  # score level과 limit exceedance가 어느 집합에서 바뀌었는지 저장한다.
    calibration_audit = pd.DataFrame(calibration_rows)  # calibration drift table을 workbook/CSV가 읽을 수 있게 변환한다.
    calibration_audit.to_csv(RESULTS_DIR / "st_awfd_calibration_drift_audit.csv", index=False, encoding="utf-8-sig")  # test 정상 score 이동을 다음 공정 분석에 쓸 수 있게 저장한다.
    test_order = np.argsort(-test_scores[primary_name], kind="mergesort")  # human review queue에서 복원 error가 큰 wafer부터 배열한다.
    ranks = np.empty(len(test_ids), dtype=np.int64)  # 원본 lot group 순서에 맞는 rank column을 저장할 버퍼다.
    ranks[test_order] = np.arange(1, len(test_ids) + 1)  # 높은 anomaly score가 우선 검토되도록 1부터 rank를 붙인다.
    queue_size = max(1, math.ceil(len(test_ids) * review_fraction))  # 기준 test example의 상위 10% 후보 수를 계산한다.
    queue = pd.DataFrame({"MaterialID": test_ids, "step_id_used": STEP_ID, "anomaly_score": test_scores[primary_name], "normal_reference_limit": thresholds[primary_name], "above_normal_reference_limit": test_scores[primary_name] > thresholds[primary_name], "review_rank": ranks, "review_candidate_at_capacity": ranks <= queue_size, "step_sample_count": test_metadata["step_sample_count"].to_numpy(), "step_duration_normalized": test_metadata["step_duration_normalized"].to_numpy()}).sort_values("review_rank").reset_index(drop=True)  # queue 결과에서 정답 label을 완전히 제외한다.
    audit = pd.DataFrame({"MaterialID": test_ids, "target_for_retrospective_audit": test_labels, "source_is_test": test_metadata["source_is_test"].to_numpy(), "TemporalAutoencoder_GPU_score": auto_test_scores, "RobustSensorLimit_score": robust_test_scores, "OneClassSVM_score": svm_test_scores, "IsolationForest_score": forest_test_scores, "RankFusionEnsemble_score": fusion_test_scores, "TemporalAutoencoder_alarm": auto_test_scores > thresholds[primary_name], "TemporalAutoencoder_review_rank": ranks})  # source target와 model scores는 오프라인 test 감사 전용 파일에만 저장한다.
    residual_rows: list[dict[str, Any]] = []  # sensor별 reconstruction residue를 PE가 확인할 단서표로 집계한다.
    for index, sensor in enumerate(feature_columns):  # 익명 channel별로 정상/이상 holdout에서 재구성 차이를 비교한다.
        normal_error = test_sensor_residuals[test_labels == 0, index]  # official test 중 정상 wafer의 센서 residue만 취한다.
        abnormal_error = test_sensor_residuals[test_labels == 1, index]  # official test 중 label 이상 wafer의 sensor residue만 취한다.
        residual_rows.append({"step_id": STEP_ID, "sensor_id": sensor, "mean_squared_reconstruction_error_normal_test": float(normal_error.mean()), "mean_squared_reconstruction_error_abnormal_test": float(abnormal_error.mean()), "abnormal_minus_normal_error": float(abnormal_error.mean() - normal_error.mean()), "interpretation": "test label로 사후 산출한 sensor-level 연관 단서; 물리적 root cause 증명 아님"})  # test label은 training에 쓰지 않고 retrospective explanation에만 쓴다.
    residual_table = pd.DataFrame(residual_rows).sort_values("abnormal_minus_normal_error", ascending=False).reset_index(drop=True)  # anomaly residue 차이가 큰 익명 sensor를 위에 둔다.
    history = pd.DataFrame(history_rows)  # epoch마다 측정한 normal MSE를 표로 바꾼다.
    history.to_csv(RESULTS_DIR / "st_awfd_training_history.csv", index=False, encoding="utf-8-sig")  # 외부 notebook에서 학습 curve를 다시 그릴 원자료를 저장한다.
    model_table.to_csv(RESULTS_DIR / "st_awfd_model_comparison.csv", index=False, encoding="utf-8-sig")  # classical/deep/ensemble 결과를 별도 테이블로 보존한다.
    queue.to_csv(RESULTS_DIR / "st_awfd_inference_review_queue.csv", index=False, encoding="utf-8-sig")  # 사람이 실제로 받는 label-free scoring queue를 저장한다.
    audit.to_csv(RESULTS_DIR / "st_awfd_holdout_audit.csv", index=False, encoding="utf-8-sig")  # 공개 test 정답은 별도 offline audit에 보존한다.
    residual_table.to_csv(RESULTS_DIR / "st_awfd_sensor_residual_audit.csv", index=False, encoding="utf-8-sig")  # waveform 재구성 오차로 얻은 사후 sensor 단서를 저장한다.
    manifest.to_csv(RESULTS_DIR / "st_awfd_official_split_manifest.csv", index=False, encoding="utf-8-sig")  # 각 lot group ID의 normal fit/calibration/test partition을 보존한다.
    checkpoint_path = MODEL_DIR / "st_awfd_step1_temporal_autoencoder.pt"  # 모델 weights와 전처리 reference를 담을 파일 경로를 만든다.
    torch.save({"state_dict": autoencoder.state_dict(), "feature_columns": feature_columns, "step_id": STEP_ID, "sequence_length": SEQUENCE_LENGTH, "scaling": scaling, "normal_reference_limit": thresholds[primary_name], "calibration_target_fpr": calibration_target_fpr, "best_epoch": best_epoch, "seed": SEED}, checkpoint_path)  # 다음 CSV 점수화에 필요한 model/scaler/threshold를 함께 직렬화한다.
    joblib.dump({"scaler": robust_model, "detector": svm_pipeline}, MODEL_DIR / "st_awfd_oneclass_svm_reference.joblib")  # SVM 재현에 필요한 정규화기와 detector를 보존한다.
    joblib.dump(forest, MODEL_DIR / "st_awfd_isolation_forest_reference.joblib")  # tree baseline의 학습된 forest를 보존한다.
    device_fields = {"device": str(device), "device_name": device_name, "cuda_available": bool(torch.cuda.is_available()), "torch_version": torch.__version__}  # 실제 학습 runtime 정보를 기록한다.
    split_counts = source.groupby(["is_test", "target"])["MaterialID"].nunique().to_dict()  # public official split 안의 class 구성(정상/이상)을 lot group 단위로 집계한다.
    target_counts = source.groupby("MaterialID")["target"].first().value_counts().sort_index().to_dict()  # 전체 source의 lot group label 비율을 기록한다.
    summary = {  # JSON root keys를 여러 줄로 써서 method와 provenance를 추적한다.
        "dataset": {"name": "STMicroelectronics ST-AWFD D2", "source_url": "https://github.com/STMicroelectronics/ST-AWFD", "original_paper": "https://doi.org/10.3390/s21165465", "license": "CC BY-NC-SA 4.0", "archive_name": RAW_ARCHIVE.name, "archive_bytes": RAW_ARCHIVE.stat().st_size, "archive_sha256": sha256_file(RAW_ARCHIVE), "row_count": int(len(source)), "material_id_count": int(source["MaterialID"].nunique()), "normal_anomalous_material_id_counts": {str(key): int(value) for key, value in target_counts.items()}, "official_is_test_by_target_material_id_counts": {f"is_test={split},target={label}": int(count) for (split, label), count in split_counts.items()}, "official_train_normal_wafers": int(split_counts.get((0, 0), 0)), "official_test_normal_wafers": int(split_counts.get((1, 0), 0)), "official_test_anomalous_wafers": int(split_counts.get((1, 1), 0)), "official_test_wafers": int(sum(count for (split, _), count in split_counts.items() if split == 1)), "feature_columns": feature_columns},  # D2 공식 원본, class count, split별 정답, license/hash를 기록한다.
        "experiment": {"task": "Normal-only anomaly detection from MaterialID Step 1 trace", "split_policy": "source is_test=0 as normal pool; group-split 80% normal fit / 20% normal threshold calibration; source is_test=1 is locked mixed test", "step_id": STEP_ID, "sequence_length": SEQUENCE_LENGTH, "seed": SEED, "review_fraction": review_fraction, "review_fraction_meaning": "top-k per batch review capacity; not a model threshold", "calibration_target_fpr": calibration_target_fpr, "calibration_limit_definition": "higher empirical quantile of normal-only validation scores; threshold fixed before mixed holdout evaluation", "preprocessing": "per-wafer Step 1 relative-time interpolation; per-sensor scale fit on training normals only; MaterialID/is_test/target excluded from model inputs", "primary_model": "small 1D convolutional denoising autoencoder trained only on normal traces with MSE reconstruction objective", "best_epoch": best_epoch, "calibration_normal_wafers": int(len(calibration_ids)), "primary_holdout_metrics": primary_metrics, "thresholds": thresholds, "calibration_thresholds": thresholds, "model_comparison": model_rows, "known_limits": ["Dataset was released in a 2021 paper but its sensor collection date is not published.", "Dataset is real ST semiconductor manufacturing telemetry but not SK hynix or memory product data.", "All sensor values were z-score normalized before publication; source scaler's original fit boundary is not disclosed.", "feature names are anonymous; physical sensor/tool/chamber/process mapping is unavailable.", "Step 1 is an earlier process stage by dataset ordering; actual measurement-to-final-outcome lead time is not specified.", "ROC/AP and recall are benchmark estimates; ST-AWFD's test is anomaly-enriched, so precision and alert fraction do not represent fab prevalence.", "5% control-limit target is a chosen normal reference quantile, not a factory SPC/FDC limit.", "sensor error association is not causal root-cause evidence; final yield uplift was not measured.", "random split within official normal pool is not cross-time, cross-product, cross-tool, or cross-fab validation."]},  # 실제 test 결과와 각 점수·운영 주장의 범위를 분리해 둔다.
        "device": device_fields,  # RTX/CUDA 상태를 결과에 연결한다.
    }  # 전체 실험 provenance를 마무리한다.
    summary_path = RESULTS_DIR / "st_awfd_run_summary.json"  # app/notebook이 다시 읽을 JSON 경로를 만든다.
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")  # JSON 표준형으로 실제 run 요약을 저장한다.
    make_charts(history, model_table, test_scores, test_labels, thresholds)  # 실제 학습 곡선과 official test 결과를 시각화한다.
    workbook_path, export_status = optional_export(lambda: make_excel_report(summary, history, model_table, queue, audit, residual_table, calibration_audit, manifest))
    summary["workbook_export"] = export_status
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"summary": summary, "history": history, "model_comparison": model_table, "queue": queue, "audit": audit, "sensor_residuals": residual_table, "calibration_audit": calibration_audit, "manifest": manifest, "excel_path": workbook_path, "model_path": checkpoint_path, "device": device}  # notebook/app에 전체 결과와 저장 경로를 반환한다.


def make_charts(history: pd.DataFrame, model_table: pd.DataFrame, scores: dict[str, np.ndarray], labels: np.ndarray, thresholds: dict[str, float]) -> None:  # 실제 학습 관측치 및 holdout score를 그림 파일로 남긴다.
    figure, axis = plt.subplots(figsize=(9, 4.5))  # train/validation MSE 두 곡선을 비교할 가로 canvas를 만든다.
    axis.plot(history["epoch"], history["train_denoising_mse"], label="Train normal denoising MSE", color="#255c85")  # 정상 waveform 재구성 학습 loss를 표시한다.
    axis.plot(history["epoch"], history["validation_normal_mse"], label="Validation normal MSE", color="#d87927")  # 정상 calibration 성능 곡선을 표시한다.
    axis.set_xlabel("Epoch")  # x축이 실제 업데이트 회차임을 밝힌다.
    axis.set_ylabel("Mean squared reconstruction error")  # y축 단위가 sensor 표준화 공간의 MSE임을 밝힌다.
    axis.set_title("ST-AWFD D2 | normal-only Step 1 temporal autoencoder")  # 모델이 정상-only로 학습됐음을 명시한다.
    axis.grid(alpha=0.2)  # 반복 측정값을 읽기 쉽게 돕는다.
    axis.legend(frameon=False)  # 각 두 곡선의 의미를 구별한다.
    figure.tight_layout()  # 긴 제목/축 label이 그림 밖으로 나가지 않게 한다.
    figure.savefig(RESULTS_DIR / "st_awfd_epoch_curve.png", dpi=180)  # PPT 및 Excel 삽입용 실측 epoch 차트를 저장한다.
    plt.close(figure)  # 반복 실행 메모리를 반환한다.
    ordered = model_table.sort_values("holdout_average_precision", ascending=True)  # 실제 test 순위 지표를 낮은 쪽부터 그린다.
    figure, axis = plt.subplots(figsize=(9, 4.5))  # detector 비교 차트를 만든다.
    axis.bar(ordered["model"], ordered["holdout_average_precision"], color=["#d87927" if name == "TemporalAutoencoder_GPU" else "#738b9b" for name in ordered["model"]])  # primary neural model과 통계 기준선을 구별한다.
    axis.axhline(float(labels.mean()), linestyle="--", color="#555555", label="Random ranking baseline = test prevalence")  # anomaly-enriched test prevalence를 무작위 AP 기준으로 보인다.
    axis.set_ylabel("Official mixed-test average precision")  # 축에서 데이터 역할과 metric을 구체적으로 밝힌다.
    axis.set_title("ST-AWFD D2 | official mixed test anomaly ranking")  # 결과 데이터셋과 측정 목적을 표시한다.
    axis.grid(axis="y", alpha=0.2)  # 비교할 때 유용한 약한 눈금을 넣는다.
    axis.legend(frameon=False)  # 기준선의 의미를 독자가 확인하게 한다.
    figure.tight_layout()  # chart labels를 canvas 내부에 둔다.
    figure.savefig(RESULTS_DIR / "st_awfd_model_comparison.png", dpi=180)  # 실제 모델 비교 결과를 파일로 저장한다.
    plt.close(figure)  # matplotlib 리소스를 반환한다.
    anomaly_scores = scores["TemporalAutoencoder_GPU"]  # primary model의 공식 mixed holdout 점수만 본다.
    figure, axis = plt.subplots(figsize=(8.5, 4.5))  # 실제 abnormal/normal 분포와 limit을 비교할 canvas를 만든다.
    axis.hist(anomaly_scores[labels == 0], bins=35, alpha=0.7, density=True, label="Official test normal", color="#3c8d7a")  # label-normal group의 score 분포를 감사한다.
    axis.hist(anomaly_scores[labels == 1], bins=35, alpha=0.55, density=True, label="Official test anomaly", color="#c95745")  # label-anomaly group의 score 분포를 감사한다.
    axis.axvline(thresholds["TemporalAutoencoder_GPU"], color="#252525", linestyle="--", label="Threshold from normal validation only")  # test를 보지 않고 고정된 validation limit을 표시한다.
    axis.set_xlabel("Reconstruction anomaly score, not probability")  # output이 calibration 된 failure probability가 아니라고 적는다.
    axis.set_ylabel("Density")  # 정규화 histogram 값이 count가 아니라 밀도임을 밝힌다.
    axis.set_title("Locked mixed holdout score audit")  # 사후 평가 분포라는 맥락을 표시한다.
    axis.legend(frameon=False)  # threshold와 class curve의 의미를 구분한다.
    axis.grid(alpha=0.2)  # 서로 겹치는 밀도 curve를 해석하기 쉽게 한다.
    figure.tight_layout()  # labels가 잘리지 않도록 조정한다.
    figure.savefig(RESULTS_DIR / "st_awfd_holdout_score_distribution.png", dpi=180)  # 실제 모델 결과 분포를 보고서용으로 저장한다.
    plt.close(figure)  # plotting state를 정리한다.


if __name__ == "__main__":  # 모듈을 직접 실행한 경우에만 한 번의 원클릭 benchmark를 시작한다.
    output = run_experiment()  # RTX 3070 Ti가 있으면 normal-only epoch 학습과 official test inference를 실제 실행한다.
    print(json.dumps(output["summary"], ensure_ascii=False, indent=2))  # terminal에 재현 가능한 수치·출처·제한을 보여준다.
