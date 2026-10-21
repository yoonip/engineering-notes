`timescale 1ns/1ps
// BUG_MODE=0은 정상, 1~5는 설명을 위한 의도적인 결함입니다.
module dot4 #(parameter integer BUG_MODE = 0) (
    input wire clk,
    input wire rst,
    input wire in_valid,
    output wire in_ready,
    input wire [15:0] in_tag,
    input wire [31:0] in_x,
    input wire [31:0] in_w,
    output wire out_valid,
    input wire out_ready,
    output wire [15:0] out_tag,
    output wire signed [31:0] out_data
);
    localparam [1:0] IDLE=0, BUSY=1, HOLD=2;
    reg [1:0] state;
    reg signed [31:0] pending_sum, result_sum;
    reg [15:0] pending_tag, result_tag;
    assign in_ready = !rst && (state == IDLE); // 수락할 수 있을 때만 ready입니다.
    assign out_valid = !rst && (state == HOLD); // reset 중에는 전송을 표시하지 않습니다.
    assign out_data = result_sum;
    assign out_tag = result_tag;

    function signed [31:0] dot;
        input [31:0] x, w;
        integer i;
        reg signed [7:0] sx, sw;
        reg signed [15:0] product;
        reg [15:0] unsigned_product;
        reg signed [31:0] accumulator;
        begin
            accumulator = 0;
            for (i=0; i<4; i=i+1) begin
                sx = x[i*8 +: 8]; // +:는 시작 비트에서 위쪽으로 8비트를 고릅니다.
                sw = w[i*8 +: 8];
                if (BUG_MODE == 1) begin
                    unsigned_product = $unsigned(sx) * $unsigned(sw);
                    accumulator = accumulator + {16'b0, unsigned_product};
                end else begin
                    product = sx * sw;
                    accumulator = accumulator + {{16{product[15]}}, product};
                    // {}는 연결, {16{...}}는 부호 비트 16회 반복입니다.
                end
            end
            if (BUG_MODE == 2)
                dot = {{16{accumulator[15]}}, accumulator[15:0]}; // 잘못된 16비트 축소입니다.
            else
                dot = accumulator;
        end
    endfunction

    always @(posedge clk) begin
        if (rst) begin
            if (BUG_MODE == 5 && state == HOLD) begin
                state <= HOLD; // 결함: reset 시 대기 중인 출력을 버리지 않습니다.
            end else begin
                state <= IDLE;
                pending_sum <= 0;
                result_sum <= 0;
                pending_tag <= 0;
                result_tag <= 0;
            end
        end else begin
            case (state)
                IDLE: if (in_valid && in_ready) begin
                    pending_sum <= dot(in_x, in_w);
                    pending_tag <= in_tag;
                    if (BUG_MODE == 4) begin
                        result_sum <= dot(in_x, in_w);
                        result_tag <= in_tag;
                        state <= HOLD; // 결함: 출력 전송이 한 edge 일찍 가능해집니다.
                    end else
                        state <= BUSY;
                end
                BUSY: begin
                    result_sum <= pending_sum;
                    result_tag <= pending_tag;
                    state <= HOLD;
                end
                HOLD: begin
                    if (BUG_MODE == 3 && in_valid) begin
                        result_sum <= dot(in_x, in_w); // 결함: ready=0인데 새 입력으로 덮습니다.
                        result_tag <= in_tag;
                    end
                    if (out_ready)
                        state <= IDLE; // valid와 ready가 함께인 edge에서만 출력 소비입니다.
                end
                default: state <= IDLE;
            endcase
        end
    end
endmodule
