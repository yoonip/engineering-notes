"""Compare row and group holdouts on repeated synthetic measurements."""
from __future__ import annotations

import argparse  # 명령행에서 새 출력 폴더를 받습니다.
import hashlib  # 실제 입력과 소스의 SHA-256을 기록합니다.
import json  # 분할 인덱스와 예측 결과를 저장합니다.
from pathlib import Path  # 경로의 생성·읽기·쓰기를 담당합니다.
import platform  # 실행 환경을 기록합니다.


def require_group_separation(groups, train_ids, test_ids):
    """새 lot 성능을 평가할 때 같은 group이 섞인 분할을 거절합니다."""
    overlap = set(groups[train_ids]) & set(groups[test_ids])  # &는 두 ID 집합의 교집합입니다.
    if overlap:
        raise ValueError(f"overlapping groups: {len(overlap)}")


def replay(out):
    import numpy as np
    import sklearn
    from sklearn.metrics import accuracy_score, confusion_matrix
    from sklearn.model_selection import GroupShuffleSplit, train_test_split
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    out.mkdir(parents=True, exist_ok=False)  # 이전 결과 폴더가 있으면 덮어쓰기를 거절합니다.
    rng = np.random.default_rng(20261021)
    centroids = rng.normal(size=(40, 6))  # 40개 group마다 다른 센서 지문을 만듭니다.
    group_labels = np.array([0, 1] * 20)
    rng.shuffle(group_labels)  # class와 새 group의 센서 중심에는 학습 가능한 규칙을 넣지 않습니다.
    groups = np.repeat(np.arange(40), 8)  # 같은 group을 8번씩 관측한 총 320행입니다.
    values = centroids[groups] + rng.normal(scale=.001, size=(320, 6))
    labels = group_labels[groups]
    row_train, row_test = train_test_split(np.arange(len(values)), test_size=.25,
                                          random_state=17, stratify=labels)
    grouped = GroupShuffleSplit(n_splits=1, test_size=.25, random_state=17)
    group_train, group_test = next(grouped.split(values, labels, groups=groups))  # 첫 분할을 꺼냅니다.

    def measure(train_ids, test_ids):
        # 거리 기반 모델을 학습 집합에만 fit하고 같은 설정으로 비교합니다.
        model = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=1))
        model.fit(values[train_ids], labels[train_ids])  # 지정한 학습 행으로만 통계와 모델을 맞춥니다.
        predicted = model.predict(values[test_ids])  # 평가 행의 class를 예측합니다.
        matrix = confusion_matrix(labels[test_ids], predicted, labels=[0, 1])
        return {"train_rows": len(train_ids), "test_rows": len(test_ids),
                "train_groups": sorted(set(map(int, groups[train_ids]))),
                "test_groups": sorted(set(map(int, groups[test_ids]))),
                "overlap_groups": sorted(set(map(int, groups[train_ids])) & set(map(int, groups[test_ids]))),
                "accuracy": float(accuracy_score(labels[test_ids], predicted)),
                "confusion_true_rows_predicted_columns": matrix.tolist(),
                "prediction": predicted.tolist(), "truth": labels[test_ids].tolist()}, model

    row_result, _ = measure(row_train, row_test)
    group_result, group_model = measure(group_train, group_test)
    overlap_rejected = False
    try:
        require_group_separation(groups, row_train, row_test)
    except ValueError:
        overlap_rejected = True
    require_group_separation(groups, group_train, group_test)
    # 평가 쪽 값만 바꿔도 저장한 학습 scaler는 바뀌지 않아야 합니다.
    saved_mean = group_model.steps[0][1].mean_.copy()
    shifted = values.copy(); shifted[group_test] += 100
    group_model.predict(shifted[group_test])
    fixed_mean_delta = float(np.max(np.abs(group_model.steps[0][1].mean_ - saved_mean)))
    leaked = StandardScaler().fit(values)
    leaked_shifted = StandardScaler().fit(shifted)
    leaked_mean_delta = float(np.max(np.abs(leaked_shifted.mean_ - leaked.mean_)))
    checks = {"row_group_overlap_rejected": overlap_rejected,
              "group_holdout_is_disjoint": not group_result["overlap_groups"],
              "same_group_rows_are_memorized": row_result["accuracy"] == 1,
              "new_group_score_is_lower": group_result["accuracy"] < row_result["accuracy"],
              "fixed_training_mean_unchanged": fixed_mean_delta == 0,
              "full_dataset_fit_reads_test_values": abs(leaked_mean_delta - 25) < 1e-10}
    dataset = {"features": values.tolist(), "labels": labels.tolist(), "groups": groups.tolist(),
               "row_train": row_train.tolist(), "row_test": row_test.tolist(),
               "group_train": group_train.tolist(), "group_test": group_test.tolist()}
    (out / "input.json").write_text(json.dumps(dataset, allow_nan=False) + "\n", encoding="utf-8")
    result = {"scope": "synthetic group-fingerprint example; not manufacturing accuracy",
              "runtime": {"python": platform.python_version(), "numpy": np.__version__,
                          "scikit_learn": sklearn.__version__, "os": platform.system()},
              "rows": len(values), "groups": 40, "row_holdout": row_result,
              "group_holdout": group_result, "fixed_training_mean_delta": fixed_mean_delta,
              "leaky_all_rows_mean_delta": leaked_mean_delta, "checks": checks,
              "input_sha256": hashlib.sha256((out / "input.json").read_bytes()).hexdigest(),
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (out / "report.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    if not all(checks.values()):
        raise AssertionError("group replay controls did not hold")
    print(json.dumps({"row_accuracy": row_result["accuracy"],
                      "group_accuracy": group_result["accuracy"],
                      "overlap_group_count": len(row_result["overlap_groups"]),
                      "checks": checks, "report": str(out / "report.json")}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    replay(parser.parse_args().out)
