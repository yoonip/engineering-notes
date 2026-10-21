#!/usr/bin/env python3
"""Run Icarus on a dual-clock FIFO and compare transactions with a Python deque."""
import argparse
import csv
from collections import deque
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
VARIANTS = [("correct", 0), ("full_one_bit", 1), ("read_empty", 2), ("one_sided_reset", 3)]
FIELDS = ["time", "domain", "reset_all", "reset_write_request", "local_reset", "enable",
          "flag", "fire", "data", "bin", "gray", "sync1", "sync2", "remote_gray"]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(path, value):
    path.write_bytes((json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8"))


def stimuli():
    writes = []
    for i in range(200):
        enabled = (3 <= i <= 9 or 20 <= i <= 79 or 95 <= i <= 98
                   or (105 <= i <= 169 and i % 6 != 2))
        writes.append({"enable": int(enabled), "data": 1000+i})
    reads = [{"enable": int((9 <= i <= 64 and i % 5 != 1) or 78 <= i <= 146)}
             for i in range(150)]
    return {"write_period_ns": 10, "read_period_ns": 14, "finish_ns": 2200,
            "common_reset_intervals_ns": [[1, 22], [1002, 1032]],
            "write_reset_intervals_ns": [[1502, 1532]], "writes": writes, "reads": reads}


def in_interval(time, intervals):
    return int(any(start <= time < end for start, end in intervals))


def expected_edges(inputs):
    expected = {}
    for domain, period, rows in (("W", 10, inputs["writes"]), ("R", 14, inputs["reads"])):
        for time in range(period//2, inputs["finish_ns"], period):
            i = time//period-1
            item = rows[i] if 0 <= i < len(rows) else {"enable": 0, "data": 0}
            expected[(time, domain)] = {"enable": item["enable"],
                "reset_all": in_interval(time, inputs["common_reset_intervals_ns"]),
                "reset_write_request": in_interval(time, inputs["write_reset_intervals_ns"])}
            if domain == "W":
                # TB는 마지막 입력 뒤 enable만 내리므로 data는 마지막 값을 유지합니다.
                expected[(time, domain)]["data"] = item.get("data", 0) if i < len(rows) else rows[-1]["data"]
    return expected


def load_trace(path, inputs):
    if not path.is_file():
        raise ValueError("missing trace.csv")
    expected = expected_edges(inputs)
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != FIELDS:
            raise ValueError("unexpected trace schema")
        actual, seen = [], set()
        for number, row in enumerate(reader, 2):
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f"CSV column count at row {number}")
            try:
                item = {key: int(value) for key, value in row.items() if key not in ("domain", "data")}
                item["domain"] = row["domain"]
                item["data"] = None if any(c in row["data"].lower() for c in "xz") else int(row["data"], 16)
            except (ValueError, TypeError) as error:
                raise ValueError(f"invalid control/pointer or data at row {number}") from error
            key = (item["time"], item["domain"])
            if key not in expected or key in seen:
                raise ValueError(f"unexpected/duplicate edge {key}")
            seen.add(key)
            for field, value in expected[key].items():
                if item[field] != value:
                    raise ValueError(f"stimulus echo mismatch {key} {field}")
            for field in ("reset_all", "reset_write_request", "local_reset", "enable", "flag", "fire"):
                if item[field] not in (0, 1):
                    raise ValueError(f"non-bit {field} at {key}")
            for field in ("bin", "gray", "sync1", "sync2", "remote_gray"):
                if not 0 <= item[field] < 8:
                    raise ValueError(f"pointer width {field} at {key}")
            actual.append(item)
    if seen != set(expected):
        raise ValueError("missing trace edges")
    return sorted(actual, key=lambda row: (row["time"], row["domain"]))  # R은 W보다 먼저 처리합니다.


def compare_trace(path, inputs):
    actual = load_trace(path, inputs)
    queue = deque()  # deque는 양 끝에서 원소를 넣고 빼는 표준 자료구조입니다.
    errors, accepted, consumed, cancelled = [], [], [], []
    previous, resets, max_occupancy = {}, [], 0
    blocked_writes = blocked_reads = wrap_w = wrap_r = 0
    conservative_full = conservative_empty = 0
    reset_episode = False
    def fail(row, reason, **detail):
        errors.append({"time": row["time"], "domain": row["domain"], "reason": reason, **detail})
    for row in actual:
        time, domain = row["time"], row["domain"]
        requested = bool(row["reset_all"] or row["reset_write_request"])
        if requested and not reset_episode:
            resets.append({"first_observed_ns": time, "flushed": list(queue)})
            cancelled.extend(queue)
            queue.clear()
        reset_episode = requested
        if requested and not row["local_reset"]:
            fail(row, "reset_request_not_applied")
        intervals = inputs["common_reset_intervals_ns"] + inputs["write_reset_intervals_ns"]
        latest = max((interval for interval in intervals if interval[0] <= time), default=None)
        if latest:
            period = inputs["write_period_ns"] if domain == "W" else inputs["read_period_ns"]
            previous_release_edges = sum(latest[1] < edge < time
                                         for edge in range(period//2, time, period))
            expected_reset = int(time < latest[1] or previous_release_edges < 2)
            if row["local_reset"] != expected_reset:
                fail(row, "local_reset_release", expected=expected_reset, observed=row["local_reset"])
        gate = row["enable"] and not row["flag"] and not row["local_reset"]
        if row["fire"] != int(gate):
            fail(row, "acceptance_gate")
        if row["local_reset"]:
            if row["fire"] or row["bin"] or row["gray"] or row["sync1"] or row["sync2"]:
                fail(row, "reset_state")
            if row["flag"] != int(domain == "R"):
                fail(row, "reset_flag")
        else:
            if row["gray"] != (row["bin"] ^ (row["bin"] >> 1)):
                fail(row, "gray_encoding")
            prior = previous.get(domain)
            if prior and not prior["local_reset"]:
                if row["bin"] != (prior["bin"] + prior["fire"]) % 8:
                    fail(row, "pointer_advance")
                if row["sync2"] != prior["sync1"] or row["sync1"] != prior["remote_gray"]:
                    fail(row, "two_stage_sync")
                delta = row["gray"] ^ prior["gray"]
                if delta and delta & (delta-1):
                    fail(row, "gray_multiple_bit_transition")
                if prior["bin"] == 7 and row["bin"] == 0:
                    if domain == "W": wrap_w += 1
                    else: wrap_r += 1
            # 동기화 지연 때문에 실제 빈자리/자료가 있어도 로컬 flag는 더 오래 유지될 수 있습니다.
            if row["flag"] and domain == "W" and len(queue) < 4:
                conservative_full += 1
            if row["flag"] and domain == "R" and queue:
                conservative_empty += 1
        if row["enable"] and row["flag"] and not row["local_reset"]:
            if domain == "W": blocked_writes += 1
            else: blocked_reads += 1
        if row["fire"]:
            if requested:
                fail(row, "accepted_during_flush")
            if domain == "R":
                if not queue:
                    fail(row, "underflow")
                else:
                    wanted = queue.popleft()  # 가장 먼저 수락한 자료를 맨 앞에서 제거합니다.
                    if row["data"] != wanted:
                        fail(row, "data_order", expected=wanted, observed=row["data"])
                consumed.append({"time": time, "data": row["data"]})
                if row["data"] is None:
                    fail(row, "unknown_accepted_data")
            else:
                if len(queue) >= 4:
                    fail(row, "overflow", occupancy_before=len(queue))
                queue.append(row["data"])  # 수락한 쓰기 값을 기준 큐의 맨 뒤에 붙입니다.
                accepted.append({"time": time, "data": row["data"]})
                max_occupancy = max(max_occupancy, len(queue))
        previous[domain] = row
    if queue:
        errors.append({"reason": "not_drained", "remaining": list(queue)})
    # 고정 구간의 리터럴은 queue 수락 신호만 믿고 아무 거래 없이 통과하는 것을 막습니다.
    literals = {"first_four_writes": accepted[:4] == [
        {"time": 45, "data": 1003}, {"time": 55, "data": 1004},
        {"time": 65, "data": 1005}, {"time": 75, "data": 1006}],
        "first_read": bool(consumed) and consumed[0] == {"time": 147, "data": 1003},
        "activity": len(accepted) > 40 and len(consumed) > 30,
        "wrap_and_stall": wrap_w > 2 and wrap_r > 2 and blocked_writes > 0 and blocked_reads > 0,
        "three_flush_episodes": len(resets) == 3}
    errors.extend({"reason": "manual_literal", "check": key} for key, value in literals.items() if not value)
    return {"status": "PASS" if not errors else "FUNCTIONAL_FAIL", "trace_rows": len(actual),
            "mismatch_count": len(errors), "mismatches": errors, "manual_checks": literals,
            "accepted": accepted, "consumed": consumed, "reset_cancelled": cancelled,
            "reset_episodes": resets, "max_occupancy": max_occupancy,
            "blocked_writes": blocked_writes, "blocked_reads": blocked_reads,
            "conservative_full_edges": conservative_full, "conservative_empty_edges": conservative_empty,
            "write_pointer_wraps": wrap_w, "read_pointer_wraps": wrap_r}


def checker_controls(correct_trace, inputs, directory):
    """RTL 변이와 별도로 trace 수집기/비교기의 거절 경로를 시험합니다."""
    directory.mkdir()
    with correct_trace.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    controls = {}
    for name in ("missing_trace", "missing_edge", "duplicate_edge", "extra_column",
                 "unknown_control", "wrong_input_echo", "unknown_accepted_data", "wrong_read_data"):
        changed = [dict(row) for row in rows]
        if name == "missing_edge": changed.pop()
        if name == "duplicate_edge": changed.append(dict(changed[0]))
        if name == "extra_column": changed[0][None] = ["unexpected"]
        if name == "unknown_control": changed[0]["flag"] = "x"
        if name == "wrong_input_echo": changed[0]["enable"] = "1"
        if name in ("unknown_accepted_data", "wrong_read_data"):
            target = next(row for row in changed if row["domain"] == "R" and row["time"] == "147")
            target["data"] = "xxxxxxxx" if name == "unknown_accepted_data" else "00000000"
        path = directory/(name + ".csv")
        if name != "missing_trace":
            with path.open("w", encoding="utf-8", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=FIELDS, extrasaction="ignore")
                writer.writeheader()
                for row in changed:
                    writer.writerow(row)
            if name == "extra_column":
                lines = path.read_text(encoding="utf-8").splitlines()
                lines[1] += ",unexpected"
                path.write_text("\n".join(lines)+"\n", encoding="utf-8")
        expected = "FUNCTIONAL_FAIL" if name in ("unknown_accepted_data", "wrong_read_data") else "INFRA_ERROR"
        try:
            result = compare_trace(path, inputs)
            observed, reason = result["status"], result.get("mismatches", [])[:2]
        except ValueError as error:
            observed, reason = "INFRA_ERROR", str(error)
        controls[name] = {"expected": expected, "observed": observed,
            "passed": observed == expected, "reason": reason,
            "sha256": sha256(path) if path.is_file() else None}
    save_json(directory/"results.json", controls)
    return controls


def command_run(command, cwd, env):
    try:
        run = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True,
                             encoding="utf-8", errors="replace", timeout=30, check=False)
        return {"command": command, "cwd": str(cwd), "returncode": run.returncode,
                "stdout": run.stdout, "stderr": run.stderr, "timed_out": False}
    except (OSError, subprocess.TimeoutExpired) as error:
        def as_text(value):
            return value.decode("utf-8", errors="replace") if isinstance(value, bytes) else (value or "")
        return {"command": command, "cwd": str(cwd), "returncode": None,
                "stdout": as_text(getattr(error, "stdout", None)),
                "stderr": as_text(getattr(error, "stderr", None)),
                "timed_out": isinstance(error, subprocess.TimeoutExpired), "error": str(error)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--iverilog", default="iverilog")
    parser.add_argument("--vvp", default="vvp")
    parser.add_argument("--build-root", type=Path)
    args = parser.parse_args()
    if args.out.exists():
        parser.error("--out must be a new directory")
    args.out.mkdir(parents=True)
    inputs = stimuli()
    save_json(args.out / "inputs.json", inputs)
    report = {"scope": "Icarus digital RTL simulation; no physical CDC/MTBF/signoff result",
        "python": sys.version, "platform": platform.platform(), "variants": {},
        "source_sha256": {name: sha256(HERE/name) for name in ("async_fifo.sv", "tb_async_fifo.sv", "run_compare.py")},
        "input_sha256": sha256(args.out / "inputs.json")}
    if args.build_root:
        args.build_root.mkdir(parents=True, exist_ok=True)
    build = Path(tempfile.mkdtemp(prefix="cdc_fifo_", dir=args.build_root or None))
    report["build_directory"] = str(build)
    env = os.environ.copy()
    env.update(TEMP=str(build), TMP=str(build))
    report["process_environment"] = {"TEMP": str(build), "TMP": str(build)}
    for tool in ("iverilog", "vvp"):
        supplied = getattr(args, tool)
        located = shutil.which(supplied)
        report[tool] = command_run([located or supplied, "-V"], build, env)
        if not located or report[tool]["returncode"] != 0:
            report.update(status="INFRA_ERROR", reason=f"unavailable {tool}")
            save_json(args.out / "report.json", report)
            print("INFRA_ERROR: unavailable " + tool)
            return 2
        setattr(args, tool, located)
    for name, mode in VARIANTS:
        work = build / name
        work.mkdir()
        result_dir = args.out / name
        result_dir.mkdir()
        for source in ("async_fifo.sv", "tb_async_fifo.sv"):
            shutil.copyfile(HERE/source, work/source)
        (work/"writes.hex").write_text("".join(f"{(r['enable'] << 32) | r['data']:09x}\n" for r in inputs["writes"]), encoding="ascii")
        (work/"reads.bin").write_text("".join(f"{r['enable']}\n" for r in inputs["reads"]), encoding="ascii")
        item = {"bug_mode": mode}
        item["compile"] = command_run([args.iverilog, "-g2012", "-gstrict-expr-width", "-Wall",
            "-s", "tb_async_fifo", f"-Ptb_async_fifo.BUG_MODE={mode}", "-o", "sim.vvp",
            "async_fifo.sv", "tb_async_fifo.sv"], work, env)
        if item["compile"]["returncode"] == 0:
            item["simulation"] = command_run([args.vvp, "sim.vvp"], work, env)
        if item["compile"]["returncode"] != 0 or item.get("simulation", {}).get("returncode") != 0:
            item.update(status="INFRA_ERROR", reason="compile/simulation did not finish successfully")
        else:
            try:
                item.update(compare_trace(work/"trace.csv", inputs))
            except ValueError as error:
                item.update(status="INFRA_ERROR", reason=str(error))
        for filename in ("trace.csv", "writes.hex", "reads.bin", "sim.vvp"):
            path = work/filename
            if path.is_file():
                shutil.copyfile(path, result_dir/filename)
        item["artifact_sha256"] = {path.name: sha256(path) for path in result_dir.iterdir() if path.is_file()}
        save_json(result_dir/"result.json", item)
        report["variants"][name] = item
    statuses = {name: result["status"] for name, result in report["variants"].items()}
    if statuses.get("correct") == "PASS":
        report["checker_controls"] = checker_controls(args.out/"correct"/"trace.csv", inputs,
                                                       args.out/"checker-controls")
    if "INFRA_ERROR" in statuses.values():
        report["status"], code = "INFRA_ERROR", 2
    else:
        expected = {name: "PASS" if mode == 0 else "FUNCTIONAL_FAIL" for name, mode in VARIANTS}
        controls_ok = all(item["passed"] for item in report.get("checker_controls", {}).values())
        report["status"], code = ("PASS", 0) if statuses == expected and controls_ok else ("FAIL", 1)
    save_json(args.out/"report.json", report)
    print(json.dumps({"status": report["status"], "variants": statuses}, ensure_ascii=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
