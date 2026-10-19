"""E8M7 일반 pairwise floating tree 독립 core를 Nexys의 FPGA part에 OOC 배치·배선한다.

실행: python tools/implement_e8m7_pairwise.py
외부 package pin/JTAG/DDR를 쓰지 않는 연구 core의 물리 구현이다. 실제 보드용
Transformer bitstream을 수정하지 않는다. 원본 소스와 로그·DCP·SHA를 함께 저장한다.
"""
from __future__ import annotations
import argparse
import ctypes
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


def subst_target(drive: str) -> str | None:
    """Windows DOS device의 실제 대상을 조회한다. 기존 drive를 해제하지 않는다."""
    query = ctypes.windll.kernel32.QueryDosDeviceW
    query.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint]
    query.restype = ctypes.c_uint
    buffer = ctypes.create_unicode_buffer(32768)
    return buffer.value if query(drive, buffer, len(buffer)) else None


def owns_subst(drive: str, stage: Path) -> bool:
    """자신이 연결한 정확한 absolute stage인지 확인한 후에만 해제한다."""
    target = subst_target(drive)
    wanted = '\\??\\' + str(stage.resolve())
    return target is not None and target.casefold() == wanted.casefold()


def create_stage_alias(stage: Path, evidence: dict) -> Path:
    if os.name != 'nt':
        evidence.update({'created':False,'mode':'non_windows_direct_stage'})
        return stage
    evidence.update({'created':False,'mode':'windows_ascii_subst',
                     'absolute_target':str(stage.resolve()),'attempts':[]})
    mask = ctypes.windll.kernel32.GetLogicalDrives()
    for number in range(ord('Z'), ord('R')-1, -1):
        drive = chr(number) + ':'
        # GetLogicalDrives와 QueryDosDevice 모두 기존 연결을 나타내지 않아야 한다.
        if mask & (1 << (number-ord('A'))) or subst_target(drive) is not None:
            continue
        done = subprocess.run(['subst',drive,str(stage.resolve())],
                              stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        evidence['attempts'].append({'drive':drive,'returncode':done.returncode,
                'message':done.stdout.decode('utf-8',errors='replace')})
        if done.returncode:
            continue  # 다른 작업이 먼저 사용한 경우 그 연결을 건드리지 않는다.
        evidence.update({'created':True,'drive':drive,'target_after_creation':subst_target(drive)})
        if not owns_subst(drive,stage):
            raise RuntimeError('새 alias의 실제 대상이 자체 stage와 다릅니다.')
        evidence['ownership_verified'] = True
        alias = Path(drive + '/')
        evidence['ascii_alias'] = alias.as_posix()
        return alias
    raise RuntimeError('R..Z에 사용할 수 있는 무료 ASCII drive가 없습니다.')


def remove_stage_alias(stage: Path, evidence: dict) -> dict:
    if not evidence.get('created'):
        return {'performed':False,'reason_ko':'이 작업이 만든 mapping 없음'}
    drive = evidence['drive']
    if not owns_subst(drive,stage):
        return {'performed':False,'ownership_matches':False,
                'reason_ko':'현재 대상이 자체 stage와 달라 해제하지 않음'}
    done = subprocess.run(['subst',drive,'/D'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    return {'performed':True,'ownership_matches':True,'drive':drive,
            'returncode':done.returncode,'removed':subst_target(drive) is None,
            'message':done.stdout.decode('utf-8',errors='replace')}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--vivado', type=Path, default=Path('C:/Xilinx/Vivado/2024.1/bin/vivado.bat'))
    parser.add_argument('--timeout', type=int, default=3600)
    args = parser.parse_args()
    stage = Path(tempfile.gettempdir())/('pw_'+uuid.uuid4().hex[:12])
    output = ROOT/'build/e8m7_pairwise/vivado'
    stage.mkdir(parents=True)
    (stage/'rtl').mkdir()
    output.mkdir(parents=True,exist_ok=True)
    sources = ['rtl/e8m7_pairwise_tree_mac.sv', 'rtl/e8m7_pairwise_registered_top.sv',
               'rtl/e8m7_pairwise_ooc_top.sv',
               'fpga/nexys4_ddr/implement_e8m7_pairwise.tcl']
    for relative in sources:
        original = ROOT/relative
        if not original.is_file():
            parser.error(f'필요한 소스가 없습니다: {relative}')
        shutil.copy2(original, stage/('rtl' if relative.startswith('rtl/') else '')/original.name)
    env = os.environ.copy()
    command = [str(args.vivado),'-mode','batch','-source','implement_e8m7_pairwise.tcl',
               '-log','vivado.log','-journal','vivado.jou']
    report = {'mode':'independent_pairwise_out_of_context_implementation','passed':False,
              'rounding_policy':'RNE_after_each_product_and_each_tree_add','lanes':16,'device':'xc7a100tcsg324-1',
              'clock_hz':5000000,'clock_period_ns':200.0,'command':command,
              'ascii_stage':str(stage),'physical_board_measured':False,
              'physical_dram_pim_measured':False,'connected_to_q88_transformer':False,
              'bitstream_produced':False}
    started = time.monotonic()
    alias_evidence = {}
    try:
        stage_alias = create_stage_alias(stage, alias_evidence)
        env['PAIRWISE_STAGE'] = stage_alias.as_posix()
        report['subst_mapping'] = alias_evidence
        report['effective_vivado_stage'] = stage_alias.as_posix()
        # alias에서 보이는 RTL 바이트가 실제 stage와 같은지 확인한다.
        for relative in sources:
            if relative.startswith('rtl/'):
                assert sha(stage_alias/'rtl'/Path(relative).name) == sha(stage/'rtl'/Path(relative).name)
        print(f'진행: 일반 E8M7 pairwise tree OOC 합성·배치·배선',flush=True)
        with (stage/'console.log').open('w',encoding='utf-8') as log:
            process = subprocess.Popen(command,cwd=stage_alias,env=env,stdout=log,stderr=subprocess.STDOUT,
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
        report['subst_mapping'] = alias_evidence
        report['subst_cleanup'] = remove_stage_alias(stage, alias_evidence)
        if alias_evidence.get('created') and not report['subst_cleanup'].get('removed'):
            report['passed'] = False
            report['failure_ko'] = '자체 stage alias 해제가 완료되지 않았습니다.'
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
        tool_snapshot = output/'driver_snapshot'
        tool_snapshot.mkdir(exist_ok=True)
        report['tool_source_snapshot'] = []
        for relative in ('build/create_pairwise_implementation_driver.py',
                         'tools/implement_e8m7_pairwise.py'):
            target = tool_snapshot/Path(relative).name
            shutil.copy2(ROOT/relative,target)
            report['tool_source_snapshot'].append({'file':relative,'sha256':sha(target)})
        (output/'result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=True),flush=True)
    return 0 if report['passed'] else 1


if __name__=='__main__':
    for stream in (sys.stdout,sys.stderr):
        if hasattr(stream,'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    raise SystemExit(main())
