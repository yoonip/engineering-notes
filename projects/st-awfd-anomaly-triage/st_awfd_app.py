# -*- coding: utf-8 -*-  # Windows에서 한국어 인터페이스 문자열을 그대로 표시한다.
# 공식 ST-AWFD D2 normal-only anomaly detection 실험을 위한 원클릭 Streamlit UI다.  # 이 페이지는 SK hynix 장비나 제조 데이터에 접속하지 않는다.
# 실행 가능한 모든 소스 행에 왜 필요한지와 현업 적용 범위에 대한 주석을 둔다.  # 빈 줄은 읽기 쉬운 블록 구분자다.

from __future__ import annotations  # type hint로 함수 API를 읽기 쉽게 둔다.
import json  # 이전에 끝난 모델 run을 화면 refresh 후 다시 불러온다.
import tempfile  # 사용자가 올린 batch CSV를 score 함수가 읽을 임시 파일로 기록한다.
from pathlib import Path  # UI 결과 파일과 실행 파일 경로를 찾는다.
from typing import Any  # JSON summary가 가진 섞인 값 형식을 UI helper에서 표시한다.

import pandas as pd  # queue/model table과 epoch values를 보기 좋은 표/선 차트로 렌더링한다.
import streamlit as st  # 학습 버튼·GPU loss·review queue·CSV upload 화면을 제공한다.
import hashlib  # 탐색 점수가 현재 저장 가중치에 대응하는지 확인한다.
from st_awfd_pipeline import MODEL_DIR, PROJECT_DIR, RESULTS_DIR, run_experiment, score_new_csv  # 검토 완료한 train/inference/Excel pipeline과 checkpoint 경로를 공유한다.

st.set_page_config(page_title="ST-AWFD PE Anomaly Triage", page_icon="🧪", layout="wide")  # 큰 표와 학습 곡선을 데스크톱 폭에 맞춰 표시한다.
st.title("ST-AWFD 공정 이상 탐지")  # current experiment이 ST-AWFD 공개 데이터에 한정됨을 밝힌다.
st.caption("STMicroelectronics D2 · Step 1 · normal-only 학습 · MaterialID group anomaly triage")  # 모델 입력과 운영 목적을 상단에 표기한다.
st.info("공개 ST-AWFD D2의 정상 lot으로 학습하고, 공정 이상 점수와 검토 순위를 계산합니다. Step 1의 익명 센서 20개를 사용합니다.")  # provenance·표본 구성·성과 범위를 한 화면에 표시한다.
st.markdown("학습 구조: 공개 is_test=0의 정상 waveform만 학습 80%와 정상 기준선 검증 20%로 MaterialID group 단위 분리합니다. 기준선은 validation normal score의 지정 quantile에서 고정한 뒤, 공개 is_test=1 혼합 집합에 한 번 적용합니다.")  # production anomaly detection과 유사한 normal-only protocol을 설명한다.

target_fpr = st.slider("정상 validation 경보 예산 가정 (비율: 0.05 = 5%)", min_value=0.01, max_value=0.20, value=0.05, step=0.01, format="%.2f", help="모델이 정상 검증 표본 중 이 비율을 넘도록 통계적 control limit을 선택합니다. 공식 fab spec은 아닙니다.")  # 사용자 선택 false-alarm 예산을 데이터 threshold와 구분한다.
review_fraction = st.slider("PE 검토 큐 batch 용량 (비율: 0.10 = 10%)", min_value=0.05, max_value=0.25, value=0.10, step=0.01, format="%.2f", help="새 batch 점수의 상위 순위에서 이 비율만 검토하는 예시입니다. 품질 기준이나 수율 향상 수치가 아닙니다.")  # review-capacity 시나리오를 직접 바꿀 수 있게 한다.

def read_saved_summary() -> dict[str, Any] | None:  # 화면 refresh 후에도 가장 최근 완료 실험을 다시 표시한다.
    summary_file = RESULTS_DIR / "st_awfd_run_summary.json"  # pipeline이 실제 실행에서 쓴 JSON 경로를 고정한다.
    if not summary_file.exists():  # 새 복사본에서 아직 학습을 안 했다면 summary가 없다.
        return None  # placeholder metric을 만들지 않고 안내 상태를 반환한다.
    return json.loads(summary_file.read_text(encoding="utf-8"))  # 실제 run에서 저장한 장치/지표/출처를 읽는다.


def render_completed_run(summary: dict[str, Any]) -> None:  # 실제 저장된 queue·지표·Excel을 화면에 연결한다.
    experiment = summary["experiment"]  # data, selected epoch, threshold 등 설정을 JSON에서 가져온다.
    metrics = experiment["primary_holdout_metrics"]  # primary TCN의 공식 test 결과를 읽는다.
    model_table_path = RESULTS_DIR / "st_awfd_model_comparison.csv"  # classical/AI 비교 표를 찾는다.
    queue_path = RESULTS_DIR / "st_awfd_inference_review_queue.csv"  # label 없는 실제 review queue 결과를 찾는다.
    audit_path = RESULTS_DIR / "st_awfd_holdout_audit.csv"  # retrospective labels는 확장 분석 영역에서만 제공한다.
    workbook_path = RESULTS_DIR / "ST_AWFD_PE_Anomaly_Triage.xlsx"  # Excel download용 실제 작성본을 찾는다.
    st.subheader("최근 실행 결과")  # 완료된 모델·장치와 통계를 구분한다.
    st.caption(f'장치: {summary["device"]["device_name"]} | CUDA: {summary["device"]["cuda_available"]} | best epoch: {experiment["best_epoch"]} | normal calibration: {experiment["calibration_normal_wafers"]} MaterialID groups')  # 실제 runtime과 calibration 표본 수를 표시한다.
    left, middle, right = st.columns(3)  # 주요 순위 지표와 정상 경보 실패를 같은 행에 나란히 표시한다.
    left.metric("Official holdout AP / ROC-AUC", f'{metrics["average_precision"]:.3f} / {metrics["roc_auc"]:.3f}', help="홀드아웃에는 정답이 있는 공개 benchmark이며, 이상 wafer 비율이 일반 fab보다 높게 선택되어 있습니다.")  # 순위 분리도를 숫자로 보여준다.
    middle.metric("임계값 초과 recall", f'{metrics["true_positive"]} / {metrics["n_anomalous"]}', help="validation normal 분포에서 미리 고정한 한계값 기준입니다.")  # 고정된 정상 reference limit을 넘긴 이상 수를 보여준다.
    right.metric("Official test 정상 오경보", f'{metrics["test_normal_false_alarm_rate"]:.1%}', delta=f'{metrics["test_normal_false_alarm_inflation_vs_target"]:.1f}× target', delta_color="inverse", help="validation normal에서 설정한 경보 예산과 official test normal 사이의 차이입니다.")  # threshold가 새 표본에 전이되지 않은 drift 핵심을 보여준다.
    if metrics["test_normal_false_alarm_rate"] > experiment["calibration_target_fpr"] * 1.5:  # 검증 기준과 official test normal 사이에 큰 경보율 차이가 있는지 표시한다.
        st.error(f'정상 validation에서 목표한 {experiment["calibration_target_fpr"]:.0%} 경보율이 official test 정상 group에서 {metrics["test_normal_false_alarm_rate"]:.1%}로 증가했습니다. 이 threshold를 양산에 그대로 적용하면 검토 workload가 과도해질 수 있습니다. target/product/tool별 matched normal reference와 drift 대응을 추가해야 합니다.')  # 사용자가 높은 recall만 보고 deployment 준비 완료라고 오해하지 않게 한다.
    st.info(f'상위 {review_fraction:.0%} 검토 큐는 {metrics["review_queue_true_positives"]}개 이상 MaterialID group을 담았습니다. 이것은 score ranking의 batch-capacity 시뮬레이션이고, 실제 생산 수율 개선 또는 불량 원인 인과 효과가 아닙니다.')  # 고정 용량 큐의 실험 의미를 밝힌다.
    comparison = pd.read_csv(model_table_path)  # 모델별 실측 holdout 결과를 CSV 원본에서 읽는다.
    st.subheader("정상 기준선에서 고정한 threshold의 test 결과")  # threshold와 ranking 차이를 구분한다.
    st.dataframe(comparison, hide_index=True, width="stretch")  # detector별 false alarm·miss와 queue 수치를 실제 표로 보여준다.
    st.subheader("엔지니어 검토 큐 · label 제외")  # 현업 검토 화면은 label이 없는 score list로 만든다.
    queue = pd.read_csv(queue_path)  # inference result의 label-free CSV를 로드한다.
    st.dataframe(queue.head(50), hide_index=True, width="stretch")  # 표 길이로 화면이 과도하게 커지지 않게 상위 50개를 표시한다.
    st.download_button("전체 검토 큐 CSV 다운로드", queue_path.read_bytes(), file_name="st_awfd_inference_review_queue.csv", mime="text/csv")  # 사용자가 label 없는 우선순위표를 바로 엑셀/다른 도구에서 연다.
    if workbook_path.exists() and summary.get("workbook_export", {}).get("status", "created") == "created":  # Excel export가 실제로 완료된 경우에만 download action을 표시한다.
        st.download_button("요약·학습곡선·검토 큐·감사 결과 Excel 다운로드", workbook_path.read_bytes(), file_name=workbook_path.name, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")  # score/epoch/sensor audit가 담긴 완성 workbook을 보낸다.
    with st.expander("사후 holdout audit와 sensor 오차 표", expanded=False):  # model training input과 정답 의존 분석을 구분한다.
        audit = pd.read_csv(audit_path)  # public label은 성능 감사용으로만 불러온다.
        residuals = pd.read_csv(RESULTS_DIR / "st_awfd_sensor_residual_audit.csv")  # 익명 signal의 test reconstruction error 표를 불러온다.
        st.caption("아래 label과 sensor residual 차이는 benchmark 결과를 설명하기 위한 사후 audit입니다. 학습이나 threshold 설정에 사용하지 않았으며, feature_번호는 물리적 장비·회로 이름을 의미하지 않습니다.")  # 원인분석이 아닌 사후 association임을 구분한다.
        st.dataframe(audit, hide_index=True, width="stretch")  # 공식 test label과 각 algorithm score를 audit view에 보여준다.
        st.dataframe(residuals, hide_index=True, width="stretch")  # 익명 sensor의 정상/이상 residue 차이를 review cue로 표시한다.


st.subheader("원클릭 학습 + 추론")  # 실제 optimizer run 시작 버튼을 결과표와 구분한다.
if st.button("정상-only 학습 → threshold 설정 → 공식 holdout 추론", type="primary", width="stretch"):  # 사용자가 직접 누르면 GPU 모델과 classical benchmark를 다시 실행한다.
    status = st.status("원본 검증과 normal-only 학습을 준비합니다.", expanded=True)  # 데이터 loading·GPU training 단계를 실시간 영역에 보여준다.
    progress_bar = st.progress(0.0, text="모델을 초기화하고 있습니다.")  # 완료된 epoch 수로 실제 progress를 계산한다.
    live_values = st.empty()  # 최신 train/calibration MSE와 best checkpoint를 표기할 위치를 예약한다.
    training_chart = st.empty()  # 실제 epoch loss line chart를 다시 그릴 placeholder를 만든다.
    epoch_events: list[dict[str, float]] = []  # optimizer가 완료한 epoch 값만 UI memory에 누적한다.
    def update_epoch(event: dict[str, Any]) -> None:  # pipeline이 epoch마다 callback으로 보내는 관측값을 렌더링한다.
        epoch_events.append({"epoch": float(event["epoch"]), "train_denoising_mse": float(event["train_loss"]), "validation_normal_mse": float(event["validation_loss"])})  # 각 epoch에서 측정한 loss 두 개만 기록한다.
        chart_data = pd.DataFrame(epoch_events).set_index("epoch")  # Streamlit의 선 차트가 이용하도록 index를 설정한다.
        progress_bar.progress(min(float(event["epoch"]) / float(event["max_epochs"]), 1.0), text=f'실제 GPU epoch {event["epoch"]}/{event["max_epochs"]} · best epoch {event["best_epoch"]} · {event["device"]}')  # timer가 아니라 완료된 epoch 수로 진행률을 표현한다.
        live_values.markdown(f'현재 epoch {event["epoch"]} | train denoising MSE {event["train_loss"]:.5f} | validation normal MSE {event["validation_loss"]:.5f} | best epoch {event["best_epoch"]} | early-stop 여유 {event["patience_left"]}')  # 실제 학습·validation MSE를 매 epoch 표시한다.
        training_chart.line_chart(chart_data, height=280, y_label="MSE in train-fitted z space")  # data-driven loss history를 실제 그래프로 그린다.
    try:  # 데이터 검증부터 Excel까지의 failure를 결과 미완료로 보이게 처리한다.
        outcome = run_experiment(PROJECT_DIR, float(target_fpr), float(review_fraction), progress_callback=update_epoch)  # GPU autoencoder, normal quantile threshold, official mixed holdout, Excel을 실행한다.
        st.session_state["st_awfd_latest_summary"] = outcome["summary"]  # 결과를 UI refresh 후에도 이번 값으로 갱신한다.
        progress_bar.progress(1.0, text=f'완료 · {len(epoch_events)} epoch · {outcome["summary"]["device"]["device_name"]}')  # pipeline과 Excel이 성공적으로 끝난 뒤에만 완료로 표시한다.
        status.update(label="학습·추론 완료" + (" · Excel 생성" if outcome["excel_path"] else " · CSV 저장"), state="complete", expanded=False)  # 저장 형식에 맞는 완료 상태를 표시한다.
        st.success("실제 PyTorch 학습이 끝났습니다. epoch 기록, mixed-test holdout, FPR drift, label 없는 queue가 아래에 나타납니다.")  # 학습값과 분석 결과 위치를 안내한다.
    except Exception as failure:  # 입력자료/의존성/output 문제를 숨기지 않는다.
        status.update(label="학습 또는 산출 단계에서 오류가 발생했습니다.", state="error", expanded=True)  # 완료되지 않은 실행임을 상태 표시한다.
        st.exception(failure)  # Stack trace를 남겨 사용자가 고칠 수 있게 한다.


st.divider()  # The Transformer comparison has a separate button so the existing CNN run remains reproducible.
st.subheader("엄밀한 GPT형 구조: strict-causal multi-horizon Transformer")  # Name the corrected model by its causal property and forecasting task.
st.markdown("구조: 미래 방향으로 padding하지 않는 Conv1d 임베딩 → causal attention을 적용한 decoder-only Transformer → 각 센서의 1·2·4·8 시점 뒤 값에 대한 평균·불확실성 예측입니다. 연속 센서값의 Gaussian NLL을 정상 데이터로만 학습합니다. 짧은 이상과 여러 시점 지속 편차를 한 score에 담는 설계 가설이며, 수율 자체를 학습하는 모델은 아닙니다.")  # Explain the new architecture and avoid equating predictive quality with yield.
st.caption("같은 D2 MaterialID group split에서 비교합니다. 정상111개를 early stopping과 5% limit에 함께 썼습니다. holdout 정답은 parameter/threshold fit에 넣지 않았지만, 같은604개를 여러 구조의 연구 비교에서 반복 조회했으므로 최종 미사용 검증으로 주장할 수 없습니다. 별도 정상 calibration 기간과 미래/tool holdout이 필요합니다.")  # 연구 비교와 최종 독립 확인의 증거 수준을 정확하게 구분한다.
if st.button("정상-only strict-causal multi-horizon Transformer 학습 → 추론", key="run_strict_causal_gpt", type="primary", width="stretch"):  # Start the corrected GPU training from a user-visible one-click action.
    from st_awfd_causal_gpt_multihorizon import run_experiment  # Import the strict-causal model only when the user starts this experiment.
    strict_status = st.status("정상 MaterialID group을 읽고 causal Transformer를 초기화합니다.", expanded=True)  # Keep data validation and model setup status visible.
    strict_progress = st.progress(0.0, text="Strict-causal 학습 대기")  # Display real epoch completion, not simulated task progress.
    strict_live = st.empty()  # Reserve a place for current NLL, best checkpoint and CUDA device.
    strict_chart = st.empty()  # Reserve a place for actual training/normal-validation loss history.
    strict_events: list[dict[str, float]] = []  # Hold this run's callback data for live chart updates.
    def update_strict_epoch(event: dict[str, Any]) -> None:  # Render actual observations emitted after every completed training epoch.
        strict_events.append({"epoch": float(event["epoch"]), "train_normal_Gaussian_NLL": float(event["train_loss"]), "validation_normal_Gaussian_NLL": float(event["validation_loss"])})  # Keep both objective curves at each epoch.
        strict_progress.progress(min(float(event["epoch"]) / float(event["max_epochs"]), 1.0), text=f"epoch {event['epoch']}/{event['max_epochs']} · best {event['best_epoch']} · {event['device']}")  # Show completed optimizer epochs and actual compute device.
        strict_live.markdown(f"Train Gaussian NLL {event['train_loss']:.4f} · normal validation {event['validation_loss']:.4f} · selected epoch {event['best_epoch']} · best validation {event['best_validation_loss']:.4f}")  # State the fitted forecasting likelihood, not anomaly accuracy or yield.
        strict_chart.line_chart(pd.DataFrame(strict_events).set_index("epoch"), height=280, y_label="Multi-horizon Gaussian NLL")  # Plot the real normal-only objective as training runs.
    try:  # Expose CUDA/data/reporting exceptions instead of marking a partial run complete.
        strict_outcome = run_experiment(progress_callback=update_strict_epoch)  # Train normal-only, calibrate normals, infer the locked holdout, and write audit outputs.
        st.session_state["strict_causal_gpt_summary"] = strict_outcome["summary"]  # Preserve the actual completed result after Streamlit reruns.
        strict_status.update(label="Transformer 학습·추론 완료" + (" · Excel 생성" if strict_outcome["workbook_path"] else " · CSV 저장"), state="complete", expanded=False)  # Mark complete only after all artifacts exist.
        st.success(f"실제 실행 장치: {strict_outcome['device']} · 선택 epoch: {strict_outcome['best_epoch']} · best normal-validation Gaussian NLL: {strict_outcome['summary']['training']['best_normal_validation_nll']:.4f}")  # Identify the completed GPU model and training run using the actual validation loss.
    except Exception as failure:  # Surface resource or schema errors to aid reproducible diagnosis.
        strict_status.update(label="Strict-causal Transformer 실험 중 오류가 발생했습니다.", state="error", expanded=True)  # Keep the interrupted phase visible.
        st.exception(failure)  # Print the exception and stack trace into the app.
strict_summary = st.session_state.get("strict_causal_gpt_summary")  # Prefer the summary produced during the current app session.
strict_summary_path = RESULTS_DIR / "causal_gpt_multihorizon" / "strict_causal_gpt_run_summary.json"  # Locate the persistent run manifest when the app restarts.
if strict_summary is None and strict_summary_path.exists():  # Do not train automatically just because the page refreshes.
    strict_summary = json.loads(strict_summary_path.read_text(encoding="utf-8"))  # Reload previously measured metrics from disk.
if strict_summary is not None:  # Render output only when the training/inference run actually finished.
    strict_metrics = strict_summary["metrics"]  # Read saved ranking and capacity-aware operating metrics.
    st.markdown("#### Strict-causal Transformer 결과")  # Separate the valid causal model results from the legacy comparison.
    strict_training = strict_summary["training"]  # 화면에서 실제 실행 장치와 best checkpoint 선택을 확인한다.
    st.caption(f"실제 장치: {strict_training['device_name']} · 완료 {strict_training['epochs_completed']} epochs · best {strict_training['selected_epoch']} · best normal validation NLL {strict_training['best_normal_validation_nll']:.5f}")  # 저장된271epoch 실행의 증거를 표시한다.
    st.caption("단위: MaterialID group = 공식 정의상 생산 lot. 전체 Step 1이 완료된 후 상대진행률 보간으로 추론합니다. causal 검증은 이미 보간된 tensor 내부의 네트워크에 한정되며 raw stream 실시간 조기경보를 검증하지 않았습니다.")  # 데이터 그룹 및 end-to-end causality 범위를 정확히 한정한다.
    strict_cols = st.columns(4)  # Show predictive ranking, drift, precision and fixed-capacity review in parallel.
    strict_cols[0].metric("AP / ROC-AUC", f"{strict_metrics['holdout_average_precision']:.3f} / {strict_metrics['holdout_roc_auc']:.3f}")  # Display retrospective ranking quality with enriched-test caveat.
    strict_cols[1].metric("정상 오경보율", f"{strict_metrics['holdout_normal_false_alarm_rate']:.1%}", delta=f"validation {strict_metrics['calibration_normal_false_alarm_rate']:.1%}", delta_color="inverse")  # Compare calibration FPR and holdout normal false alarms.
    strict_cols[2].metric("고정 기준 이상 recall / precision", f"{strict_metrics['holdout_anomaly_recall_at_normal_limit']:.1%} / {strict_metrics['holdout_precision_at_normal_limit']:.1%}")  # Show the false-alarm/miss tradeoff under the normal-only limit.
    strict_cols[3].metric("상위 review 10%의 이상 포착률", f"{strict_metrics['top_review_anomaly_recall']:.1%}", help=f"검토 후보 {strict_metrics['top_review_count']}개 기준 precision {strict_metrics['top_review_precision']:.1%}")  # 검토 후보 수와 전체 이상 포착률의 분모를 혼동하지 않는다.
    causal_audit = strict_summary.get("causality_audit", {})  # Read the model's future-perturbation invariant from the saved run manifest.
    if causal_audit.get("passes_strict_causal_invariance"):  # Show a successful implementation sanity check distinctly from model quality.
        st.success(f"미래정보 차단 sanity check 통과: cutoff 뒤 입력을 교란했을 때 forecast mean 최대 변화 {causal_audit.get('max_forecast_mean_delta_at_cutoff', float('nan')):.6g}, log_sigma 최대 변화 {causal_audit.get('max_log_sigma_delta_at_cutoff', float('nan')):.6g}.")  # Explain exactly what was perturbed and what remained invariant.
    else:  # Make missing or failed causality evidence visible rather than assuming the attention mask was enough.
        st.warning("저장된 causal invariance audit가 없거나 통과하지 못했습니다. 이 run을 strict-causal로 주장하기 전에 future perturbation 점검이 필요합니다.")  # Avoid an unsupported causal guarantee.
    st.caption(f"holdout normal FPR Wilson 95% CI: {strict_metrics['holdout_normal_false_alarm_ci95_low']:.1%}–{strict_metrics['holdout_normal_false_alarm_ci95_high']:.1%}. 이 test는 anomaly 비율 {367 / 604:.1%}인 enriched benchmark이며 현장 prevalence가 아닙니다.")  # Include uncertainty and the benchmark's enriched label mix.
    strict_comparison_path = RESULTS_DIR / "causal_gpt_multihorizon" / "model_comparison.csv"  # Read the same-split CNN and corrected Transformer comparison.
    if strict_comparison_path.exists():  # Present all available comparison rows after they were written.
        valid_comparisons = pd.read_csv(strict_comparison_path)  # 미래 누설이 있던 legacy 행은 정상 비교표에서 제외한다.
        valid_comparisons = valid_comparisons.loc[~valid_comparisons["model"].str.contains("legacy|non-causal", case=False, regex=True)]  # 오류 구현의 점수를 잘못 사용하지 않게 한다.
        st.dataframe(valid_comparisons, hide_index=True, width="stretch")  # Make balanced accuracy, FPR, precision/recall, and review queue inspectable.
    strict_chart_path = RESULTS_DIR / "causal_gpt_multihorizon" / "strict_causal_gpt_experiment.png"  # Locate actual loss and holdout-score visualization.
    if strict_chart_path.exists():  # Avoid broken image widgets when a partial run failed.
        st.image(str(strict_chart_path), width="stretch")  # Show the train/validation curve and retrospective score audit.
    strict_workbook_path = RESULTS_DIR / "causal_gpt_multihorizon" / "strict_causal_gpt_experiment.xlsx"  # Locate the complete comparison workbook.
    if strict_workbook_path.exists() and strict_summary.get("workbook_export", {}).get("status", "created") == "created":  # Offer the user a workbook only after it exists on disk.
        st.download_button("strict-causal 학습·추론·비교 Excel 다운로드", strict_workbook_path.read_bytes(), file_name=strict_workbook_path.name, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key="download_strict_causal_workbook")  # Download metrics, train history, calibration and feature audit together.
    strict_audit_path = RESULTS_DIR / "causal_gpt_multihorizon" / "official_holdout_audit_scores.csv"  # Locate per-feature and per-horizon retrospective attribution scores.
    if strict_audit_path.exists():  # Only offer attribution when the underlying completed run wrote its audit table.
        with st.expander("사후 audit 점수 분해: 익명 feature / horizon", expanded=False):  # Keep a diagnostic drilldown separate from the headline model metrics.
            st.caption("이 화면은 공식 holdout의 retrospective audit 전용입니다. 익명 feature 번호는 물리 센서나 원인으로 대응할 수 없고, 이 분해는 인과 설명이 아닙니다.")  # Prevent score attribution from being mistaken for physical root-cause analysis.
            strict_audit_frame = pd.read_csv(strict_audit_path)  # Read the scored holdout output after the fit and calibration were already locked.
            selected_material_id = st.selectbox("MaterialID group", strict_audit_frame["MaterialID"].astype(str).tolist(), key="strict_gpt_audit_material_id")  # Let the user inspect one group without using its label to retrain or retune.
            selected_audit_row = strict_audit_frame.loc[strict_audit_frame["MaterialID"].astype(str) == selected_material_id].iloc[0]  # Select only the row requested by the user.
            feature_columns = [column for column in strict_audit_frame.columns if column.startswith("feature_") and column.endswith("_mean_nll")]  # Identify sensor-wise components of the same predictive surprise score.
            horizon_columns = [column for column in strict_audit_frame.columns if column.startswith("horizon_") and column.endswith("_mean_nll")]  # Identify how short/long forecast steps contributed to the score.
            feature_breakdown = pd.DataFrame({"익명 feature": feature_columns, "mean Gaussian NLL": [float(selected_audit_row[column]) for column in feature_columns]}).sort_values("mean Gaussian NLL", ascending=False)  # Rank channels by their score contribution without inferring channel meaning.
            horizon_breakdown = pd.DataFrame({"horizon": horizon_columns, "mean Gaussian NLL": [float(selected_audit_row[column]) for column in horizon_columns]}).sort_values("mean Gaussian NLL", ascending=False)  # Rank forecast horizons to make multi-horizon behavior inspectable.
            st.write(f"전체 score {float(selected_audit_row['multi_horizon_gaussian_nll']):.4f} · 고정 limit 초과 {bool(selected_audit_row['exceeds_fixed_limit'])}")  # Show only score/decision audit fields, not the retrospective target label.
            audit_cols = st.columns(2)  # Compare sensor and horizon score components side-by-side.
            audit_cols[0].dataframe(feature_breakdown.head(10), hide_index=True, width="stretch")  # Display the ten largest anonymous feature contributions.
            audit_cols[1].dataframe(horizon_breakdown, hide_index=True, width="stretch")  # Display the four forecast-horizon contributions.
    with st.expander("GPT 예측 잔차의 센서 공분산 반영 실험", expanded=False):  # 익명 센서 상관관계를 활용한 개선 시도의 실제 결과를 제공한다.
        st.caption("신경망 weight는 고정하고 정상441 lot의 표준화 예측 잔차에 LedoitWolf 공분산을 적합합니다. 정상111 lot만으로 limit을 고정합니다. 이미 본 holdout의 탐색 분석이며 전체 우위나 수율 증가를 보장하지 않습니다.")  # 추가 epoch 없이 어떤 학습·점수가 달라지는지 명시한다.
        if st.button("저장 GPT + 정상 residual 공분산 실제 GPU 재실행", key="run_covariance_exploratory"):  # 사용자에게 개선 방법을 실제로 재실행할 수 있게 한다.
            try:  # 모델 부재나 구조 mismatch를 화면에서 설명한다.
                from st_awfd_gpt_covariance_audit import run_covariance_audit  # 독립 구현의 고정 정책과 같은 함수를 사용한다.
                with st.spinner("고정 GPT forecast → 정상 공분산 적합 → limit → 탐색 audit..."):  # CPU covariance fit과 GPU forward 단계를 설명한다.
                    run_covariance_audit()  # 정상/reference만 적합하고 label은 마지막 사후 감사에서만 읽는다.
            except Exception as failure:  # 실패를 개선 결과로 감추지 않는다.
                st.exception(failure)  # 재실행 실패 원인을 제공한다.
        covariance_dir = RESULTS_DIR / "gpt_covariance_exploratory"  # 실제 공분산 실험 결과 폴더를 읽는다.
        covariance_summary_path = covariance_dir / "covariance_exploratory_summary.json"  # 저장된 CPU fit/GPU 추론 evidence를 찾는다.
        if covariance_summary_path.exists():  # 완료한 탐색 결과만 표시한다.
            covariance_summary = json.loads(covariance_summary_path.read_text(encoding="utf-8"))  # 재실행하지 않고도 마지막 결과를 볼 수 있다.
            checkpoint_file = MODEL_DIR / "st_awfd_strict_causal_multihorizon_gpt.pt"  # 현재 사용자 모델의 실제 가중치 파일이다.
            same_checkpoint = checkpoint_file.exists() and hashlib.sha256(checkpoint_file.read_bytes()).hexdigest() == covariance_summary["policy"]["checkpoint_sha256"]  # 추가 학습 후 이전 covariance 결과를 비교하지 않는다.
            if same_checkpoint:  # 같은 고정 가중치의 실제 탐색일 때만 값을 표시한다.
                original_metrics = covariance_summary["original_gpt_nll_metrics"]  # 원래 Gaussian NLL 방식의 지표를 읽는다.
                covariance_metrics = covariance_summary["metrics"]  # 정상 공분산을 적용한 지표를 읽는다.
                st.write(f"오경보 {original_metrics['holdout_false_alarm_count']} → {covariance_metrics['holdout_false_alarm_count']}개 · recall {covariance_metrics['holdout_anomaly_recall_at_normal_limit']:.1%} · F1 {original_metrics['holdout_f1_at_normal_limit']:.4f} → {covariance_metrics['holdout_f1_at_normal_limit']:.4f} · AP {original_metrics['holdout_average_precision']:.4f} → {covariance_metrics['holdout_average_precision']:.4f} · top10% capture {original_metrics['top_review_anomaly_recall']:.1%} → {covariance_metrics['top_review_anomaly_recall']:.1%}. 여러 지표의 절충을 함께 검토합니다.")  # 새 실행에서도 실제 숫자를 사용해 trade-off를 설명한다.
                st.dataframe(pd.read_csv(covariance_dir / "model_comparison_exploratory.csv"), hide_index=True, width="stretch")  # 같은 model reference의 여러 지표를 보여준다.
                st.image(str(covariance_dir / "covariance_exploratory_audit.png"), width="stretch")  # 정상 분포 이동과 오경보/miss 절충을 시각화한다.
            else:  # 재학습 이후 가중치가 바뀌면 독립 탐색을 다시 수행해야 한다.
                st.info("현재 가중치가 covariance 탐색 당시와 다릅니다. 위 재실행 버튼으로 새 가중치의 탐색 결과를 만들어 주세요.")  # 오래된 점수를 최신 결과로 표시하지 않는다.
    st.warning("이상 score와 abnormal label 분리는 최종 die yield 증가의 증거가 아닙니다. 공개 데이터에는 good die/tested die, WAT/PCM/CP/ATE 결과 및 공정 변경 후 outcome이 없어 수율 개선은 계산할 수 없습니다.")  # Prevent an anomaly detection result from being described as causal yield uplift.

saved_summary = st.session_state.get("st_awfd_latest_summary") or read_saved_summary()  # 이번 세션 실행이 없으면 디스크에 마지막으로 성공한 결과를 읽는다.
if saved_summary is not None:  # 유효한 실험결과가 있는 경우만 후속 화면을 렌더링한다.
    render_completed_run(saved_summary)  # metric, threshold drift, queue, Excel 버튼을 실제 output 파일에 연결한다.
else:  # 아무 실행도 끝나지 않은 새 copy에서 placeholder 값을 만들지 않는다.
    st.info("저장된 실험 결과가 없습니다. 위 버튼을 눌러 첫 actual training/inference 실행을 시작하세요.")  # 첫 작업을 사용자가 쉽게 찾게 한다.

st.subheader("보유 CSV의 새로운 MaterialID batch 추론")  # train/test benchmark와 별도로 new unlabeled batch를 scoring한다.
inference_model = st.selectbox("저장된 모델 선택", ["GPT형 strict-causal Transformer", "1D CNN denoising autoencoder"], key="new_batch_model")  # 재학습 없이 사용할 모델을 사용자가 명시한다.
st.caption("모델 weight·train scaler·normal reference limit을 그대로 불러옵니다. 새 CSV로 fit하거나 threshold를 수정하지 않습니다. 완성된 Step 1 trace의 검토 우선순위이며, 원인 확정/불량 확률/수율 예측값은 아닙니다.")  # 버튼이 실제로 수행하는 작업과 범위를 설명한다.
uploaded_csv = st.file_uploader("MaterialID, StepID, duration_ms, feature_1…feature_20이 있는 label-free CSV를 선택하세요", type=["csv"], help="StepID=1 trace가 있어야 합니다. target/is_test는 새 batch에서 필요하지 않습니다.")  # 실무에서 정답이 붙지 않은 새 lot group trace를 업로드할 수 있다.
demo_inference = st.button("공개 label-free 예제 CSV 추론", key="infer_saved_demo", disabled=not (RESULTS_DIR / "st_awfd_label_free_demo_input.csv").is_file())  # 파일 선택 없이도 저장 모델로 실제 GPU 추론을 눈으로 확인한다.
upload_inference = False  # 파일 업로드가 없으면 누를 수 있는 upload 실행은 없다.
if uploaded_csv is not None:  # 새 입력 파일을 선택했을 때만 파일 이름과 점수화 버튼을 표시한다.
    st.caption(f"선택 파일: {uploaded_csv.name} · {uploaded_csv.size:,} bytes · 내부 모델 threshold는 정상 validation에서 고정한 ST-AWFD reference입니다.")  # 입력 파일 이름·크기·reference domain을 보여준다.
    upload_inference = st.button("선택한 저장 모델로 새 CSV 점수화", key="score_external_csv")  # 사용자가 명시적으로 누르면 새로운 batch 추론을 시작한다.
if demo_inference or upload_inference:  # 두 실행 버튼 모두 같은 저장 가중치 추론 경로를 사용한다.
    temporary_path: Path | None = None  # 업로드 임시 파일 정리를 위해 경로를 초기화한다.
    try:  # schema·checkpoint·CUDA 오류를 화면에서 확인할 수 있게 한다.
        input_path = RESULTS_DIR / "st_awfd_label_free_demo_input.csv"  # 공개 예제는 이미 정답 열을 제거한 완성 trace 파일이다.
        if upload_inference:  # 예제 대신 사용자가 선택한 bytes를 사용한다.
            with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temporary_file:  # pandas path interface를 위한 임시 CSV를 만든다.
                temporary_file.write(uploaded_csv.getvalue())  # 현재 업로드 내용만 임시 저장한다.
                temporary_path = Path(temporary_file.name)  # finally에서 정확한 임시 파일만 삭제한다.
                input_path = temporary_path  # 파일 추론 함수로 전달할 실제 입력 경로다.
        with st.spinner("저장된 checkpoint 로드 → 고정 scaler → 실제 추론 중..."):  # 학습 없이도 현재 추론이 실행됨을 보여준다.
            if inference_model.startswith("GPT"):  # 저장된 strict GPT형 Gaussian forecast model을 선택한다.
                from st_awfd_causal_gpt_multihorizon import score_new_csv as score_gpt_csv  # 코드와 notebook의 동일한 추론 함수를 사용한다.
                new_queue = score_gpt_csv(input_path, review_fraction=float(review_fraction))  # label 없이 정상 pattern 예측 surprise와 기여도를 계산한다.
            else:  # 비교용으로 CNN 복원오차 추론을 선택한다.
                new_queue = score_new_csv(input_path, review_fraction=float(review_fraction))  # 기존 저장 CNN과 normal threshold를 재사용한다.
        st.session_state["new_batch_queue"] = new_queue  # 다운로드나 UI 상호작용 후에도 완료 결과를 유지한다.
        st.session_state["new_batch_model_name"] = inference_model  # 결과를 만든 모델 이름을 새 선택값과 구분해 보존한다.
    except Exception as failure:  # 실행되지 않은 입력을 성공 예측처럼 보여주지 않는다.
        st.exception(failure)  # 구체적인 예외와 원인을 표시한다.
    finally:  # 업로드는 처리 종료 후 불필요하게 디스크에 남기지 않는다.
        if temporary_path is not None and temporary_path.exists():  # 현재 실행이 만든 임시 경로만 정리한다.
            temporary_path.unlink()  # 임시 upload 파일 한 장을 지운다.
if "new_batch_queue" in st.session_state:  # 완료한 실제 추론 결과가 있을 때만 표와 다운로드를 표시한다.
    new_queue = st.session_state["new_batch_queue"]  # 마지막으로 성공한 batch 결과를 읽는다.
    st.success(f"저장 모델 추론 완료 · {st.session_state['new_batch_model_name']} · {len(new_queue)} lot groups · 장치 {new_queue.attrs.get('device_name', 'CNN runtime')} · checkpoint epoch {new_queue.attrs.get('selected_epoch', 'CNN saved best')}")  # 실제 사용 모델과 장치/epoch를 확인한다.
    st.dataframe(new_queue, hide_index=True, width="stretch")  # 검토 우선순위와 score·익명 channel 단서를 보여준다.
    st.download_button("새 batch 결과 CSV 다운로드", new_queue.to_csv(index=False).encode("utf-8-sig"), file_name="st_awfd_new_batch_review_queue.csv", mime="text/csv")  # Excel에서 조사·filter·routing할 결과를 내보낸다.
    st.caption("신규 sensor의 물리 정의·단위·순서·공정이 ST-AWFD와 같다는 조건의 공개 데이터 실습입니다. 현장 data에는 tag/recipe/tool mapping과 별도 검증이 필요합니다.")  # 도메인 전이 조건을 설명한다.

with st.expander("입력과 모델 출력", expanded=False):
    st.markdown("정상 공정의 파형을 학습한 뒤, 새 trace의 복원 오차 또는 다음값 예측 분포로 이상 점수를 계산합니다. 점수가 높은 lot을 검토 큐에 배치하고 정상 reference에서 정한 경보 기준과 함께 표시합니다.")
    st.caption("전체 공정 step을 보간한 사후 분석입니다. 실제 센서 이름과 설비 mapping, 최종 die 수율과 공정 조치 결과는 데이터에 포함되지 않습니다.")
