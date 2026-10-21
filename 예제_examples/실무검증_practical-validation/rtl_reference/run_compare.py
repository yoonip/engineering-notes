#!/usr/bin/env python3
"""Compile real RTL, simulate it, and compare traces with an independent queue model."""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import platform
import random
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
VARIANTS = [("correct", 0), ("unsigned", 1), ("narrow", 2),
            ("ignore_ready", 3), ("early_valid", 4), ("reset_not_flushed", 5)]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(path, value):
    path.write_bytes((json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)
                      + "\n").encode("utf-8"))


def stimuli():
    # 입력을 구동하는 일정과 oracle의 상태 갱신 코드는 분리합니다.
    rows = [{"cycle": c, "rst": int(c < 2), "valid": 0, "ready": 1,
             "tag": 0, "x": [0]*4, "w": [0]*4} for c in range(32)]

    def put(cycle, tag, x, w, ready=1, rst=0):
        rows[cycle].update(rst=rst, valid=1, ready=ready, tag=tag, x=x, w=w)

    a = ([20, -3, 5, 6], [7, -2, 3, 4])
    b = ([-128]*4, [-128]*4)
    put(3, 1, *a)
    for c in range(4, 9):
        put(c, 2, *b, ready=int(c >= 7))  # 준비 전부터 다음 입력을 안정적으로 유지합니다.
    put(12, 3, [-128]*4, [127]*4)
    put(16, 4, [1, 2, 3, 4], [1]*4)
    rows[18].update(rst=1, ready=0)  # 대기 중인 출력을 소비하기 전에 reset합니다.
    put(21, 5, [0, 1, -1, 5], [127, 3, 3, 0])
    rng = random.Random(20261021)
    for item in range(32):
        base = len(rows)
        x = [rng.randrange(-128, 128) for _ in range(4)]
        w = [rng.randrange(-128, 128) for _ in range(4)]
        for offset in range(8):
            rows.append({"cycle": base+offset, "rst": int(item % 11 == 5 and offset == 3),
                         "valid": int(offset == 0), "ready": int(offset not in (2, 3)),
                         "tag": item+100, "x": x, "w": w})
    return rows


def reference(rows):
    """RTL 상태기를 복제하지 않고 수락한 거래와 가장 이른 출력 edge를 추적합니다."""
    pending = None
    expected, accepted, consumed, cancelled = [], [], [], []
    waiting_input = None
    for row in rows:
        cycle = row["cycle"]
        payload = (row["tag"], row["x"], row["w"])
        if row["rst"]:
            if pending is not None:
                cancelled.append(pending["tag"])
            pending, waiting_input = None, None
            expected.append({"in_ready": 0, "out_valid": 0})
            continue
        ready = int(pending is None)
        valid = int(pending is not None and cycle >= pending["due"])
        item = {"in_ready": ready, "out_valid": valid}
        if valid:
            item.update(out_tag=pending["tag"], out_data=pending["value"])
        expected.append(item)
        if waiting_input is not None and (not row["valid"] or payload != waiting_input):
            raise ValueError("source changed valid data before acceptance")
        waiting_input = payload if row["valid"] and not ready else None
        if valid and row["ready"]:
            consumed.append(pending["tag"])
            pending = None
        if ready and row["valid"]:
            # Python 정수의 곱과 합은 RTL의 부호 확장·레지스터 폭에 의존하지 않습니다.
            value = sum(left * right for left, right in zip(row["x"], row["w"]))
            pending = {"tag": row["tag"], "value": value, "due": cycle+2}
            accepted.append(row["tag"])
    if pending is not None:
        raise ValueError("stimulus ended before output was drained or reset")
    return expected, {"accepted": accepted, "consumed": consumed, "reset_cancelled": cancelled}


def command_run(command, cwd, env):
    try:
        run = subprocess.run(command, cwd=cwd, env=env, capture_output=True,
                             text=True, encoding="utf-8", errors="replace", timeout=30, check=False)
        return {"command": command, "cwd": str(cwd), "returncode": run.returncode,
                "stdout": run.stdout, "stderr": run.stderr, "timed_out": False}
    except (OSError, subprocess.TimeoutExpired) as error:
        def text(value):
            return value.decode("utf-8", errors="replace") if isinstance(value, bytes) else (value or "")
        return {"command": command, "cwd": str(cwd), "returncode": None,
                "stdout": text(getattr(error, "stdout", None)),
                "stderr": text(getattr(error, "stderr", None)),
                "timed_out": isinstance(error, subprocess.TimeoutExpired),
                "error": type(error).__name__ + ": " + str(error)}


def compare_trace(path, rows, expected):
    if not path.is_file():
        raise ValueError("simulation produced no trace.csv")
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["cycle", "rst", "in_valid", "in_ready", "in_tag", "out_ready",
                                  "out_valid", "out_tag", "out_data"]:
            raise ValueError("unexpected trace schema")
        actual = []
        for row_number, row in enumerate(reader, 2):
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f"trace column count mismatch at CSV row {row_number}")
            try:
                actual.append({key: int(value) for key, value in row.items()})
            except (ValueError, TypeError) as error:
                raise ValueError(f"non-integer or X/Z trace field at CSV row {row_number}") from error
    if len(actual) != len(rows):
        raise ValueError("trace row count does not match stimulus")
    mismatches = []
    for stimulus, want, got in zip(rows, expected, actual):
        for key, value in (("cycle", stimulus["cycle"]), ("rst", stimulus["rst"]),
                           ("in_valid", stimulus["valid"]), ("in_tag", stimulus["tag"]),
                           ("out_ready", stimulus["ready"]), *want.items()):
            if got[key] != value:
                mismatches.append({"cycle": stimulus["cycle"], "signal": key,
                                   "expected": value, "actual": got[key]})
    return mismatches


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--build-root", type=Path,
                        help="optional new build folder; ASCII path helps diagnose Windows path issues")
    parser.add_argument("--iverilog", default=shutil.which("iverilog") or "C:/iverilog/bin/iverilog.exe")
    parser.add_argument("--vvp", default=shutil.which("vvp") or "C:/iverilog/bin/vvp.exe")
    args = parser.parse_args()
    out = args.out.resolve()
    try:
        out.mkdir(parents=True, exist_ok=False)
        if args.build_root:
            build_root = args.build_root.resolve()
            build_root.mkdir(parents=True, exist_ok=False)
        else:
            build_root = Path(tempfile.mkdtemp(prefix="rtl-ref-build-"))
    except FileExistsError:
        parser.error("output and explicit build folders must be new")
    sources = [HERE / name for name in ("dot4.sv", "tb_dot4.sv", "run_compare.py")]
    before = {p.name: sha256(p) for p in sources}
    rows = stimuli()
    expected, transactions = reference(rows)
    save_json(out / "input.json", {"rows": rows, "seed": 20261021,
                                   "contract": "single flight; transfer earliest accepted edge+2; synchronous reset flush"})
    save_json(out / "expected.json", {"edges": expected, "transactions": transactions})
    stimulus = "".join(" ".join(map(str, [r["cycle"], r["rst"], r["valid"], r["ready"],
                             r["tag"], *r["x"], *r["w"]])) + "\n" for r in rows)
    (out / "stimulus.txt").write_bytes(stimulus.encode("ascii"))
    versions = {"iverilog": command_run([args.iverilog, "-V"], out, dict(os.environ)),
                "vvp": command_run([args.vvp, "-V"], out, dict(os.environ))}
    save_json(out / "versions.json", versions)
    results = []
    for name, bug in VARIANTS:  # compile은 순차 실행하며 각 작업의 TEMP/TMP를 나눕니다.
        folder, build = out / name, build_root / name
        folder.mkdir()
        build.mkdir()
        temp = build / "temp"
        temp.mkdir()
        env = dict(os.environ, TEMP=str(temp), TMP=str(temp), PYTHONIOENCODING="utf-8")
        for source in sources[:2]:
            shutil.copyfile(source, build / source.name)
            shutil.copyfile(source, folder / source.name)
        (build / "stimulus.txt").write_bytes(stimulus.encode("ascii"))
        compile_result = command_run([args.iverilog, "-g2012", "-gstrict-expr-width", "-Wall",
                                      "-s", "tb_dot4", f"-Ptb_dot4.BUG_MODE={bug}",
                                      "-o", "sim.vvp", "dot4.sv", "tb_dot4.sv"], build, env)
        save_json(folder / "compile.json", compile_result)
        result = {"variant": name, "bug_mode": bug, "compile": compile_result,
                  "build_directory": str(build), "temp_directory": str(temp)}
        if compile_result["returncode"] != 0:
            result.update(status="INFRA_ERROR", error="compile did not complete successfully")
        else:
            simulation = command_run([args.vvp, "sim.vvp"], build, env)
            save_json(folder / "simulate.json", simulation)
            result["simulation"] = simulation
            if (build / "trace.csv").is_file():
                shutil.copyfile(build / "trace.csv", folder / "trace.csv")
            if (build / "sim.vvp").is_file():
                shutil.copyfile(build / "sim.vvp", folder / "sim.vvp")
            if simulation["returncode"] != 0:
                result.update(status="INFRA_ERROR", error="simulation did not complete successfully")
            else:
                try:
                    mismatches = compare_trace(folder / "trace.csv", rows, expected)
                    result.update(status="FAIL" if mismatches else "PASS", mismatches=mismatches,
                                  trace_sha256=sha256(folder / "trace.csv"))
                except (ValueError, OSError) as error:
                    result.update(status="INFRA_ERROR", error=str(error))
        result["expected_status"] = "PASS" if bug == 0 else "FAIL"
        result["control_matches"] = result["status"] == result["expected_status"]
        save_json(folder / "comparison.json", result)
        results.append(result)
    after = {p.name: sha256(p) for p in sources}
    infrastructure = any(r["status"] == "INFRA_ERROR" for r in results)
    passed = all(r["control_matches"] for r in results) and before == after
    report = {"status": "INFRA_ERROR" if infrastructure else ("PASS" if passed else "FAIL"),
              "scope": "Icarus RTL simulation against an independent Python transaction oracle",
              "runtime": {"python": platform.python_version(), "os": platform.system(), "machine": platform.machine()},
              "input_sha256": sha256(out / "input.json"), "stimulus_sha256": sha256(out / "stimulus.txt"),
              "expected_sha256": sha256(out / "expected.json"), "cycles": len(rows),
              "transactions": transactions, "source_sha256_before": before, "source_sha256_after": after,
              "build_root": str(build_root), "build_root_is_ascii": str(build_root).isascii(),
              "results": results, "not_run": ["synthesis", "formal equivalence", "STA", "layout", "physical device"]}
    save_json(out / "summary.json", report)
    print(json.dumps({"status": report["status"], "cycles": len(rows),
                      "variants": [{"name": r["variant"], "status": r["status"],
                                    "mismatches": len(r.get("mismatches", []))} for r in results]}, ensure_ascii=False))
    return 2 if infrastructure else (0 if passed else 1)


if __name__ == "__main__":
    raise SystemExit(main())
