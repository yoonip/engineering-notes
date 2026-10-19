// 독립 pairwise baseline의 OOC/경계검증용 등록 wrapper.
// MAX-EX wrapper와 같은 경계: edge N에 a/b를 저장하고 edge N+1에 결과/valid를
// 저장한다. 내부 곱셈·adder tree는 조합 회로이며 단계마다 pipeline한 구조가 아니다.
// 16lane packed bus에서는 lane i가 [16*i+:16]; Python little-word packing과 같다.
module e8m7_pairwise_registered_top #(
    parameter integer LANES = 16
) (
    input wire clk,
    input wire reset_n,
    input wire input_valid,
    input wire [16*LANES-1:0] a_packed,
    input wire [16*LANES-1:0] b_packed,
    output reg [15:0] result,
    output reg output_valid
);
    reg [15:0] a [0:LANES-1];
    reg [15:0] b [0:LANES-1];
    reg registered_valid;
    wire [15:0] combinational_result;
    integer lane_index;
    e8m7_pairwise_tree_mac #(.LANES(LANES)) arithmetic (
        .a(a), .b(b), .result(combinational_result)
    );
    // synchronous active-low reset: 다음 상승 edge에서 pending 결과를 취소한다.
    // reset과 valid가 동시에 1이어도 reset이 우선한다. bubble은 valid를 내리며
    // 입력 register를 유지한다. result는 매 clock 등록하므로 invalid 때 소비하지 않는다.
    always @(posedge clk) begin
        if (!reset_n) begin
            for (lane_index=0; lane_index<LANES; lane_index=lane_index+1) begin
                a[lane_index] <= 0;
                b[lane_index] <= 0;
            end
            registered_valid <= 0;
            output_valid <= 0;
            result <= 0;
        end else begin
            registered_valid <= input_valid;
            output_valid <= registered_valid;
            result <= combinational_result;
            if (input_valid) begin
                for (lane_index=0; lane_index<LANES; lane_index=lane_index+1) begin
                    a[lane_index] <= a_packed[16*lane_index+:16];
                    b[lane_index] <= b_packed[16*lane_index+:16];
                end
            end
        end
    end
endmodule
