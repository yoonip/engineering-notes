module top_module(input clk, reset, output reg [3:0] q); // 0~9를 담는 네 비트 카운터
    always @(posedge clk) begin // 상승 에지마다 한 번 상태 변경
        if (reset || q == 4'd9) q <= 4'd0; // 동기 리셋 또는9의 다음은0
        else q <= q + 4'd1; // 나머지 정상 상태는 한 단계 증가
    end // 십진 주기의 상태 갱신 끝
endmodule // 모듈로10 카운터 끝
