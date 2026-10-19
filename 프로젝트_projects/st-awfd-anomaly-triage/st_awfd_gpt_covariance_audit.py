# -*- coding: utf-8 -*-  # 한국어 해설 주석을 Windows와 Jupyter에서 동일하게 읽는다.
# 고정된 strict GPT의 센서 간 잔차 상관관계를 반영하는 사전 정책 탐색 실험이다.  # 새 Transformer 학습이나 실제 양산 수율 측정은 수행하지 않는다.
from __future__ import annotations  # 최신 타입 표기를 선언 시점에 평가하지 않도록 한다.
import hashlib  # 사용한 checkpoint가 바뀌지 않았음을 파일 hash로 확인한다.
import json  # 정책, 결과와 한계를 사람이 읽을 수 있는 JSON으로 남긴다.
import time  # 실제 GPU forward 시간과 전체 실행 시간을 측정한다.
from datetime import datetime, timezone  # holdout 점수 계산 전 정책 저장 시각을 UTC로 기록한다.
from pathlib import Path  # 현재 스크립트 기준 경로로 다른 실행 위치에서도 재현한다.
from typing import Any  # JSON 결과와 추정기 목록의 타입을 표현한다.
import matplotlib  # GUI가 없어도 결과 그림을 저장할 backend를 지정한다.
matplotlib.use("Agg")  # 터미널 실행에서 별도 그림 창을 열지 않는다.
import matplotlib.pyplot as plt  # 점수 분포와 운영 지표 비교 그림을 만든다.
import numpy as np  # 공분산, Mahalanobis 잔차 에너지와 점수표를 계산한다.
import pandas as pd  # 정상 reference와 holdout 감사 결과 CSV를 작성한다.
import torch  # 저장된 strict GPT를 RTX GPU에서 실제 forward 한다.
from sklearn.covariance import LedoitWolf  # 역행렬이 불안정해지지 않게 공분산을 자동 shrinkage 한다.
import st_awfd_causal_gpt_multihorizon as gpt  # 완료된 모델 구조, 동일 분할과 평가 함수를 재사용한다.

PROJECT_DIR = Path(__file__).resolve().parent  # 외부 working directory에 의존하지 않는 project root다.
RESULT_DIR = PROJECT_DIR / "results" / "st_awfd" / "gpt_covariance_exploratory"  # 기존 결과를 덮어쓰지 않는 별도 탐색 결과 폴더다.
CHECKPOINT_PATH = PROJECT_DIR / "models" / "st_awfd" / "st_awfd_strict_causal_multihorizon_gpt.pt"  # 실제 271 epoch 학습에서 선택된 epoch 241 가중치를 고정한다.
ALPHA = 0.05  # 기존 CNN/GPT와 같은 정상 reference 상위 5% control-limit 가정을 유지한다.
BATCH_SIZE = 64  # 기존 실험과 같은 batch로 CUDA 메모리 사용을 제한한다.
SCORE_POLICY = "equal_horizon_mean_of_time_mean_Mahalanobis_energy_divided_by_channel_count"  # holdout 결과를 보기 전에 하나의 집계 정책을 고정한다.


def sha256_file(path: Path) -> str:  # 신경망 가중치가 탐색 중 변경되지 않는지 hash를 계산한다.
    digest = hashlib.sha256()  # 표준 SHA-256 누적 hash 객체를 만든다.
    with path.open("rb") as handle:  # checkpoint를 텍스트가 아닌 원래 bytes로 읽는다.
        for block in iter(lambda: handle.read(1024 * 1024), b""):  # 큰 파일도 메모리에 한 번에 올리지 않고 읽는다.
            digest.update(block)  # 모든 bytes를 순서대로 hash에 반영한다.
    return digest.hexdigest()  # 재실행 비교가 가능한 16진수 hash를 반환한다.


def standardized_residuals(model: gpt.CausalMultiHorizonGPT, signals: np.ndarray, device: torch.device) -> tuple[list[np.ndarray], float]:  # 각 horizon의 [group, time, channel] 표준화 예측 잔차를 계산한다.
    model.eval()  # dropout을 끄고 checkpoint의 고정 예측값을 사용한다.
    collections: list[list[np.ndarray]] = [[] for _ in model.horizons]  # horizon별 batch 결과를 분리해 보관한다.
    if device.type == "cuda":  # CUDA 연산이 대기열에 있을 수 있어 시간 측정 전에 완료시킨다.
        torch.cuda.synchronize()  # 이전 GPU 작업을 기다려 현재 forward 시간을 정확히 잰다.
    started = time.perf_counter()  # GPU forward와 CPU 결과 복사를 포함한 시작시각을 기록한다.
    with torch.no_grad():  # 이 탐색에서는 gradient를 저장하거나 가중치를 갱신하지 않는다.
        for first in range(0, len(signals), BATCH_SIZE):  # MaterialID 그룹을 고정 batch 크기로 나눈다.
            block = torch.from_numpy(signals[first:first + BATCH_SIZE]).float().to(device)  # 이전 학습의 고정 scaler로 변환된 trace를 GPU에 올린다.
            mean, log_sigma = model(block[:, :, :-1])  # 현재 token까지의 tensor context로 미래의 평균과 분산을 예측한다.
            for index, horizon in enumerate(model.horizons):  # 서로 다른 forecast distance의 잔차를 각각 계산한다.
                valid_count = block.shape[-1] - horizon  # 실제 미래 target이 trace 안에 존재하는 시점만 남긴다.
                observed = block[:, :, horizon:horizon + valid_count].transpose(1, 2)  # x[t+h]를 [group, time, channel]로 정렬한다.
                residual = (observed - mean[:, :valid_count, index]) * torch.exp(-log_sigma[:, :valid_count, index])  # 예측 표준편차를 사용해 각 센서의 상대 예측오차를 계산한다.
                collections[index].append(residual.cpu().numpy().astype(np.float64))  # 공분산과 역행렬 계산에 float64 CPU 배열을 사용한다.
    if device.type == "cuda":  # 결과 복사 후 GPU 작업을 마무리해 실제 완료시간을 기록한다.
        torch.cuda.synchronize()  # 비동기 실행 시간 때문에 forward 시간을 과소평가하지 않는다.
    elapsed = time.perf_counter() - started  # 이번 분할의 실제 추론 소요시간을 계산한다.
    return [np.concatenate(parts, axis=0) for parts in collections], elapsed  # 원래 그룹 순서를 유지한 horizon별 잔차와 실행시간을 반환한다.


def fit_reference_covariance(training_residuals: list[np.ndarray]) -> list[LedoitWolf]:  # 정상 training 그룹만으로 horizon별 센서 잔차 공분산을 적합한다.
    estimators: list[LedoitWolf] = []  # 네 horizon의 중심과 precision matrix를 보관한다.
    for residual in training_residuals:  # 각 horizon의 시간 길이가 다르므로 별도로 추정한다.
        pooled = residual.reshape(-1, residual.shape[-1])  # training group과 상대시간축을 묶어 20채널 잔차 벡터 표본으로 만든다.
        estimator = LedoitWolf(store_precision=True, assume_centered=False).fit(pooled)  # 평균 잔차 편향과 축 간 상관관계를 정상 reference에서만 학습한다.
        estimators.append(estimator)  # train에서 계산한 중심/공분산을 calibration과 holdout에서 고정해 쓴다.
    return estimators  # 신경망 가중치와 독립된 정상 잔차 reference 모델을 반환한다.


def covariance_scores(residuals: list[np.ndarray], estimators: list[LedoitWolf]) -> tuple[np.ndarray, np.ndarray]:  # correlated sensor residual의 Mahalanobis energy를 사전 정책대로 집계한다.
    horizon_scores: list[np.ndarray] = []  # 각 그룹의 horizon별 에너지 평균을 보관한다.
    for residual, estimator in zip(residuals, estimators, strict=True):  # 같은 forecast distance의 잔차와 training reference를 정확히 연결한다.
        centered = residual - estimator.location_[None, None, :]  # 정상 모델에서 남은 평균 forecast bias를 제거한다.
        energy = np.einsum("ntc,cd,ntd->nt", centered, estimator.precision_, centered, optimize=True)  # 센서의 공변동 방향은 덜 중복 집계하고 드문 조합 방향은 더 큰 에너지로 만든다.
        energy = np.maximum(energy, 0.0) / residual.shape[-1]  # 수치 반올림 음수를 제거하고 20채널로 나눠 크기를 해석하기 쉽게 한다.
        horizon_scores.append(energy.mean(axis=1))  # 상위 꼬리를 사후 선택하지 않고 모든 valid time의 평균만 사용한다.
    by_horizon = np.stack(horizon_scores, axis=1)  # [group, 4 horizon] 점수를 만들어 기여도를 보존한다.
    return by_horizon.mean(axis=1), by_horizon  # 네 horizon을 동일 가중해 하나의 검토 점수로 만든다.


def score_frame(ids: np.ndarray, scores: np.ndarray, by_horizon: np.ndarray, threshold: float) -> pd.DataFrame:  # label 없는 추론 결과에도 사용할 수 있는 점수표를 만든다.
    table = pd.DataFrame({"MaterialID": ids, "covariance_residual_energy": scores, "normal_reference_limit": threshold, "review_candidate": scores > threshold})  # ID는 식별용이며 모델 feature가 아니다.
    table["review_rank"] = pd.Series(scores).rank(method="first", ascending=False).astype(int)  # 고정 review 인력으로 볼 순서를 원래 행 위치에 기록한다.
    for index, horizon in enumerate(gpt.HORIZONS):  # 평균 점수의 원천을 거리별로 분리해 남긴다.
        table[f"horizon_{horizon}_energy"] = by_horizon[:, index]  # 해당 forecast distance의 집계 에너지를 기록한다.
    return table  # sensor 관련성이 실제 물리 원인이라는 주장은 포함하지 않는다.


def run_covariance_audit() -> dict[str, Any]:  # 고정 checkpoint 추론, 정상 공분산 적합, 정상 threshold, holdout 감사를 한 번에 실행한다.
    started = time.perf_counter()  # 파일 읽기부터 결과 저장까지 전체 소요시간을 측정한다.
    RESULT_DIR.mkdir(parents=True, exist_ok=True)  # 다른 실험 파일을 건드리지 않고 별도 폴더를 만든다.
    before_hash = sha256_file(CHECKPOINT_PATH)  # forward 전에 가중치의 정확한 hash를 기록한다.
    policy = {"score_policy": SCORE_POLICY, "policy_fixed_at_utc": datetime.now(timezone.utc).isoformat(), "checkpoint_sha256": before_hash, "fit_scope": "training normal 441 MaterialID groups only", "threshold_scope": "existing normal 111 MaterialID groups only", "aggregation": "time mean per horizon, then equal horizon mean; no tail selection", "threshold_rule": "same empirical higher 95th normal-score quantile as baseline", "hyperparameters_tuned_on_holdout": False, "exploratory_reason": "Official mixed holdout was already inspected in earlier architecture experiments; this is not a fresh confirmatory evaluation."}  # 현재 holdout가 새로운 최종 검증 데이터가 아니라는 사실까지 정책에 포함한다.
    (RESULT_DIR / "score_policy_before_audit.json").write_text(json.dumps(policy, indent=2, ensure_ascii=False), encoding="utf-8")  # test score 계산 전에 정책을 디스크에 고정한다.
    checkpoint = torch.load(CHECKPOINT_PATH, map_location="cpu", weights_only=True)  # 프로젝트가 직접 생성한 tensor와 기본 타입 checkpoint만 안전한 모드로 불러온다.
    train, calibration, holdout, labels, train_ids, calibration_ids, holdout_ids, scaler = gpt.prepare_data()  # 기존 실험과 동일한 train-only scaler 및 group 분할을 사용한다.
    if checkpoint["scaler"] != scaler:  # 저장 모델과 재구성한 전처리 통계가 다르면 비교 자체를 중단한다.
        raise ValueError("checkpoint scaler와 동일 분할에서 재생성한 scaler가 일치하지 않습니다.")  # 다른 단위/전처리로 나온 점수를 기존 성능과 섞지 않는다.
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # RTX 3070 Ti가 감지되면 실제 forward에 우선 사용한다.
    model = gpt.CausalMultiHorizonGPT(checkpoint["feature_count"], checkpoint["sequence_length"]).to(device)  # 저장 가중치와 차원이 같은 신경망 shell만 만든다.
    model.load_state_dict(checkpoint["state_dict"])  # 초기화된 가중치를 실제 학습된 epoch 241 가중치로 교체한다.
    train_residuals, train_seconds = standardized_residuals(model, train, device)  # training normal forecast를 실제 GPU에서 실행한다.
    estimators = fit_reference_covariance(train_residuals)  # holdout와 calibration을 사용하지 않고 normal training 잔차 reference를 적합한다.
    training_scores, training_horizons = covariance_scores(train_residuals, estimators)  # training 잔차 에너지 분포를 기록한다.
    calibration_residuals, calibration_seconds = standardized_residuals(model, calibration, device)  # 고정 모델로 normal calibration forecast를 실행한다.
    calibration_scores, calibration_horizons = covariance_scores(calibration_residuals, estimators)  # 고정 normal reference로 calibration을 점수화한다.
    threshold = gpt.empirical_normal_limit(calibration_scores, alpha=ALPHA)  # test target을 보지 않고 기존 95th percentile 규칙으로 limit을 정한다.
    holdout_residuals, holdout_seconds = standardized_residuals(model, holdout, device)  # 모든 방법이 고정된 뒤 공식 mixed holdout를 실제 추론한다.
    holdout_scores, holdout_horizons = covariance_scores(holdout_residuals, estimators)  # 학습/정책 조정 없이 holdout energy를 계산한다.
    metrics = gpt.evaluate(labels, holdout_scores, threshold, calibration_scores)  # holdout label을 여기서만 사후 성능 감사에 사용한다.
    score_frame(train_ids, training_scores, training_horizons, threshold).to_csv(RESULT_DIR / "training_normal_scores.csv", index=False, encoding="utf-8-sig")  # covariance reference fit 데이터의 점수를 보존한다.
    score_frame(calibration_ids, calibration_scores, calibration_horizons, threshold).to_csv(RESULT_DIR / "normal_calibration_scores.csv", index=False, encoding="utf-8-sig")  # 정상 control-limit의 원천 점수를 보존한다.
    holdout_table = score_frame(holdout_ids, holdout_scores, holdout_horizons, threshold)  # label 없는 원래 inference 표를 먼저 만든다.
    holdout_table["target_for_retrospective_audit_only"] = labels  # benchmark 감사용 정답을 학습 feature와 분리해 마지막 열로 추가한다.
    holdout_table.to_csv(RESULT_DIR / "official_holdout_exploratory_audit_scores.csv", index=False, encoding="utf-8-sig")  # 반복 연구에 사용된 holdout임을 파일 이름에도 표시한다.
    np.savez_compressed(RESULT_DIR / "normal_residual_covariance_reference.npz", locations=np.stack([estimator.location_ for estimator in estimators]), covariances=np.stack([estimator.covariance_ for estimator in estimators]), precisions=np.stack([estimator.precision_ for estimator in estimators]), horizons=np.asarray(gpt.HORIZONS), threshold=np.asarray(threshold))  # 새 CSV 추론에 재사용할 공분산 reference와 limit을 저장한다.
    previous = json.loads((gpt.RESULT_DIR / "strict_causal_gpt_run_summary.json").read_text(encoding="utf-8"))  # original GPT NLL 집계의 actual 결과를 비교에 가져온다.
    rows = [{"model": "Fixed strict GPT + mean LedoitWolf residual energy (exploratory)", **metrics}, {"model": "Strict GPT mean Gaussian NLL", **previous["metrics"]}]  # 새로운 모델 학습 없이 score 계산만 바뀐 비교표를 만든다.
    comparison_source = pd.read_csv(gpt.RESULT_DIR / "model_comparison.csv")  # 기존 동일 분할 CNN/classical 지표를 불러온다.
    for _, row in comparison_source.iterrows():  # 모든 정상 지표를 함께 볼 수 있도록 실제 비교 결과를 확장한다.
        if "GPT" not in str(row["model"]) and "Transformer" not in str(row["model"]):  # 기존 GPT와 구현 오류 legacy 행을 중복 추가하지 않는다.
            rows.append(row.to_dict())  # CNN와 classical baseline의 사전 calibration 결과를 보존한다.
    comparison = pd.DataFrame(rows)  # point metric과 confidence interval을 한 파일로 결합한다.
    comparison.to_csv(RESULT_DIR / "model_comparison_exploratory.csv", index=False, encoding="utf-8-sig")  # 성능이 나빠져도 동일하게 모든 지표를 저장한다.
    after_hash = sha256_file(CHECKPOINT_PATH)  # 탐색 종료 후 가중치가 그대로인지 다시 확인한다.
    if before_hash != after_hash:  # 다른 프로세스의 재학습이 checkpoint를 바꿨으면 현재 비교를 성공으로 내놓지 않는다.
        raise RuntimeError("실행 중 checkpoint가 변경되어 고정 모델 비교가 유효하지 않습니다.")  # 가중치 변경과 score 개선을 혼동하지 않게 한다.
    summary = {"policy": policy, "device": str(device), "device_name": torch.cuda.get_device_name(0) if device.type == "cuda" else "CPU", "checkpoint_best_epoch": int(checkpoint["best_epoch"]), "checkpoint_unchanged": before_hash == after_hash, "new_neural_training_epochs": 0, "actual_forward_group_counts": {"training_normal": len(train), "normal_calibration": len(calibration), "mixed_holdout": len(holdout)}, "forward_seconds_including_cpu_copy": {"training_normal": train_seconds, "normal_calibration": calibration_seconds, "mixed_holdout": holdout_seconds}, "horizons": list(gpt.HORIZONS), "covariance_diagnostics": [{"horizon": horizon, "pooled_training_vectors": int(residual.shape[0] * residual.shape[1]), "shrinkage": float(estimator.shrinkage_), "covariance_condition_number": float(np.linalg.cond(estimator.covariance_))} for horizon, residual, estimator in zip(gpt.HORIZONS, train_residuals, estimators, strict=True)], "metrics": metrics, "original_gpt_nll_metrics": previous["metrics"], "limitations": ["Exploratory score audit: this official mixed holdout has already been reviewed in several earlier experiments, so it is not a fresh confirmatory final test.", "No holdout labels or scores are used to tune the covariance model, aggregation, alpha or threshold in this script.", "Existing 111 normal groups selected the neural checkpoint and now set the score threshold; an independent calibration period is required for formal guarantees.", "Pooled within-trace residual vectors are temporally dependent; LedoitWolf is a numerical regularizer here and does not establish independent-sample covariance confidence guarantees.", "Covariance scoring removes the Gaussian log_sigma term and accounts for residual correlation; it is a Mahalanobis anomaly heuristic, not the same likelihood objective optimized during training.", "Strict causality holds only for the model on resampled tensors: full-step interpolation and normalization of progress use the completed trace, so this is post-step trace triage rather than demonstrated online raw-stream early warning.", "MaterialID is a production lot according to the official README; this project evaluates those groups and does not establish wafer/die counts.", "No physical sensor/tool/recipe mapping or final tested-die yield/intervention outcome is available; true yield improvement remains unmeasured.", "The empirical normal quantile rule is kept for comparison and is not a finite-sample conformal guarantee under distribution shift."], "sources": {"ST_AWFD": "https://github.com/STMicroelectronics/ST-AWFD", "LedoitWolf_documentation": "https://scikit-learn.org/stable/modules/generated/sklearn.covariance.LedoitWolf.html", "LedoitWolf_primary_paper": "https://www.ledoit.net/Well-conditioned2004.pdf"}}  # 실제 실행과 주장 범위를 모두 결과 manifest에 남긴다.
    figure, axes = plt.subplots(1, 2, figsize=(13.8, 5.2))  # 분포와 모델 trade-off를 하나의 정적인 연구 그림으로 만든다.
    plotted_values = np.concatenate([calibration_scores, holdout_scores])  # threshold 계산과 별개로 그림만의 공통 축 범위를 정한다.
    plot_bins = np.geomspace(max(float(plotted_values.min()), 1e-8), float(plotted_values.max()) * 1.01, 32)  # 극단적 에너지 때문에 정상 분포가 첫 bin에 숨지 않도록 log 간격을 쓴다.
    axes[0].hist(calibration_scores, bins=plot_bins, alpha=0.65, label="Normal calibration reference")  # calibration tail이 어디에 있는지 점수 분포를 보여준다.
    axes[0].hist(holdout_scores[labels == 0], bins=plot_bins, alpha=0.55, label="Holdout normal audit")  # 정상 분포 이동 여부를 holdout label로 사후 감사한다.
    axes[0].hist(holdout_scores[labels == 1], bins=plot_bins, alpha=0.55, label="Holdout abnormal audit")  # 이상 분포가 새 score에서 분리되는지 기록한다.
    axes[0].set_xscale("log")  # 몇 배의 score 차이가 있는지 읽을 수 있게 에너지 축만 로그로 표시한다.
    axes[0].axvline(threshold, color="#111827", linestyle="--", label="Fixed normal 95th quantile")  # normal-only threshold를 그린다.
    axes[0].set(xlabel="Mean covariance-adjusted residual energy", ylabel="MaterialID groups", title="Exploratory score audit; no yield measurement")  # 그림에서 표본 단위와 검증 범위를 설명한다.
    axes[0].legend(fontsize=8)  # 정상 reference와 감사 분포를 구분한다.
    chosen = comparison[comparison["model"].isin([rows[0]["model"], rows[1]["model"], "1D CNN denoising autoencoder", "RankFusionEnsemble", "IsolationForest"])].copy()  # 한눈에 볼 핵심 비교 모델을 모두 사전 정한 목록에서 표시한다.
    positions = np.arange(len(chosen))  # 같은 모델의 FPR과 recall bar를 나란히 배치한다.
    axes[1].barh(positions - 0.17, chosen["holdout_normal_false_alarm_rate"], height=0.32, color="#D97706", label="Normal false alarms (lower)")  # 정상 검토 부담을 분리해 표현한다.
    axes[1].barh(positions + 0.17, chosen["holdout_anomaly_recall_at_normal_limit"], height=0.32, color="#0F766E", label="Abnormal recall (higher)")  # 이상 capture가 줄어드는 trade-off를 숨기지 않는다.
    labels_short = ["GPT + covariance (exploratory)" if "LedoitWolf" in name else "GPT mean NLL" if "Gaussian" in name else "CNN autoencoder" if "CNN" in name else str(name) for name in chosen["model"]]  # 그래프의 긴 모델 이름을 읽을 수 있게 줄인다.
    axes[1].set(yticks=positions, yticklabels=labels_short, xlim=(0, 1.06), xlabel="Rate", title="Same normal-limit policy; joint operating metrics")  # 서로 다른 score 단위 대신 운영 비율을 비교한다.
    axes[1].legend(fontsize=8, loc="lower right")  # 두 막대의 의미를 명시한다.
    figure.tight_layout()  # 긴 비교 이름과 axis가 겹치지 않게 배치를 조정한다.
    figure.savefig(RESULT_DIR / "covariance_exploratory_audit.png", dpi=180)  # 앱과 분석 자료에 사용할 실제 결과 그림을 저장한다.
    plt.close(figure)  # 반복 실행 시 그림 메모리를 해제한다.
    summary["total_seconds"] = time.perf_counter() - started  # 저장까지 완료한 실제 총 실행시간을 기록한다.
    (RESULT_DIR / "covariance_exploratory_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")  # 과장 없이 결과와 한계를 모두 기록한다.
    return summary  # 앱/노트북에서 같은 실제 결과를 사용할 수 있도록 반환한다.


if __name__ == "__main__":  # 사용자가 이 파일을 실행할 때에만 고정 모델 탐색을 시작한다.
    result = run_covariance_audit()  # GPU forward와 normal-only covariance calibration 및 사후 감사를 실행한다.
    print(json.dumps({"device": result["device_name"], "new_neural_training_epochs": result["new_neural_training_epochs"], "checkpoint_unchanged": result["checkpoint_unchanged"], "metrics": result["metrics"], "forward_seconds": result["forward_seconds_including_cpu_copy"], "total_seconds": result["total_seconds"], "result_dir": str(RESULT_DIR)}, ensure_ascii=False, indent=2))  # 실제 측정값과 생성 파일 위치를 터미널에 보여준다.
