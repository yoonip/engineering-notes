#!/usr/bin/env python3
"""Matched-serial ATE/SLT analysis on deterministic synthetic data."""
import argparse
from collections import Counter
import csv
import json
from pathlib import Path


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def make_dataset(folder):
    ate, slt, truth = [], [], []
    for index in range(1000):
        serial = f"SIM-{index:04d}"
        if index < 900:
            ar, sr, good = "PASS", "PASS", True
        elif index < 960:
            ar, sr, good = "PASS", "FAIL", index < 930
        elif index < 980:
            ar, sr, good = "FAIL", "PASS", index < 970
        else:
            ar, sr, good = "FAIL", "FAIL", False
        common = {"serial": serial, "lot": f"L{index // 250}",
                  "temperature_c": "25", "voltage_v": "0.80"}
        ate.append(dict(common, result=ar, site=f"A{index % 4}",
                        program="ate_sim_v1"))
        slt.append(dict(common, result=sr, site=f"S{index % 4}",
                        firmware="slt_sim_v1", test="fixed_seed_workload"))
        truth.append({"serial": serial, "classification":
                      "GOOD" if good else "BAD",
                      "basis": "synthetic_independent_ground_truth"})
    # Deliberately different row ordering: join by serial, never row number.
    write_csv(folder / "ate.csv", ate)
    write_csv(folder / "slt.csv", list(reversed(slt)))
    write_csv(folder / "truth.csv", truth)


def load_unique(path):
    with path.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    result = {}
    for row in rows:
        serial = row.get("serial", "")
        if not serial or serial in result:
            raise ValueError(f"missing or duplicate serial in {path}: {serial}")
        result[serial] = row
    if not result:
        raise ValueError(f"empty data: {path}")
    return result


def analyse(folder, include_truth):
    ate = load_unique(folder / "ate.csv")
    slt = load_unique(folder / "slt.csv")
    if ate.keys() != slt.keys():
        raise ValueError("Unmatched serials: repair data before correlation")
    matrix = Counter()
    for serial in sorted(ate):
        a, s = ate[serial], slt[serial]
        if a["result"] not in {"PASS", "FAIL"}:
            raise ValueError("ATE result is not a completed valid test")
        if s["result"] not in {"PASS", "FAIL"}:
            raise ValueError("SLT result is not a completed valid test")
        for condition in ["lot", "temperature_c", "voltage_v"]:
            if a[condition] != s[condition]:
                raise ValueError(f"Condition mismatch: {serial} {condition}")
        matrix[(a["result"], s["result"])] += 1
    n = len(ate)
    disagreement = matrix[("PASS", "FAIL")] + matrix[("FAIL", "PASS")]
    report = {"simulation_only": True, "parts": n,
              "matrix_ate_slt": {f"{a}/{s}": matrix[(a, s)]
                                 for a in ["PASS", "FAIL"]
                                 for s in ["PASS", "FAIL"]},
              "agreement": 1 - disagreement / n,
              "warning": "Disagreement alone cannot identify escape/overkill"}
    if include_truth:
        truth = load_unique(folder / "truth.csv")
        if truth.keys() != ate.keys():
            raise ValueError("Truth serials must match all test serials")
        for serial, row in truth.items():
            if row.get("classification") not in {"GOOD", "BAD"}:
                raise ValueError(f"Invalid truth classification: {serial}")
        confusion = Counter((slt[serial]["result"],
                             truth[serial]["classification"])
                            for serial in slt)
        good = sum(v for (r, t), v in confusion.items() if t == "GOOD")
        bad = sum(v for (r, t), v in confusion.items() if t == "BAD")
        passed = sum(v for (r, t), v in confusion.items() if r == "PASS")
        false_accept = confusion[("PASS", "BAD")]
        false_reject = confusion[("FAIL", "GOOD")]
        # A zero denominator means unavailable, never a measured zero rate.
        per_bad = false_accept / bad if bad else None
        per_good = false_reject / good if good else None
        shipped_fraction = false_accept / passed if passed else None
        metrics = {
            "good_parts": good, "bad_parts": bad, "passed_parts": passed,
            "false_accept_parts": false_accept,
            "false_reject_parts": false_reject,
            "false_accept_per_bad": per_bad,
            "false_reject_per_good": per_good,
            "shipped_defective_fraction": shipped_fraction,
            "shipped_dppm": (shipped_fraction * 1e6
                             if shipped_fraction is not None else None),
            "slt_yield": passed / n}
        metrics["undefined_metrics"] = [
            key for key, value in metrics.items() if value is None]
        report["independent_truth_metrics"] = metrics
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="results/correlation")
    parser.add_argument("--analyse-existing", action="store_true")
    parser.add_argument("--with-truth", action="store_true")
    args = parser.parse_args()
    folder = Path(args.out)
    folder.mkdir(parents=True, exist_ok=True)
    if not args.analyse_existing:
        make_dataset(folder)
    report = analyse(folder, args.with_truth)
    text = json.dumps(report, indent=2)
    (folder / "report.json").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
