"""배치·배선 완료 checkpoint의 실제 FPGA primitive를 UART까지 기능 시뮬레이션한다.

실행: python fpga/nexys4_ddr/verify_netlist.py
전체 cache: --full-context 8 또는 --full-context 32. 생략하면 기존 R/RO 시험이다.

이 검증은 RTL 소스를 다시 시뮬레이션하는 대신 routed.dcp에서 Vivado가 export한
funcsim netlist를 사용한다. IBUF/MMCM/BUFG, LUT, FF, DSP와 UART를 그대로 두고,
100MHz 외부 clock과 PC UART(8토큰 115200baud, 32토큰 57600baud)를 testbench에서 제공한다. 지연 SDF를 붙이지
않으므로 배선 지연을 포함한 timing simulation도, 실제 보드 측정도 아니다.

Vivado 2024.1의 한글 경로 문제를 피하도록 영문 임시 폴더에 입력을 복사한다.
기존 보드 보고서·가중치·bitstream을 수정하지 않으며 netlist_simulation 하위에만
작업한다. 단계별 로그와 실패 결과도 원본 프로젝트에 보존한다. 이미 설치된
Vivado의 xvlog/xelab/xsim 및 unisims 라이브러리를 사용하므로 새 도구를 설치하지 않는다.

공식 사용법: AMD UG900 2024.1의 xelab / xsim Executable Options / Library
Mapping File(xsim.ini). write_verilog -mode funcsim → xvlog → xelab → xsim 순서다.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from model.gpt_q88 import forward_q88, load_checkpoint


def sha256(path: Path) -> str:
    """회로 checkpoint와 학습 checkpoint를 결과에 특정하기 위한 내용 해시다."""
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verification_plan(model: dict, input_ids: list[int], full_context: int | None) -> dict:
    """실제 핀으로 보낼 명령과 각 정상 응답의 독립 Python 정답을 준비한다.

    full_context가 없으면 reset ACK + R + O의 기존 3 frame/130 logit 시험이다.
    전체 시험은 초기 reset·invalid ID·N개 정상 token·context-full·다시 reset·
    첫 token 반복이다. 오류/ACK frame에는 정답 logit 행이 없으며, 마지막
    정상 행은 새 문맥의 첫 token을 다시 계산한 결과여야 stale cache를 검출한다.
    """
    if not input_ids or any(type(token) is not int or not 0 <= token < 65 for token in input_ids):
        raise ValueError("시험 입력은 하나 이상의 유효한 vocab ID 0~64여야 합니다.")
    if full_context is None and input_ids != [30, 27]:
        raise ValueError("기본 작은 시험은 기존 R30/O27 입력을 유지합니다.")
    if full_context is not None and (full_context not in (8, 32) or len(input_ids) != full_context):
        raise ValueError("전체 시험의 입력 ID 개수는 지정한 context8/32와 같아야 합니다.")
    prefixes = [input_ids[:i + 1] for i in range(len(input_ids))]
    # 전체 forward를 매 prefix마다 새로 계산한다. DUT의 cache에 의존하지 않는다.
    rows = [forward_q88(model, prefix)[1][-1] for prefix in prefixes]
    commands = [(255, 1, 0, 0, 0)]
    if full_context is not None:
        commands.append((65, 0xe0, 0, 0, 0))
    commands.extend((token, 0, i + 1, 65, i) for i, token in enumerate(input_ids))
    if full_context is not None:
        commands.extend([(0, 0xe2, full_context, 0, 0), (255, 1, 0, 0, 0),
                         (input_ids[0], 0, 1, 65, len(rows))])
        prefixes.append([input_ids[0]])
        rows.append(forward_q88(model, prefixes[-1])[1][-1])
    return {"input_ids": list(input_ids), "rows": rows, "commands": commands,
            "prefixes": prefixes,
            "coverage_label": (f"context{full_context} full, invalid ID, overflow, reset/restart"
                               if full_context is not None else "reset ACK + R/O")}


def testbench(host_baud: int, commands: list[tuple[int, int, int, int, int]] | None = None,
              expected_words: int = 130, coverage_label: str = "reset ACK + R/O") -> str:
    """실제 핀을 구동하는 작은 PC 대역 모델을 만든다. DUT 내부 값을 강제하지 않는다."""
    if commands is None:
        commands = [(255, 1, 0, 0, 0), (30, 0, 1, 65, 0), (27, 0, 2, 65, 1)]
    # frame task 자체는 공통이며 명령열·정답 memory 크기·마지막 비교 수만 바꾼다.
    # SV의 expected는 실제 DUT가 아닌 독립 정답 저장소다. 내부 memory를 초기화하거나
    # primitive 출력을 강제하지 않으며 UART 핀에서 받은 16bit word와만 비교한다.
    command_lines = "\n        ".join(
        "send_and_check(" + ",".join(str(value) for value in command) + ");" for command in commands)
    bench = r'''`timescale 1ns/1ps
module tb_nexys_netlist;
    // 실제 보드 top의 100MHz input. MMCM과 BUFG는 netlist/vendor model 안에 있다.
    reg CLK100MHZ=0;
    always #5 CLK100MHZ=~CLK100MHZ;
    reg CPU_RESETN=0, UART_TXD_IN=1;
    wire UART_RXD_OUT;
    wire [3:0] LED;
    nexys4_ddr_gpt_top dut(.CLK100MHZ(CLK100MHZ),.CPU_RESETN(CPU_RESETN),
        .UART_TXD_IN(UART_TXD_IN),.UART_RXD_OUT(UART_RXD_OUT),.LED(LED));
    reg [15:0] expected[0:EXPECTED_LAST];
    integer comparisons=0,frames=0;
    localparam real HOST_BIT_NS=1000000000.0/HOST_BAUD_VALUE;

    // 모델 ID를 한 byte로 전송한다. 30은 R, 27은 O이며 ASCII 문자 값이 아니다.
    // 8N1: start0→8개 data(LSB 먼저)→stop1. FPGA divider와 PC baud 차이를 유지한다.
    task automatic send_byte(input [7:0] value);
        integer bitnum;
        begin
            @(negedge CLK100MHZ); UART_TXD_IN=0; #(HOST_BIT_NS);
            for(bitnum=0;bitnum<8;bitnum=bitnum+1) begin
                UART_TXD_IN=value[bitnum]; #(HOST_BIT_NS);
            end
            UART_TXD_IN=1; #(HOST_BIT_NS);
        end
    endtask

    // FPGA TX 핀의 start edge부터 각 data bit 중앙을 PC baud로 샘플한다.
    // function으로 결과 packet을 만들어 넣는 방식이 아니며 LUT/FF UART 출력이다.
    task automatic receive_byte(output [7:0] value);
        integer bitnum;
        begin
            @(negedge UART_RXD_OUT);
            #(HOST_BIT_NS*1.5);
            for(bitnum=0;bitnum<8;bitnum=bitnum+1) begin
                value[bitnum]=UART_RXD_OUT; #(HOST_BIT_NS);
            end
            if(UART_RXD_OUT!==1'b1) $fatal(1,"UART stop bit mismatch at %0t",$time);
        end
    endtask
    task automatic check_byte(input integer expected_byte);
        reg [7:0] value;
        begin
            receive_byte(value);
            if(value!==expected_byte[7:0])
                $fatal(1,"header mismatch got=%h expected=%h at %0t",value,expected_byte,$time);
        end
    endtask
    task automatic check_frame(input integer status,input integer count,input integer words,input integer row);
        reg [7:0] low_byte,high_byte;
        reg [15:0] word;
        integer i;
        begin
            check_byte(71); check_byte(80); check_byte(status); check_byte(count); check_byte(words);
            for(i=0;i<words;i=i+1) begin
                receive_byte(low_byte); receive_byte(high_byte); word={high_byte,low_byte};
                // 16bit 패턴을 exact 비교한다. 사람이 읽을 때에는 signed raw/256이 Q8.8 값이다.
                if(word!==expected[row*65+i])
                    $fatal(1,"logit mismatch row=%0d id=%0d got=%h expected=%h at %0t",
                           row,i,word,expected[row*65+i],$time);
                comparisons=comparisons+1;
            end
            frames=frames+1;
            $display("CHECK: frame=%0d status=%0d token_count=%0d words=%0d exact_logits=%0d time_ps=%0t",
                     frames,status,count,words,comparisons,$time);
            // 마지막 stop bit와 bridge의 다음 입력 허용을 기다린다.
            repeat(600) @(posedge CLK100MHZ);
        end
    endtask
    task automatic send_and_check(input integer command,input integer status,input integer count,input integer words,input integer row);
        begin
            // reset ACK는 입력 stop 종료 전에 시작될 수 있어 송신과 수신을 동시에 감시한다.
            fork send_byte(command[7:0]); check_frame(status,count,words,row); join
        end
    endtask
    initial begin
        $readmemh("expected.mem",expected);
        // glbl의 초기 GSR와 MMCM 초기 상태가 끝난 뒤 버튼 reset을 해제한다.
        repeat(200) @(negedge CLK100MHZ);
        CPU_RESETN=1;
        wait(LED[0]===1'b1);
        repeat(200) @(negedge CLK100MHZ);
        $display("CHECK: board ready through vendor MMCM/BUFG at %0t",$time);
        COMMAND_SEQUENCE
        if(comparisons!=EXPECTED_WORDS || frames!=EXPECTED_FRAMES) $fatal(1,"coverage count mismatch");
        $display("PASS: post-route functional netlist, actual MMCM/BUFG/pins, COVERAGE_LABEL, EXPECTED_FRAMES frames, EXPECTED_WORDS exact logits");
        $finish;
    end
    // 시뮬레이션 시간의 timeout이며 실제 보드 latency를 측정하는 값이 아니다.
    // 실수형 지연 리터럴로 40억 ns를 표현한다. unsized 정수는 일부
    // 시뮬레이터에서 32비트 범위를 넘으면 0시각으로 처리될 수 있다.
    initial begin #4000000000.0; $fatal(1,"netlist UART simulation timeout"); end
endmodule
'''
    for placeholder, value in [("HOST_BAUD_VALUE", f"{host_baud}.0"),
                               ("EXPECTED_LAST", expected_words - 1), ("EXPECTED_WORDS", expected_words),
                               ("EXPECTED_FRAMES", len(commands)), ("COVERAGE_LABEL", coverage_label),
                               ("COMMAND_SEQUENCE", command_lines)]:
        bench = bench.replace(placeholder, str(value))
    return bench


def validate_simulation_output(simulation: str, plan: dict) -> dict:
    """PASS 문자열뿐 아니라 모든 실제 frame의 상태·길이·누적 비교 수를 검증한다."""
    pattern = (r"^CHECK: frame=(\d+) status=(\d+) token_count=(\d+) words=(\d+) "
               r"exact_logits=(\d+) time_ps=(\d+)\s*$")
    names = ("frame", "status", "token_count", "words", "exact_logits", "time_ps")
    actual = [dict(zip(names, map(int, values))) for values in re.findall(pattern, simulation, re.M)]
    expected_frames = len(plan["commands"])
    expected_words = sum(command[3] for command in plan["commands"])
    if len(actual) != expected_frames:
        raise RuntimeError(f"실제 CHECK frame 수 {len(actual)}가 기대 {expected_frames}와 다릅니다.")
    cumulative = 0
    for frame_index, (frame, command) in enumerate(zip(actual, plan["commands"]), start=1):
        _, status, count, words, _ = command
        cumulative += words
        expected = (frame_index, status, count, words, cumulative)
        got = tuple(frame[name] for name in names[:-1])
        if got != expected:
            raise RuntimeError(f"실제 frame 상태/count/words/누적 비교 수가 다릅니다: {got} != {expected}")
    pass_counts = re.findall(
        r"^PASS: post-route functional netlist, actual MMCM/BUFG/pins, "
        + re.escape(plan["coverage_label"]) + r", (\d+) frames, (\d+) exact logits\s*$", simulation, re.M)
    if pass_counts != [(str(expected_frames), str(expected_words))]:
        raise RuntimeError("xsim의 최종 PASS/coverage 비교 수가 기대와 다릅니다. simulation.log를 확인하세요.")
    return {"reply_frames": len(actual), "exact_logit_comparisons": cumulative,
            "actual_logit_rows": sum(frame["words"] != 0 for frame in actual),
            "reply_frame_checks": actual,
            "simulated_frame_end_time_ps": [frame["time_ps"] for frame in actual]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, default=ROOT / "build/nexys4_ddr/board/routed.dcp")
    parser.add_argument("--model-checkpoint", type=Path,
                        default=ROOT / "output/tiny_gpt_full_ops_qat/tiny_gpt_qat_q88.json")
    parser.add_argument("--vivado-root", type=Path, default=Path("C:/Xilinx/Vivado/2024.1"))
    parser.add_argument("--stage", type=Path,
                        default=Path(tempfile.gettempdir()) / "nexys4_gpt_ascii_20261004/netlist_simulation")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "build/nexys4_ddr/netlist_simulation")
    parser.add_argument("--host-baud", type=int, default=115200)
    parser.add_argument("--full-context", type=int, choices=(8, 32),
                        help="실제 해당 context의 모든 prefix·invalid·full·reset/restart를 검증; 생략 시 R/RO")
    parser.add_argument("--uart-result", type=Path,
                        help="전체 시험에서 입력 ID열을 재사용할 기존 UART RTL result.json")
    parser.add_argument("--timeout", type=int, default=3600, help="각 tool 단계의 최대 벽시계 초")
    args = parser.parse_args()
    stage = args.stage.resolve()
    output = args.output_dir.resolve()
    if not str(stage).isascii():
        parser.error("--stage는 쓰기 가능한 영문/ASCII 경로여야 합니다.")
    if args.host_baud <= 0 or args.timeout <= 0:
        parser.error("--host-baud와 --timeout은 양수여야 합니다.")
    if stage == args.checkpoint.resolve().parent or output == args.checkpoint.resolve().parent:
        parser.error("기존 routed.dcp 폴더를 stage/output으로 사용하지 마세요. 별도 하위 폴더를 지정하세요.")
    if stage == output:
        parser.error("--stage와 --output-dir는 서로 다른 폴더여야 합니다.")
    for path in [args.checkpoint, args.model_checkpoint, args.vivado_root / "data/verilog/src/glbl.v"]:
        if not path.is_file():
            parser.error(f"필요한 파일이 없습니다: {path}")
    stage.mkdir(parents=True, exist_ok=True)
    output.mkdir(parents=True, exist_ok=True)
    model = load_checkpoint(args.model_checkpoint)
    # 보드 구현 보고서가 있으면 실제 DCP 해시와 context/저장 구조를 결과에 연결한다.
    # --full-context 값은 시험 요청이고 실제 하드웨어 크기는 보고서에서 읽는다.
    # 옵션이나 폴더 이름만으로 DCP의 context/저장 primitive를 추측하지 않는다.
    board_report_path = args.checkpoint.resolve().parent / 'result.json'
    board_metadata = {}
    if board_report_path.is_file():
        board_metadata = json.loads(board_report_path.read_text(encoding='utf-8'))
        expected_dcp_sha = board_metadata.get('routed_checkpoint', {}).get('sha256')
        if expected_dcp_sha and expected_dcp_sha != sha256(args.checkpoint):
            parser.error('구현 보고서의 routed DCP 해시가 지정한 checkpoint와 다릅니다.')
        expected_model_sha = board_metadata.get('checkpoint_sha256')
        if expected_model_sha and expected_model_sha != sha256(args.model_checkpoint):
            parser.error('구현 보고서의 학습 checkpoint 해시가 지정한 모델과 다릅니다.')
        if board_metadata.get('host_baud') is not None and args.host_baud != board_metadata['host_baud']:
            parser.error('PC baud가 지정한 bitstream profile과 다릅니다. 32 저속 구성은 --host-baud 57600을 사용하세요.')
    if len(model["vocab"]) != 65 or model["vocab"][30] != "R" or model["vocab"][27] != "O":
        parser.error("현재 검증은 checkpoint의 V65/R30/O27 정의를 사용합니다.")
    input_ids = [30, 27]
    uart_result_path = None
    if args.full_context is not None:
        if (board_metadata.get('max_context') != args.full_context
                or not board_metadata.get('routed_checkpoint', {}).get('sha256')
                or not board_metadata.get('checkpoint_sha256')):
            parser.error('전체 cache 시험에는 context가 같고 DCP/모델 해시가 기록된 구현 result.json이 필요합니다.')
        if args.uart_result is not None:
            uart_result_path = args.uart_result.resolve()
        else:
            uart_folder = ('uart_simulation' if args.full_context == 8 else
                           'uart_flat32_slow_simulation' if board_metadata.get('clock_hz') == 2500000 else
                           'uart_flat32_simulation' if board_metadata.get('cache_storage') == 'distributed' else
                           'uart_simulation_context32')
            uart_result_path = ROOT / 'build/nexys4_ddr' / uart_folder / 'result.json'
        if not uart_result_path.is_file():
            parser.error(f'입력 ID열을 읽을 UART 결과가 없습니다: {uart_result_path}')
        uart_result = json.loads(uart_result_path.read_text(encoding='utf-8-sig'))
        if uart_result.get('passed') is not True or uart_result.get('core_context') != args.full_context:
            parser.error('입력 ID열의 UART 결과가 PASS가 아니거나 context가 다릅니다.')
        if (uart_result.get('core_clock_hz') != board_metadata.get('clock_hz')
                or uart_result.get('simulated_host_baud') != args.host_baud):
            parser.error('전체 시험 입력의 UART RTL profile과 실제 보드 clock/PC baud가 다릅니다.')
        input_ids = uart_result.get('input_ids', [])
    elif args.uart_result is not None:
        parser.error('--uart-result는 --full-context와 함께 사용하세요.')
    try:
        plan = verification_plan(model, input_ids, args.full_context)
    except ValueError as error:
        parser.error(str(error))
    rows = plan['rows']
    expected_frames = len(plan['commands'])
    expected_words = sum(command[3] for command in plan['commands'])
    (stage / "expected.mem").write_text("".join(f"{value & 0xffff:04x}\n" for row in rows for value in row),
                                         encoding="ascii")
    (stage / "tb_nexys_netlist.sv").write_text(
        testbench(args.host_baud, plan['commands'], expected_words, plan['coverage_label']), encoding="utf-8")
    shutil.copy2(args.checkpoint, stage / "routed.dcp")
    shutil.copy2(args.vivado_root / "data/verilog/src/glbl.v", stage / "glbl.v")
    # 상대 경로만 Tcl에 전달하여 원본의 한글 경로가 Tcl parser에 들어가지 않게 한다.
    (stage / "export_netlist.tcl").write_text(
        "set_param general.maxThreads 1\n"
        "open_checkpoint routed.dcp\n"
        "write_verilog -force -mode funcsim nexys4_ddr_gpt_funcsim.v\n"
        "foreach primitive {MMCME2_ADV MMCME2_BASE BUFG IBUF OBUF DSP48E1 FDRE FDCE LUT6 RAMD64E RAMS64E RAMD32 RAMS32 RAM64M RAM32M} {\n"
        "  puts \"NETLIST_PRIMITIVE: $primitive [llength [get_cells -hier -filter REF_NAME==$primitive]]\"\n"
        "}\nexit\n", encoding="ascii")
    # run all은 $finish/timeout까지 실행한다. waveform을 기록하지 않아 큰 netlist의 메모리를 아낀다.
    (stage / "run_sim.tcl").write_text("run all\nquit\n", encoding="ascii")
    report = {
        "mode": "post_route_functional_netlist_simulation",
        "physical_board_measured": False,
        "physical_programming_performed": False,
        "sdf_annotated": False,
        "routed_delays_simulated": False,
        "passed": False,
        "routed_checkpoint": str(args.checkpoint.resolve()),
        "routed_checkpoint_sha256": sha256(args.checkpoint),
        "model_checkpoint_sha256": sha256(args.model_checkpoint),
        "ascii_stage": str(stage),
        "host_baud": args.host_baud,
        "input_ids": input_ids,
        "input_characters": ''.join(model['vocab'][token] for token in input_ids),
        "expected_logits_raw_q88": rows,
        "expected_logit_rows": len(rows),
        "expected_prefix_token_ids": plan['prefixes'],
        "expected_frame_commands": [dict(zip(('command_byte', 'status', 'token_count', 'words', 'oracle_row'),
                                             command)) for command in plan['commands']],
        "full_context_coverage": False,
        "requested_full_context": args.full_context,
        "uart_input_sequence_source": str(uart_result_path) if uart_result_path else None,
        "uart_input_sequence_source_sha256": sha256(uart_result_path) if uart_result_path else None,
        "board_implementation_report": str(board_report_path) if board_report_path.is_file() else None,
        "board_implementation_report_sha256": sha256(board_report_path) if board_report_path.is_file() else None,
        "simulation_time_unit": "1ps",
        "simulation_timeout_ns": 4000000000,
        "tool_stage_timeout_seconds": args.timeout,
        "expected_reply_frames": expected_frames,
        "expected_exact_logit_comparisons": expected_words,
        "reply_frames": None,
        "exact_logit_comparisons": None,
        "actual_logit_rows": None,
        "core_context": board_metadata.get('max_context'),
        "cache_storage": board_metadata.get('cache_storage', 'unspecified'),
        "board_clock_hz": board_metadata.get('clock_hz'),
        "steps": [],
        "official_references": [
            "https://docs.amd.com/r/2024.1-English/ug900-vivado-logic-simulation/xelab",
            "https://docs.amd.com/r/2024.1-English/ug900-vivado-logic-simulation/xsim-Executable-Options",
            "https://docs.amd.com/r/2024.1-English/ug900-vivado-logic-simulation/Library-Mapping-File-xsim.ini",
        ],
        "notes_ko": [
            "실제 배치·배선 회로의 기능 netlist를 export하여 정수값과 UART를 확인한다.",
            "MMCM/BUFG/IO primitive를 stub으로 대체하지 않으며 vendor 라이브러리를 사용한다.",
            "SDF 지연은 포함하지 않으므로 timing 검증은 route STA 보고서와 별개다.",
            "실제 FPGA 보드 programming·측정 결과가 아니다.",
        ],
    }
    env = os.environ.copy()
    env["XILINX_VIVADO"] = str(args.vivado_root.resolve())

    def run_step(name: str, arguments: list[str]) -> None:
        """각 프로그램을 별도 단계로 실행하고 returncode·명령·실패 로그를 남긴다."""
        print(f"진행: {name}", flush=True)
        started = time.monotonic()
        logpath = stage / f"{name}.console.log"
        timed_out = False
        process_pid = None
        process_tree_cleanup = None
        cleanup_error = None
        # subprocess의 list 인수로 호출하여 prompt/경로가 shell 코드가 되지 않게 한다.
        with logpath.open("w", encoding="utf-8") as log:
            # Windows에서는 .bat의 cmd/loader 아래에 Vivado/xsim 자식이 생긴다.
            # run(timeout)만 쓰면 wrapper만 종료될 수 있어, 직접 시작한 PID의 트리를 정리한다.
            process = subprocess.Popen(arguments, cwd=stage, env=env, stdout=log,
                                       stderr=subprocess.STDOUT,
                                       creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
            process_pid = process.pid
            try:
                returncode = process.wait(timeout=args.timeout)
            except subprocess.TimeoutExpired:
                timed_out = True
                returncode = None
                report["failure_ko"] = f"{name} 단계의 벽시계 제한 {args.timeout}초 초과"
                if os.name == "nt":
                    try:
                        cleanup = subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                                                 stdout=log, stderr=subprocess.STDOUT, timeout=30)
                        process_tree_cleanup = cleanup.returncode == 0
                        if not process_tree_cleanup:
                            cleanup_error = f"자체 PID {process.pid}의 tree 정리 실패(returncode={cleanup.returncode})"
                    except Exception as error:
                        process_tree_cleanup = False
                        cleanup_error = str(error)
                else:
                    process.kill()
                # 정리에 성공한 wrapper만 회수한다. 권한 거부 때 다른 process를 찾거나 종료하지 않는다.
                if process_tree_cleanup or os.name != "nt":
                    try:
                        process.wait(timeout=30)
                    except subprocess.TimeoutExpired:
                        cleanup_error = "tree 종료 요청 후 wrapper 회수 시간 제한 초과"
                if cleanup_error:
                    report["failure_ko"] += "; " + cleanup_error + ". 로그/PID를 확인한 뒤 재실행하세요."
        report["steps"].append({"stage": name, "command": arguments, "returncode": returncode,
                                 "started_process_pid": process_pid, "timed_out": timed_out,
                                 "timeout_process_tree_cleaned": process_tree_cleanup,
                                 "timeout_cleanup_error": cleanup_error,
                                 "wall_seconds": round(time.monotonic() - started, 3),
                                 "log": str(output / logpath.name)})
        if returncode != 0:
            raise RuntimeError(report.get("failure_ko", f"{name} 실패(returncode={returncode})"))
        print(f"완료: {name}", flush=True)

    bin_dir = args.vivado_root / "bin"
    try:
        run_step("export", [str(bin_dir / "vivado.bat"), "-mode", "batch", "-source", "export_netlist.tcl",
                            "-log", "export.log", "-journal", "export.jou"])
        exported_log = (stage / "export.console.log").read_text(encoding="utf-8", errors="replace")
        primitive_counts = {name: int(count) for name, count in
                            re.findall(r"NETLIST_PRIMITIVE: (\w+) (\d+)", exported_log)}
        report["exported_primitive_counts"] = primitive_counts
        if (primitive_counts.get("MMCME2_ADV", 0) + primitive_counts.get("MMCME2_BASE", 0) < 1
                or primitive_counts.get("BUFG", 0) < 2
                or primitive_counts.get("IBUF", 0) < 3
                or primitive_counts.get("OBUF", 0) < 5):
            raise RuntimeError("실제 MMCM/BUFG/입출력 primitive가 예상과 다릅니다. export.log를 확인하세요.")
        netlist = stage / "nexys4_ddr_gpt_funcsim.v"
        report["functional_netlist_sha256"] = sha256(netlist)
        report["functional_netlist_bytes"] = netlist.stat().st_size
        run_step("xvlog", [str(bin_dir / "xvlog.bat"), "--sv", "--work", "xil_defaultlib",
                           "nexys4_ddr_gpt_funcsim.v", "tb_nexys_netlist.sv", "glbl.v"])
        run_step("xelab", [str(bin_dir / "xelab.bat"), "--mt", "2", "--O2", "--debug", "off",
                           "-L", "unisims_ver", "-L", "unimacro_ver", "-L", "secureip",
                           "xil_defaultlib.tb_nexys_netlist", "xil_defaultlib.glbl", "-s", "nexys_netlist"])
        run_step("xsim", [str(bin_dir / "xsim.bat"), "nexys_netlist", "-tclbatch", "run_sim.tcl",
                          "-log", "simulation.log"])
        simulation = (stage / "xsim.console.log").read_text(encoding="utf-8", errors="replace")
        report.update(validate_simulation_output(simulation, plan))
        report.update({"passed": True, "full_context_coverage": args.full_context is not None,
                       "coverage": ["100MHz input clock", "vendor MMCM/BUFG/IO primitives",
                                    "global startup glbl", "reset ACK", f"{args.host_baud}baud serial RX/TX",
                                    (f"all {args.full_context} prefixes full65 signed Q8.8 logits"
                                     if args.full_context is not None else "R and RO full65 signed Q8.8 logits")]
                                   + (["invalid token ID65/E0", "context full/E2", "reset then first token repeat"]
                                      if args.full_context is not None else [])})
    except Exception as error:
        report["failure_ko"] = str(error)
        print(f"실패: {error}", flush=True)
    finally:
        # xsim.dir의 대형 중간 산출물은 stage에 보존하고 작은 입력·로그·netlist만 복사한다.
        for path in stage.iterdir():
            if path.is_file() and path.name != "routed.dcp":
                shutil.copy2(path, output / path.name)
        (output / "result.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "mode": report["mode"],
                      "physical_board_measured": False, "sdf_annotated": False,
                      "report": str(output / "result.json")}, ensure_ascii=True), flush=True)
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    # Windows redirected stdout도 한글 진행 메시지를 UTF-8로 저장하게 한다.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    raise SystemExit(main())
