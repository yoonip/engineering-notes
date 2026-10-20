#!/usr/bin/env python3
"""Validate subprocess execution and structured chip-job evidence separately.

All children are controlled synthetic fixtures. No physical chip, RTL simulator,
ATE or instrument is connected. The literal oracle is independent of child code.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
import uuid


HERE = Path(__file__).resolve().parent
CHILD = HERE / "fixture_child.py"
# 고정한 손계산: 140+6+15+24=185, 4*16384=65536, 3-3=0입니다.
ORACLE = {"signed_dot": 185, "edge_dot": 65536, "zero_dot": 0}
PLAN = [
    ("normal", "ACCEPT"), ("dut_fail", "DUT_FAIL"),
    ("lying_pass", "FALSE_VERDICT"), ("stdout_only", "MISSING_RESULT"),
    ("stale_result", "RUN_ID"), ("wrong_hash", "INPUT_HASH"),
    ("missing_case", "CASE_SET"), ("duplicate_case", "DUPLICATE_CASE"),
    ("unknown_case", "CASE_SET"), ("schema_bool", "SCHEMA"),
    ("wrong_type", "FIELD_TYPE"), ("bad_json", "INVALID_JSON"),
    ("duplicate_json_key", "INVALID_JSON"), ("nan", "INVALID_JSON"),
    ("nonzero_exit", "EXIT_CODE"), ("timeout", "TIMEOUT"),
]


class InvalidReport(ValueError):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    # 명시적 UTF-8·LF 바이트로 쓰므로 운영체제의 줄바꿈 변환을 피합니다.
    path.write_bytes((json.dumps(value, indent=2, allow_nan=False) + "\n").encode("utf-8"))


def unique_object(pairs):
    value = {}
    for key, item in pairs:  # JSON의 같은 key가 앞 값을 덮기 전에 검사합니다.
        if key in value:
            raise ValueError("duplicate JSON key: " + key)
        value[key] = item
    return value


def reject_constant(value):
    raise ValueError("non-standard JSON constant: " + value)


def read_report(path):
    if not path.is_file():
        raise InvalidReport("MISSING_RESULT", "child produced no result file")
    if path.stat().st_size > 65536:  # 이 작은 결과 형식의 크기 상한입니다.
        raise InvalidReport("INVALID_JSON", "result exceeds 64 KiB")
    try:
        return json.loads(path.read_text(encoding="utf-8"),
                          object_pairs_hook=unique_object, parse_constant=reject_constant)
    except (ValueError, UnicodeError) as error:
        raise InvalidReport("INVALID_JSON", str(error)) from error


def validate_report(report, run_id, input_hash):
    expected_keys = {"schema_version", "run_id", "input_sha256", "status", "cases"}
    if (type(report) is not dict or set(report) != expected_keys
            or type(report["schema_version"]) is not int or report["schema_version"] != 1):
        raise InvalidReport("SCHEMA", "expected exact version-1 result fields")
    if report["run_id"] != run_id:
        raise InvalidReport("RUN_ID", "result belongs to another attempt")
    if report["input_sha256"] != input_hash:
        raise InvalidReport("INPUT_HASH", "result does not match actual input bytes")
    if type(report["cases"]) is not list:
        raise InvalidReport("SCHEMA", "cases must be a list")
    found = {}
    for row in report["cases"]:
        if (type(row) is not dict or set(row) != {"id", "status", "actual"}
                or type(row["id"]) is not str or not row["id"]):
            raise InvalidReport("SCHEMA", "invalid case fields")
        if row["id"] in found:
            raise InvalidReport("DUPLICATE_CASE", "duplicate case: " + row["id"])
        found[row["id"]] = row
    if set(found) != set(ORACLE):
        raise InvalidReport("CASE_SET", "planned and reported case IDs differ")
    any_failed = False
    for name, expected in ORACLE.items():
        row = found[name]
        if type(row["actual"]) is not int:  # bool·float·문자열을 같은 값으로 받아들이지 않습니다.
            raise InvalidReport("FIELD_TYPE", "actual must be an integer")
        expected_status = "PASS" if row["actual"] == expected else "FAIL"
        if row["status"] != expected_status:
            raise InvalidReport("FALSE_VERDICT", "reported verdict conflicts with independent oracle")
        any_failed = any_failed or expected_status == "FAIL"
    aggregate = "FAIL" if any_failed else "PASS"
    if report["status"] != aggregate:
        raise InvalidReport("FALSE_VERDICT", "aggregate status does not match case verdicts")
    return "DUT_FAIL" if any_failed else "ACCEPT"


def make_input(run_id):
    return {"simulation_only": True, "run_id": run_id, "operation": "int32_dot4",
            "cases": [{"id": "signed_dot", "left": [20, -3, 5, 6], "right": [7, -2, 3, 4]},
                      {"id": "edge_dot", "left": [-128] * 4, "right": [-128] * 4},
                      {"id": "zero_dot", "left": [0, 1, -1, 5], "right": [127, 3, 3, 0]}]}


def as_text(value):
    # TimeoutExpired의 캡처 값은 text=True여도 bytes일 수 있습니다.
    return value.decode("utf-8", errors="replace") if isinstance(value, bytes) else (value or "")


def run_one(folder, mode, expected_code):
    folder.mkdir()  # 실행마다 별도 폴더를 만듭니다.
    run_id = uuid.uuid4().hex  # 같은 입력 값이어도 시도마다 식별자가 다릅니다.
    input_path, result_path = folder / "input.json", folder / "result.json"
    write_json(input_path, make_input(run_id))
    input_hash = sha256(input_path)
    old_hash = None
    if mode == "stale_result":
        old = {"schema_version": 1, "run_id": "OLD-ATTEMPT", "input_sha256": "f" * 64,
               "status": "PASS", "cases": [{"id": k, "status": "PASS", "actual": v}
                                            for k, v in ORACLE.items()]}
        write_json(result_path, old)  # 이전 결과를 흉내 낸 대조 파일을 의도적으로 심습니다.
        old_hash = sha256(result_path)
    command = [sys.executable, "-B", str(CHILD), "--input", str(input_path),
               "--result", str(result_path), "--mode", mode]
    timeout_s = .25 if mode == "timeout" else 5.0
    started = time.monotonic()
    stdout, stderr, returncode, timed_out = "", "", None, False
    try:
        completed = subprocess.run(command, cwd=folder, stdin=subprocess.DEVNULL,
                                   capture_output=True, text=True, encoding="utf-8",
                                   timeout=timeout_s, check=False, shell=False,
                                   env=dict(os.environ, PYTHONIOENCODING="utf-8",
                                            PYTHONDONTWRITEBYTECODE="1"))
        stdout, stderr, returncode = completed.stdout, completed.stderr, completed.returncode
    except subprocess.TimeoutExpired as error:
        stdout, stderr, timed_out = as_text(error.stdout), as_text(error.stderr), True
    (folder / "stdout.txt").write_text(stdout, encoding="utf-8")
    (folder / "stderr.txt").write_text(stderr, encoding="utf-8")
    error_message = None
    if timed_out:
        observed_code = "TIMEOUT"
    elif returncode != 0:
        observed_code = "EXIT_CODE"
    else:
        try:
            observed_code = validate_report(read_report(result_path), run_id, input_hash)
        except InvalidReport as error:
            observed_code, error_message = error.code, str(error)
    record = {"fixture": mode, "simulation_only": True, "command": command,
              "run_id": run_id, "input_sha256": input_hash,
              "process": {"returncode": returncode, "timed_out": timed_out,
                          "timeout_s": timeout_s, "host_elapsed_s": time.monotonic() - started},
              "naive_exit_zero": returncode == 0 and not timed_out,
              "naive_stdout_pass": returncode == 0 and not timed_out and "PASS" in stdout,
              "observed": observed_code, "expected": expected_code,
              "check": "PASS" if observed_code == expected_code else "FAIL",
              "diagnostic": error_message, "seeded_old_result_sha256": old_hash,
              "result_sha256": sha256(result_path) if result_path.is_file() else None}
    write_json(folder / "job.json", record)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    try:
        out.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        parser.error("--out must be a new folder; existing files were preserved")
    source_before = {p.name: sha256(p) for p in (Path(__file__), CHILD)}
    records = [run_one(out / mode, mode, expected) for mode, expected in PLAN]
    source_after = {p.name: sha256(p) for p in (Path(__file__), CHILD)}
    counts = {"planned_jobs": len(PLAN), "completed_processes": sum(not r["process"]["timed_out"] for r in records),
              "accepted_jobs": sum(r["observed"] == "ACCEPT" for r in records),
              "valid_dut_failures": sum(r["observed"] == "DUT_FAIL" for r in records),
              "naive_exit_zero_accepts": sum(r["naive_exit_zero"] for r in records),
              "naive_stdout_pass_accepts": sum(r["naive_stdout_pass"] for r in records),
              "fixture_checks_passed": sum(r["check"] == "PASS" for r in records)}
    passed = counts["fixture_checks_passed"] == len(PLAN) and source_before == source_after
    summary = {"schema_version": 1, "simulation_only": True,
               "status": "PASS" if passed else "FAIL", "counts": counts,
               "runtime": {"python": platform.python_version(), "os": platform.system(),
                           "implementation": platform.python_implementation(), "machine": platform.machine()},
               "literal_oracle": ORACLE, "source_sha256_before": source_before,
               "source_sha256_after": source_after, "jobs": records,
               "limits": ["controlled direct children only", "no physical chip or instrument",
                          "no RTL simulation", "not a sandbox or cryptographic attestation"]}
    write_json(out / "summary.json", summary)
    print(json.dumps({"status": summary["status"], "counts": counts}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
