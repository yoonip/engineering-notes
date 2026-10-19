#!/usr/bin/env python3
# 같은 shape/config의 comb/seq core를 같은 Yosys 설정으로 비교한다.
# generic cell 감소율과 FPGA LUT/FF/BRAM/Fmax/전력은 다른 지표다.
# Yosys -noabc는 technology-independent 합성이다. generic cell 수를 특정 FPGA LUT/FF로 해석하면 안 된다.
# FPGA 자원/배선/clock 만족은 part/XDC가 지정된 Vivado implementation으로 별도 확인한다.
"""같은 dimensions의 end-to-end comb와 순차 GPT top을 Yosys로 비교한다."""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOOL_ROOT = Path(os.environ.get(
    "OSS_CAD_SUITE", Path.home() / "Documents" / "ChatGPT" / "oss-cad-suite"
)).resolve()
YOSYS = TOOL_ROOT / "bin" / "yosys.exe"
REPORTS = ROOT / "build" / "reports"
COMMON = "rtl/dram_pim_pu_synth.sv"
COMB_SOURCES = [
    COMMON, "rtl/dram_pim_vmm_bank.sv", "rtl/transformer_decoder_mha_pim_comb.sv",
    "rtl/transformer_gpt_decoder_stack_comb.sv", "rtl/transformer_gpt_language_model_comb.sv",
    "rtl/gpt_comb_synth_top.sv",
]
SEQ_SOURCES = [COMMON, "rtl/transformer_gpt_language_model_seq.sv", "rtl/gpt_seq_synth_top.sv"]


# read/hierarchy/synth -noabc/check/stat으로 generic 합성 후 구조검사/cell을 확인한다.
# vendor part mapping/place/route clock timing은 이 함수의 검증 범위에 포함하지 않는다.
def synthesize(top: str, files: list[str], log_path: Path, env: dict[str, str]) -> int:
    script = "; ".join([
        "read_verilog -sv " + " ".join(files),
        f"hierarchy -top {top}",
        f"synth -top {top} -flatten -noabc",
        "check -assert",
        "stat",
    ])
    with log_path.open("w", encoding="utf-8", newline="\n") as log:
        # 외부 도구 실제 실행. argument list로 전달하고 stdout/stderr/종료코드 또는 log를 남긴다.
        # 실패/누락 출력은 성공으로 간주하지 않도록 뒤에서 returncode와 oracle 숫자를 확인한다.
        result = subprocess.run(
            [str(YOSYS), "-Q", "-p", script], cwd=ROOT, env=env,
            stdout=log, stderr=subprocess.STDOUT, text=True,
            encoding="utf-8", errors="replace", check=False,
        )
    content = log_path.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"^\s*(\d+) cells\s*$", content, re.M)
    if result.returncode or not match:
        print(f"Yosys failed for {top}; inspect {log_path}", file=sys.stderr)
        print("\n".join(content.splitlines()[-50:]), file=sys.stderr)
        raise SystemExit(result.returncode or 1)
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if "Found and reported 0 problems." not in content:
        raise AssertionError(f"Yosys structural check did not pass for {top}")
    return int(match.group(1))


# 명령행 진입 함수. 옵션/입력/도구를 준비해 이 파일의 학습·추론·검증·분석 결과를 저장한다.
# 성공은 return0,오류는 예외/종료코드로 알린다. __main__ 직접 실행에서 자동 호출된다.
def main() -> int:
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if not YOSYS.exists():
        raise FileNotFoundError(f"Yosys를 찾지 못했습니다: {YOSYS}")
    REPORTS.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["YOSYSHQ_ROOT"] = str(TOOL_ROOT)
    env["PATH"] = os.pathsep.join([
        str(TOOL_ROOT / "bin"), str(TOOL_ROOT / "lib"), env.get("PATH", "")
    ])
    env["SSL_CERT_FILE"] = str(TOOL_ROOT / "etc" / "cacert.pem")
    comb = synthesize(
        "gpt_comb_synth_top", COMB_SOURCES,
        REPORTS / "gpt_comb_e2e_yosys_generic.log", env,
    )
    seq = synthesize(
        "gpt_seq_synth_top", SEQ_SOURCES,
        REPORTS / "gpt_sequential_yosys_generic.log", env,
    )
    reduction = (comb - seq) * 100.0 / comb
    version = subprocess.check_output(
        [str(YOSYS), "-V"], env=env, text=True, encoding="utf-8", errors="replace"
    ).strip()
    print(version)
    print("동일 구성: token ID → embedding → T=3,V=8,D=4,H=2,F=8,L=2 → logits")
    print(f"comb generic cells: {comb:,}")
    print(f"seq  generic cells: {seq:,}")
    print(f"차이: sequential shared-compute top이 {reduction:.2f}% 적은 generic cells")
    print("주의: generic logic cells이며 FPGA LUT/FF·timing·power 결과가 아닙니다.")
    return 0


# 직접 실행할 때만 진입점을 실행한다. import한 다른 파일은 여기 함수/정의를 호출해 사용한다.
if __name__ == "__main__":
    raise SystemExit(main())
