#!/usr/bin/env python3
# Icarus로 SV testbench를 compile/simulate하고 출력 숫자를 독립 Python oracle과 비교한다.
# iverilog는 simulation image를 만들고 vvp가 실행한다. Vivado bitstream/board 구동은 아니다.
# PASS marker와 모든 숫자 일치를 함께 확인하며 종료코드0만으로 정답이라고 판정하지 않는다.
"""SystemVerilog RTL 두 종류의 자가검증 테스트와 Python 기준 모델 비교를 실행한다."""

from __future__ import annotations

import re
import os
import shutil
import sys
from pathlib import Path

from model.reference import reference_output
from model.gpt_core_reference import decoder_stack
from model.gpt_language_model_reference import language_model_logits
# 한국어 Windows의 Icarus는 경로를 CP949로 출력할 수 있다. 콘솔 문자 해석만
# 공통 함수에 맡기며 argument list·RTL 수식·PASS/숫자 비교는 그대로 유지한다.
from tools.console_text import run_console

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"
RTL = ROOT / "rtl"
TB = ROOT / "tb" / "tb_transformer.sv"
TREE_TB = ROOT / "tb" / "tb_vmm_adder_tree.sv"
GPT_TB = ROOT / "tb" / "tb_gpt_stack.sv"


# PATH/프로젝트 설치 후보에서 실행파일을 찾고 없으면 명시적으로 실패한다.
def find_tool(name: str, windows_fallback: str) -> str:
    found = shutil.which(name)
    if found:
        return found
    fallback = Path(windows_fallback)
    if fallback.exists():
        return str(fallback)
    suite_root = Path(os.environ.get("OSS_CAD_SUITE", Path.home() / "Documents" / "ChatGPT" / "oss-cad-suite"))
    suite_tool = suite_root / "bin" / f"{name}.exe"
    if suite_tool.exists():
        return str(suite_tool)
    raise FileNotFoundError(
        f"{name}를 찾지 못했습니다. Icarus Verilog 12 이상을 설치하거나 PATH에 추가하세요."
    )


# 명령행 진입 함수. 옵션/입력/도구를 준비해 이 파일의 학습·추론·검증·분석 결과를 저장한다.
# 성공은 return0,오류는 예외/종료코드로 알린다. __main__ 직접 실행에서 자동 호출된다.
def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    compiler = find_tool("iverilog", "C:/iverilog/bin/iverilog.exe")
    simulator = find_tool("vvp", "C:/iverilog/bin/vvp.exe")
    BUILD.mkdir(exist_ok=True)
    image = BUILD / "transformer_tb.vvp"
    tree_image = BUILD / "vmm_tree_tb.vvp"
    gpt_image = BUILD / "gpt_stack_tb.vvp"
    # 컴파일할 RTL/core/TB 목록. top을 지정하여 의도한 회로를 검사한다.
    sources = [
        RTL / "dram_pim_nonvmm_pu.sv",
        RTL / "dram_pim_vmm_bank.sv",
        RTL / "dram_pim_scheduler.sv",
        RTL / "transformer_decoder_pim_comb.sv",
        RTL / "transformer_decoder_pim.sv",
        TB,
    ]

    # 외부 도구 실제 실행. argument list로 전달하고 stdout/stderr/종료코드 또는 log를 남긴다.
    # 실패/누락 출력은 성공으로 간주하지 않도록 뒤에서 returncode와 oracle 숫자를 확인한다.
    compile_result = run_console(
        [compiler, "-g2012", "-Wall", "-s", "tb_transformer", "-o", str(image),
         *map(str, sources)],
        cwd=ROOT, capture_output=True,
    )
    if compile_result.stdout:
        print(compile_result.stdout, end="")
    if compile_result.stderr:
        print(compile_result.stderr, end="", file=sys.stderr)
    if compile_result.returncode:
        return compile_result.returncode

    # 별도 테스트벤치는 K=3을 사용해 2의 거듭제곱이 아닌 내적 길이와
    # adder tree의 0 padding, 상쇄, 출력 포화를 집중 점검한다.
    # 외부 도구 실제 실행. argument list로 전달하고 stdout/stderr/종료코드 또는 log를 남긴다.
    # 실패/누락 출력은 성공으로 간주하지 않도록 뒤에서 returncode와 oracle 숫자를 확인한다.
    tree_compile = run_console(
        [compiler, "-g2012", "-Wall", "-s", "tb_vmm_adder_tree", "-o", str(tree_image),
         str(RTL / "dram_pim_vmm_bank.sv"), str(TREE_TB)],
        cwd=ROOT, capture_output=True,
    )
    if tree_compile.stdout:
        print(tree_compile.stdout, end="")
    if tree_compile.stderr:
        print(tree_compile.stderr, end="", file=sys.stderr)
    if tree_compile.returncode:
        return tree_compile.returncode

    # 외부 도구 실제 실행. argument list로 전달하고 stdout/stderr/종료코드 또는 log를 남긴다.
    # 실패/누락 출력은 성공으로 간주하지 않도록 뒤에서 returncode와 oracle 숫자를 확인한다.
    simulation = run_console(
        [simulator, str(image)], cwd=ROOT, capture_output=True,
    )
    clean_stdout = "\n".join(
        line for line in simulation.stdout.splitlines()
        if "$finish called at" not in line
    )
    if clean_stdout:
        print(clean_stdout)
    if simulation.stderr:
        print(simulation.stderr, end="", file=sys.stderr)
    if simulation.returncode:
        return simulation.returncode
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if "PASS: transformer datapath" not in clean_stdout:
        raise AssertionError("Transformer 테스트벤치가 PASS 표식을 출력하지 않았습니다.")

    # 외부 도구 실제 실행. argument list로 전달하고 stdout/stderr/종료코드 또는 log를 남긴다.
    # 실패/누락 출력은 성공으로 간주하지 않도록 뒤에서 returncode와 oracle 숫자를 확인한다.
    tree_simulation = run_console(
        [simulator, str(tree_image)], cwd=ROOT, capture_output=True,
    )
    if tree_simulation.stdout:
        print(tree_simulation.stdout, end="")
    if tree_simulation.stderr:
        print(tree_simulation.stderr, end="", file=sys.stderr)
    if tree_simulation.returncode:
        return tree_simulation.returncode
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if "PASS: balanced Q8.8 VMM adder tree" not in tree_simulation.stdout:
        raise AssertionError("VMM adder tree 테스트가 PASS 표식을 출력하지 않았습니다.")

    actual: dict[int, list[int]] = {}
    for line in clean_stdout.splitlines():
        match = re.fullmatch(r"OUTPUT token=(\d+) (-?\d+(?: -?\d+)*)", line.strip())
        if match:
            actual[int(match.group(1))] = [int(value) for value in match.group(2).split()]

    # Python oracle 정답. 실제 RTL 숫자와 전체 비교한다.
    expected = reference_output()
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if actual != {i: row for i, row in enumerate(expected)}:
        raise AssertionError(
            f"RTL과 Python 기준값이 다릅니다.\nRTL: {actual}\n기준값: {expected}"
        )
    print("PASS: Python 기준 모델과 RTL의 16개 출력값이 모두 일치합니다.")

    # 2-head×2-layer decoder core. 각 layer는 다른 packed weights를 받고,
    # stack의 앞 layer 출력이 다음 layer 입력이 되는지 독립 기준 모델과 확인한다.
    gpt_sources = [
        RTL / "dram_pim_pu_synth.sv",
        RTL / "dram_pim_vmm_bank.sv",
        RTL / "transformer_decoder_mha_pim_comb.sv",
        RTL / "transformer_gpt_decoder_stack_comb.sv",
        RTL / "transformer_gpt_language_model_comb.sv",
        RTL / "transformer_gpt_language_model_seq.sv",
        RTL / "transformer_gpt_kvcache_seq.sv",
        GPT_TB,
    ]
    # 외부 도구 실제 실행. argument list로 전달하고 stdout/stderr/종료코드 또는 log를 남긴다.
    # 실패/누락 출력은 성공으로 간주하지 않도록 뒤에서 returncode와 oracle 숫자를 확인한다.
    gpt_compile = run_console(
        [compiler, "-g2012", "-Wall", "-s", "tb_gpt_stack", "-o", str(gpt_image),
         *map(str, gpt_sources)],
        cwd=ROOT, capture_output=True,
    )
    if gpt_compile.stdout:
        print(gpt_compile.stdout, end="")
    if gpt_compile.stderr:
        print(gpt_compile.stderr, end="", file=sys.stderr)
    if gpt_compile.returncode:
        return gpt_compile.returncode

    # 외부 도구 실제 실행. argument list로 전달하고 stdout/stderr/종료코드 또는 log를 남긴다.
    # 실패/누락 출력은 성공으로 간주하지 않도록 뒤에서 returncode와 oracle 숫자를 확인한다.
    gpt_simulation = run_console(
        [simulator, str(gpt_image)], cwd=ROOT, capture_output=True,
    )
    gpt_stdout = "\n".join(
        line for line in gpt_simulation.stdout.splitlines()
        if "$finish called at" not in line
    )
    if gpt_stdout:
        print(gpt_stdout)
    if gpt_simulation.stderr:
        print(gpt_simulation.stderr, end="", file=sys.stderr)
    if gpt_simulation.returncode:
        return gpt_simulation.returncode
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if "PASS: GPT embeddings" not in gpt_stdout:
        raise AssertionError("GPT multi-head stack 테스트가 PASS 표식을 출력하지 않았습니다.")
    actual_gpt: dict[int, list[int]] = {}
    for line in gpt_stdout.splitlines():
        match = re.fullmatch(r"OUTPUT token=(\d+) (-?\d+(?: -?\d+)*)", line.strip())
        if match:
            actual_gpt[int(match.group(1))] = [int(value) for value in match.group(2).split()]
    expected_gpt = decoder_stack()
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if actual_gpt != {i: row for i, row in enumerate(expected_gpt)}:
        raise AssertionError(
            f"multi-head RTL과 Python 기준값이 다릅니다.\nRTL: {actual_gpt}\n기준값: {expected_gpt}"
        )
    print("PASS: 2-head×2-layer RTL과 Python 기준 모델의 12개 출력값이 모두 일치합니다.")
    # SV의 실제 raw 후보 점수들. 소수 오차 허용 없이 정수 그대로 비교한다.
    actual_logits: dict[int, list[int]] = {}
    for line in gpt_stdout.splitlines():
        match = re.fullmatch(r"LOGITS token=(\d+) (-?\d+(?: -?\d+)*)", line.strip())
        if match:
            actual_logits[int(match.group(1))] = [int(value) for value in match.group(2).split()]
    # oracle의 모든 후보 점수. 선택 ID만 우연히 같은 경우를 넘어서 검증한다.
    expected_logits = language_model_logits()
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if actual_logits != {i: row for i, row in enumerate(expected_logits)}:
        raise AssertionError(
            f"end-to-end GPT logits가 Python 기준값과 다릅니다.\nRTL: {actual_logits}\n기준값: {expected_logits}"
        )
    print("PASS: token/position embedding부터 vocabulary logits까지 RTL과 기준 모델이 일치합니다.")
    actual_cached_logits: dict[int, list[int]] = {}
    for line in gpt_stdout.splitlines():
        match = re.fullmatch(r"KCACHE_LOGITS token=(\d+) (-?\d+(?: -?\d+)*)", line.strip())
        if match:
            actual_cached_logits[int(match.group(1))] = [int(value) for value in match.group(2).split()]
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if actual_cached_logits != {i: row for i, row in enumerate(expected_logits)}:
        raise AssertionError(
            f"streaming KV-cache RTL과 full-context Python logits가 다릅니다.\n"
            f"RTL: {actual_cached_logits}\n기준값: {expected_logits}"
        )
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if "true layer-wise KV-cache streaming" not in gpt_stdout:
        raise AssertionError("KV-cache RTL의 completion marker가 없습니다.")
    print("PASS: 한 token씩 처리하는 RTL KV-cache logits도 Python full-context 결과와 모두 일치합니다.")
    return 0


# 직접 실행할 때만 진입점을 실행한다. import한 다른 파일은 여기 함수/정의를 호출해 사용한다.
if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"실패: {error}", file=sys.stderr)
        raise SystemExit(1)
