`timescale 1ns/1ps // 시뮬레이션 시간 단위와 정밀도
module elastic_buffer #( // 한 항목을 보관하는 전송 버퍼
    parameter bit BUG_DROP_ON_STALL = 1'b0 // 음성 대조에서만 켤 의도적인 정체 중 유실
) ( // 포트 목록 시작
    input logic clk, rst, // 단일 클록과 active-high 동기 상태 리셋
    input logic in_valid, // 입력 항목이 유효하다는 표시
    input logic [7:0] in_data, // 입력 항목의8비트 값
    output logic in_ready, // 이번 에지에 입력을 받을 수 있는지 표시
    output logic out_valid, // 보관한 출력 항목의 유효 표시
    output logic [7:0] out_data, // 보관한 출력 값
    input logic out_ready // 소비자가 이번 에지에 받을 수 있는지 표시
); // 포트 선언 끝
    logic full; // 한 칸의 점유 여부
    logic [7:0] stored; // 다음 소비 때까지 보존할 항목
    always_comb begin // 현재 상태와 소비 준비로 조합 출력 계산
        in_ready = !rst && (!full || out_ready); // 빈 칸이 있거나 이번 항목을 비우면 새 입력 허용
        out_valid = !rst && full; // 리셋 중에는 이전 항목을 전송하지 않기
        out_data = stored; // 유효할 때만 의미가 있는 저장 값 연결
    end // 모든 조합 출력을 항상 할당해 래치 방지
    always_ff @(posedge clk) begin // 상승 에지에서만 저장 상태 변경
        if (rst) begin // 리셋이 입력·출력 전송보다 우선
            full <= 1'b0; // 보관 중인 항목 취소
            stored <= 8'd0; // 리셋 뒤 관측할 값을 정해두기
        end else if (BUG_DROP_ON_STALL && full && !out_ready) begin // 잘못된 정체 처리의 음성 대조
            full <= 1'b0; // 의도적으로 미소비 항목을 버리기
        end else if (in_ready) begin // 칸을 채우거나 비울 수 있는 에지
            full <= in_valid; // 새 입력이 있으면 점유하고 없으면 비우기
            if (in_valid) stored <= in_data; // 수락한 항목만 저장 값으로 반영
        end // 정체 중에는 할당 없이 이전 값 유지
    end // 순차 상태 갱신 끝
endmodule // 전송 대기 버퍼 끝
