#!/usr/bin/env python3
"""Compile an SV command fixture; monitor a deliberately limited DDR-style contract."""
import argparse
import csv
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
FIELDS = ["cycle", "op", "bank", "row", "col", "tag", "wdata", "rvalid", "rtag", "rdata"]
NOP, ACT, WR, RD, PRE, REF = range(6)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(path, value):
    path.write_bytes((json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+"\n").encode("utf-8"))


def make_program(case):
    phases = 2 if case["pattern"] == "checkerboard_inverse" else 1
    program = [{"cycle": c, "op": NOP, "bank": 0, "row": 0, "col": 0, "tag": 0, "wdata": 0}
               for c in range(256*phases)]
    tag = 0
    def put(cycle, op, bank=0, row=0, col=0, data=0):
        nonlocal tag
        tag += 1
        program[cycle].update(op=op, bank=bank, row=row, col=col, tag=tag, wdata=data)
    for phase in range(phases):
        for block in range(8):
            base = phase*256 + block*32
            bank, row = divmod(block, 4)
            put(base, REF)
            put(base+8, ACT, bank, row)
            for col in range(4):
                address = bank*16+row*4+col
                if case["pattern"] == "zero": value = 0
                elif case["pattern"] == "address": value = 0xA500 ^ (address*0x101)
                else: value = (0xAA55 if address % 2 == 0 else 0x55AA) ^ (0xFFFF if phase else 0)
                put(base+11+col, WR, bank, row, col, value)
                put(base+16+2*col, RD, bank, row, col)
            put(base+26, PRE, bank)
    # 명령표의 의도적 오류이며 정상 controller가 만들어 낸 실행 결과가 아닙니다.
    moves = {"rcd": (11, 10), "ras": (26, 9), "rp": (40, 27), "rfc": (8, 7)}
    if case["change"] in moves:
        old, new = moves[case["change"]]
        program[new] = {**program[old], "cycle": new}
        program[old] = {**program[old], "op": NOP, "tag": 0, "wdata": 0}
    if case["change"] in ("refresh", "unwritten"):
        cycle = 32 if case["change"] == "refresh" else 11
        program[cycle].update(op=NOP, tag=0, wdata=0)
    return program


def load_trace(path, program):
    if not path.is_file():
        raise ValueError("missing trace.csv")
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != FIELDS:
            raise ValueError("unexpected trace schema")
        rows = []
        for line, raw in enumerate(reader, 2):
            if None in raw or any(v is None for v in raw.values()):
                raise ValueError(f"column count at line {line}")
            try:
                row = {k: int(v, 16) if k == "wdata" else int(v) for k, v in raw.items() if k != "rdata"}
                row["rdata"] = None if any(c in raw["rdata"].lower() for c in "xz") else int(raw["rdata"], 16)
            except (ValueError, TypeError) as error:
                raise ValueError(f"unknown/invalid command or control at line {line}") from error
            if row["cycle"] != len(rows) or len(rows) >= len(program):
                raise ValueError("missing/duplicate/out-of-order/unexpected cycle")
            if any(row[k] != program[len(rows)][k] for k in program[len(rows)]):
                raise ValueError("command/input echo mismatch")
            if row["rvalid"] not in (0, 1) or not 0 <= row["rtag"] <= 65535:
                raise ValueError("response control out of range")
            if row["rdata"] is not None and not 0 <= row["rdata"] <= 65535:
                raise ValueError("response width out of range")
            rows.append(row)
    if len(rows) != len(program):
        raise ValueError("incomplete trace")
    return rows


def monitor(path, program, timing):
    """SV의 배열 주소 구현을 복제하지 않고 tuple 키의 거래 자료와 시각을 추적합니다."""
    rows = load_trace(path, program)
    opened, activated, precharged = [None, None], [None, None], [-1000, -1000]
    last_write, last_read = [-1000, -1000], [-1000, -1000]
    memory, due, errors, responses = {}, {}, [], []
    writes = reads = refreshes = value_mismatches = 0
    last_refresh, refresh_busy_until, deadline_reported = 0, 0, False
    def fail(cycle, reason, **details):
        errors.append({"cycle": cycle, "reason": reason, **details})
    for row in rows:
        c, op, bank = row["cycle"], row["op"], row["bank"]
        if c-last_refresh > timing["refresh_deadline"] and not deadline_reported:
            fail(c, "refresh_deadline", last_refresh=last_refresh)
            deadline_reported = True
        want = due.pop(c, None)
        if row["rvalid"]:
            responses.append({"cycle": c, "tag": row["rtag"], "data": row["rdata"]})
            if want is None:
                fail(c, "unexpected_response")
            else:
                if row["rtag"] != want["tag"]:
                    fail(c, "response_order", expected=want["tag"], observed=row["rtag"])
                if want["value"] is None:
                    fail(c, "read_uninitialized", address=want["address"])
                if row["rdata"] is None:
                    fail(c, "unknown_valid_data")
                elif want["value"] is not None and row["rdata"] != want["value"]:
                    value_mismatches += 1
                    fail(c, "data_mismatch", expected=want["value"], observed=row["rdata"], address=want["address"])
        elif want is not None:
            fail(c, "missing_response", tag=want["tag"])
        if op != NOP and c < refresh_busy_until:
            fail(c, "tRFC", earliest=refresh_busy_until)
        if op == ACT:
            if opened[bank] is not None: fail(c, "ACT_on_open_bank")
            if c-precharged[bank] < timing["tRP"]: fail(c, "tRP", elapsed=c-precharged[bank])
            opened[bank], activated[bank] = row["row"], c
        elif op in (WR, RD):
            if opened[bank] is None:
                fail(c, "column_without_ACT")
            elif c-activated[bank] < timing["tRCD"]:
                fail(c, "tRCD", elapsed=c-activated[bank])
            key = (bank, opened[bank], row["col"])
            if op == WR:
                writes += 1
                last_write[bank] = c
                if opened[bank] is not None: memory[key] = row["wdata"]
            else:
                reads += 1
                last_read[bank] = c
                due[c+timing["read_latency"]] = {"tag": row["tag"], "value": memory.get(key), "address": key}
        elif op == PRE:
            if opened[bank] is None: fail(c, "PRE_on_closed_bank")
            elif c-activated[bank] < timing["tRAS"]: fail(c, "tRAS", elapsed=c-activated[bank])
            if c-last_write[bank] < timing["tWR"]: fail(c, "tWR", elapsed=c-last_write[bank])
            if c-last_read[bank] < timing["tRTP"]: fail(c, "tRTP", elapsed=c-last_read[bank])
            opened[bank], precharged[bank] = None, c
        elif op == REF:
            if any(value is not None for value in opened): fail(c, "REF_with_open_bank")
            if any(c-time < timing["tRP"] for time in precharged): fail(c, "REF_before_tRP")
            last_refresh, refresh_busy_until, deadline_reported = c, c+timing["tRFC"], False
            refreshes += 1
    if due: fail(len(rows), "undrained_response", count=len(due))
    if any(value is not None for value in opened): fail(len(rows), "bank_not_closed")
    if len(memory) > 32: fail(len(rows), "capacity_exceeded")
    return {"status": "FUNCTIONAL_FAIL" if errors else "PASS", "trace_rows": len(rows),
        "mismatch_count": len(errors), "mismatches": errors, "writes": writes, "reads": reads,
        "responses": responses, "response_count": len(responses), "refreshes": refreshes,
        "initialized_addresses": len(memory), "naive_value_only_mismatches": value_mismatches}


def run(command, cwd, env):
    try:
        result = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=30, check=False)
        return {"command": command, "cwd": str(cwd), "returncode": result.returncode,
            "stdout": result.stdout, "stderr": result.stderr, "timed_out": False}
    except (OSError, subprocess.TimeoutExpired) as error:
        def text(value): return value.decode("utf-8",errors="replace") if isinstance(value,bytes) else (value or "")
        return {"command": command, "cwd": str(cwd), "returncode": None,
            "stdout": text(getattr(error,"stdout",None)), "stderr": text(getattr(error,"stderr",None)),
            "timed_out": isinstance(error,subprocess.TimeoutExpired), "error": str(error)}


def checker_controls(trace, program, timing, out):
    out.mkdir()
    rows = trace.read_text(encoding="utf-8").splitlines()
    checks = {}
    for name in ("missing", "truncated", "duplicate", "extra_column", "x_control", "wrong_echo", "swapped_tags"):
        changed = rows[:]
        if name == "truncated": changed.pop()
        if name == "duplicate": changed[2] = changed[1]
        if name == "extra_column": changed[1] += ",extra"
        if name in ("x_control", "wrong_echo"):
            values = changed[1].split(",")
            values[1] = "x" if name == "x_control" else "1"
            changed[1] = ",".join(values)
        if name == "swapped_tags":
            a, b = changed[19].split(","), changed[21].split(",")  # cycle18/20 첫 두 read 응답입니다.
            a[8], b[8] = b[8], a[8]
            changed[19], changed[21] = ",".join(a), ",".join(b)
        path = out/(name+".csv")
        if name != "missing": path.write_bytes(("\n".join(changed)+"\n").encode("utf-8"))
        expected = "FUNCTIONAL_FAIL" if name == "swapped_tags" else "INFRA_ERROR"
        try: observed = monitor(path, program, timing)["status"]
        except ValueError: observed = "INFRA_ERROR"
        checks[name] = {"expected": expected, "observed": observed, "passed": observed == expected,
            "sha256": digest(path) if path.is_file() else None}
    save_json(out/"results.json",checks)
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",required=True,type=Path)
    parser.add_argument("--iverilog",default="iverilog")
    parser.add_argument("--vvp",default="vvp")
    parser.add_argument("--build-root",type=Path)
    args = parser.parse_args()
    if args.out.exists(): parser.error("--out must be a new directory")
    args.out.mkdir(parents=True)
    fixture = json.loads((HERE/"fixtures.json").read_text(encoding="utf-8"))
    programs = {case["name"]:make_program(case) for case in fixture["cases"]}
    save_json(args.out/"inputs.json", {"fixture":fixture,"programs":programs})
    report = {"scope":fixture["scope"], "environment":{"python":sys.version,"platform":platform.platform(),"optimized":not __debug__},
        "source_sha256":{name:digest(HERE/name) for name in ("ddr_command_fixture.sv","run_validation.py","fixtures.json")},
        "input_sha256":digest(args.out/"inputs.json"),"cases":{}}
    if args.build_root: args.build_root.mkdir(parents=True,exist_ok=True)
    build = Path(tempfile.mkdtemp(prefix="ddr_fixture_",dir=args.build_root or None))
    env = os.environ.copy()
    env.update(TEMP=str(build),TMP=str(build))
    report["process_environment"] = {"TEMP":str(build),"TMP":str(build)}
    for name in ("iverilog","vvp"):
        tool = shutil.which(getattr(args,name))
        report[name] = run([tool or getattr(args,name),"-V"],build,env)
        if not tool or report[name]["returncode"] != 0:
            report.update(status="INFRA_ERROR",reason="unavailable "+name)
            save_json(args.out/"report.json",report)
            print("INFRA_ERROR: unavailable "+name)
            return 2
        setattr(args,name,tool)
    for case in fixture["cases"]:
        name = case["name"]
        program = programs[name]
        work, output = build/name, args.out/name
        work.mkdir(); output.mkdir()
        shutil.copyfile(HERE/"ddr_command_fixture.sv",work/"ddr_command_fixture.sv")
        words = [(r["op"]<<37)|(r["bank"]<<36)|(r["row"]<<34)|(r["col"]<<32)|(r["tag"]<<16)|r["wdata"] for r in program]
        (work/"program.hex").write_bytes("".join(f"{v:016x}\n" for v in words).encode("ascii"))
        item = {"expected":case["expected"],"fault":case["fault"],"pattern":case["pattern"],"change":case["change"]}
        item["compile"] = run([args.iverilog,"-g2012","-gstrict-expr-width","-Wall","-s","ddr_command_fixture",
            f"-Pddr_command_fixture.FAULT={case['fault']}",f"-Pddr_command_fixture.CYCLES={len(program)}",
            "-o","sim.vvp","ddr_command_fixture.sv"],work,env)
        if item["compile"]["returncode"] == 0: item["simulation"] = run([args.vvp,"sim.vvp"],work,env)
        if item["compile"]["returncode"] != 0 or item.get("simulation",{}).get("returncode") != 0:
            item.update(status="INFRA_ERROR",reason="compile/sim failure",process_ok=False)
        else:
            item["process_ok"] = True
            try: item.update(monitor(work/"trace.csv",program,fixture["timing_cycles"]))
            except ValueError as error: item.update(status="INFRA_ERROR",reason=str(error))
        for filename in ("trace.csv","program.hex","sim.vvp"):
            if (work/filename).is_file(): shutil.copyfile(work/filename,output/filename)
        item["artifact_sha256"] = {p.name:digest(p) for p in output.iterdir() if p.is_file()}
        item["expected_outcome_matched"] = item["status"] == item["expected"] and item["process_ok"]
        save_json(output/"result.json",item)
        report["cases"][name] = item
    correct = report["cases"]["correct_address"]
    if correct["status"] == "PASS":
        report["checker_controls"] = checker_controls(args.out/"correct_address/trace.csv",programs["correct_address"],fixture["timing_cycles"],args.out/"checker-controls")
    controls_ok = bool(report.get("checker_controls")) and all(v["passed"] for v in report["checker_controls"].values())
    expected_ok = all(v["expected_outcome_matched"] for v in report["cases"].values())
    unexpected_infra = any(v["status"] == "INFRA_ERROR" and (v["expected"] != "INFRA_ERROR" or not v["process_ok"]) for v in report["cases"].values())
    report["status"] = "INFRA_ERROR" if unexpected_infra else "PASS" if expected_ok and controls_ok else "FAIL"
    save_json(args.out/"report.json",report)
    print(json.dumps({"status":report["status"],"cases":{k:v["status"] for k,v in report["cases"].items()}},ensure_ascii=True))
    return 0 if report["status"] == "PASS" else 2 if report["status"] == "INFRA_ERROR" else 1


if __name__ == "__main__":
    raise SystemExit(main())
