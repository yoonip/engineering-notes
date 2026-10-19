"""Strict-causal Transformer의 구조·Gaussian loss·고정 모델 추론."""
from __future__ import annotations
import math
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F

HORIZONS = (1, 2, 4, 8)  # 한 시점, 짧은 구간, 중간 구간, 더 긴 구간 변화까지 직접 예측한다.


D_MODEL = 64  # hidden feature 폭을 공개 데이터의 표본 수에 맞는 작은 규모로 제한한다.


N_HEADS = 4  # attention을 네 관점으로 나누는 head 수다.


N_LAYERS = 3  # 서로 다른 길이의 관계를 순차적으로 학습할 Transformer block 수다.


FFN_DIM = 128  # attention 이후 token별 비선형 변환의 중간 폭이다.


KERNEL_SIZE = 5  # local sensor transient를 임베딩할 causal convolution 폭이다.


DROPOUT = 0.10  # 표본이 많지 않은 데이터에서 작은 regularization을 준다.


LOG_SIGMA_MIN = -3.0  # Gaussian 표준편차의 하한을 둬 수치적 발산과 과신을 막는다.


LOG_SIGMA_MAX = 2.0  # Gaussian 표준편차의 상한을 둬 불필요한 분산 회피를 막는다.


class StrictCausalConvEmbedding(nn.Module):  # 현재 시점까지의 신호만 보는 왼쪽 padding 1D convolution이다.
    def __init__(self, feature_count: int, d_model: int, kernel_size: int) -> None:  # 익명 sensor 수와 임베딩 크기로 convolution을 만든다.
        super().__init__()  # nn.Module의 parameter 관리 기능을 초기화한다.
        self.left_padding = kernel_size - 1  # 길이 보존을 위해 과거 방향으로만 넣을 padding 개수를 계산한다.
        self.conv = nn.Conv1d(feature_count, d_model, kernel_size=kernel_size, padding=0)  # 양쪽 자동 padding을 끄고 엄격한 causal 출력만 만든다.
        self.norm = nn.LayerNorm(d_model)  # feature 축을 정규화해 attention 입력의 수치 범위를 안정시킨다.
        self.activation = nn.GELU()  # 센서 국소 파형을 부드러운 비선형 특징으로 변환한다.

    def forward(self, values: torch.Tensor) -> torch.Tensor:  # [batch, sensors, time]을 [batch, time, hidden]으로 바꾼다.
        left_padded = F.pad(values, (self.left_padding, 0))  # 미래 방향에는 padding을 넣지 않아 t 토큰이 x[t+1:]를 보지 못하게 한다.
        projected = self.conv(left_padded).transpose(1, 2)  # 인과 convolution으로 각 시점의 hidden token을 만든다.
        return self.activation(self.norm(projected))  # normalized GELU embedding을 causal attention stack에 전달한다.


class CausalMultiHorizonGPT(nn.Module):  # decoder-only causal Transformer의 원리를 공정 trace 예측에 적용한다.
    def __init__(self, feature_count: int, sequence_length: int) -> None:  # sensor 수와 최대 trace 길이로 모형을 구성한다.
        super().__init__()  # PyTorch 모듈의 자동 parameter 등록을 시작한다.
        self.feature_count = feature_count  # 예측 헤드의 sensor 축 크기를 저장한다.
        self.sequence_length = sequence_length  # positional embedding의 최대 길이를 저장한다.
        self.horizons = HORIZONS  # 학습·추론에 사용할 예측 거리 tuple을 보관한다.
        self.embedding = StrictCausalConvEmbedding(feature_count, D_MODEL, KERNEL_SIZE)  # causal local filter로 수치 token을 임베딩한다.
        self.position = nn.Parameter(torch.empty(1, sequence_length, D_MODEL))  # 공정 상대시간 순서를 표현하는 학습 가능한 위치 벡터다.
        nn.init.normal_(self.position, mean=0.0, std=0.02)  # position vector를 작은 분산으로 초기화해 초반 학습을 안정화한다.
        block = nn.TransformerEncoderLayer(d_model=D_MODEL, nhead=N_HEADS, dim_feedforward=FFN_DIM, dropout=DROPOUT, activation="gelu", batch_first=True, norm_first=True)  # causal mask와 함께 쓸 pre-norm decoder형 Transformer block이다.
        self.decoder = nn.TransformerEncoder(block, num_layers=N_LAYERS, enable_nested_tensor=False)  # 같은 causal attention block을 세 층 쌓는다.
        self.output = nn.Linear(D_MODEL, len(self.horizons) * feature_count * 2)  # 각 horizon·sensor별 예측 평균과 로그 표준편차를 출력한다.

    def forward(self, history: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:  # 과거 history에서 각 시점별 미래 sensor 분포를 예측한다.
        batch_size, _, time_count = history.shape  # 출력 텐서 reshape에 필요한 batch/time 차원을 얻는다.
        if time_count > self.sequence_length:  # positional embedding 범위를 넘어서는 추론을 조기에 막는다.
            raise ValueError(f"입력 시점 {time_count}개가 모델 최대 {self.sequence_length}개보다 깁니다.")  # 오류 원인을 사용자가 바로 볼 수 있게 한다.
        hidden = self.embedding(history)  # strict-causal convolution이 각 과거 시점을 hidden token으로 바꾼다.
        hidden = hidden + self.position[:, :time_count, :]  # 모든 token에 해당하는 상대시간 위치 정보를 더한다.
        future_block = torch.triu(torch.ones(time_count, time_count, device=history.device, dtype=torch.bool), diagonal=1)  # 위쪽 삼각형을 막아 t가 t+1 이후 hidden token에 접근하지 못하게 한다.
        hidden = self.decoder(hidden, mask=future_block)  # 과거와 현재 token만 누적 참조하는 decoder-only attention을 실행한다.
        raw = self.output(hidden).view(batch_size, time_count, len(self.horizons), self.feature_count, 2)  # 출력 차원을 시간·예측거리·센서·분포 parameter로 분해한다.
        mean = raw[..., 0]  # 연속 센서값의 예측 평균을 분리한다.
        log_sigma = raw[..., 1].clamp(LOG_SIGMA_MIN, LOG_SIGMA_MAX)  # 예측 불확실성 log standard deviation을 제한한다.
        return mean, log_sigma  # 다중 거리의 평균과 데이터 의존 불확실성을 반환한다.


def gaussian_nll(target: torch.Tensor, mean: torch.Tensor, log_sigma: torch.Tensor) -> torch.Tensor:  # 연속 센서값의 예측 불확실성까지 학습하는 Gaussian negative log-likelihood다.
    standardized_error = (target - mean) * torch.exp(-log_sigma)  # 편차를 추정 표준편차로 나누어 상대 surprise를 계산한다.
    return 0.5 * standardized_error.square() + log_sigma + 0.5 * math.log(2.0 * math.pi)  # 정규화 상수까지 포함해 정확한 연속 Gaussian negative log-likelihood를 계산한다.


def multi_horizon_loss(model: CausalMultiHorizonGPT, signals: torch.Tensor) -> torch.Tensor:  # 여러 lead time에서 과거만으로 값을 예측하는 평균 NLL을 계산한다.
    history = signals[:, :, :-1]  # 마지막 값은 목표로 남기고 이전 값들만 모델 입력으로 둔다.
    mean, log_sigma = model(history)  # 모든 valid input 시점의 horizon별 분포를 산출한다.
    horizon_losses: list[torch.Tensor] = []  # 거리별 loss를 같은 비중으로 합산할 buffer다.
    for horizon_index, horizon in enumerate(model.horizons):  # 각 미래 lead time의 독립 loss를 계산한다.
        valid_length = history.shape[-1] - (horizon - 1)  # trace 끝을 넘어 예측하는 시점을 제거한다.
        target = signals[:, :, horizon : horizon + valid_length].transpose(1, 2)  # 실제 x[t+h]와 시점 t의 forecast를 맞춘다.
        horizon_mean = mean[:, :valid_length, horizon_index]  # 미래 target이 존재하는 과거 token까지만 잘라낸다.
        horizon_log_sigma = log_sigma[:, :valid_length, horizon_index]  # 같은 valid 구간의 불확실성만 사용한다.
        horizon_losses.append(gaussian_nll(target, horizon_mean, horizon_log_sigma).mean())  # sensor·lot group·시점을 평균해 거리별 NLL을 만든다.
    return torch.stack(horizon_losses).mean()  # 한 걸음 예측만 과도하게 우세하지 않도록 네 거리를 동일 가중 합산한다.


def score_signals(model: CausalMultiHorizonGPT, signals: np.ndarray, device: torch.device, batch_size: int = 64) -> tuple[np.ndarray, np.ndarray, np.ndarray]:  # trace, sensor attribution, horizon contribution을 계산한다.
    model.eval()  # dropout 등을 끄고 학습 완료된 고정 parameter로 추론한다.
    total_scores: list[np.ndarray] = []  # 각 lot의 결합 surprise score를 저장한다.
    sensor_scores: list[np.ndarray] = []  # feature_1..20 별 평균 surprise를 담는다.
    horizon_scores: list[np.ndarray] = []  # h=1,2,4,8별 평균 surprise를 담는다.
    with torch.no_grad():  # 역전파 gradient를 저장하지 않아 GPU memory와 시간을 아낀다.
        for start in range(0, len(signals), batch_size):  # 많은 lot을 inference batch로 나누어 처리한다.
            block = torch.from_numpy(signals[start : start + batch_size]).to(device)  # 현재 batch를 CUDA 또는 CPU에 올린다.
            mean, log_sigma = model(block[:, :, :-1])  # causal context는 과거 입력뿐이고 trace 마지막 값은 각 horizon target에 포함될 수 있다.
            by_horizon: list[torch.Tensor] = []  # horizon별 [batch, sensor] negative log-likelihood를 쌓는다.
            for horizon_index, horizon in enumerate(model.horizons):  # 거리별 score를 독립 집계한다.
                valid_length = block.shape[-1] - horizon  # 입력 위치 t에서 실제 t+h 값이 있는 개수를 센다.
                target = block[:, :, horizon : horizon + valid_length].transpose(1, 2)  # h-step forecast target과 시점 정렬을 일치시킨다.
                mean_h = mean[:, :valid_length, horizon_index]  # forecast horizon과 target time을 맞춘 예측평균이다.
                log_sigma_h = log_sigma[:, :valid_length, horizon_index]  # 해당 거리의 추정 uncertainty다.
                nll = gaussian_nll(target, mean_h, log_sigma_h)  # sensor/time별 예측 surprise를 계산한다.
                by_horizon.append(nll.mean(dim=1))  # 시간축 평균으로 trace×sensor 점수를 만든다.
            horizon_tensor = torch.stack(by_horizon, dim=1)  # [batch, horizon, sensor] attribution matrix로 만든다.
            sensor_tensor = horizon_tensor.mean(dim=1)  # 네 prediction distance를 동일 가중해 sensor contribution으로 축약한다.
            total_tensor = sensor_tensor.mean(dim=1)  # feature scale이 동일 표준화되어 있어 sensor 평균을 lot score로 쓴다.
            total_scores.append(total_tensor.cpu().numpy())  # GPU 결과만 CPU NumPy로 옮겨 파일/통계 계산에 쓴다.
            sensor_scores.append(sensor_tensor.cpu().numpy())  # 익명 channel별 추론 결과를 보존한다.
            horizon_scores.append(horizon_tensor.mean(dim=2).cpu().numpy())  # horizon별 추론 결과를 보존한다.
    return np.concatenate(total_scores), np.concatenate(sensor_scores), np.concatenate(horizon_scores)  # 모든 batch를 원래 ID 순으로 결합한다.


def causal_invariance_audit(model: CausalMultiHorizonGPT, signal: np.ndarray, device: torch.device, cutoff: int = 24) -> dict[str, float | bool]:  # 현재 이후 입력을 바꿔도 cutoff의 forecast가 바뀌지 않는지 수치 검증한다.
    model.eval()  # dropout을 끄고 deterministic inference를 수행한다.
    prefix = torch.from_numpy(signal[None, :, :-1]).float().to(device)  # 실제 예측에서 모델이 보는 입력 trace 하나를 만든다.
    altered = prefix.clone()  # 원래 입력을 보존한 채 비교용 tensor를 복사한다.
    altered[:, :, cutoff + 1 :] += 3.0  # cutoff 이후 구간에만 큰 변화를 넣어 미래 누출 여부를 살핀다.
    with torch.no_grad():  # 구조 검증에서는 gradient가 필요하지 않다.
        original_mean, original_log_sigma = model(prefix)  # 원래 trace에서 모든 horizon 예측을 산출한다.
        altered_mean, altered_log_sigma = model(altered)  # 미래만 변형한 trace에서 다시 예측한다.
    mean_delta = float((original_mean[:, cutoff] - altered_mean[:, cutoff]).abs().max().cpu())  # cutoff 예측의 sensor/horizon mean 차이 최댓값이다.
    sigma_delta = float((original_log_sigma[:, cutoff] - altered_log_sigma[:, cutoff]).abs().max().cpu())  # 같은 위치의 uncertainty 차이 최댓값이다.
    return {"future_perturbation_cutoff_index": int(cutoff), "future_change_magnitude": 3.0, "max_forecast_mean_delta_at_cutoff": mean_delta, "max_log_sigma_delta_at_cutoff": sigma_delta, "passes_strict_causal_invariance": bool(mean_delta < 1e-6 and sigma_delta < 1e-6)}  # 미래에 민감하지 않은지 증거를 manifest에 기록한다.
