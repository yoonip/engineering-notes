`timescale 1ns/1ps
// =============================================================================
// 독립 pooling PU의 입력/출력 register 경계다.
// 입력을 rising edge N에서 input_valid=1로 수락하면 N+1 직후 결과를 출력한다.
// 연속 valid에서는 매 clock 한 결과를 낼 수 있는 구조지만, 실제 최고 주파수는
// 별도 합성/배치/배선 STA로 확인해야 한다. 이 파일만으로 timing을 보장하지 않는다.
// reset_n은 동기 active-low reset: edge에서 reset이 우선하고 pending 입력을 취소한다.
// bubble(input_valid=0)은 다음 output_valid=0이며 그때 결과/count는 0으로 정의한다.
// Python verify_pooling_pu.py의 schedule scoreboard가 같은 1clock 계약을 검사한다.
// =============================================================================
module dram_pim_pooling_registered_top #(
    parameter integer WINDOW = 16
) (
    input wire clk,
    input wire reset_n,
    input wire input_valid,
    input wire [WINDOW*16-1:0] values_packed,
    input wire [WINDOW-1:0] valid_mask,
    input wire operation_avg,
    output reg signed [15:0] result,
    output reg [$clog2(WINDOW+1)-1:0] valid_count,
    output reg output_valid
);
    reg [WINDOW*16-1:0] values_registered;
    reg [WINDOW-1:0] mask_registered;
    reg operation_registered;
    reg registered_valid;
    wire signed [15:0] combinational_result;
    wire [$clog2(WINDOW+1)-1:0] combinational_count;

    dram_pim_pooling_pu #(.WINDOW(WINDOW)) u_pooling (
        .values_packed(values_registered), .valid_mask(mask_registered),
        .operation_avg(operation_registered), .result(combinational_result),
        .valid_count(combinational_count)
    );

    always @(posedge clk) begin
        if (!reset_n) begin
            values_registered <= {WINDOW*16{1'b0}};
            mask_registered <= {WINDOW{1'b0}};
            operation_registered <= 1'b0;
            registered_valid <= 1'b0;
            result <= 16'sd0;
            valid_count <= {$clog2(WINDOW+1){1'b0}};
            output_valid <= 1'b0;
        end else begin
            if (input_valid) begin
                values_registered <= values_packed;
                mask_registered <= valid_mask;
                operation_registered <= operation_avg;
            end
            registered_valid <= input_valid;
            // <=는 같은 edge의 새 입력이 아니라 직전 register의 조합 결과를
            // 받는다. 그래서 입력 N에 대응하는 출력은 N+1에서 나타난다.
            output_valid <= registered_valid;
            result <= registered_valid ? combinational_result : 16'sd0;
            valid_count <= registered_valid ? combinational_count : {$clog2(WINDOW+1){1'b0}};
        end
    end
endmodule
