module top_module(input clk, areset, load, ena, input [3:0] data, output reg [3:0] q); // 비동기 리셋과 적재·이동 제어
    always @(posedge clk or posedge areset) begin // 클록 에지와 리셋 상승을 모두 감지
        if (areset) q <= 4'd0; // 비동기 리셋이 모든 동작보다 우선
        else if (load) q <= data; // load와ena가 함께1이어도 병렬 적재 우선
        else if (ena) q <= {1'b0, q[3:1]}; // 높은 자리에0을 채우며 한 비트 오른쪽 이동
    end // 어떤 제어도 없으면 기존 값을 유지
endmodule // 4비트 우측 시프트 레지스터 끝
