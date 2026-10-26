module top_module(input clk, reset, input [7:0] d, output reg [7:0] q); // 상승 에지 저장과 동기식 high 리셋
    always @(posedge clk) begin // 클록 상승 에지에서만 출력 갱신
        if (reset) q <= 8'd0; // 리셋이 데이터 저장보다 우선
        else q <= d; // 같은 에지 직전의8비트 입력 저장
    end // nonblocking 대입의 순차 저장 끝
endmodule // 동기 리셋8비트 레지스터 끝
