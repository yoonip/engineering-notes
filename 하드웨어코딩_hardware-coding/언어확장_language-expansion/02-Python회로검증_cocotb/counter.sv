`timescale 1ns/1ps // 테스트와 맞출 시뮬레이션 시간 단위
module mod10_counter ( // 0부터 9까지 순환하는 enable 카운터
    input logic clk, clear, enable, // 상승 에지 클록과 우선 초기화·증가 허용
    output logic [3:0] count // 십진 상태를 담는 네 비트
); // 포트 선언 끝
    always_ff @(posedge clk) begin // 상태 변화는 상승 에지에만 반영
        if (clear) count <= 4'd0; // 증가보다 동기 초기화 우선
        else if (enable) begin // 허용한 에지에서만 한 단계 진행
            if (count == 4'd9) count <= 4'd0; // 9 다음은 0
            else count <= count + 4'd1; // 0부터 8은 1씩 증가
        end // enable이 0이면 기존 상태 유지
    end // nonblocking 순차 갱신 끝
endmodule // 직접 구성한 카운터 끝
