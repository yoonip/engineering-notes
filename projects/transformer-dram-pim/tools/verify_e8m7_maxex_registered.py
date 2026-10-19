#!/usr/bin/env python3
"""독립 등록 MAX-EX의 clock·valid·bubble·동기 reset·packed lane 계약을 검증한다."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from model.e8m7_maxex import maxex_dot
from tools.verify_e8m7_maxex import make_vectors, resolve_executable, run_tool


# packed input은 lane0이 최하위16bit다. mem 문자열은 왼쪽이 가장 높은 bit이므로
# 리스트를 역순으로 출력한다. 이것은 문자 UTF-8이나 UART byte 순서와 다른 층이다.
def packed_hex(words: list[int]) -> str:
    if any(not 0 <= word <= 0xffff for word in words):
        raise ValueError("E8M7 word는 0..65535여야 합니다.")
    return "".join(f"{word:04x}" for word in reversed(words))


# 서로 다른 lane별 알려진 word로 packed register index 검사를 읽기 쉽게 한다.
# 모든 값은 유한 정상수이고 Python maxex_dot가 최종 내적 정답을 만든다.
def lane_tag_vector(lanes: int) -> dict:
    return {"name": "distinct_lane_tags",
            "a_words": [0x3f80 + lane for lane in range(lanes)],
            "b_words": [0x4000 + lane * 3 for lane in range(lanes)]}


# schedule 한 항목은 rising edge 하나의 입력이다. accepted라는 단어는 reset이
# 풀리고 input_valid가1인 edge를 뜻한다. reset과 valid가 동시에1이면 reset 우선이다.
def make_schedule(vectors: list[dict]) -> list[dict]:
    rows: list[dict] = []

    def add(phase: str, reset_n: bool, valid: bool = False, index: int = 0) -> None:
        rows.append({"cycle": len(rows), "phase": phase, "reset_n": reset_n,
                     "input_valid": valid, "vector_index": index})

    add("initial_reset", False)
    add("reset_priority_ignores_valid", False, True, 1)
    add("release_idle", True)
    add("single_input", True, True, 0)
    add("single_output_then_bubble", True)
    add("idle", True)
    # 모든 경계·random vector를 한clock 간격으로 넣어 throughput과 순서를 검사한다.
    for index in range(len(vectors)):
        add("continuous", True, True, index)
    add("continuous_flush", True)
    add("idle_after_burst", True)
    # 0/1/2개의bubble을 순환해 valid pulse의 폭과 데이터 유지 경계를 검사한다.
    for index in range(min(32, len(vectors))):
        add("bubble_sequence_input", True, True, index)
        for _ in range(index % 3):
            add("bubble_sequence_idle", True)
    add("bubble_flush", True)
    # 두 연속 입력 중 첫 결과는 나오고, 두 번째의 pending 결과는 reset으로 취소한다.
    add("before_reset_input_1", True, True, 2)
    add("before_reset_input_2", True, True, 3)
    add("reset_cancels_pending_and_ignores_new_valid", False, True, 4)
    add("held_reset", False)
    add("release_after_cancel_idle", True)
    add("repeat_after_reset_1", True, True, 2)
    add("repeat_after_reset_2", True, True, 3)
    add("final_flush", True)
    add("final_idle", True)
    return rows


# TB 내부 scoreboard와 별도로 Python에서도1clock 지연을 예측한다. 현재 edge의
# expected output은 직전 accepted 입력에서 오며 reset edge에서는 출력0으로 지운다.
def expected_cycles(schedule: list[dict], vectors: list[dict], guard: int, lanes: int) -> tuple[list[dict], dict]:
    pending: int | None = None
    expected = []
    counts = {"accepted": 0, "cancelled": 0, "resets": 0, "exact": 0,
              "lane_checks": 0, "valid_checks": len(schedule),
              "synchronous_checks": len(schedule), "maximum_burst": 0}
    burst = 0
    for row in schedule:
        if not row["reset_n"]:
            expected.append({"valid": 0, "word": 0})
            counts["resets"] += 1
            counts["cancelled"] += pending is not None
            pending = None
            burst = 0
        else:
            expected.append({"valid": int(pending is not None), "word": pending})
            counts["exact"] += pending is not None
            if row["input_valid"]:
                vector = vectors[row["vector_index"]]
                pending = maxex_dot(vector["a_words"], vector["b_words"], guard)
                counts["accepted"] += 1
                counts["lane_checks"] += 2 * lanes
                burst += 1
                counts["maximum_burst"] = max(counts["maximum_burst"], burst)
            else:
                pending = None
                burst = 0
    assert pending is None, "마지막 pending 입력을 flush해야 합니다."
    assert counts["accepted"] == counts["exact"] + counts["cancelled"]
    return expected, counts


# 각 mem은 schedule의 cycle index와 같은 줄 수다. expected.mem은 그cycle의 입력
# 내적 정답이고 TB가 이를 보관한 뒤 다음edge에서 비교한다. idle 결과는 비교하지 않는다.
def write_memories(folder: Path, schedule: list[dict], vectors: list[dict], guard: int) -> None:
    content = {"controls.mem": [], "a.mem": [], "b.mem": [], "expected.mem": []}
    for row in schedule:
        vector = vectors[row["vector_index"]]
        content["controls.mem"].append(f"{2 * row['reset_n'] + row['input_valid']:x}")
        content["a.mem"].append(packed_hex(vector["a_words"]))
        content["b.mem"].append(packed_hex(vector["b_words"]))
        content["expected.mem"].append(f"{maxex_dot(vector['a_words'], vector['b_words'], guard):04x}")
    for filename, lines in content.items():
        (folder / filename).write_text("\n".join(lines) + "\n", encoding="ascii")


# LANES3은 홀수 padding과 wrapper packing, LANES16은 원 제안의16lane를 검사한다.
# 기본 G16/G32는 실제 OOC의 설정이며 이 명령은 Vivado/OOC/SDF를 새로 실행하지 않는다.
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lanes", nargs="+", type=int, default=[3, 16],
                        help="wrapper lane 수; 기본3 16, Icarus 배열 지원상2..32")
    parser.add_argument("--guard-bits", nargs="+", type=int, choices=[16, 32], default=[16, 32],
                        help="실제 OOC와 같은 guard 폭; 기본16 32")
    parser.add_argument("--random-cases", type=int, default=128, help="lane별 추가 seeded vector 수")
    parser.add_argument("--seed", type=int, default=20261004, help="vector 생성 고정 seed")
    parser.add_argument("--timeout", type=int, default=300, help="도구 단계별 벽시계 제한 초")
    parser.add_argument("--iverilog", help="Icarus compiler 절대 경로")
    parser.add_argument("--vvp", help="Icarus runtime 절대 경로")
    parser.add_argument("--output", type=Path,
                        default=ROOT / "build/reports/e8m7_maxex_registered_verification.json",
                        help="실제 명령·판정·로그·SHA를 저장할 JSON")
    args = parser.parse_args()
    if any(not 2 <= lanes <= 32 for lanes in args.lanes) or args.random_cases < 0 or args.timeout <= 0:
        parser.error("LANES2..32, random-cases>=0, timeout>0이 필요합니다.")
    compiler = resolve_executable("iverilog", args.iverilog)
    runtime = resolve_executable("vvp", args.vvp)
    files = [ROOT / "rtl/dram_pim_e8m7_maxex_mac.sv", ROOT / "rtl/e8m7_maxex_registered_top.sv",
             ROOT / "tb/tb_e8m7_maxex_registered_top.sv", Path(__file__),
             ROOT / "tools/verify_e8m7_maxex.py", ROOT / "model/e8m7_maxex.py"]
    report = {"passed": False, "mode": "registered_maxex_rtl_clock_protocol_regression",
              "clock_hz": 5000000, "latency_clocks": 1, "seed": args.seed,
              "physical_board_measured": False, "sdf_annotated": False,
              "routed_delays_simulated": False, "gpt_q88_connected": False,
              "source_sha256": {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in files}, "configurations": [], "schedules": {}}
    output_root = ROOT / "build/e8m7_maxex" / args.output.stem
    try:
        for lanes in args.lanes:
            vectors = [lane_tag_vector(lanes)] + make_vectors(lanes, args.random_cases, args.seed)
            schedule = make_schedule(vectors)
            report["schedules"][str(lanes)] = {"vectors": vectors, "cycles": schedule}
            for guard in args.guard_bits:
                folder = output_root / f"lanes{lanes}_guard{guard}"
                folder.mkdir(parents=True, exist_ok=True)
                write_memories(folder, schedule, vectors, guard)
                expected, counts = expected_cycles(schedule, vectors, guard, lanes)
                compile_step = run_tool([compiler, "-g2012", "-s", "tb_e8m7_maxex_registered_top",
                    f"-Ptb_e8m7_maxex_registered_top.LANES={lanes}",
                    f"-Ptb_e8m7_maxex_registered_top.GUARD_BITS={guard}",
                    f"-Ptb_e8m7_maxex_registered_top.CYCLES={len(schedule)}", "-o", "simulation.vvp",
                    str(files[0]), str(files[1]), str(files[2])], folder, "compile", args.timeout)
                simulation_step = run_tool([runtime, "simulation.vvp"], folder, "simulation", args.timeout)
                text = simulation_step["stdout"]
                rows = re.findall(r"CHECK_REG cycle=(\d+) valid=(\d+) result=([0-9a-fA-F]{4}) exact=(\d+)", text)
                assert len(rows) == len(schedule), "cycle 출력 수 불일치"
                compared = 0
                for index, (cycle, valid, word, count) in enumerate(rows):
                    assert int(cycle) == index and int(valid) == expected[index]["valid"]
                    if expected[index]["valid"]:
                        assert int(word, 16) == expected[index]["word"]
                        compared += 1
                    elif not schedule[index]["reset_n"]:
                        assert int(word, 16) == 0, "reset result는0이어야 합니다."
                    assert int(count) == compared
                wanted = (f"PASS_REG lanes={lanes} guard={guard} cycles={len(schedule)} "
                          + " ".join(f"{key}={counts[key]}" for key in
                             ["exact", "accepted", "cancelled", "resets", "lane_checks", "valid_checks",
                              "synchronous_checks", "maximum_burst"]))
                assert wanted in text, "TB의 protocol 검사 개수가 Python 예측과 다릅니다."
                assert not re.search(r"FATAL:|ERROR:", text), "TB 오류 로그"
                report["configurations"].append({"lanes": lanes, "guard_bits": guard,
                    "vector_count": len(vectors), "cycles": len(schedule), **counts,
                    "one_clock_latency_checked": True, "continuous_valid_checked": True,
                    "bubble_checked": True, "pending_cancelled_by_reset": True,
                    "packed_lane_register_order_checked": True,
                    "compile": {k: v for k, v in compile_step.items() if k != "stdout"},
                    "simulation": {k: v for k, v in simulation_step.items() if k != "stdout"}})
                print(f"REGISTERED MAXEX PASS lanes={lanes} guard={guard} "
                      f"cycles={len(schedule)} exact={counts['exact']} accepted={counts['accepted']} "
                      f"cancelled={counts['cancelled']} maximum-burst={counts['maximum_burst']}")
        report["total_word_comparisons"] = sum(c["exact"] for c in report["configurations"])
        report["total_cycle_valid_checks"] = sum(c["valid_checks"] for c in report["configurations"])
        report["total_packed_lane_word_checks"] = sum(c["lane_checks"] for c in report["configurations"])
        report["passed"] = True
    except Exception as error:
        report["failure_ko"] = f"{type(error).__name__}: {error}"
        raise
    finally:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"전체 등록 MAXEX PASS: {report['total_word_comparisons']}word / "
          f"{report['total_cycle_valid_checks']}cycle valid, 결과 {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
