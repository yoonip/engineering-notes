#!/usr/bin/env python3
"""Controlled offline chip-job fixture; deliberately emits faulty reports."""
import argparse  # 부모가 지정한 입력·결과 경로와 오류 종류를 받습니다.
import hashlib  # 실제 읽은 입력 바이트의 지문을 계산합니다.
import json  # 결과 형식을 만듭니다.
from pathlib import Path
import time  # timeout 대조에서만 기다립니다.


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--mode", required=True)
    args = parser.parse_args()
    payload = args.input.read_bytes()
    request = json.loads(payload)
    mode = args.mode
    if mode == "timeout":
        print("PASS text appeared before completion", flush=True)
        time.sleep(5)  # 부모는 더 짧은 제한 시간으로 실제 자식을 종료합니다.
        return 0
    if mode in {"stdout_only", "stale_result"}:
        print("PASS text only; no fresh report was written", flush=True)
        return 0
    rows = []
    for case in request["cases"]:
        total = 0  # DUT 역할의 순차 누산이며 부모의 고정 기대값을 가져오지 않습니다.
        for left, right in zip(case["left"], case["right"]):
            total += left * right
        rows.append({"id": case["id"], "status": "PASS", "actual": total})
    report = {"schema_version": 1, "run_id": request["run_id"],
              "input_sha256": hashlib.sha256(payload).hexdigest(),
              "status": "PASS", "cases": rows}
    if mode in {"dut_fail", "lying_pass"}:
        rows[0]["actual"] -= 1  # 정수 185 대신 184를 돌려주는 기능 오류입니다.
        if mode == "dut_fail":
            rows[0]["status"] = "FAIL"
            report["status"] = "FAIL"  # 기능 실패를 정직하게 보고하지만 종료 코드는 0입니다.
    elif mode == "wrong_hash":
        report["input_sha256"] = "0" * 64
    elif mode == "missing_case":
        report["cases"] = rows[:-1]
    elif mode == "duplicate_case":
        report["cases"] = rows + [dict(rows[0])]
    elif mode == "unknown_case":
        report["cases"] = rows + [{"id": "UNPLANNED", "status": "PASS", "actual": 0}]
    elif mode == "schema_bool":
        report["schema_version"] = True  # True == 1인 Python 비교만 쓰면 놓칠 수 있습니다.
    elif mode == "wrong_type":
        rows[-1]["actual"] = False  # False == 0이지만 정수 산술 출력 계약은 아닙니다.
    elif mode == "nan":
        rows[0]["actual"] = float("nan")
    text = json.dumps(report, indent=2, allow_nan=True)
    if mode == "bad_json":
        text = "{unfinished"
    elif mode == "duplicate_json_key":
        text = text.replace('"schema_version": 1',
                            '"schema_version": 999, "schema_version": 1', 1)
    args.result.write_bytes((text + "\n").encode("utf-8"))
    print("PASS text is diagnostic output, not a verdict", flush=True)
    return 7 if mode == "nonzero_exit" else 0


if __name__ == "__main__":
    raise SystemExit(main())
