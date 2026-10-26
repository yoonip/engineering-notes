`timescale 1ns/1ps // 시뮬레이션 시간 단위와 정밀도
module uart_tx #( // 한 바이트를8N1로 송신하는 회로
    parameter integer CLOCKS_PER_BIT = 3, // 데이터 비트 한 개를 유지할 클록 수
    parameter bit BUG_REVERSE_DATA = 1'b0 // 음성 대조에서만 켤 데이터 비트 순서 결함
) ( // 포트 목록 시작
    input logic clk, rst, // 단일 클록과 active-high 동기 리셋
    input logic send, // idle 상태에서 한 바이트를 요청하는 표시
    input logic [7:0] data, // 요청과 함께 수락할 바이트
    output logic ready, // 새 바이트를 수락할 수 있는지 표시
    output logic tx, // idle1·start0·LSB 우선 데이터·stop1의 직렬 선
    output logic busy, // 프레임이 진행 중이라는 표시
    output logic done // 프레임 끝에서 한 클록만 나오는 완료 표시
); // 포트 선언 끝
    logic [9:0] frame; // start·데이터8개·stop을 낮은 비트부터 저장
    logic [3:0] bit_index; // 현재 내보내는 프레임 비트0~9
    integer ticks; // 현재 비트에서 지난 클록 수
    always_comb begin // 저장 상태를 외부 신호로 해석
        ready = !rst && !busy; // 리셋이나 송신 중에는 요청 수락 금지
        tx = busy ? frame[bit_index] : 1'b1; // idle은1이고 송신 중에는 현재 비트 연결
    end // 조합 출력 계산 끝
    always_ff @(posedge clk) begin // 상승 에지에서만 프레임 진행
        if (rst) begin // 진행 중인 프레임도 리셋에서 취소
            busy <= 1'b0; // idle 상태로 복귀
            done <= 1'b0; // 취소를 완료로 보고하지 않기
            frame <= 10'h3ff; // 저장된 비트를 idle 수준으로 초기화
            bit_index <= 4'd0; // 다음 프레임은 start부터 시작
            ticks <= 0; // 비트 주기 카운터 초기화
        end else begin // 정상 송신 동작
            done <= 1'b0; // 완료 펄스의 기본값은0
            if (!busy) begin // 진행 중인 프레임이 없는 경우
                if (send) begin // ready가1인 에지의 새 바이트 수락
                    if (BUG_REVERSE_DATA) frame <= {1'b1, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], 1'b0}; // 의도적으로 MSB부터 내보내는 결함
                    else frame <= {1'b1, data, 1'b0}; // 낮은 비트에 start를 두어 LSB부터 전송
                    busy <= 1'b1; // 이번 에지 뒤 start 비트를 내보내기
                    bit_index <= 4'd0; // start 비트 위치 선택
                    ticks <= 0; // start 유지 시간을 처음부터 세기
                end // 요청이 없으면 idle 유지
            end else if (ticks == CLOCKS_PER_BIT - 1) begin // 현재 비트의 마지막 클록 경계
                ticks <= 0; // 다음 비트 주기 시작
                if (bit_index == 9) begin // stop 비트까지 온전히 보낸 경우
                    busy <= 1'b0; // 다음 에지부터 새 요청 허용
                    done <= 1'b1; // 프레임 완료를 한 클록 알리기
                end else bit_index <= bit_index + 1'b1; // 다음 직렬 비트로 이동
            end else ticks <= ticks + 1; // 같은 비트를 한 클록 더 유지
        end // 리셋 또는 정상 동작 분기 끝
    end // 순차 송신 상태 갱신 끝
endmodule // UART 송신기 끝
