"""독립 Pooling PU의 실제 배선 DCP를 UNISIM XSim 기능 회로로 실행한다.

원본 RTL을 DUT로 컴파일하지 않는다. 확대 시험의 WINDOW16 입력과 순서를
복사하여 배선 netlist의 외부 result/count/valid와 동기 reset을 검사한다.
내부 packed register 검사는 이전 RTL 시험에 있으며 이 시험에서 주장하지
않는다. SDF·실물·GPT 연결 시험이 아니다. 기존 결과가 있으면 새 출력 폴더를
지정해야 하며 모든 입력·원시 로그와 SHA를 함께 보존한다.
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
import time
import uuid

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from model.pooling_q88 import pool_details
from tools.verify_pooling_pu import expected_registered, write_memories


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as source:
        for block in iter(lambda:source.read(1024*1024),b''): h.update(block)
    return h.hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--vivado-root',type=Path,default=Path('C:/Xilinx/Vivado/2024.1'))
    parser.add_argument('--timeout',type=int,default=600)
    parser.add_argument('--output-dir',type=Path,default=ROOT/'build/pooling_pu/netlist_window16')
    parser.add_argument('--implementation-dir',type=Path,default=ROOT/'build/pooling_pu/vivado_window16',
                        help='검사할 WINDOW16 OOC result.json과 routed.dcp가 있는 프로젝트 내 폴더')
    parser.add_argument('--fixture-report',type=Path,default=ROOT/'build/reports/pooling_pu_extended_verification.json',
                        help='WINDOW16 입력·원시 로그·mem SHA를 기록한 프로젝트 내 RTL 시험 JSON')
    args=parser.parse_args()
    output=args.output_dir.resolve(); output.relative_to(ROOT.resolve())
    if args.timeout<=0 or (output/'result.json').exists():
        parser.error('양수 timeout 및 기존 결과가 없는 새 출력 폴더가 필요합니다.')
    output.mkdir(parents=True,exist_ok=True)
    stage=Path('D:/CodexResearchTiming')/('pool_net_'+uuid.uuid4().hex)
    stage.mkdir(parents=True,exist_ok=False)
    (stage/'compiler_temp').mkdir()
    board=args.implementation_dir.resolve(); board.relative_to(ROOT.resolve())
    evidence=args.fixture_report.resolve(); evidence.relative_to(ROOT.resolve())
    report={'passed':False,'mode':'post_route_independent_pooling_functional_netlist',
            'window':16,'ascii_stage':str(stage),'sdf_annotated':False,
            'routed_delays_simulated':False,'physical_board_measured':False,
            'physical_dram_pim_measured':False,'canonical_gpt_connected':False,
            'internal_packed_registers_checked':False,'new_xsim_simulation_performed':True,'steps':[]}
    env=os.environ.copy()
    env.update(XILINX_VIVADO=str(args.vivado_root.resolve()),TEMP=str(stage/'compiler_temp'),TMP=str(stage/'compiler_temp'))
    started=time.monotonic()
    def run(name,argv):
        print('진행: Pooling 배선 기능 '+name,flush=True)
        step={'name':name,'command':argv}
        begin=time.monotonic()
        with (stage/(name+'.console.log')).open('wb') as log:
            process=subprocess.Popen(argv,cwd=stage,env=env,stdout=log,stderr=subprocess.STDOUT,
                                     creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
            step['started_process_pid']=process.pid
            try: step['returncode']=process.wait(timeout=args.timeout)
            except subprocess.TimeoutExpired:
                if os.name=='nt': subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],stdout=log,stderr=subprocess.STDOUT,timeout=30)
                else: process.kill()
                step['timed_out']=True
                raise RuntimeError(name+' 자체 작업 시간 제한 초과')
            finally:
                step['wall_seconds']=round(time.monotonic()-begin,6)
                report['steps'].append(step)
        if step['returncode']!=0: raise RuntimeError(name+' 정상 종료 실패')
    try:
        impl=json.loads((board/'result.json').read_text(encoding='utf-8'))
        fixture=json.loads(evidence.read_text(encoding='utf-8'))
        assert impl['passed'] and impl['window']==16 and fixture['passed']
        assert sha(board/'routed.dcp')==impl['routed_checkpoint_sha256']
        config=next(row for row in fixture['configurations'] if row['window']==16)
        data_path=ROOT/config['vectors_and_schedule']
        assert sha(data_path)==config['vectors_and_schedule_sha256']
        data=json.loads(data_path.read_text(encoding='utf-8'))
        vectors,schedule=data['vectors'],data['schedule']
        details=[pool_details(v['values_raw'],v['valid_mask'],v['operation']) for v in vectors]
        predicted,counts=expected_registered(schedule,details)
        source_paths=set(impl['source_sha256_before'])|set(fixture['source_sha256'])|{'tb/tb_pooling_netlist.sv','tools/verify_pooling_netlist.py'}
        before={p:sha(ROOT/p) for p in sorted(source_paths)}
        assert all(before[p]==h for p,h in impl['source_sha256_before'].items())
        assert all(before[p]==h for p,h in fixture['source_sha256'].items())
        report.update(source_sha256_before=before,implementation_result_sha256=sha(board/'result.json'),
                      fixture_report_sha256=sha(evidence),routed_checkpoint_sha256=impl['routed_checkpoint_sha256'],
                      implementation_directory=board.relative_to(ROOT).as_posix(),fixture_report=evidence.relative_to(ROOT).as_posix(),
                      vector_count=len(vectors),registered_cycles=len(schedule),vectors_and_schedule_sha256=sha(data_path))
        for relative in before:
            target=output/'source_snapshot'/relative; target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(ROOT/relative,target); assert sha(target)==before[relative]
        shutil.copy2(board/'routed.dcp',stage/'routed.dcp')
        assert sha(stage/'routed.dcp')==report['routed_checkpoint_sha256']
        shutil.copy2(data_path,stage/'vectors_and_schedule.json')
        memories=write_memories(stage,vectors,details,schedule,16)
        assert memories==config['mem_sha256']
        report['mem_sha256']=memories
        tb=(ROOT/'tb/tb_pooling_netlist.sv').read_text(encoding='utf-8')
        assert tb.count('__VECTORS__')==2 and tb.count('__CYCLES__')==2
        tb=tb.replace('__VECTORS__',str(len(vectors))).replace('__CYCLES__',str(len(schedule)))
        (stage/'tb.sv').write_text(tb,encoding='utf-8')
        (stage/'export.tcl').write_text('open_checkpoint routed.dcp\nwrite_verilog -force -mode funcsim design.v\nexit\n',encoding='ascii')
        (stage/'run.tcl').write_text('run all\nquit\n',encoding='ascii')
        shutil.copy2(args.vivado_root/'data/verilog/src/glbl.v',stage/'glbl.v')
        bindir=args.vivado_root/'bin'
        run('export',[str(bindir/'vivado.bat'),'-mode','batch','-source','export.tcl'])
        report['functional_netlist_sha256']=sha(stage/'design.v')
        run('xvlog',[str(bindir/'xvlog.bat'),'--sv','--work','xil_defaultlib','design.v','tb.sv','glbl.v'])
        run('xelab',[str(bindir/'xelab.bat'),'--mt','2','--O2','--debug','off','-L','unisims_ver','-L','unimacro_ver','-L','secureip','xil_defaultlib.tb_pooling_netlist','xil_defaultlib.glbl','-s','pool_netlist'])
        run('xsim',[str(bindir/'xsim.bat'),'pool_netlist','-tclbatch','run.tcl','-log','simulation.log'])
        log=(stage/'xsim.console.log').read_text(encoding='utf-8',errors='strict')
        rows=re.findall(r'^CHECK_POOL_NET cycle=(\d+) valid=(\d+) result=([0-9a-fA-F]+) count=(\d+) exact=(\d+)\s*$',log,re.M)
        assert len(rows)==len(schedule)
        exact=0
        for n,(cycle,valid,word,count,total) in enumerate(rows):
            expected=predicted[n]; exact+=expected['valid']
            assert (int(cycle),int(valid),int(word,16),int(count),int(total))==(n,expected['valid'],expected['word'],expected['count'],exact)
        final=f"PASS_POOL_NET cycles={len(schedule)} exact={counts['exact']} accepted={counts['accepted']} cancelled={counts['cancelled']} resets={counts['resets']} maximum_burst={counts['maximum_burst']}"
        assert final in log and not re.search(r'Fatal:|Error:|ERROR:|\$fatal',log)
        after={p:sha(ROOT/p) for p in before}; assert after==before
        report.update(passed=True,exact_result_comparisons=exact,cycle_valid_checks=len(rows),
                      synchronous_port_checks=len(rows),accepted_inputs=counts['accepted'],
                      cancelled_pending_inputs=counts['cancelled'],reset_cycles=counts['resets'],
                      maximum_continuous_burst=counts['maximum_burst'],
                      source_sha256_after=after,source_before_after_sha_match=True)
    except Exception as error:
        report['failure_ko']=str(error)
    finally:
        report['wall_seconds']=round(time.monotonic()-started,6)
        for path in stage.iterdir():
            if path.is_file() and path.suffix in {'.log','.v','.sv','.tcl','.mem','.jou','.json'}:
                shutil.copy2(path,output/path.name)
        report['output_files_sha256']={p.name:sha(p) for p in output.iterdir() if p.is_file() and p.name!='result.json'}
        (output/'result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in {'output_files_sha256','source_sha256_before','source_sha256_after'}},ensure_ascii=True))
    return 0 if report['passed'] else 1


if __name__=='__main__':
    for stream in (sys.stdout,sys.stderr):
        if hasattr(stream,'reconfigure'):stream.reconfigure(encoding='utf-8')
    raise SystemExit(main())
