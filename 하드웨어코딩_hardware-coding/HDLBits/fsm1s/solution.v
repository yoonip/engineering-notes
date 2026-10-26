module top_module(input clk, reset, in, output out); // 두 상태 Moore 기계의 입력과 상태 출력
    localparam A = 1'b0, B = 1'b1; // 출력0의A와 출력1의B를 한 비트로 구분
    reg state; // 현재 상태를 저장할 플립플롭
    always @(posedge clk) begin // 동기 리셋과 상태 전이를 상승 에지에서 처리
        if (reset) state <= B; // 공식 명세의 리셋 상태는B
        else if (!in) state <= ~state; // 입력0이면A와B 사이를 이동
    end // 입력1이면 할당 없이 현재 상태 유지
    assign out = (state == B); // 현재 상태가B인 동안만 출력1
endmodule // 동기 리셋 두 상태 기계 끝
