`timescale 1ns/1ps // 시뮬레이션 시간 단위와 정밀도
module sequence_detector #( // 겹침을 허용하는1011 순서 검출기
    parameter bit BUG_NO_OVERLAP = 1'b0 // 음성 대조에서만 켤 접미사 유실 결함
) ( // 포트 목록 시작
    input logic clk, rst, // 단일 클록과 active-high 동기 리셋
    input logic sample_enable, // 이번 에지에 입력 비트를 소비할지 표시
    input logic bit_in, // 소비할 직렬 입력 비트
    output logic hit // 이번에 소비한 비트로1011이 완성된 표시
); // 포트 선언 끝
    typedef enum logic [1:0] {EMPTY, SEEN_1, SEEN_10, SEEN_101} state_t; // 남아 있는 최장 접미사의 네 상태
    state_t state, next_state; // 현재 상태와 다음 에지의 후보 상태
    logic next_hit; // 이번 입력이 패턴을 완성하는지 계산한 값
    always_comb begin // 현재 접미사와 새 비트의 조합 전이
        next_state = state; // 소비하지 않으면 접미사 상태 유지
        next_hit = 1'b0; // 완성한 에지에서만 검출 표시
        if (sample_enable) begin // 유효한 입력 비트가 있는 경우에만 전이
            case (state) // 지금까지의 최장 일치 접미사 구분
                EMPTY: begin // 아직 남길 접두사가 없는 상태
                    if (bit_in) next_state = SEEN_1; // 1은 새 패턴의 시작
                    else next_state = EMPTY; // 0만으로는 시작 접두사 없음
                end // 빈 접미사의 전이 끝
                SEEN_1: begin // 최근 접미사가1인 상태
                    if (bit_in) next_state = SEEN_1; // 11의 마지막1을 새 시작으로 보존
                    else next_state = SEEN_10; // 0을 붙여10까지 일치
                end // 1 접미사의 전이 끝
                SEEN_10: begin // 최근 접미사가10인 상태
                    if (bit_in) next_state = SEEN_101; // 1을 붙여101까지 일치
                    else next_state = EMPTY; // 100에는 시작 접두사 접미사가 없음
                end // 10 접미사의 전이 끝
                SEEN_101: begin // 다음1이면 전체 패턴이 완성되는 상태
                    if (bit_in) begin // 1011 완성
                        next_hit = 1'b1; // 이번 에지의 검출 표시
                        if (BUG_NO_OVERLAP) next_state = EMPTY; // 의도적으로 마지막1의 재사용을 잃는 결함
                        else next_state = SEEN_1; // 마지막1을 다음 패턴의 시작으로 보존
                    end else next_state = SEEN_10; // 1010의 마지막10을 재사용
                end // 101 접미사의 전이 끝
                default: next_state = EMPTY; // 정의되지 않은 상태의 복귀 후보
            endcase // 모든 상태의 전이 계산 끝
        end // 입력 소비 조건 끝
    end // 기본값으로 조합 출력의 래치 방지
    always_ff @(posedge clk) begin // 상승 에지에서 상태와 검출 펄스 저장
        if (rst) begin // 리셋은 입력 소비보다 우선
            state <= EMPTY; // 이전 비트의 접미사 취소
            hit <= 1'b0; // 리셋을 검출로 보고하지 않기
        end else begin // 정상 입력 진행
            state <= next_state; // 조합 전이가 정한 접미사 저장
            hit <= next_hit; // 해당 소비 에지 뒤 한 클록 검출 표시
        end // 리셋과 정상 갱신 분기 끝
    end // 순차 상태 갱신 끝
endmodule // 순서 검출기 끝
