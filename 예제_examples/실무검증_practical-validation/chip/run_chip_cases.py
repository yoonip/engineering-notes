#!/usr/bin/env python3
"""Replay arithmetic, test-data identity and split-window faults offline.

Only Python's standard library is used. No chip, ATE, PHY or instrument is
connected. Existing practical-silicon-lab functions are imported unchanged.
The overall PASS means expected faults were detected, not that faulty DUTs pass.
"""
import sys

sys.dont_write_bytecode = True

import argparse
from collections import Counter
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import shutil


ROOT = Path(__file__).resolve().parents[3]
LAB = ROOT / "프로젝트_projects" / "practical-silicon-lab"
SOURCE_PATHS = [LAB / "validation" / name for name in
                ("npu.py", "correlation.py", "training_ber.py")]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_hashes():
    return {path.relative_to(ROOT).as_posix(): sha256(path)
            for path in SOURCE_PATHS}


def load_module(path):
    spec = importlib.util.spec_from_file_location("replay_" + path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def save_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")


class Checks:
    """Record equality and expected rejection without using removable assert."""
    def __init__(self):
        self.records = []

    def equal(self, name, actual, expected):
        self.records.append({"name": name, "status":
                             "PASS" if actual == expected else "FAIL",
                             "expected": expected, "observed": actual})

    def rejects(self, name, function, message):
        try:
            function()
        except ValueError as error:
            self.records.append({"name": name, "status":
                                 "PASS" if message in str(error) else "FAIL",
                                 "expected_exception": "ValueError",
                                 "observed_exception": type(error).__name__,
                                 "message": str(error)})
        else:
            self.records.append({"name": name, "status": "FAIL",
                                 "expected_exception": "ValueError",
                                 "observed_exception": None})


def validate_int8(matrix, rows, columns):
    if len(matrix) != rows or any(len(row) != columns for row in matrix):
        raise ValueError("shape mismatch")
    if any(type(value) is not int or not -128 <= value <= 127
           for row in matrix for value in row):
        raise ValueError("signed int8 integer required")


def narrow(value, contract):
    """Explicit mathematical conversion, not C signed-overflow execution."""
    if contract == "int32":
        if not -(1 << 31) <= value < (1 << 31):
            raise ValueError("int32 output out of range")
        return value
    if contract == "wrap8":
        return (value + 128) % 256 - 128
    if contract == "saturate8":
        return max(-128, min(127, value))
    raise ValueError("unknown output contract")


def arithmetic(out, module, checks):
    folder = out / "arithmetic"
    folder.mkdir()
    contract = {"simulation_only": True,
                "image": [[20, -3, 4], [5, 6, -7], [8, 9, 10]],
                "weights": [[7, -2], [3, 4]],
                "layout": "HW_row_major", "input": "signed_int8",
                "operation": "valid_cross_correlation_stride1",
                "accumulator_and_output": "signed_int32",
                "scale_zero_point_bias_activation": "not_modelled"}
    save_json(folder / "input.json", contract)
    image, weights = contract["image"], contract["weights"]
    validate_int8(image, 3, 3)
    validate_int8(weights, 2, 2)
    # Hand-calculated fixed oracle; neither existing implementation generates it.
    oracle = [[185, -39], [83, 123]]
    checks.equal("arithmetic.scalar_reference", module.reference(image, weights), oracle)
    cases = []
    for fault in ("none", "layout", "stale", "overflow"):
        actual = module.device_model(image, weights, fault)
        mismatch = [{"y": y, "x": x, "expected": oracle[y][x],
                     "actual": actual[y][x]}
                    for y in range(2) for x in range(2)
                    if actual[y][x] != oracle[y][x]]
        case = {"injected_fault": fault, "dut_status":
                "FAIL" if mismatch else "PASS", "expected_fault": fault != "none",
                "input_sha256": sha256(folder / "input.json"),
                "expected": oracle, "actual": actual, "mismatches": mismatch}
        cases.append(case)
        checks.equal("arithmetic.detect_" + fault, bool(mismatch), fault != "none")
    checks.equal("arithmetic.wrap_185", cases[-1]["actual"][0][0], -71)
    # Boundary products remain within signed int32 for this four-product kernel.
    for label, value, weight, expected in (
            ("positive", -128, -128, 65536),
            ("negative", -128, 127, -65024)):
        extreme_image = [[value] * 3 for _ in range(3)]
        extreme_weights = [[weight] * 2 for _ in range(2)]
        checks.equal("arithmetic.int32_boundary_" + label,
                     module.device_model(extreme_image, extreme_weights, "none"),
                     [[expected] * 2 for _ in range(2)])
    values = [127, 128, -128, -129, 65536]
    conversion = {kind: [narrow(v, kind) for v in values]
                  for kind in ("int32", "wrap8", "saturate8")}
    checks.equal("arithmetic.wrap_contract", conversion["wrap8"],
                 [127, -128, -128, 127, 0])
    checks.equal("arithmetic.saturation_contract", conversion["saturate8"],
                 [127, 127, -128, -128, 127])
    checks.equal("arithmetic.wide_contract", conversion["int32"], values)
    for name, matrix, rows, columns, message in (
            ("out_of_range", [[128]], 1, 1, "int8"),
            ("float", [[1.0]], 1, 1, "int8"),
            ("bool", [[True]], 1, 1, "int8"),
            ("ragged", [[1, 2], [3]], 2, 2, "shape")):
        checks.rejects("arithmetic.reject_" + name,
                       lambda m=matrix, r=rows, c=columns: validate_int8(m, r, c),
                       message)
    checks.rejects("arithmetic.reject_int32_overflow",
                   lambda: narrow(1 << 31, "int32"), "range")
    # A symmetric fixture cannot reveal a transpose fault: record this blind spot.
    symmetric = [[1] * 3 for _ in range(3)]
    checks.equal("arithmetic.symmetric_blind_spot",
                 module.device_model(symmetric, weights, "layout"),
                 module.reference(symmetric, weights))
    report = {"cases": cases, "narrowing_inputs": values,
              "narrowing_outputs": conversion,
              "coverage_limit": "symmetric input hides transpose; no physical cache tested"}
    save_json(folder / "report.json", report)
    return report


def read_rows(path):
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def row_zip_report(ate, slt):
    """Deliberately wrong control: equal length does not establish identity."""
    pairs = list(zip(ate, slt))
    matrix = Counter((a["result"], s["result"]) for a, s in pairs)
    return {"pairs": len(pairs),
            "serial_mismatch_pairs": sum(a["serial"] != s["serial"] for a, s in pairs),
            "agreement": sum(a["result"] == s["result"] for a, s in pairs) / len(pairs),
            "matrix_ate_slt": {f"{a}/{s}": matrix[(a, s)]
                               for a in ("PASS", "FAIL") for s in ("PASS", "FAIL")}}


def correlation(out, module, checks):
    folder = out / "correlation"
    folder.mkdir()
    standard = folder / "thousand_parts"
    standard.mkdir()
    module.make_dataset(standard)
    proper = module.analyse(standard, True)
    naive = row_zip_report(read_rows(standard / "ate.csv"),
                           read_rows(standard / "slt.csv"))
    checks.equal("correlation.matrix_1000", proper["matrix_ate_slt"],
                 {"PASS/PASS": 900, "PASS/FAIL": 60, "FAIL/PASS": 20, "FAIL/FAIL": 20})
    metrics = proper["independent_truth_metrics"]
    checks.equal("correlation.agreement", proper["agreement"], .92)
    for key, expected in (("false_accept_per_bad", 10 / 60),
                          ("false_reject_per_good", 30 / 940),
                          ("shipped_defective_fraction", 10 / 920),
                          ("slt_yield", 920 / 1000)):
        checks.equal("correlation." + key, metrics[key], expected)
    save_json(standard / "serial_join.json", proper)
    save_json(standard / "wrong_row_zip.json", naive)

    # Same CSV pair, two algorithms: row order manufactures perfect agreement.
    tiny = folder / "four_parts"
    tiny.mkdir()
    common = {"lot": "EDUCATION", "temperature_c": "25", "voltage_v": "0.80"}
    ate = [dict(common, serial=f"T-{i}", result="PASS" if i < 2 else "FAIL")
           for i in range(4)]
    slt = [dict(common, serial=f"T-{i}", result="PASS" if i >= 2 else "FAIL")
           for i in (2, 3, 0, 1)]
    module.write_csv(tiny / "ate.csv", ate)
    module.write_csv(tiny / "slt.csv", slt)
    tiny_proper = module.analyse(tiny, False)
    tiny_naive = row_zip_report(read_rows(tiny / "ate.csv"), read_rows(tiny / "slt.csv"))
    checks.equal("correlation.four_serial_agreement", tiny_proper["agreement"], 0.0)
    checks.equal("correlation.four_row_zip_false_agreement", tiny_naive["agreement"], 1.0)
    checks.equal("correlation.four_row_zip_identity_mismatch", tiny_naive["serial_mismatch_pairs"], 4)
    save_json(tiny / "serial_join.json", tiny_proper)
    save_json(tiny / "wrong_row_zip.json", tiny_naive)

    mutations = (
        ("duplicate_id", "slt.csv", lambda rows: rows + [dict(rows[0])], "duplicate"),
        ("missing_row", "slt.csv", lambda rows: rows[:-1], "Unmatched"),
        ("empty_id", "slt.csv", lambda rows: [dict(rows[0], serial="")] + rows[1:], "missing"),
        ("condition", "slt.csv", lambda rows: [dict(rows[0], voltage_v="0.81")] + rows[1:], "Condition"),
        ("invalid_result", "slt.csv", lambda rows: [dict(rows[0], result="TIMEOUT")] + rows[1:], "valid test"),
        ("invalid_truth", "truth.csv", lambda rows: [dict(rows[0], classification="UNKNOWN")] + rows[1:], "Invalid truth"),
    )
    for name, filename, mutate, message in mutations:
        changed = folder / ("reject_" + name)
        changed.mkdir()
        for csv_name in ("ate.csv", "slt.csv", "truth.csv"):
            shutil.copyfile(standard / csv_name, changed / csv_name)
        module.write_csv(changed / filename, mutate(read_rows(changed / filename)))
        checks.rejects("correlation.reject_" + name,
                       lambda path=changed: module.analyse(path, True), message)
    checks.equal("correlation.no_truth_no_escape_claim",
                 "independent_truth_metrics" in module.analyse(standard, False), False)
    zero = folder / "zero_denominators"
    zero.mkdir()
    one = dict(common, serial="ONE", result="FAIL")
    module.write_csv(zero / "ate.csv", [one])
    module.write_csv(zero / "slt.csv", [one])
    module.write_csv(zero / "truth.csv", [{"serial": "ONE", "classification": "GOOD"}])
    zero_metrics = module.analyse(zero, True)["independent_truth_metrics"]
    checks.equal("correlation.zero_bad_is_unavailable", zero_metrics["false_accept_per_bad"], None)
    checks.equal("correlation.zero_passed_is_unavailable", zero_metrics["shipped_defective_fraction"], None)
    report = {"simulation_only": True, "thousand_parts": proper,
              "wrong_row_zip_1000": naive, "four_parts_serial_join": tiny_proper,
              "four_parts_wrong_row_zip": tiny_naive,
              "zero_denominator_metrics": zero_metrics}
    save_json(folder / "report.json", report)
    return report


def training(out, module, checks):
    folder = out / "training"
    folder.mkdir()
    taps = [1, 2, 3, 9, 10]
    naive = (min(taps) + max(taps)) // 2
    proper = module.longest_window(taps)
    checks.equal("training.global_midpoint_fails", naive in taps, False)
    checks.equal("training.contiguous_midpoint", proper["chosen_tap"], 2)
    checks.equal("training.chosen_tap_was_tested_passing", proper["chosen_tap"] in taps, True)
    checks.equal("training.margin_steps", proper["margin_steps"], 1)
    checks.equal("training.no_pass", module.longest_window([])["pass"], False)
    checks.equal("training.duplicates_and_tie", module.longest_window([11, 2, 1, 10, 2])["chosen_tap"], 1)
    checks.equal("training.singleton_margin", module.longest_window([7])["margin_steps"], 0)
    grid = [[True, True, False, False], [True, True, True, False], [True] * 4]
    checks.equal("shmoo.point_pass_count", sum(sum(row) for row in grid), 9)
    report = {"simulation_only": True, "passing_taps": taps,
              "wrong_global_midpoint": naive, "wrong_choice_passed": naive in taps,
              "contiguous_window": proper,
              "synthetic_shmoo": {"voltage_v": [.90, .95, 1.00],
                                  "frequency_mhz": [80, 100, 120, 140],
                                  "passed": grid, "point_pass_fraction": 9 / 12},
              "limits": "one-dimensional integer taps; no measured PHY or 2D connected-region solver"}
    save_json(folder / "input.json", {"passing_taps": taps, "grid": grid})
    save_json(folder / "report.json", report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True,
                        help="new output folder; existing paths are rejected")
    args = parser.parse_args()
    try:
        args.out.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        parser.error("--out must be a new folder; existing output was preserved")
    before = source_hashes()
    checks = Checks()
    modules = [load_module(path) for path in SOURCE_PATHS]
    unexpected = None
    try:
        arithmetic(args.out, modules[0], checks)
        correlation(args.out, modules[1], checks)
        training(args.out, modules[2], checks)
    except Exception as error:
        unexpected = {"type": type(error).__name__, "message": str(error)}
    after = source_hashes()
    checks.equal("sources.unchanged", after, before)
    failed = sum(record["status"] != "PASS" for record in checks.records)
    report = {"schema_version": 1, "simulation_only": True,
              "status": "PASS" if not failed and unexpected is None else "FAIL",
              "scope": "offline arithmetic and synthetic CSV/tap fixtures",
              "runtime": {"python": platform.python_version(),
                          "implementation": platform.python_implementation(),
                          "os": platform.system(), "machine": platform.machine()},
              "counts": {"checks": len(checks.records), "failed": failed},
              "checks": checks.records, "unexpected_error": unexpected,
              "source_sha256_before": before, "source_sha256_after": after,
              "replay_script_sha256": sha256(Path(__file__)),
              "input_sha256": {p.relative_to(args.out).as_posix(): sha256(p)
                               for p in sorted(args.out.rglob("*"))
                               if p.is_file() and (p.suffix == ".csv" or p.name == "input.json")},
              "not_run": ["physical_chip", "ATE", "DDR_PHY", "RTL", "CMSIS-NN_execution"]}
    save_json(args.out / "summary.json", report)
    print(json.dumps({"status": report["status"], "counts": report["counts"],
                      "unexpected_error": unexpected}, ensure_ascii=False))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
