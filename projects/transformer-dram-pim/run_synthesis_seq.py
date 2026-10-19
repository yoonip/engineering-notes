#!/usr/bin/env python3
# 소형 context 전체 sequential core의 Yosys generic 합성 결과를 기록한다.
# Yosys -noabc는 technology-independent 합성이다. generic cell 수를 특정 FPGA LUT/FF로 해석하면 안 된다.
# FPGA 자원/배선/clock 만족은 part/XDC가 지정된 Vivado implementation으로 별도 확인한다.
"""resource-shared 순차 GPT core를 Yosys generic cell까지 합성한다.

합성 통계는 comb 기준 top과 같은 작은 multi-head/multi-layer dimensions를 사용한다.
보고된 generic cells는 FPGA vendor LUT/FF 수나 place-and-route timing 결과가 아니다.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOOL_ROOT = Path(os.environ.get(
    "OSS_CAD_SUITE", Path.home() / "Documents" / "ChatGPT" / "oss-cad-suite"
)).resolve()
YOSYS = TOOL_ROOT / "bin" / "yosys.exe"
LOG = ROOT / "build" / "reports" / "gpt_sequential_yosys_generic.log"


# 명령행 진입 함수. 옵션/입력/도구를 준비해 이 파일의 학습·추론·검증·분석 결과를 저장한다.
# 성공은 return0,오류는 예외/종료코드로 알린다. __main__ 직접 실행에서 자동 호출된다.
def main() -> int:
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if not YOSYS.exists():
        raise FileNotFoundError(f"Yosys를 찾지 못했습니다: {YOSYS}")
    LOG.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["YOSYSHQ_ROOT"] = str(TOOL_ROOT)
    env["PATH"] = os.pathsep.join([
        str(TOOL_ROOT / "bin"), str(TOOL_ROOT / "lib"), env.get("PATH", "")
    ])
    env["SSL_CERT_FILE"] = str(TOOL_ROOT / "etc" / "cacert.pem")
    script = "; ".join([
        "read_verilog -sv rtl/dram_pim_pu_synth.sv rtl/transformer_gpt_language_model_seq.sv rtl/gpt_seq_synth_top.sv",
        "hierarchy -top gpt_seq_synth_top",
        "synth -top gpt_seq_synth_top -flatten -noabc",
        "check -assert",
        "stat",
    ])
    with LOG.open("w", encoding="utf-8", newline="\n") as log:
        # 외부 도구 실제 실행. argument list로 전달하고 stdout/stderr/종료코드 또는 log를 남긴다.
        # 실패/누락 출력은 성공으로 간주하지 않도록 뒤에서 returncode와 oracle 숫자를 확인한다.
        result = subprocess.run(
            [str(YOSYS), "-Q", "-p", script], cwd=ROOT, env=env,
            stdout=log, stderr=subprocess.STDOUT, text=True,
            encoding="utf-8", errors="replace", check=False,
        )
    # 생성 SV source 문장 목록. list 안 문자열은 실제 별도 HDL 코드다.
    lines = LOG.read_text(encoding="utf-8", errors="replace").splitlines()
    print("\n".join(lines[-70:]))
    if result.returncode:
        print(f"순차 core generic synthesis 실패. 전체 로그: {LOG}", file=sys.stderr)
        return result.returncode
    version = subprocess.check_output(
        [str(YOSYS), "-V"], env=env, text=True, encoding="utf-8", errors="replace"
    ).strip()
    print(version)
    print("합성 top: T=3,V=8,D=4,H=2,F=8,L=2; one shared MAC + one Softmax PU + one LayerNorm PU")
    print("주의: generic logic 통계이며 FPGA LUT/FF, timing, power 결과가 아닙니다.")
    print(f"로그: {LOG}")
    return 0


# 직접 실행할 때만 진입점을 실행한다. import한 다른 파일은 여기 함수/정의를 호출해 사용한다.
if __name__ == "__main__":
    raise SystemExit(main())
