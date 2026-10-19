// E8M7 MAX-EX 누산기의 FPGA 물리 구현을 따로 측정하는 등록형 wrapper입니다.
// 현재 Q8.8 Transformer 보드 top을 바꾸는 파일이 아닙니다. 원 제안의
// 부동소수점 누산 구조를 독립 연구 모듈로 합성·배치·배선하기 위한 경계입니다.
// 많은 병렬 입력은 out-of-context(OOC)의 가상 포트이므로 실제 Nexys 핀에
// 연결했다는 뜻이 아닙니다. 실제 보드 bitstream과 이 OOC 결과를 구분합니다.
`timescale 1ns/1ps
module e8m7_maxex_registered_top #(
    parameter integer LANES=16,
    parameter integer GUARD_BITS=16
) (
    input wire clk,
    // reset_n은 clk edge에서 검사하는 동기 reset입니다.
    input wire reset_n,
    input wire input_valid,
    // lane i의 16bit E8M7은 [16*i +: 16]에 들어갑니다.
    // Python에서는 a_words[i], b_words[i] 두 정수 리스트에 해당합니다.
    input wire [LANES*16-1:0] a_packed,
    input wire [LANES*16-1:0] b_packed,
    output reg [15:0] result,
    output reg output_valid
);
    reg [15:0] a_registered[0:LANES-1];
    reg [15:0] b_registered[0:LANES-1];
    reg registered_valid;
    wire [15:0] combinational_result;
    integer lane;

    // 곱→최대 지수→정렬→adder tree→정규화/RNE를 이 조합 모듈이 담당합니다.
    // 두 경계 register 사이의 지연을 STA로 검사할 수 있도록 입력과 결과를
    // register에 둡니다. 내부가 여러 pipeline stage로 나뉘었다는 뜻은 아닙니다.
    dram_pim_e8m7_maxex_mac #(.LANES(LANES),.GUARD_BITS(GUARD_BITS)) u_maxex
        (.a(a_registered),.b(b_registered),.result(combinational_result));

    always @(posedge clk) begin
        if (!reset_n) begin
            for (lane=0;lane<LANES;lane=lane+1) begin
                a_registered[lane]<=16'h0000;
                b_registered[lane]<=16'h0000;
            end
            registered_valid<=1'b0;
            result<=16'h0000;
            output_valid<=1'b0;
        end else begin
            // edge에서 입력을 받은 뒤 다음 edge에서 계산 결과가 등록됩니다.
            // nonblocking <=이므로 이 줄의 result는 이번 edge에 덮어쓴 입력이
            // 아니라 직전 edge에 등록한 입력의 결과를 받습니다.
            if (input_valid) begin
                for (lane=0;lane<LANES;lane=lane+1) begin
                    a_registered[lane]<=a_packed[16*lane +: 16];
                    b_registered[lane]<=b_packed[16*lane +: 16];
                end
            end
            registered_valid<=input_valid;
            result<=combinational_result;
            output_valid<=registered_valid;
        end
    end
endmodule
