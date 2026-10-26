module top_module(input clk, input [7:0] in, output reg [7:0] pedge); // 각 입력 비트의 등록된 상승 변화 표시
    reg [7:0] previous; // 직전 상승 에지에 관측한 입력
    always @(posedge clk) begin // 같은 에지의 이전값과 현재 입력을 비교
        previous <= in; // 다음 비교를 위해 현재 입력 보관
        pedge <= in & ~previous; // 이전0·현재1인 비트만 출력 레지스터에 표시
    end // 두 nonblocking 대입 모두 에지 직전 previous를 사용
endmodule // 8비트 상승 변화 검출기 끝
