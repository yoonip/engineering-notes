#!/usr/bin/env python3
"""독립 pooling PU를 Python 정수 기준과 실제 Icarus RTL로 검증한다."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from model.pooling_q88 import make_vectors, pool_details, pool_q88, signed_to_word, truncate_division_zero, word_to_signed


def sha(path: Path) -> str:
    # 결과 JSON의 주장과 실제 당시 source/mem/raw log byte를 연결한다.
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_tool(name: str, explicit: str | None) -> str:
    candidates = [explicit] if explicit else [shutil.which(name), f"C:/iverilog/bin/{name}.exe"]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return str(Path(candidate).resolve())
    raise FileNotFoundError(f"{name} 실행파일이 없습니다. --{name} 옵션으로 실제 경로를 지정하세요.")


def run_tool(command: list[str], folder: Path, label: str, timeout: int) -> tuple[dict, str]:
    # shell 문자열이 아닌 argv 리스트를 사용한다. 한글 프로젝트 절대 경로도
    # Icarus 인자로 그대로 전달하고 원시 stdout/stderr를 모두 보존한다.
    started = time.perf_counter()
    try:
        run = subprocess.run(command, cwd=folder, capture_output=True, text=True,
                             encoding="utf-8", errors="replace", timeout=timeout)
        raw_text = run.stdout + run.stderr
        code, timed_out = run.returncode, False
    except subprocess.TimeoutExpired as error:
        def decoded(value: bytes | str | None) -> str:
            return value.decode("utf-8", errors="replace") if isinstance(value, bytes) else (value or "")
        raw_text = decoded(error.stdout) + decoded(error.stderr)
        code, timed_out = None, True
    raw = folder / f"{label}.console.log"
    raw.write_text(raw_text, encoding="utf-8")
    record = {"argv": command, "cwd": str(folder), "returncode": code, "timed_out": timed_out,
              "wall_seconds": round(time.perf_counter()-started, 6),
              "raw_log": raw.relative_to(ROOT).as_posix(), "raw_log_sha256": sha(raw)}
    if code != 0 or timed_out:
        raise RuntimeError(f"{label} 실패: {json.dumps(record, ensure_ascii=False)}")
    return record, raw_text


def check_reference_contract() -> list[dict]:
    # RTL에서 만든 정답을 다시 기준으로 쓰지 않는다. 손으로 계산한 작은
    # 사례로 Python의 부호/분모/mask/0방향 절삭 계약도 먼저 확인한다.
    cases = [
        ("empty_max", [32767, -32768], 0, "max", 0),
        ("empty_average", [32767, -32768], 0, "avg", 0),
        ("negative_max_excludes_invalid_zero", [-256, 0], 1, "max", -256),
        ("negative_average_truncates_zero", [-1, -2], 3, "avg", -1),
        ("positive_average_truncates_zero", [1, 2], 3, "avg", 1),
        ("small_negative_average_becomes_zero", [-1, 0], 3, "avg", 0),
        ("extreme_average_no_overflow", [-32768, 32767], 3, "avg", 0),
        ("all_minimum_no_overflow", [-32768]*16, 65535, "avg", -32768),
        ("all_maximum_no_overflow", [32767]*16, 65535, "avg", 32767),
        ("single_last_lane", [32767, -513], 2, "max", -513),
        ("partial_denominator_not_window", [256, 32767, 512], 5, "avg", 384),
        ("odd_window_max", [-512, -1, -256], 7, "max", -1),
        ("odd_window_average", [-512, -1, -256], 7, "avg", -256),
        ("maximum_tie", [257, 257, -32768], 7, "max", 257),
        ("single_minimum", [-32768], 1, "avg", -32768),
    ]
    results = []
    for name, values, mask, operation, wanted in cases:
        actual = pool_q88(values, mask, operation)
        assert actual == wanted, (name, actual, wanted)
        results.append({"name": name, "actual_raw": actual, "expected_raw": wanted, "passed": True})
    # 정수 word 경계와 잘못된 입력을 명시적으로 거부하는 API도 확인한다.
    assert word_to_signed(0x8000) == -32768 and word_to_signed(0xFFFF) == -1
    assert signed_to_word(-32768) == 0x8000 and signed_to_word(-1) == 0xFFFF
    results.append({"name": "two_complement_boundary_conversion", "passed": True})
    invalid = [
        ("empty_window_rejected", lambda: pool_q88([], 0)),
        ("outside_raw_rejected", lambda: pool_q88([32768], 1)),
        ("outside_mask_rejected", lambda: pool_q88([0], 2)),
        ("negative_mask_rejected", lambda: pool_q88([0], -1)),
        ("unknown_operation_rejected", lambda: pool_q88([0], 1, "sum")),
        ("zero_divisor_rejected", lambda: truncate_division_zero(-1, 0)),
        ("outside_word_rejected", lambda: word_to_signed(65536)),
        ("outside_signed_rejected", lambda: signed_to_word(-32769)),
    ]
    for name, action in invalid:
        try:
            action()
        except ValueError:
            results.append({"name": name, "passed": True})
        else:
            raise AssertionError(name)
    return results


def make_schedule(vector_count: int) -> list[dict]:
    # 1clock 계약을 확인할 입력 순서다. reset 중 valid는 무시하고, pending
    # 거래 하나를 reset으로 취소한다. 연속 입력과 0/1/2개의 bubble도 포함한다.
    rows = []
    def add(phase: str, reset_n: bool, valid: bool = False, vector: int = 0) -> None:
        rows.append({"cycle": len(rows), "phase": phase, "reset_n": reset_n,
                     "input_valid": valid, "vector_index": vector})
    add("initial_reset", False)
    add("reset_priority", False, True, 1)
    add("release_idle", True)
    add("single_input", True, True, 2)
    add("single_flush", True)
    add("idle", True)
    for index in range(vector_count):
        add("continuous", True, True, index)
    add("burst_flush", True)
    add("burst_idle", True)
    for index in range(16):
        add("bubble_input", True, True, index)
        for _ in range(index % 3):
            add("bubble_idle", True)
    add("bubble_flush", True)
    add("before_reset_first", True, True, 4)
    add("before_reset_second", True, True, 5)
    add("cancel_pending_and_ignore_valid", False, True, 6)
    add("held_reset", False)
    add("release_after_reset", True)
    add("repeat_after_reset_first", True, True, 4)
    add("repeat_after_reset_second", True, True, 5)
    add("final_flush", True)
    add("final_idle", True)
    return rows


def expected_registered(schedule: list[dict], details: list) -> tuple[list[dict], dict]:
    pending = None
    predicted = []
    counts = {"exact": 0, "accepted": 0, "cancelled": 0, "resets": 0,
              "valid_checks": len(schedule), "packed_checks": 0,
              "synchronous_checks": len(schedule), "maximum_burst": 0}
    burst = 0
    for row in schedule:
        if not row["reset_n"]:
            predicted.append({"valid": 0, "word": 0, "count": 0})
            counts["cancelled"] += pending is not None
            counts["resets"] += 1
            pending, burst = None, 0
        else:
            predicted.append({"valid": int(pending is not None),
                              "word": 0 if pending is None else pending.result_word,
                              "count": 0 if pending is None else pending.valid_count})
            counts["exact"] += pending is not None
            if row["input_valid"]:
                pending = details[row["vector_index"]]
                counts["accepted"] += 1
                burst += 1
                counts["maximum_burst"] = max(counts["maximum_burst"], burst)
            else:
                pending, burst = None, 0
    assert pending is None and counts["accepted"] == counts["exact"] + counts["cancelled"]
    return predicted, counts


def write_memories(folder: Path, vectors: list[dict], details: list, schedule: list[dict], window: int) -> dict:
    # .mem은 hex bit-pattern이고 Python raw는 signed 정수다. packed 문자열의
    # 왼쪽은 높은 lane이므로 리스트를 뒤집어 lane0을 가장 오른쪽에 놓는다.
    sum_width = details[0].sum_width
    mask_digits, count_digits = (window+3)//4, ((window+1).bit_length()+3)//4
    lines = {
        "values.mem": ["".join(f"{signed_to_word(v):04x}" for v in reversed(row["values_raw"])) for row in vectors],
        "masks.mem": [f"{row['valid_mask']:0{mask_digits}x}" for row in vectors],
        "operations.mem": ["1" if row["operation"] == "avg" else "0" for row in vectors],
        "expected.mem": [f"{row.result_word:04x}" for row in details],
        "counts.mem": [f"{row.valid_count:0{count_digits}x}" for row in details],
        "sums.mem": [f"{row.signed_sum & ((1 << sum_width)-1):0{(sum_width+3)//4}x}" for row in details],
        "controls.mem": [f"{2*row['reset_n']+row['input_valid']:x}" for row in schedule],
        "indices.mem": [f"{row['vector_index']:08x}" for row in schedule],
    }
    for filename, rows in lines.items():
        (folder / filename).write_text("\n".join(rows)+"\n", encoding="ascii")
    return {filename: sha(folder / filename) for filename in lines}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--windows", nargs="+", type=int, default=[1, 3, 5, 16],
                        help="window 길이. 기본1/3/5/16은 단일·홀수·2의 거듭제곱을 모두 검사")
    parser.add_argument("--random-cases", type=int, default=128, help="각 window의 고정 seed 추가 벡터 수")
    parser.add_argument("--seed", type=int, default=20261005, help="Python 난수 입력의 재현 seed")
    parser.add_argument("--timeout", type=int, default=120, help="Icarus 단계별 실제 벽시계 제한 초")
    parser.add_argument("--iverilog", help="iverilog.exe 실제 경로")
    parser.add_argument("--vvp", help="vvp.exe 실제 경로")
    parser.add_argument("--output", type=Path, default=ROOT / "build/reports/pooling_pu_verification.json",
                        help="판정·원시 로그·당시 source SHA·실제 검사 수를 기록할 JSON")
    args = parser.parse_args()
    if any(not 1 <= window <= 64 for window in args.windows) or args.random_cases < 0 or args.timeout <= 0:
        parser.error("window1..64, random-cases>=0, timeout>0이 필요합니다.")
    compiler, runtime = resolve_tool("iverilog", args.iverilog), resolve_tool("vvp", args.vvp)
    source_paths = [ROOT / "rtl/dram_pim_pooling_pu.sv", ROOT / "rtl/dram_pim_pooling_registered_top.sv",
                    ROOT / "tb/tb_pooling_pu.sv", ROOT / "model/pooling_q88.py", Path(__file__)]
    sources = {path.relative_to(ROOT).as_posix(): sha(path) for path in source_paths}
    report = {"passed": False, "recorded_utc": datetime.now(timezone.utc).isoformat(),
              "mode": "independent_q88_pooling_actual_icarus_rtl",
              "source_sha256": sources, "seed": args.seed, "random_cases_per_window": args.random_cases,
              "clock_hz_in_testbench": 5000000, "registered_latency_clocks": 1,
              "new_rtl_simulations_performed": True, "vivado_implementation_performed": False,
              "sdf_annotated": False, "physical_board_measured": False,
              "physical_dram_pim_measured": False, "canonical_gpt_connected": False,
              "configurations": []}
    started = time.perf_counter()
    output_root = ROOT / "build/pooling_pu" / args.output.stem
    try:
        report["python_contract_checks"] = check_reference_contract()
        for window in args.windows:
            vectors = make_vectors(window, args.random_cases, args.seed)
            details = [pool_details(v["values_raw"], v["valid_mask"], v["operation"]) for v in vectors]
            schedule = make_schedule(len(vectors))
            predicted, counts = expected_registered(schedule, details)
            counts["packed_checks"] = counts["accepted"] * (window+2)
            folder = output_root / f"window{window}"
            folder.mkdir(parents=True, exist_ok=True)
            memories = write_memories(folder, vectors, details, schedule, window)
            vector_json = folder / "vectors_and_schedule.json"
            vector_json.write_text(json.dumps({"vectors": vectors, "schedule": schedule}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
            configuration = {"window": window, "tree_leaves": details[0].tree_leaves,
                             "sum_width": details[0].sum_width, "vector_count": len(vectors),
                             "max_vectors": sum(v["operation"] == "max" for v in vectors),
                             "avg_vectors": sum(v["operation"] == "avg" for v in vectors),
                             "empty_vectors": sum(d.valid_count == 0 for d in details),
                             "negative_fractional_averages": sum(v["operation"] == "avg" and d.signed_sum < 0
                                 and d.valid_count != 0 and abs(d.signed_sum) % d.valid_count != 0
                                 for v,d in zip(vectors,details)),
                             "registered_cycles": len(schedule), **counts, "mem_sha256": memories,
                             "vectors_and_schedule": vector_json.relative_to(ROOT).as_posix(),
                             "vectors_and_schedule_sha256": sha(vector_json), "passed": False}
            report["configurations"].append(configuration)
            compile_step, _ = run_tool([compiler, "-g2012", "-s", "tb_pooling_pu",
                f"-Ptb_pooling_pu.WINDOW={window}", f"-Ptb_pooling_pu.VECTORS={len(vectors)}",
                f"-Ptb_pooling_pu.CYCLES={len(schedule)}", "-o", "simulation.vvp",
                str(source_paths[0]), str(source_paths[1]), str(source_paths[2])], folder, "compile", args.timeout)
            configuration["compile"] = compile_step
            simulation_step, output = run_tool([runtime, "simulation.vvp"], folder, "simulation", args.timeout)
            configuration["simulation"] = simulation_step
            comb = re.findall(r"CHECK_POOL vector=(\d+) op=(\d+) count=(\d+) result=([0-9a-fA-F]{4}) sum=(-?\d+)", output)
            assert len(comb) == len(vectors), "조합 비교 줄 개수가 다릅니다."
            for index, (number, operation, count, word, signed_sum) in enumerate(comb):
                expected = details[index]
                assert int(number) == index and int(operation) == (vectors[index]["operation"] == "avg")
                assert (int(count), int(word, 16), int(signed_sum)) == (expected.valid_count, expected.result_word, expected.signed_sum)
            registered = re.findall(r"CHECK_POOL_REG cycle=(\d+) valid=(\d+) result=([0-9a-fA-F]{4}) count=(\d+) exact=(\d+)", output)
            assert len(registered) == len(schedule), "등록 clock 비교 줄 개수가 다릅니다."
            cumulative = 0
            for index, (cycle, valid, word, count, exact) in enumerate(registered):
                expected = predicted[index]
                cumulative += expected["valid"]
                assert (int(cycle), int(valid), int(word,16), int(count), int(exact)) == (
                    index, expected["valid"], expected["word"], expected["count"], cumulative)
            wanted = (f"PASS_POOL window={window} vectors={len(vectors)} comb_checks={len(vectors)} cycles={len(schedule)} "
                      + " ".join(f"{name}={counts[name]}" for name in ["exact", "accepted", "cancelled", "resets",
                                "valid_checks", "packed_checks", "synchronous_checks", "maximum_burst"]))
            assert wanted in output and not re.search(r"FATAL:|ERROR:", output), "TB 최종 검사 개수가 다릅니다."
            configuration.update({"passed": True, "comb_result_comparisons": len(comb),
                                  "wide_sum_checks": len(comb), "valid_count_checks": len(comb),
                                  "continuous_valid_checked": True, "bubble_checked": True,
                                  "synchronous_reset_checked": True, "pending_cancelled_by_reset": True})
            print(f"POOLING PASS window={window} comb={len(comb)} registered={counts['exact']} cycles={len(schedule)}")
        report["total_comb_result_comparisons"] = sum(c["comb_result_comparisons"] for c in report["configurations"])
        report["total_registered_result_comparisons"] = sum(c["exact"] for c in report["configurations"])
        report["total_cycle_valid_checks"] = sum(c["valid_checks"] for c in report["configurations"])
        report["total_packed_field_checks"] = sum(c["packed_checks"] for c in report["configurations"])
        report["total_reset_cancelled_inputs"] = sum(c["cancelled"] for c in report["configurations"])
        report["source_unchanged_during_execution"] = all(sha(ROOT / filename) == digest for filename,digest in sources.items())
        assert report["source_unchanged_during_execution"]
        report["passed"] = True
    except Exception as error:
        report["failure_ko"] = f"{type(error).__name__}: {error}"
        raise
    finally:
        report["wall_seconds"] = round(time.perf_counter()-started, 6)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(f"전체 POOLING PASS: 조합{report['total_comb_result_comparisons']}·등록{report['total_registered_result_comparisons']}·clock{report['total_cycle_valid_checks']}, {report['wall_seconds']:.3f}초")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
