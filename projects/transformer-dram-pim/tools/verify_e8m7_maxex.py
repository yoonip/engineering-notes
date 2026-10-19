#!/usr/bin/env python3
"""독립 E8M7 MAX-EX MAC의 Python/SV 정수 비트 대조 실행 입구."""

# 이 파일은 원 제안서의 부동소수점 내적 아이디어만 독립 검증한다. 기존 Q8.8
# GPT checkpoint와 이미 생성한 Nexys bitstream을 수정하거나 재학습하지 않는다.
# Python reference가 정한 bit 결과와 실제 Icarus 출력을 비교하며, 정확한
# Fraction dot product와의 차이는 ‘허용된 alignment 근사 오차’로 별도 기록한다.
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random
import re
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from model.e8m7_maxex import (
    decode_e8m7_fraction,
    exact_dot_e8m7,
    maxex_dot_details,
)


# 실행 환경이 이미 PATH를 준비했으면 그 Icarus를 사용한다. Windows 현재 환경의
# 설치 경로는 fallback이며 사용자 PC에서도 --iverilog/--vvp로 지정할 수 있다.
def resolve_executable(name: str, explicit: str | None) -> str:
    if explicit:
        path = Path(explicit)
        if not path.is_file():
            raise FileNotFoundError(f"실행 파일이 없습니다: {path}")
        return str(path.resolve())
    candidate = shutil.which(name)
    if candidate:
        return candidate
    path = Path("C:/iverilog/bin") / f"{name}.exe"
    if path.is_file():
        return str(path)
    raise FileNotFoundError(f"{name}를 PATH 또는 --{name} 옵션으로 지정하세요.")


# 다른 precision 결과가 한 실행을 덮어쓰지 않도록 lane/guard별 작업 폴더에서
# 독립 compile/simulation한다. stdout/stderr·종료코드·명령을 실제 그대로 보존한다.
def run_tool(command: list[str], directory: Path, label: str, timeout: int) -> dict:
    started = time.perf_counter()
    completed = subprocess.run(command, cwd=directory, capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=timeout)
    log = directory / f"{label}.log"
    log.write_text(completed.stdout + completed.stderr, encoding="utf-8")
    record = {"command": command, "returncode": completed.returncode,
              "wall_seconds": round(time.perf_counter() - started, 6), "log": str(log)}
    if completed.returncode:
        raise RuntimeError(f"{label} 실패(exit {completed.returncode}): {log}")
    record["stdout"] = completed.stdout
    return record


# 2^exponent의 정확한 E8M7 정상수 word. 아래 vector 생성의 exponent는 -126..127
# 범위이므로 Python float 반올림이나 platform 차이가 개입하지 않는다.
def power_word(exponent: int, negative: bool = False) -> int:
    if not -126 <= exponent <= 127:
        raise ValueError("정상수 지수 범위를 벗어났습니다.")
    return (0x8000 if negative else 0) | ((exponent + 127) << 7)


# lane 수가 작은 경우 구성할 수 없는 multi-term 사례는 생략한다. 각 실제 사례는
# 나머지 lane을 +0으로 채워 odd-LANES padding과 zero exponent sentinel도 검사한다.
def make_vectors(lanes: int, count: int, seed: int, finite_random: bool = False) -> list[dict]:
    vectors: list[dict] = []

    def add(name: str, a: list[int], b: list[int]) -> None:
        if len(a) <= lanes:
            vectors.append({"name": name, "a_words": a + [0] * (lanes - len(a)),
                            "b_words": b + [0] * (lanes - len(b))})

    # 특수값·부호 zero·최소 subnormal·RNE tie·overflow를 먼저 고정 사례로 검사한다.
    add("all_positive_zero", [0], [0])
    add("signed_zero_sum_is_positive_zero", [0x8000], [0x3f80])
    add("one_times_one", [0x3f80], [0x3f80])
    add("negative_one_times_two", [0xbf80], [0x4000])
    add("minimum_subnormal", [0x0001], [0x3f80])
    add("negative_minimum_subnormal", [0x8001], [0x3f80])
    add("positive_half_subnormal_tie_to_zero", [0x0001], [0x3f00])
    add("negative_half_subnormal_tie_to_negative_zero", [0x8001], [0x3f00])
    add("one_and_half_subnormal_tie_to_even_two", [0x0003], [0x3f00])
    add("minimum_normal", [0x0080], [0x3f80])
    add("maximum_finite", [0x7f7f], [0x3f80])
    add("finite_multiply_overflow", [0x7f7f], [0x4000])
    add("negative_finite_multiply_overflow", [0xff7f], [0x4000])
    add("infinity_times_finite", [0x7f80], [0x3f80])
    add("negative_infinity_times_negative_finite", [0xff80], [0xbf80])
    add("infinity_times_zero_invalid", [0x7f80], [0])
    add("zero_times_negative_infinity_invalid", [0x8000], [0xff80])
    add("quiet_nan_canonical", [0x7fc1], [0x3f80])
    add("signaling_nan_canonical", [0xff81], [0x3f80])
    add("opposite_infinities_invalid", [0x7f80, 0xff80], [0x3f80, 0x3f80])
    add("finite_exact_cancellation", [0x3f80, 0xbf80], [0x3f80, 0x3f80])
    add("normal_halfway_even_down", [0x3f80, power_word(-8)], [0x3f80, 0x3f80])
    add("normal_halfway_odd_up", [0x3f81, power_word(-8)], [0x3f80, 0x3f80])
    add("subnormal_round_to_minimum_normal", [0x007f, 0x0001], [0x3f80, 0x3f00])
    add("maximum_finite_round_to_infinity", [0x7f7f, power_word(119)], [0x3f80, 0x3f80])
    add("guard_precision_after_cancellation", [power_word(20), power_word(20, True),
                                              power_word(-20)], [0x3f80] * 3)
    add("negative_guard_precision_after_cancellation", [power_word(20), power_word(20, True),
                                                       power_word(-20, True)], [0x3f80] * 3)
    # 유한 입력끼리의 곱이 E8M7 저장 범위를 넘어도 곱을 먼저Inf로 바꾸지 않는다.
    # 큰 두 항은 정확히 상쇄하며 작은1은 guard16/32 모두 정렬 중 잃을 수 있다.
    # exact Fraction dot은1이므로 guard32도 exact-dot와 항상 같지 않음을 보여 준다.
    add("extreme_finite_cancellation_loses_unit", [0x7f7f, 0xff7f, 0x3f80],
        [0x7f7f, 0x7f7f, 0x3f80])
    add("wide_accumulator_same_sign_all_lanes", [0x3fff] * lanes, [0x3fff] * lanes)
    add("all_subnormal_lanes", [0x007f] * lanes, [0x007f] * lanes)

    rng = random.Random(seed + lanes)
    # 광폭 guard512 시험은 모든 유한 입력에서 exact Fraction-dot 결과와 같아야
    # 한다. finite_random을 켜면 임의 입력 중 exponent255의 NaN/Inf만 제외한다.
    # 고정 경계 vector의 NaN/Inf 시험은 그대로 유지한다.
    def random_word() -> int:
        word = rng.randrange(65536)
        while finite_random and (word & 0x7f80) == 0x7f80:
            word = rng.randrange(65536)
        return word

    for index in range(count):
        # 큰 양수·음수를 상쇄한 다음 작은 항만 남는 사례를 반복 생성해 GUARD16/32
        # 차이를 우연에 맡기지 않는다. 나머지는 전체16bit 패턴의 결정론적 random.
        if lanes >= 3 and index % 4 == 0:
            exponent = rng.randint(0, 100)
            gap = rng.randint(33, 45)
            negative = bool(rng.getrandbits(1))
            a = [power_word(exponent), power_word(exponent, True),
                 power_word(exponent - gap, negative)]
            b = [0x3f80] * 3
            a += [0] * (lanes - 3)
            b += [0] * (lanes - 3)
            name = f"random_cancellation_gap_{gap}_{index}"
        else:
            a = [random_word() for _ in range(lanes)]
            b = [random_word() for _ in range(lanes)]
            name = f"random_word_patterns_{index}"
        vectors.append({"name": name, "a_words": a, "b_words": b})
    return vectors


# reference 내부에서는 Fraction을 쓰므로 guard 손실과 최종 E8M7 저장 반올림을
# 따로 알 수 있다. JSON에 Fraction을 ‘분자/분모’ 문자열로 저장해 정보 손실을 막는다.
def finite_fraction(word: int) -> Fraction | None:
    if (word >> 7) & 255 == 255:
        return None
    return decode_e8m7_fraction(word)


# 마지막 저장 결과 기준의1ULP를 정의한다. 정상수는 해당 exponent의 fraction1칸,
# subnormal/zero는2^-133이다. 값이 Inf/NaN인 경우 오차 단위를 억지로 만들지 않는다.
def output_ulp(word: int) -> Fraction | None:
    exponent = (word >> 7) & 255
    if exponent == 255:
        return None
    power = -133 if exponent == 0 else exponent - 127 - 7
    return Fraction(1 << power, 1) if power >= 0 else Fraction(1, 1 << -power)


# mem 파일은 첫 원소부터 row-major lane 순서로 쓴다. readmemh의 배열 index와
# Python list index가 일치하고, E8M7 word는 소수 문자열이 아닌4자리 hex다.
def write_words(path: Path, words: list[int]) -> None:
    path.write_text("".join(f"{word:04x}\n" for word in words), encoding="ascii")


# 합법적인 사용자 검증 범위를 argparse로 명시한다. 기본4종 lane은 단일lane,
# 두 odd 크기, 원 제안의16lane이며 guard16/32를 같은 vector에 적용한다.
def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="E8M7 MAX-EX Python/RTL 비트 대조")
    parser.add_argument("--lanes", nargs="+", type=int, default=[1, 3, 5, 16],
                        help="내적 lane 수; odd lane padding 포함(기본1 3 5 16)")
    parser.add_argument("--guard-bits", nargs="+", type=int, default=[16, 32],
                        help="정렬 후 보존할 추가 bit 수(기본16 32, 허용0..512)")
    parser.add_argument("--random-cases", type=int, default=256,
                        help="lane 구성마다 추가할 결정론적 random vector 수")
    parser.add_argument("--seed", type=int, default=20261004, help="재현 random seed")
    parser.add_argument("--finite-random", action="store_true",
                        help="random vector에서 NaN/Inf를 제외; 고정 특수값 경계 시험은 유지")
    parser.add_argument("--timeout", type=int, default=300, help="각 도구 벽시계 제한 초")
    parser.add_argument("--iverilog", help="Icarus compiler 실행 파일 절대 경로")
    parser.add_argument("--vvp", help="Icarus runtime 실행 파일 절대 경로")
    parser.add_argument("--output", type=Path,
                        default=ROOT / "build/reports/e8m7_maxex_rtl_verification.json",
                        help="전체 검증 JSON 저장 위치")
    args = parser.parse_args()
    if any(value < 1 for value in args.lanes):
        parser.error("LANES는1 이상이어야 합니다.")
    if any(not 0 <= value <= 512 for value in args.guard_bits):
        parser.error("GUARD_BITS는0..512 범위여야 합니다.")
    if args.random_cases < 0 or args.timeout < 1:
        parser.error("random-cases>=0 및 timeout>=1이 필요합니다.")
    return args


# expected word는 Python MAX-EX 사양이고 exact Fraction dot은 별도 비교값이다.
# 합성 회로와 Python reference 일치는 assert로 요구하지만 두 수치 알고리즘의
# 차이는 정당한 근사 차이로 기록한다. 후자를 무조건 ‘버그’로 지우지 않는다.
def main() -> None:
    args = parse_arguments()
    compiler = resolve_executable("iverilog", args.iverilog)
    runtime = resolve_executable("vvp", args.vvp)
    # 기본시험과 확대시험의 log/mem을 함께 보존한다. 출력 JSON 이름별 작업 root를
    # 나누므로 확대시험이 기본시험에 기록된 compile/simulation log를 덮어쓰지 않는다.
    work_root = ROOT / "build/e8m7_maxex" / args.output.stem
    report = {
        "passed": False, "mode": "independent_e8m7_maxex_rtl_python_verification",
        "gpt_q88_connected": False, "physical_board_measured": False,
        "definition_ko": "정확한8x8 product→균형 MAX-EX→magnitude alignment 절삭→signed 넓은 트리→최종RNE",
        "lanes": args.lanes, "guard_bits": args.guard_bits, "seed": args.seed,
        "random_cases_per_lane": args.random_cases, "configurations": [],
        "finite_random": args.finite_random,
        "guard16_guard32_differences": [], "vectors": [],
        "scope_ko": "Python MAX-EX reference와 비트 일치. 좁은 alignment 손실이 있어 exact-dot와 같다고 주장하지 않음.",
    }
    report["source_sha256"] = {
        path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in [ROOT / "rtl/dram_pim_e8m7_maxex_mac.sv",
                     ROOT / "tb/tb_e8m7_maxex_mac.sv", Path(__file__),
                     ROOT / "model/e8m7_maxex.py"]
    }
    try:
        for lanes in args.lanes:
            vectors = make_vectors(lanes, args.random_cases, args.seed, args.finite_random)
            exact_words = [exact_dot_e8m7(v["a_words"], v["b_words"]) for v in vectors]
            results_by_guard: dict[int, list[int]] = {}
            for guard in args.guard_bits:
                directory = work_root / f"lanes{lanes}_guard{guard}"
                directory.mkdir(parents=True, exist_ok=True)
                details = [maxex_dot_details(v["a_words"], v["b_words"], guard_bits=guard)
                           for v in vectors]
                expected = [d.result_word for d in details]
                # 둘이 같은 잘못된 rounding을 공유하는 상황을 줄이기 위해 알려진
                # 비트 패턴을 따로 요구한다. 대부분 guard와 무관한 경계 정답이며,
                # 극단 상쇄의 작은1 보존 여부는 아래처럼 guard 폭에 따라 달리 요구한다.
                known_words = {"normal_halfway_even_down": 0x3f80,
                               "normal_halfway_odd_up": 0x3f82,
                               "subnormal_round_to_minimum_normal": 0x0080,
                               "maximum_finite_round_to_infinity": 0x7f80,
                               "negative_half_subnormal_tie_to_negative_zero": 0x8000,
                               "opposite_infinities_invalid": 0x7fc0,
                               "extreme_finite_cancellation_loses_unit": (0x3f80 if guard >= 240 else 0x0000)}
                for vector, word in zip(vectors, expected):
                    if vector["name"] in known_words:
                        assert word == known_words[vector["name"]], vector["name"]
                # 유한 product exponent 차의 최대는254-(-252)=506이다. G>=506이면
                # 각 product의 모든 bit가 정렬 후 남아 exact Fraction-dot를 마지막에
                # RNE한 결과와 같아야 한다. 좁은16/32 버전에 이 요구를 적용하지 않는다.
                if guard >= 506:
                    assert expected == exact_words, (lanes, guard, "wide-guard exact Fraction dot")
                write_words(directory / "a.mem", [w for v in vectors for w in v["a_words"]])
                write_words(directory / "b.mem", [w for v in vectors for w in v["b_words"]])
                write_words(directory / "expected.mem", expected)
                compile_step = run_tool([
                    compiler, "-g2012", "-s", "tb_e8m7_maxex_mac",
                    f"-Ptb_e8m7_maxex_mac.LANES={lanes}",
                    f"-Ptb_e8m7_maxex_mac.GUARD_BITS={guard}",
                    f"-Ptb_e8m7_maxex_mac.CASES={len(vectors)}", "-o", "simulation.vvp",
                    str(ROOT / "rtl/dram_pim_e8m7_maxex_mac.sv"),
                    str(ROOT / "tb/tb_e8m7_maxex_mac.sv"),
                ], directory, "compile", args.timeout)
                simulation_step = run_tool([runtime, "simulation.vvp"], directory, "simulation", args.timeout)
                rows = re.findall(r"MAXEX case=(\d+) result=([0-9a-fA-F]{4}) maxexp=(-?\d+) accumulator=(-?\d+)",
                                  simulation_step["stdout"])
                if len(rows) != len(vectors):
                    raise AssertionError(f"출력 행 수가 다릅니다: lanes{lanes}/guard{guard}")
                # 결과word뿐 아니라 모든 유한 입력에서 MAXEX와 누산값도 비교한다.
                # 이는 잘못된 부호 shift·width overflow가 우연히 최종 반올림에 가려지는
                # 경우를 잡는다. 특수값은 canonical 결과word의 우선순위만 검사한다.
                intermediate_checks = 0
                for index, word_hex, maxexp, accumulator in rows:
                    i = int(index)
                    detail = details[i]
                    assert int(word_hex, 16) == detail.result_word, (lanes, guard, i, vectors[i]["name"])
                    if detail.reconstructed is not None:
                        assert int(maxexp) == (detail.max_exponent if detail.max_exponent is not None else -512)
                        assert int(accumulator) == detail.accumulator, (lanes, guard, i, "accumulator")
                        intermediate_checks += 1
                results_by_guard[guard] = expected
                mismatch_count = sum(a != b for a, b in zip(expected, exact_words))
                report["configurations"].append({
                    "lanes": lanes, "guard_bits": guard, "cases": len(vectors),
                    "rtl_exact_matches": len(rows), "finite_intermediate_checks": intermediate_checks,
                    "exact_dot_different_results": mismatch_count,
                    "compile": {k: v for k, v in compile_step.items() if k != "stdout"},
                    "simulation": {k: v for k, v in simulation_step.items() if k != "stdout"},
                })
                print(f"MAXEX PASS lanes={lanes} guard={guard} cases={len(rows)} exact-dot-differences={mismatch_count}")

            for index, vector in enumerate(vectors):
                record = {"lanes": lanes, "case": index, **vector,
                          "exact_result": f"{exact_words[index]:04x}",
                          "guard_results": {str(g): f"{words[index]:04x}" for g, words in results_by_guard.items()}}
                # 전체 vector 목록에 원본 word를 남겨 차이가 난 사례를 제3자가 재실행하게 한다.
                report["vectors"].append(record)
                if 16 in results_by_guard and 32 in results_by_guard:
                    g16, g32 = results_by_guard[16][index], results_by_guard[32][index]
                    if g16 != g32:
                        exact = maxex_dot_details(vector["a_words"], vector["b_words"], guard_bits=32).exact
                        unit = output_ulp(exact_words[index])
                        errors = {}
                        for guard, word in ((16, g16), (32, g32)):
                            value = finite_fraction(word)
                            errors[str(guard)] = (str(abs(value-exact) / unit)
                                                 if value is not None and exact is not None and unit is not None else None)
                        report["guard16_guard32_differences"].append({
                            **record, "exact_value_fraction": str(exact),
                            "ulp_unit_fraction": str(unit), "absolute_error_in_exact_output_ulp": errors})
        report["passed"] = True
        report["total_rtl_word_comparisons"] = sum(c["rtl_exact_matches"] for c in report["configurations"])
        report["total_guard16_guard32_differences"] = len(report["guard16_guard32_differences"])
    except Exception as error:
        report["failure_ko"] = f"{type(error).__name__}: {error}"
        raise
    finally:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"전체 MAXEX RTL/Python PASS: {report['total_rtl_word_comparisons']}개, 결과 {args.output}")


if __name__ == "__main__":
    main()
