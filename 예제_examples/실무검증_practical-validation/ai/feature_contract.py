"""Fit a small synthetic model; replay serving faults and a named-input fix."""
from __future__ import annotations

import argparse  # 명령행에서 새 결과 폴더를 받습니다.
import copy  # 오류 입력을 만들 때 원래 객체를 보존합니다.
import hashlib  # 입력·모델·소스의 지문을 기록합니다.
import json  # 명시적인 모델 상태와 결과를 텍스트로 저장합니다.
import math  # 유한값 검사와 sigmoid 계산을 사용합니다.
from pathlib import Path  # 운영체제에 맞게 파일 경로를 다룹니다.
import platform  # 재현에 사용한 Python·OS 버전을 기록합니다.


FEATURES = ["temperature_c", "vibration_mm_s", "load_pct"]
UNITS = {"temperature_c": "degC", "vibration_mm_s": "mm/s", "load_pct": "%"}


def number(value):
    """JSON 숫자만 허용하며 bool·NaN·Infinity를 거절합니다."""
    if type(value) not in (int, float):
        raise ValueError("expected a finite JSON number")
    try:
        converted = float(value)  # JSON의 큰 정수도 모델이 사용하는 실수 범위로 바꿉니다.
    except OverflowError as error:
        raise ValueError("JSON number exceeds floating-point range") from error
    if not math.isfinite(converted):
        raise ValueError("expected a finite JSON number")
    return converted


def validate_bundle(bundle):
    """이 예제의 이진 선형 모델 형식만 검사합니다."""
    if type(bundle.get("schema_version")) is not int or bundle["schema_version"] != 1:
        raise ValueError("unsupported schema version")
    names = bundle["features"]
    if (not isinstance(names, list) or not names
            or any(not isinstance(x, str) or not x for x in names)
            or len(set(names)) != len(names)):
        raise ValueError("feature names must be unique nonempty strings")
    if (set(bundle["units"]) != set(names)
            or any(not isinstance(u, str) or not u for u in bundle["units"].values())):
        raise ValueError("unit metadata does not match features")
    for key in ("mean", "scale", "coef"):
        if len(bundle[key]) != len(names):
            raise ValueError("model dimension mismatch")
        for value in bundle[key]:
            number(value)
    if any(value <= 0 for value in bundle["scale"]):
        raise ValueError("scales must be positive")
    number(bundle["intercept"])
    if not 0 < number(bundle["threshold"]) < 1:
        raise ValueError("threshold must lie between zero and one")
    if bundle["classes"] != [0, 1]:
        raise ValueError("only class order [0, 1] is supported")


def safe_probability(row, units, bundle):
    """열 이름으로 정렬하고 학습 때 저장한 변환을 적용합니다."""
    validate_bundle(bundle)
    names = bundle["features"]
    if set(row) != set(names):  # 누락과 예상 밖 열을 조용히 받아들이지 않습니다.
        raise ValueError("request feature set mismatch")
    if units != bundle["units"]:  # 선언된 단위가 다르면 추측해서 환산하지 않습니다.
        raise ValueError("request unit mismatch")
    values = [number(row[name]) for name in names]  # dict 삽입 순서 대신 계약 순서입니다.
    normalized = [(x - m) / s for x, m, s in
                  zip(values, bundle["mean"], bundle["scale"])]
    logit = bundle["intercept"] + math.fsum(
        weight * value for weight, value in zip(bundle["coef"], normalized))
    if not math.isfinite(logit):
        raise ValueError("non-finite model arithmetic")
    if logit >= 0:  # 큰 음수·양수에서 exp의 overflow를 피하는 같은 sigmoid입니다.
        return 1 / (1 + math.exp(-logit))
    exponential = math.exp(logit)
    return exponential / (1 + exponential)


def rejected(call):
    try:
        call()
    except ValueError:
        return True
    return False


def replay(out):
    import numpy as np  # 학습과 독립 배열 계산에만 필요한 외부 패키지입니다.
    import sklearn
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    out.mkdir(parents=True, exist_ok=False)  # 이전 실패 기록을 덮어쓰지 않습니다.
    rng = np.random.default_rng(21)
    train = np.column_stack((rng.uniform(20, 90, 160),
                             rng.uniform(.1, 8, 160), rng.uniform(10, 100, 160)))
    # 아래 규칙은 자체 학습 자료의 정답이며 실제 설비의 불량 규격이 아닙니다.
    labels = (train[:, 1] + .02 * train[:, 0] - .015 * train[:, 2] > 4).astype(int)
    pipeline = make_pipeline(StandardScaler(), LogisticRegression(C=2, max_iter=500))
    pipeline.fit(train, labels)
    scaler, classifier = pipeline.steps[0][1], pipeline.steps[1][1]
    bundle = {"schema_version": 1, "features": FEATURES, "units": UNITS,
              "mean": scaler.mean_.tolist(), "scale": scaler.scale_.tolist(),
              "coef": classifier.coef_[0].tolist(),
              "intercept": float(classifier.intercept_[0]),
              "classes": classifier.classes_.tolist(), "threshold": .5}
    model_path = out / "model.json"
    model_path.write_text(json.dumps(bundle, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    restored = json.loads(model_path.read_text(encoding="utf-8"))
    rows = [dict(zip(FEATURES, values)) for values in
            [[30., .5, 80.], [80., 7., 20.], [45., 3., 60.], [70., 4.5, 75.]]]
    raw = np.array([[row[name] for name in FEATURES] for row in rows])
    reference = pipeline.predict_proba(raw)[:, 1]
    fixed = np.array([safe_probability(row, UNITS, restored) for row in rows])
    order = ["load_pct", "temperature_c", "vibration_mm_s"]
    wrong_order = pipeline.predict_proba(np.array([[row[n] for n in order] for row in rows]))[:, 1]
    no_scaler = classifier.predict_proba(raw)[:, 1]
    refitted = classifier.predict_proba(StandardScaler().fit_transform(raw))[:, 1]
    singleton_refit = classifier.predict_proba(StandardScaler().fit_transform(raw[:1]))[0, 1]
    bad_rows = {}
    missing = dict(rows[0]); missing.pop("load_pct"); bad_rows["missing_feature"] = missing
    extra = dict(rows[0], target=0); bad_rows["unexpected_feature"] = extra
    for name, value in (("nan", float("nan")), ("infinity", float("inf")),
                        ("bool", True), ("string", "0.5"), ("huge_integer", 10**400)):
        bad = dict(rows[0]); bad["vibration_mm_s"] = value; bad_rows[name] = bad
    refusals = {name: rejected(lambda row=row: safe_probability(row, UNITS, restored))
                for name, row in bad_rows.items()}
    wrong_units = dict(UNITS, vibration_mm_s="um/s")
    refusals["unit_mismatch"] = rejected(lambda: safe_probability(rows[0], wrong_units, restored))
    zero_scale = copy.deepcopy(restored); zero_scale["scale"][1] = 0
    refusals["zero_scale"] = rejected(lambda: safe_probability(rows[0], UNITS, zero_scale))
    wrong_dimension = copy.deepcopy(restored); wrong_dimension["coef"].pop()
    refusals["model_dimension"] = rejected(lambda: safe_probability(rows[0], UNITS, wrong_dimension))
    error = float(np.max(np.abs(fixed - reference)))
    decisions = reference >= .5
    changed = {"feature_order": int(np.sum((wrong_order >= .5) != decisions)),
               "scaler_omitted": int(np.sum((no_scaler >= .5) != decisions)),
               "request_refit": int(np.sum((refitted >= .5) != decisions))}
    reversed_keys = [dict(reversed(list(row.items()))) for row in rows]
    checks = {"export_matches_pipeline": error < 1e-12,
              "dict_order_independent": all(safe_probability(a, UNITS, restored) == safe_probability(b, UNITS, restored)
                                            for a, b in zip(rows, reversed_keys)),
              "feature_order_fault_detected": changed["feature_order"] > 0,
              "missing_scaler_fault_detected": changed["scaler_omitted"] > 0,
              "request_refit_changes_scores": float(np.max(np.abs(refitted - reference))) > .01,
              "request_batch_dependency_detected": abs(float(refitted[0]) - float(singleton_refit)) > .01,
              "invalid_inputs_rejected": all(refusals.values())}
    input_text = json.dumps({"training": train.tolist(), "labels": labels.tolist(), "requests": rows},
                            sort_keys=True, allow_nan=False)
    (out / "input.json").write_text(input_text + "\n", encoding="utf-8")
    result = {"scope": "synthetic CPU training and serving replay; no industrial data",
              "runtime": {"python": platform.python_version(), "numpy": np.__version__,
                          "scikit_learn": sklearn.__version__, "os": platform.system()},
              "train_rows": len(train), "request_rows": len(rows),
              "probabilities": {"pipeline": reference.tolist(), "exported": fixed.tolist(),
                                "wrong_order": wrong_order.tolist(), "scaler_omitted": no_scaler.tolist(),
                                "request_refit": refitted.tolist(), "singleton_refit_first": float(singleton_refit)},
              "changed_decisions": changed, "max_export_error": error,
              "rejected_inputs": refusals, "checks": checks,
              "input_sha256": hashlib.sha256((out / "input.json").read_bytes()).hexdigest(),
              "model_sha256": hashlib.sha256(model_path.read_bytes()).hexdigest(),
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (out / "report.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    if not all(checks.values()):
        raise AssertionError("replay did not produce the expected controls")
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    replay(parser.parse_args().out)
