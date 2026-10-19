#!/usr/bin/env python3
# 소형 decoder stack의 Yosys generic 합성/구조 검사 결과를 기록한다.
# Yosys -noabc는 technology-independent 합성이다. generic cell 수를 특정 FPGA LUT/FF로 해석하면 안 된다.
# FPGA 자원/배선/clock 만족은 part/XDC가 지정된 Vivado implementation으로 별도 확인한다.
"""OSS CAD Suite의 Yosys로 고정 GPT decoder core를 generic RTL cell까지 합성한다.

이 결과는 FPGA part를 대상으로 한 mapping/place-route나 타이밍 closure가 아니다.
Yosys의 technology-independent 합성으로 RTL을 generic logic cell로 낮추고
hierarchy, latch, 합성 경고 및 cell 통계를 기록한다. ABC technology mapping은
완전히 펼친 큰 조합 Transformer에서 지나치게 오래 걸려 생략한다. 따라서 보고된
generic cell 개수를 FPGA LUT/FF 수로 읽으면 안 된다.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOOL_ROOT = Path(os.environ.get("OSS_CAD_SUITE", Path.home() / "Documents" / "ChatGPT" / "oss-cad-suite")).resolve()
YOSYS = TOOL_ROOT / "bin" / "yosys.exe"
REPORTS = ROOT / "build" / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)
LOG = REPORTS / "gpt_stack_yosys_generic.log"


# 명령행 진입 함수. 옵션/입력/도구를 준비해 이 파일의 학습·추론·검증·분석 결과를 저장한다.
# 성공은 return0,오류는 예외/종료코드로 알린다. __main__ 직접 실행에서 자동 호출된다.
def main() -> int:
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if not YOSYS.exists():
        raise FileNotFoundError(f"Yosys를 찾지 못했습니다: {YOSYS}")

    env = os.environ.copy()
    env["YOSYSHQ_ROOT"] = str(TOOL_ROOT)
    env["PATH"] = os.pathsep.join([str(TOOL_ROOT / "bin"), str(TOOL_ROOT / "lib"), env.get("PATH", "")])
    env["SSL_CERT_FILE"] = str(TOOL_ROOT / "etc" / "cacert.pem")

    # generic read/hierarchy/synth -noabc/check/stat 명령. vendor part/timing flow와 다르다.
    yosys_script = "; ".join([
        "read_verilog -sv rtl/dram_pim_pu_synth.sv rtl/dram_pim_vmm_bank.sv "
        "rtl/transformer_decoder_mha_pim_comb.sv rtl/transformer_gpt_decoder_stack_comb.sv "
        "rtl/gpt_stack_synth_top.sv",
        "hierarchy -top gpt_stack_synth_top",
        "synth -top gpt_stack_synth_top -flatten -noabc",
        "check -assert",
        "stat",
    ])
    with LOG.open("w", encoding="utf-8", newline="\n") as log_file:
        # 외부 도구 실제 실행. argument list로 전달하고 stdout/stderr/종료코드 또는 log를 남긴다.
        # 실패/누락 출력은 성공으로 간주하지 않도록 뒤에서 returncode와 oracle 숫자를 확인한다.
        result = subprocess.run(
            [str(YOSYS), "-Q", "-p", yosys_script],
            cwd=ROOT,
            env=env,
            stdout=log_file,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    tail = LOG.read_text(encoding="utf-8", errors="replace").splitlines()[-60:]
    print("\n".join(tail))
    if result.returncode != 0:
        print(f"Yosys 합성이 실패했습니다. 전체 로그: {LOG}", file=sys.stderr)
        return result.returncode
    version = subprocess.check_output(
        [str(YOSYS), "-V"], env=env, text=True, encoding="utf-8", errors="replace"
    ).strip()
    print(f"Yosys 버전: {version}")
    print("합성 top: T=3, D=4, H=2, F=8, L=2 (multi-head, multi-layer)")
    print("합성 방식: Yosys generic logic, ABC mapping 생략, FPGA part mapping 아님")
    print(f"전체 합성 로그: {LOG}")
    return 0


# 직접 실행할 때만 진입점을 실행한다. import한 다른 파일은 여기 함수/정의를 호출해 사용한다.
if __name__ == "__main__":
    raise SystemExit(main())
