"""실제 OOC 배선 DCP의 등록형 E8M7 pairwise floating tree를 XSim에서 직접 실행한다.

원본 RTL을 다시 DUT로 컴파일하지 않는다. DCP에서 export한 vendor primitive
netlist의 packed 입력/결과/valid/reset을 검사한다. 이 도구는 기능 netlist
시험이며 SDF 배선 지연 시험과 실물 장비 측정으로 해석하지 않는다.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from model.e8m7_maxex import edge_vectors, rounded_product_tree_dot


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pack(words: list[int]) -> str:
    """SV [16*i +: 16]와 같게 lane0을 256bit 버스의 최하위에 둔다."""
    return ''.join(f'{word:04x}' for word in reversed(words))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--random-cases', type=int, default=128)
    parser.add_argument('--timeout', type=int, default=1800)
    parser.add_argument('--vivado-root', type=Path, default=Path('C:/Xilinx/Vivado/2024.1'))
    args = parser.parse_args()
    if args.random_cases < 0 or args.timeout < 1:
        parser.error('random-cases는 0 이상, timeout은 1 이상이어야 합니다.')
    board = ROOT/'build/e8m7_pairwise/vivado'
    output = ROOT/'build/e8m7_pairwise/netlist'
    stage = Path(tempfile.gettempdir())/('pairwise_netlist_'+uuid.uuid4().hex)
    stage.mkdir()
    output.mkdir(parents=True, exist_ok=True)
    report = {'passed': False, 'mode': 'post_route_independent_pairwise_functional_netlist',
              'rounding_policy':'RNE_after_each_product_and_each_tree_add', 'lanes': 16, 'ascii_stage': str(stage),
              'sdf_annotated': False, 'routed_delays_simulated': False,
              'physical_board_measured': False, 'gpt_q88_connected': False, 'steps': []}
    env = os.environ.copy()
    env['XILINX_VIVADO'] = str(args.vivado_root.resolve())
    def run(name, command):
        print('진행: 일반 E8M7 tree netlist '+name, flush=True)
        started = time.monotonic()
        with (stage/f'{name}.console.log').open('w', encoding='utf-8') as log:
            process = subprocess.Popen(command, cwd=stage, env=env, stdout=log,
                    stderr=subprocess.STDOUT,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
            try:
                code = process.wait(timeout=args.timeout)
            except subprocess.TimeoutExpired:
                if os.name=='nt':
                    subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],
                                   stdout=log,stderr=subprocess.STDOUT,timeout=30)
                else:
                    process.kill()
                raise RuntimeError(name+' 자체 작업 시간 제한 초과')
        report['steps'].append({'name':name,'command':command,'returncode':code,
                               'wall_seconds':round(time.monotonic()-started,3)})
        if code:
            raise RuntimeError(name+' exit '+str(code))
    try:
        implementation = json.loads((board/'result.json').read_text(encoding='utf-8'))
        assert implementation['passed'] and implementation['lanes']==16
        assert sha(board/'routed.dcp') == implementation['routed_checkpoint_sha256']
        for item in implementation['source_snapshot']:
            assert sha(ROOT/item['file']) == item['sha256'], item['file']+' source 변경'
        report['routed_checkpoint_sha256'] = implementation['routed_checkpoint_sha256']
        # 이 Windows Vivado는 UTF-8 Tcl 안의 한글 경로를 다른 문자로 읽는다.
        # 검증한 DCP 바이트를 영문 임시 위치에 복사하고 복사 후에도 SHA를 검사한다.
        shutil.copy2(board/'routed.dcp',stage/'routed.dcp')
        assert sha(stage/'routed.dcp') == report['routed_checkpoint_sha256']
        report['source_sha256'] = {x['file']:x['sha256'] for x in implementation['source_snapshot']}
        report['source_sha256']['model/e8m7_maxex.py'] = sha(ROOT/'model/e8m7_maxex.py')
        report['source_sha256']['tools/verify_e8m7_pairwise_netlist.py'] = sha(Path(__file__))
        vectors = []
        for edge in edge_vectors():
            a,b = edge['a_words'], edge['b_words']
            vectors.append({'name':edge['name'], 'a_words':a+[0]*(16-len(a)),
                            'b_words':b+[0]*(16-len(b))})
        vectors.append({'name':'pairwise_half_ulp_then_cancel',
                        'a_words':[0x3f80,0x3b80,0xbf80]+[0]*13,
                        'b_words':[0x3f80,0x3f80,0x3f80]+[0]*13})
        rng = random.Random(20261004)
        for i in range(args.random_cases):
            vectors.append({'name':'random_'+str(i),'a_words':[rng.randrange(65536) for _ in range(16)],
                            'b_words':[rng.randrange(65536) for _ in range(16)]})
        for row in vectors:
            row['expected_word'] = rounded_product_tree_dot(row['a_words'],row['b_words'])
        count = len(vectors)
        report['expected_comparisons'] = count+1
        report['vectors'] = vectors
        for filename, values in [('a.mem',[pack(x['a_words']) for x in vectors]),
                                 ('b.mem',[pack(x['b_words']) for x in vectors]),
                                 ('expected.mem',[f"{x['expected_word']:04x}" for x in vectors])]:
            (stage/filename).write_text('\n'.join(values)+'\n',encoding='ascii')
        (stage/'export.tcl').write_text(
            'open_checkpoint routed.dcp\n'
            'write_verilog -force -mode funcsim design.v\nexit\n',encoding='utf-8')
        tb = f'''`timescale 1ns/1ps
// DUT는 Vivado가 실제 배선 checkpoint에서 내보낸 primitive 회로다.
// 입력을 받은 edge의 다음 edge에 output_valid가 올라오는 register 동작을 검사한다.
module tb_pairwise_netlist;
reg clk=0, reset_n=0, input_valid=0;
reg [255:0] a_packed=0,b_packed=0;
wire [15:0] result;
wire output_valid;
reg [255:0] a_values[0:{count-1}],b_values[0:{count-1}];
reg [15:0] expected[0:{count-1}];
integer i, exact_count=0;
pw_top dut(.clk(clk),.reset_n(reset_n),.input_valid(input_valid),
    .a_packed(a_packed),.b_packed(b_packed),.result(result),.output_valid(output_valid));
always #100 clk=~clk; // OOC 제약과 같은 5MHz/200ns clock이다.
task automatic transaction(input integer index);
begin
    @(negedge clk); a_packed=a_values[index]; b_packed=b_values[index]; input_valid=1;
    @(negedge clk); input_valid=0;
    @(posedge clk); #1;
    if(output_valid!==1 || result!==expected[index])
        $fatal(1,"PAIRWISE mismatch index=%0d result=%h expected=%h valid=%b",index,result,expected[index],output_valid);
    exact_count=exact_count+1;
    $display("CHECK: case=%0d result=%h exact=%0d",index,result,exact_count);
end
endtask
initial begin
    $readmemh("a.mem",a_values); $readmemh("b.mem",b_values); $readmemh("expected.mem",expected);
    repeat(4) @(negedge clk); reset_n=1;
    for(i=0;i<{count};i=i+1) transaction(i);
    // 새 입력이 register에 들어간 뒤 동기 reset으로 pending 결과를 취소한다.
    @(negedge clk); a_packed=a_values[2]; b_packed=b_values[2]; input_valid=1;
    @(negedge clk); reset_n=0; input_valid=0;
    @(posedge clk); #1;
    if(output_valid!==0 || result!==0) $fatal(1,"reset did not clear output");
    @(negedge clk); reset_n=1;
    transaction(2);
    @(negedge clk); @(posedge clk); #1;
    if(output_valid!==0) $fatal(1,"output_valid did not drop after idle");
    $display("PASS: PAIRWISE routed functional netlist exact=%0d reset=1 idle=1",exact_count);
    $finish;
end
initial begin #1000000.0; $fatal(1,"timeout"); end
endmodule
'''
        (stage/'tb.sv').write_text(tb,encoding='utf-8')
        shutil.copy2(args.vivado_root/'data/verilog/src/glbl.v',stage/'glbl.v')
        (stage/'run.tcl').write_text('run all\nquit\n',encoding='ascii')
        bindir=args.vivado_root/'bin'
        run('export',[str(bindir/'vivado.bat'),'-mode','batch','-source','export.tcl'])
        report['functional_netlist_sha256'] = sha(stage/'design.v')
        run('xvlog',[str(bindir/'xvlog.bat'),'--sv','--work','xil_defaultlib','design.v','tb.sv','glbl.v'])
        run('xelab',[str(bindir/'xelab.bat'),'--mt','2','--O2','--debug','off',
                    '-L','unisims_ver','-L','unimacro_ver','-L','secureip',
                    'xil_defaultlib.tb_pairwise_netlist','xil_defaultlib.glbl','-s','pairwise_netlist'])
        run('xsim',[str(bindir/'xsim.bat'),'pairwise_netlist','-tclbatch','run.tcl','-log','simulation.log'])
        log=(stage/'xsim.console.log').read_text(encoding='utf-8',errors='replace')
        rows=re.findall(r'^CHECK: case=(\d+) result=([0-9a-fA-F]+) exact=(\d+)\s*$',log,re.M)
        assert len(rows)==count+1, 'actual comparison row count'
        for index,(case,word,compared) in enumerate(rows):
            wanted=index if index<count else 2
            assert int(case)==wanted and int(word,16)==vectors[wanted]['expected_word']
            assert int(compared)==index+1
        assert f'PASS: PAIRWISE routed functional netlist exact={count+1} reset=1 idle=1' in log
        assert not re.search(r'Fatal:|Error:|\$fatal',log), 'xsim fatal/error'
        report.update({'passed':True,'exact_word_comparisons':count+1,'reset_checked':True,'idle_valid_checked':True})
    except Exception as error:
        report['failure_ko']=str(error)
    finally:
        for path in stage.iterdir():
            if path.is_file() and path.suffix in ('.log','.v','.sv','.tcl','.mem','.jou'):
                shutil.copy2(path,output/path.name)
        (output/'result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='vectors'},ensure_ascii=True))
    return 0 if report['passed'] else 1


if __name__=='__main__':
    for stream in (sys.stdout,sys.stderr):
        if hasattr(stream,'reconfigure'): stream.reconfigure(encoding='utf-8')
    raise SystemExit(main())
