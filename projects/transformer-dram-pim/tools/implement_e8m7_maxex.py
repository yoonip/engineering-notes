"""E8M7 MAX-EX 독립 core를 Nexys의 FPGA part에 OOC 배치·배선한다.

실행: python tools/implement_e8m7_maxex.py --guard-bits 16
      python tools/implement_e8m7_maxex.py --guard-bits 32
외부 package pin/JTAG/DDR를 쓰지 않는 연구 core의 물리 구현이다. 실제 보드용
Transformer bitstream을 수정하지 않는다. 원본 소스와 로그·DCP·SHA를 함께 저장한다.
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

ROOT = Path(__file__).resolve().parents[1]


def sha(path: Path) -> str:
    value = hashlib.sha256()
    with path.open('rb') as source:
        for chunk in iter(lambda: source.read(1024*1024), b''):
            value.update(chunk)
    return value.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--guard-bits', type=int, choices=(16,32), default=16)
    parser.add_argument('--vivado', type=Path, default=Path('C:/Xilinx/Vivado/2024.1/bin/vivado.bat'))
    parser.add_argument('--timeout', type=int, default=3600)
    args = parser.parse_args()
    stage = Path(tempfile.gettempdir())/('maxex_ooc_'+uuid.uuid4().hex)
    output = ROOT/f'build/e8m7_maxex/vivado_guard{args.guard_bits}'
    stage.mkdir(parents=True)
    (stage/'rtl').mkdir()
    output.mkdir(parents=True,exist_ok=True)
    sources = ['rtl/dram_pim_e8m7_maxex_mac.sv', 'rtl/e8m7_maxex_registered_top.sv',
               'fpga/nexys4_ddr/implement_e8m7_maxex.tcl']
    for relative in sources:
        original = ROOT/relative
        if not original.is_file():
            parser.error(f'필요한 소스가 없습니다: {relative}')
        shutil.copy2(original, stage/('rtl' if relative.startswith('rtl/') else '')/original.name)
    env = os.environ.copy()
    env['MAXEX_STAGE'] = stage.as_posix()
    env['MAXEX_GUARD_BITS'] = str(args.guard_bits)
    command = [str(args.vivado),'-mode','batch','-source','implement_e8m7_maxex.tcl',
               '-log','vivado.log','-journal','vivado.jou']
    report = {'mode':'independent_maxex_out_of_context_implementation','passed':False,
              'guard_bits':args.guard_bits,'lanes':16,'device':'xc7a100tcsg324-1',
              'clock_hz':5000000,'clock_period_ns':200.0,'command':command,
              'ascii_stage':str(stage),'physical_board_measured':False,
              'physical_dram_pim_measured':False,'connected_to_q88_transformer':False,
              'bitstream_produced':False}
    started = time.monotonic()
    try:
        print(f'진행: MAX-EX guard{args.guard_bits} OOC 합성·배치·배선',flush=True)
        with (stage/'console.log').open('w',encoding='utf-8') as log:
            process = subprocess.Popen(command,cwd=stage,env=env,stdout=log,stderr=subprocess.STDOUT,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
            report['started_process_pid'] = process.pid
            try:
                report['returncode'] = process.wait(timeout=args.timeout)
            except subprocess.TimeoutExpired:
                if os.name=='nt':
                    cleanup = subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],
                                             stdout=log,stderr=subprocess.STDOUT,timeout=30)
                    report['own_process_tree_cleanup_returncode'] = cleanup.returncode
                else:
                    process.kill()
                raise RuntimeError('자체 Vivado 작업의 벽시계 시간 제한 초과')
        if report['returncode'] != 0:
            raise RuntimeError(f"Vivado exit={report['returncode']}; console.log를 확인하세요.")
        folder = stage/'output'
        util = (folder/'routed_utilization.rpt').read_text(encoding='utf-8')
        timing = (folder/'routed_timing.rpt').read_text(encoding='utf-8')
        resources = {}
        for name, pattern in [('LUT','Slice LUTs'),('FF','Slice Registers'),('DSP','DSPs'),('BRAM36','Block RAM Tile')]:
            row = re.search(r'\|\s*'+pattern+r'\s*\|\s*(\d+)\s*\|\s*\d+\s*\|\s*\d+\s*\|\s*(\d+)\s*\|\s*([\d.]+)',util)
            if not row:
                raise RuntimeError(f'자원 보고서의 {name} 행 누락')
            resources[name] = {'used':int(row[1]),'available':int(row[2]),'percent':float(row[3])}
        section = timing.split('Design Timing Summary',1)[1]
        row = re.search(r'\n\s*([-\d.]+)\s+([-\d.]+)\s+(\d+)\s+(\d+)\s+([-\d.]+)\s+([-\d.]+)\s+(\d+)\s+(\d+)\s+([-\d.]+)\s+([-\d.]+)\s+(\d+)\s+(\d+)\s*\n',section)
        if not row:
            raise RuntimeError('타이밍 보고서의 요약 행 누락')
        metrics = dict(zip(['WNS_ns','TNS_ns','setup_failing_endpoints','setup_endpoints',
                            'WHS_ns','THS_ns','hold_failing_endpoints','hold_endpoints',
                            'WPWS_ns','TPWS_ns','pulse_failing_endpoints','pulse_endpoints'],map(float,row.groups())))
        assert min(metrics['WNS_ns'],metrics['WHS_ns'],metrics['WPWS_ns']) >= 0
        assert 'All user specified timing constraints are met.' in timing
        assert 'checking no_clock (0)' in timing and 'checking unconstrained_internal_endpoints (0)' in timing
        report.update({'passed':True,'resources_routed':resources,'timing':metrics,
                       'routed_checkpoint_sha256':sha(folder/'routed.dcp'),
                       'no_clock_endpoints':0,'unconstrained_internal_endpoints':0})
    except Exception as error:
        report['failure_ko'] = str(error)
        print(f'실패: {error}',flush=True)
    finally:
        report['wall_seconds'] = round(time.monotonic()-started,3)
        for filename in ('console.log','vivado.log','vivado.jou'):
            if (stage/filename).is_file():
                shutil.copy2(stage/filename,output/filename)
        if (stage/'output').is_dir():
            for path in (stage/'output').iterdir():
                if path.is_file():
                    shutil.copy2(path,output/path.name)
        snapshot = output/'source_snapshot'
        source_hashes = []
        for relative in sources:
            source = stage/('rtl' if relative.startswith('rtl/') else '')/Path(relative).name
            target = snapshot/relative
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(source,target)
            source_hashes.append({'file':relative,'sha256':sha(target)})
        report['source_snapshot'] = source_hashes
        (output/'result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=True),flush=True)
    return 0 if report['passed'] else 1


if __name__=='__main__':
    for stream in (sys.stdout,sys.stderr):
        if hasattr(stream,'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    raise SystemExit(main())
