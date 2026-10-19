`timescale 1ns/1ps
// 독립 MAX-EX 회로 검증용 testbench. tools/verify_e8m7_maxex.py가 같은 directory에
// a.mem/b.mem/expected.mem을 생성하고 Icarus를 실행한다. 여기서 실행되는 #1은
// 조합 신호가 모든 delta cycle을 거쳐 안정되도록 기다리는 것일 뿐, 실물 지연
// 또는 clock 주파수를 측정한 값이 아니다. 실제 timing은 Vivado OOC 보고서를 본다.
module tb_e8m7_maxex_mac #(
    parameter integer LANES = 16,
    parameter integer GUARD_BITS = 16,
    parameter integer CASES = 1
);
    reg [15:0] a [0:LANES-1];
    reg [15:0] b [0:LANES-1];
    wire [15:0] result;
    reg [15:0] a_memory [0:CASES*LANES-1];
    reg [15:0] b_memory [0:CASES*LANES-1];
    reg [15:0] expected_memory [0:CASES-1];
    localparam integer ACC_WIDTH = 16 + GUARD_BITS + ((LANES <= 1) ? 0 : $clog2(LANES)) + 1;
    wire signed [9:0] maximum_exponent;
    wire signed [ACC_WIDTH-1:0] accumulator;
    integer case_index;
    integer lane_index;

    // Icarus12는 길이1 unpacked array 포트를 scalar 연결로 elaboration한다.
    // testbench에서만 같은16bit 원소를 명시해 이 compiler 제약을 처리한다.
    // 실제 DUT의 LANES와 숫자 알고리즘은 바꾸지 않는다. 다중lane은 원 배열 연결이다.
    generate
        if (LANES == 1) begin : gen_single_lane
            dram_pim_e8m7_maxex_mac #(.LANES(LANES), .GUARD_BITS(GUARD_BITS)) dut (
                .a(a[0]), .b(b[0]), .result(result)
            );
            assign maximum_exponent = dut.max_nodes[1];
            assign accumulator = dut.sum_nodes[1];
        end else begin : gen_multiple_lanes
            dram_pim_e8m7_maxex_mac #(.LANES(LANES), .GUARD_BITS(GUARD_BITS)) dut (
                .a(a), .b(b), .result(result)
            );
            assign maximum_exponent = dut.max_nodes[1];
            assign accumulator = dut.sum_nodes[1];
        end
    endgenerate

    initial begin
        $readmemh("a.mem", a_memory);
        $readmemh("b.mem", b_memory);
        $readmemh("expected.mem", expected_memory);
        for (case_index = 0; case_index < CASES; case_index = case_index + 1) begin
            for (lane_index = 0; lane_index < LANES; lane_index = lane_index + 1) begin
                a[lane_index] = a_memory[case_index*LANES+lane_index];
                b[lane_index] = b_memory[case_index*LANES+lane_index];
            end
            #1;
            // 결과뿐 아니라 최대 지수와 넓은 누산값도 Python 상세 reference와 비교한다.
            // 특수값이 있어도 유한 항의 내부 트리는 독립적으로 계산되지만, driver는
            // 특수값 출력만 판정하고 수치 의미가 없는 중간값 비교는 생략한다.
            $display("MAXEX case=%0d result=%04h maxexp=%0d accumulator=%0d", case_index,
                result, maximum_exponent, accumulator);
            if (result !== expected_memory[case_index])
                $fatal(1, "MAXEX mismatch case=%0d result=%04h expected=%04h", case_index,
                    result, expected_memory[case_index]);
        end
        $display("MAXEX PASS lanes=%0d guard=%0d cases=%0d", LANES, GUARD_BITS, CASES);
        $finish;
    end
endmodule
