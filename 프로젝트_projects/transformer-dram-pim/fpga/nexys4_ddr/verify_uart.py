"""실기기 없이 UART wire-level 8N1 프레임과 실제 학습 RTL logits를 대조한다.

MMCM/pad는 Vivado 구현으로 확인하고, 여기서는 profile의 5MHz 또는2.5MHz core clock을 testbench가
제공한다. 가짜 UART/고정 점수로 대체하지 않고 RX/TX 직렬 비트와 Transformer
core를 모두 실행한다. context8/invalid ID/reset 응답도 검사한다.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from model.gpt_q88 import load_checkpoint, forward_q88, write_mem_files
from verify_trained_generation import find_tool
# 아래 함수는 PC 도구의 stdout/stderr만 읽는다. UART의 int16 payload나
# FPGA의 Q8.8 값을 문자 encoding으로 바꾸는 동작은 하지 않는다.
from tools.console_text import run_console


def main() -> int:
    # 실제 PC baud와 FPGA 정수 divider의 속도 차이도 검사한다.
    # 기본115200은 FPGA의5MHz/43=116279.07과 약0.94% 다르다.
    parser=argparse.ArgumentParser(description='실제 UART bit와 학습 Transformer 정수 결과를 비교')
    parser.add_argument('--host-baud',type=int,default=115200,help='PC를 흉내 내는 송수신 baud')
    parser.add_argument('--core-clock-hz',type=int,choices=[2500000,5000000],default=5000000,
                        help='testbench가 실제로 제공할 clock. 32 저속 profile은2500000')
    parser.add_argument('--fpga-baud',type=int,default=0,help='RTL target baud; 0이면 clock에 따라115200/57600')
    parser.add_argument('--context',type=int,default=8,choices=range(1,33),help='실제 core cache 한도; 기본8')
    parser.add_argument('--flat-cache',action='store_true',help='K/V의 flat distributed memory RTL 경로를 검증')
    parser.add_argument('--compare-cache-layouts',action='store_true',
                        help='반대 저장형태 core도 같은 입력으로 실행해 모든 cycle의 제어/hidden/logits/카운터/UART를 대조')
    parser.add_argument('--output-dir',type=Path,default=ROOT/'build/nexys4_ddr/uart_simulation')
    args=parser.parse_args()
    if args.fpga_baud==0: args.fpga_baud=57600 if args.core_clock_hz==2500000 else 115200
    if args.host_baud<=0: parser.error('--host-baud는 양수여야 합니다.')
    if args.fpga_baud<=0 or args.core_clock_hz//args.fpga_baud<8: parser.error('유효한 FPGA UART 분주값이 필요합니다.')
    work=args.output_dir.resolve()
    work.mkdir(parents=True,exist_ok=True)
    model=load_checkpoint(ROOT/'output/tiny_gpt_full_ops_qat/tiny_gpt_qat_q88.json')
    write_mem_files(model,work/'weights')
    ids=[30,27]
    ids=ids[:args.context]
    while len(ids)<args.context:
        logits=forward_q88(model,ids)[1][-1]
        ids.append(max(range(65),key=lambda i:logits[i]))
    expected=[forward_q88(model,ids[:i+1])[1][-1] for i in range(args.context)]
    expected.append(forward_q88(model,[30])[1][-1])
    total_logits=(args.context+1)*65
    total_frames=args.context+5
    (work/'expected.mem').write_text(''.join(f'{x&0xffff:04x}\n' for row in expected for x in row),encoding='ascii')
    commands=['send_and_check(255,1,0,0,0);','send_and_check(65,224,0,0,0);']
    commands += [f'send_and_check({tid},0,{i+1},65,{i});' for i,tid in enumerate(ids)]
    commands += [f'send_and_check(30,226,{args.context},0,0);','send_and_check(255,1,0,0,0);',
                 f'send_and_check(30,0,1,65,{args.context});']
    bench=r'''`timescale 1ns/1ps
module tb_nexys_uart;
    reg clk=0; always #CLOCK_HALF_NS clk=~clk;
    reg reset_n=0, rx=1;
    wire tx; wire [3:0] led;
    nexys4_ddr_gpt_uart_bridge #(.CLOCK_HZ(CLOCK_HZ_VALUE),.BAUD(FPGA_BAUD_VALUE),.MAX_CONTEXT(CONTEXT_VALUE),.FLAT_DISTRIBUTED_CACHE(FLAT_VALUE)) dut(.clk(clk),.reset_n(reset_n),.uart_rx(rx),.uart_tx(tx),.status_led(led));
    CACHE_LAYOUT_COMPARISON
    reg [15:0] expected[0:LOGITS_LAST];
    integer comparisons=0, frames=0;
    localparam real HOST_BIT_NS=1000000000.0/HOST_BAUD_VALUE;
    // PC baud는 DUT divider에 맞추어 강제하지 않는다. 비동기 위상/baud차이를 포함한다.
    task automatic send_byte(input [7:0] value);
        integer bitnum;
        begin
            @(negedge clk); rx=0; #(HOST_BIT_NS);
            for(bitnum=0;bitnum<8;bitnum=bitnum+1) begin
                rx=value[bitnum]; #(HOST_BIT_NS);
            end
            rx=1; #(HOST_BIT_NS);
        end
    endtask
    // 송신선을 직접 샘플한다. header만 함수로 주입하는 시험과 달리 실제serialbit를본다.
    task automatic receive_byte(output [7:0] value);
        integer bitnum;
        begin
            @(negedge tx);
            #(HOST_BIT_NS*1.5);
            for(bitnum=0;bitnum<8;bitnum=bitnum+1) begin
                value[bitnum]=tx; #(HOST_BIT_NS);
            end
            if(tx!==1'b1) $fatal(1,"UART stop bit mismatch");
        end
    endtask
    task automatic check_byte(input integer expected_byte);
        reg [7:0] value;
        begin receive_byte(value); if(value!==expected_byte[7:0]) $fatal(1,"byte mismatch got=%h expected=%h",value,expected_byte); end
    endtask
    task automatic check_frame(input integer status,input integer count,input integer words,input integer row);
        reg [7:0] low_byte,high_byte;
        reg [15:0] word;
        integer i;
        begin
            check_byte(71); check_byte(80); check_byte(status); check_byte(count); check_byte(words);
            for(i=0;i<words;i=i+1) begin
                receive_byte(low_byte); receive_byte(high_byte); word={high_byte,low_byte};
                if(word!==expected[row*65+i]) $fatal(1,"logit mismatch row=%0d id=%0d got=%h expected=%h",row,i,word,expected[row*65+i]);
                comparisons=comparisons+1;
            end
            frames=frames+1;
            // 마지막 stop bit의 나머지 구간과 controller IDLE 복귀를 기다린다.
            repeat(30) @(posedge clk);
        end
    endtask
    task automatic send_and_check(input integer command,input integer status,input integer count,input integer words,input integer row);
        begin
            // reset ACK는 input stop bit 종료 전에도 시작될 수 있으므로 송수신을동시에기다린다.
            fork send_byte(command[7:0]); check_frame(status,count,words,row); join
        end
    endtask
    initial begin
        $readmemh("expected.mem",expected);
        repeat(6) @(negedge clk); reset_n=1; repeat(12) @(negedge clk);
        COMMANDS
        if(comparisons!=LOGITS_VALUE || frames!=FRAMES_VALUE) $fatal(1,"coverage count mismatch");
        $display("PASS: Nexys UART 8N1, FRAMES_VALUE frames, LOGITS_VALUE exact logits, contextCONTEXT_VALUE, invalid ID, reset/restart");
        $finish;
    end
    initial begin #2000000000; $fatal(1,"UART simulation timeout"); end
endmodule
'''.replace('COMMANDS','\n        '.join(commands)).replace('HOST_BAUD_VALUE',f'{args.host_baud}.0')
    # 옵션을 켜면 flat/legacy 양쪽의 결과만 아니라 clock 단위 제어와 계산 cycle도 대조한다.
    # 동일 RX/clock/reset을 공유하고 실제 TX line과 내부 완료/유효/카운터를 비교하므로,
    # 같은 logits를 한 cycle 늦게 내는 변경이나 reset 뒤 stale cache 사용도 검출한다.
    comparison=r'''
    wire peer_tx; wire [3:0] peer_led;
    nexys4_ddr_gpt_uart_bridge #(.CLOCK_HZ(CLOCK_HZ_VALUE),.BAUD(FPGA_BAUD_VALUE),.MAX_CONTEXT(CONTEXT_VALUE),.FLAT_DISTRIBUTED_CACHE(PEER_FLAT_VALUE)) peer
        (.clk(clk),.reset_n(reset_n),.uart_rx(rx),.uart_tx(peer_tx),.status_led(peer_led));
    always @(posedge clk) if(reset_n) begin
        if({tx,led}!=={peer_tx,peer_led}) $fatal(1,"cache layout UART/LED cycle mismatch");
        if({dut.core.transformer_core.input_ready,dut.core.transformer_core.busy,
            dut.core.transformer_core.done,dut.core.transformer_core.result_valid,dut.core.transformer_core.error,
            dut.core.transformer_core.token_count,dut.core.transformer_core.cycle_count,dut.core.transformer_core.mac_count}
           !=={peer.core.transformer_core.input_ready,peer.core.transformer_core.busy,
            peer.core.transformer_core.done,peer.core.transformer_core.result_valid,peer.core.transformer_core.error,
            peer.core.transformer_core.token_count,peer.core.transformer_core.cycle_count,peer.core.transformer_core.mac_count})
            $fatal(1,"cache layout control/counter cycle mismatch");
        if(dut.core.transformer_core.hidden_flat!==peer.core.transformer_core.hidden_flat ||
           dut.core.transformer_core.logits_flat!==peer.core.transformer_core.logits_flat)
            $fatal(1,"cache layout hidden/logits cycle mismatch");
    end
'''
    bench=bench.replace('CACHE_LAYOUT_COMPARISON',comparison if args.compare_cache_layouts else '')
    bench=bench.replace('PEER_FLAT_VALUE',str(int(not args.flat_cache)))
    bench=bench.replace('FLAT_VALUE',str(int(args.flat_cache)))
    for key,value in [('CONTEXT_VALUE',args.context),('LOGITS_LAST',total_logits-1),
                      ('CLOCK_HALF_NS',500000000/args.core_clock_hz),
                      ('CLOCK_HZ_VALUE',args.core_clock_hz),('FPGA_BAUD_VALUE',args.fpga_baud),
                      ('LOGITS_VALUE',total_logits),('FRAMES_VALUE',total_frames)]:
        bench=bench.replace(key,str(value))
    (work/'tb_nexys_uart.sv').write_text(bench,encoding='utf-8')
    sources=[ROOT/'rtl'/name for name in ['dram_pim_pu_synth.sv','dram_pim_vmm_bank.sv',
        'transformer_gpt_kvcache_seq.sv','gpt_kvcache_rom_board_top.sv',
        'nexys4_ddr_uart.sv','nexys4_ddr_gpt_uart_bridge.sv']]
    compile_result=run_console([find_tool('iverilog'),'-g2012','-s','tb_nexys_uart','-o','simulation.out',
        *map(str,sources),'tb_nexys_uart.sv'],cwd=work,capture_output=True)
    (work/'compile.log').write_text(compile_result.stdout+compile_result.stderr,encoding='utf-8')
    if compile_result.returncode: raise SystemExit(compile_result.stderr)
    run=run_console([find_tool('vvp'),'simulation.out'],cwd=work,capture_output=True,timeout=240)
    (work/'simulation.log').write_text(run.stdout+run.stderr,encoding='utf-8')
    if run.returncode or 'PASS: Nexys UART' not in run.stdout: raise SystemExit(run.stdout+run.stderr)
    report={'mode':'rtl_wire_level_simulation','physical_board_measured':False,'passed':True,
        'input_ids':ids,'input_characters':''.join(model['vocab'][i] for i in ids),
        'core_context':args.context,'core_clock_hz':args.core_clock_hz,'uart_divisor':args.core_clock_hz//args.fpga_baud,
        'flat_distributed_cache':args.flat_cache,'cache_layout_cycle_exact_compared':args.compare_cache_layouts,
        'simulated_host_baud':args.host_baud,'fpga_target_baud':args.fpga_baud,
        'fpga_actual_baud':args.core_clock_hz/(args.core_clock_hz//args.fpga_baud),
        'reply_frames':total_frames,'exact_logit_comparisons':total_logits,
        'coverage':['8N1 serial RX/TX','little-endian signed int16','token mapping',
                    f'context{args.context} full','invalid token ID','reset ACK','reset then repeat token'],
        'simulation_log':str(work/'simulation.log')}
    (work/'result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(run.stdout.strip())
    return 0


if __name__=='__main__': raise SystemExit(main())
