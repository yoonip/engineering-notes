"""등록형 max/average Pooling PU를 독립 OOC 회로로 실제 배치·배선한다.

기능의 기준은 model/pooling_q88.py이고, RTL 수치·valid/reset 시험은
tools/verify_pooling_pu.py가 담당한다. 이 도구는 그와 별개로 200ns clock과
2ns 입출력 지연에서 FPGA 자원·STA·DCP를 측정한다. 실제 GPT bitstream을
교체하거나 보드를 programming하지 않는다. 새 실행마다 ASCII 임시 폴더를
만들며, 보존할 결과가 있으면 --output-dir로 새로운 이름을 지정한다.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
import uuid

# 이미 별도 OOC에서 사용한 소유권 확인·해제 함수를 재사용한다. 이 의존
# 파일도 아래 SOURCES에 포함해 실행한 판본의 SHA와 원문을 보존한다.
from implement_e8m7_pairwise import create_stage_alias, remove_stage_alias

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ["rtl/dram_pim_pooling_pu.sv", "rtl/dram_pim_pooling_registered_top.sv",
           "fpga/nexys4_ddr/implement_pooling_pu.tcl", "tools/implement_pooling_pu.py",
           "tools/implement_e8m7_pairwise.py"]


def sha(path: Path) -> str:
    # 큰 DCP도 작은 조각으로 읽어 메모리를 일정하게 사용한다.
    value = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def parse_reports(folder: Path) -> tuple[dict, dict]:
    util = (folder / "routed_utilization.rpt").read_text(encoding="utf-8")
    timing = (folder / "routed_timing.rpt").read_text(encoding="utf-8")
    resources = {}
    for label, row_name in (("LUT", "Slice LUTs"), ("FF", "Slice Registers"),
                            ("DSP", "DSPs"), ("BRAM36", "Block RAM Tile")):
        row = re.search(r"\|\s*" + row_name + r"\s*\|\s*(\d+)\s*\|\s*\d+\s*\|\s*\d+\s*\|\s*(\d+)\s*\|\s*([\d.]+)", util)
        if not row:
            raise RuntimeError("자원 요약 행 누락: " + label)
        resources[label] = {"used": int(row[1]), "available": int(row[2]), "percent": float(row[3])}
    section = timing.split("Design Timing Summary", 1)[1]
    row = re.search(r"\n\s*([-\d.]+)\s+([-\d.]+)\s+(\d+)\s+(\d+)\s+([-\d.]+)\s+([-\d.]+)\s+(\d+)\s+(\d+)\s+([-\d.]+)\s+([-\d.]+)\s+(\d+)\s+(\d+)\s*\n", section)
    if not row:
        raise RuntimeError("STA 요약 행 누락")
    metrics = dict(zip(("WNS_ns", "TNS_ns", "setup_failing_endpoints", "setup_endpoints",
                        "WHS_ns", "THS_ns", "hold_failing_endpoints", "hold_endpoints",
                        "WPWS_ns", "TPWS_ns", "pulse_failing_endpoints", "pulse_endpoints"),
                       map(float, row.groups())))
    if min(metrics["WNS_ns"], metrics["WHS_ns"], metrics["WPWS_ns"]) < 0:
        raise RuntimeError("setup/hold/pulse STA 여유가 음수입니다.")
    if ("All user specified timing constraints are met." not in timing
            or "checking no_clock (0)" not in timing
            or "checking unconstrained_internal_endpoints (0)" not in timing):
        raise RuntimeError("clock/내부 endpoint 누락 또는 STA 완료 증거 부족")
    if any(metrics[name] != 0 for name in ("setup_failing_endpoints", "hold_failing_endpoints", "pulse_failing_endpoints")):
        raise RuntimeError("STA 실패 endpoint가 있습니다.")
    return resources, metrics


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--window", type=int, choices=range(1, 65), default=16)
    parser.add_argument("--vivado", type=Path, default=Path("C:/Xilinx/Vivado/2024.1/bin/vivado.bat"))
    parser.add_argument("--timeout", type=int, default=3600)
    parser.add_argument("--stage", type=Path)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    if args.timeout <= 0 or not args.vivado.is_file():
        parser.error("양수 timeout과 실제 Vivado 실행 파일이 필요합니다.")
    task_base = Path("D:/CodexResearchTiming") if os.name == "nt" and Path("D:/").is_dir() else Path(tempfile.gettempdir())
    stage = (args.stage or task_base / ("pool_ooc_" + uuid.uuid4().hex)).resolve()
    output = (args.output_dir or ROOT / f"build/pooling_pu/vivado_window{args.window}").resolve()
    output.relative_to(ROOT.resolve())
    if not str(stage).isascii() or stage.exists() or stage == output:
        parser.error("새 ASCII stage가 필요하며 output과 달라야 합니다.")
    if (output / "result.json").exists():
        parser.error("기존 결과를 보존하려면 --output-dir로 새 폴더를 지정하세요.")
    before = {relative: sha(ROOT / relative) for relative in SOURCES}
    stage.mkdir(parents=True, exist_ok=False)
    (stage / "rtl").mkdir()
    (stage / "compiler_temp").mkdir()
    output.mkdir(parents=True, exist_ok=True)
    for relative in SOURCES:
        target = stage / ("rtl" if relative.startswith("rtl/") else "") / Path(relative).name
        shutil.copy2(ROOT / relative, target)
        if sha(target) != before[relative]:
            raise RuntimeError("임시 입력 복사 SHA 불일치: " + relative)
    # 포트·연산·등록 경계를 보존하고 최상위 module 선언 이름만 한 곳 바꾼다.
    # Vivado의 긴 이름 내부 Tcl 생성 실패에 대한 실행 우회다. 문서나 기능
    # 원본을 바꾸지 않고 반대로 치환했을 때 원본 byte가 복원됨을 검사한다.
    original_top = (stage / "rtl/dram_pim_pooling_registered_top.sv").read_bytes()
    original_declaration = b"module dram_pim_pooling_registered_top #("
    alias_declaration = b"module pool_top #("
    if original_top.count(original_declaration) != 1:
        raise RuntimeError("최상위 module 선언 하나를 찾지 못했습니다.")
    alias_bytes = original_top.replace(original_declaration, alias_declaration, 1)
    if alias_bytes.replace(alias_declaration, original_declaration, 1) != original_top:
        raise RuntimeError("module 이름 변경의 원문 복원 실패")
    alias_path = stage / "rtl/pool_top.sv"
    alias_path.write_bytes(alias_bytes)
    env = os.environ.copy()
    env.update(POOLING_STAGE=stage.as_posix(), POOLING_WINDOW=str(args.window),
               TEMP=str(stage / "compiler_temp"), TMP=str(stage / "compiler_temp"))
    command = [str(args.vivado.resolve()), "-mode", "batch", "-source", "implement_pooling_pu.tcl",
               "-log", "vivado.log", "-journal", "vivado.jou"]
    report = {"mode": "independent_pooling_out_of_context_implementation", "passed": False,
              "window": args.window, "device": "xc7a100tcsg324-1", "clock_hz": 5000000,
              "clock_period_ns": 200.0, "input_delay_ns": 2.0, "output_delay_ns": 2.0,
              "false_path_added": False, "multicycle_added": False,
              "registered_edge_latency": 1, "command": command, "ascii_stage": str(stage),
              "physical_board_measured": False, "physical_dram_pim_measured": False,
              "connected_to_q88_transformer": False, "bitstream_produced": False,
              "source_sha256_before": before,
              "top_name_alias": {"original": "dram_pim_pooling_registered_top", "synthesis": "pool_top",
                                 "module_declaration_replacements": 1,
                                 "source_exact_restore": True, "alias_sha256": sha(alias_path),
                                 "restored_sha256": hashlib.sha256(original_top).hexdigest()}}
    started = time.monotonic()
    drive_alias_evidence = {}
    try:
        # 기존 synthesis의 내부 realtime Tcl 실패를 짧은 drive 경로로
        # 우회한다. 빈 R..Z 중 하나만 쓰고 자체 mapping 소유권을 검사해
        # 종료 시 해제한다. 사용자의 기존 drive mapping은 변경하지 않는다.
        effective_stage = create_stage_alias(stage, drive_alias_evidence)
        env['POOLING_STAGE'] = effective_stage.as_posix()
        report['effective_vivado_stage'] = effective_stage.as_posix()
        for relative in SOURCES:
            copied = ("rtl/" if relative.startswith("rtl/") else "") + Path(relative).name
            if sha(effective_stage / copied) != before[relative]:
                raise RuntimeError("drive 별칭으로 보이는 소스 SHA 불일치")
        if sha(effective_stage / 'rtl/pool_top.sv') != sha(alias_path):
            raise RuntimeError("drive 별칭의 module 이름 사본 SHA 불일치")
        print("진행: 독립 Pooling PU OOC 합성·배치·배선", flush=True)
        with (stage / "console.log").open("wb") as log:
            process = subprocess.Popen(command, cwd=effective_stage, env=env, stdout=log, stderr=subprocess.STDOUT,
                                       creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
            report["started_process_pid"] = process.pid
            try:
                report["returncode"] = process.wait(timeout=args.timeout)
            except subprocess.TimeoutExpired:
                # 이 실행이 시작한 부모의 자식만 종료한다. 다른 Vivado/SDF 작업을
                # 이름으로 검색하거나 사용자의 앱을 닫지 않는다.
                if os.name == "nt":
                    done = subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                                          stdout=log, stderr=subprocess.STDOUT, timeout=30)
                    report["own_process_tree_cleanup_returncode"] = done.returncode
                else:
                    process.kill()
                raise RuntimeError("자체 Vivado 작업의 벽시계 시간 제한 초과")
        if report["returncode"] != 0:
            raise RuntimeError("Vivado 정상 종료 실패: " + str(report["returncode"]))
        folder = stage / "output"
        resources, metrics = parse_reports(folder)
        after = {relative: sha(ROOT / relative) for relative in SOURCES}
        if after != before:
            raise RuntimeError("실행 중 원본 소스가 바뀌었습니다.")
        report.update(passed=True, resources_routed=resources, timing=metrics,
                      routed_checkpoint_sha256=sha(folder / "routed.dcp"),
                      no_clock_endpoints=0, unconstrained_internal_endpoints=0,
                      source_sha256_after=after, source_before_after_sha_match=True)
    except Exception as error:
        report["failure_ko"] = str(error)
        print("실패: " + str(error), flush=True)
    finally:
        report['subst_mapping'] = drive_alias_evidence
        report['subst_cleanup'] = remove_stage_alias(stage, drive_alias_evidence)
        if drive_alias_evidence.get('created') and not report['subst_cleanup'].get('removed'):
            report['passed'] = False
            report['failure_ko'] = '자체 drive 별칭 해제 확인 실패'
        report["wall_seconds"] = round(time.monotonic() - started, 3)
        for filename in ("console.log", "vivado.log", "vivado.jou"):
            if (stage / filename).is_file():
                shutil.copy2(stage / filename, output / filename)
        if (stage / "output").is_dir():
            for path in (stage / "output").iterdir():
                if path.is_file():
                    shutil.copy2(path, output / path.name)
        snapshots = output / "source_snapshot"
        for relative in SOURCES:
            target = snapshots / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            source = stage / ("rtl" if relative.startswith("rtl/") else "") / Path(relative).name
            shutil.copy2(source, target)
        shutil.copy2(alias_path, output / "pool_top.sv")
        report["output_files_sha256"] = {path.name: sha(path) for path in output.iterdir()
                                         if path.is_file() and path.name != "result.json"}
        (output / "result.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=True), flush=True)
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    raise SystemExit(main())
