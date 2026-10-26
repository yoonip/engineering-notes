`timescale 1ns/1ps // 클록과 관측 지연의 시간 단위
module tb_sequence_detector; // 최근 네 비트 기준으로 검사하는 테스트벤치
    parameter bit BUG_NO_OVERLAP = 1'b0; // 겹침 유실 결함의 음성 대조 선택
    logic clk = 0, rst = 1, sample_enable = 0, bit_in = 0, hit; // 시작 전 제어와 관측 출력
    logic [3:0] history = 0; // 유효 입력만 담는 독립 이동 창
    int seen = 0, checks = 0, samples = 0, pauses = 0, resets = 0, hits = 0, strings_checked = 0; // 실제 입력과 검사 수
    sequence_detector #(.BUG_NO_OVERLAP(BUG_NO_OVERLAP)) dut (.*); // 선택한 DUT 설정 연결
    always #5 clk = ~clk; // 주기10ns의 클록
    task automatic step(input bit reset_value, input bit enabled, input bit value); // 입력 비트 한 개 또는 대기 에지 실행
        bit expected_hit; // 내부 FSM 없이 계산할 검출 기대값
        @(negedge clk); rst = reset_value; sample_enable = enabled; bit_in = value; // 상승 에지와 분리해 입력 배치
        @(posedge clk); // 입력을 소비하는 기준 에지
        expected_hit = 0; // 비활성·리셋 에지는 검출 없음
        if (rst) begin // 리셋에서 독립 입력 이력도 지우기
            history = 0; seen = 0; resets++; // 이전 입력과 구분되는 새 스트림
        end else if (sample_enable) begin // 실제로 소비한 비트만 이동 창에 추가
            history = {history[2:0], bit_in}; // 최근 네 비트의 단순 이동
            if (seen < 4) seen++; // 네 비트가 모이기 전의 길이 기록
            expected_hit = seen == 4 && history == 4'b1011; // 완성된 네 비트와 상수 패턴 비교
            samples++; // 소비한 비트 수 집계
        end else pauses++; // 입력 대기 에지 집계
        #1; // DUT의 nonblocking 상태·출력 갱신 후 관측
        checks++; // 실제 출력 비교 수
        if (hit !== expected_hit) $fatal(1, "SEQUENCE sample=%0d history=%04b expected=%0b actual=%0b", samples, history, expected_hit, hit); // 겹침·리셋·대기 차이 검출
        if (hit) hits++; // 실제 패턴 발생 수 기록
    endtask // 한 에지 검사 끝
    initial begin // 직접 흐름과 짧은 문자열 전수 검사
        step(1, 1, 1); // reset과 유효 입력이 함께 와도 이전 이력 삭제
        step(0, 1, 1); step(0, 1, 0); step(0, 1, 1); // 첫 세 비트101
        step(0, 0, 0); step(0, 0, 1); // 중간 대기에서는 입력 값을 소비하지 않기
        step(0, 1, 1); // 첫1011 검출
        step(0, 1, 0); step(0, 1, 1); step(0, 1, 1); // 마지막1을 재사용한 두 번째1011
        if (hits != 2) $fatal(1, "SEQUENCE directed overlap count"); // 겹친 두 발생을 실제로 지났는지 확인
        step(0, 1, 1); step(0, 1, 0); // 리셋 전 접미사10 만들기
        step(1, 1, 1); step(0, 1, 1); step(0, 1, 1); // 리셋 뒤11은 이전10과 결합하지 않기
        for (int length = 0; length <= 8; length++) begin // 길이0~8의 모든 이진 문자열
            for (int pattern = 0; pattern < (1 << length); pattern++) begin // 고정 길이의 모든 값 열거
                step(1, 0, 0); // 각 문자열은 독립 리셋 상태에서 시작
                for (int index = length - 1; index >= 0; index--) begin // 왼쪽 비트부터 시간순 입력
                    step(0, 1, (pattern >> index) & 1); // 열거한 입력을 한 비트씩 소비
                end // 문자열의 모든 비트 입력 끝
                strings_checked++; // 실제로 완료한 문자열 수
            end // 현재 길이의 모든 문자열 끝
        end // 짧은 문자열 전수 검사 끝
        if (strings_checked != 511 || pauses < 2) $fatal(1, "SEQUENCE scenario accounting"); // 전수 범위와 대기 경계 확인
        $display("PASS checks=%0d samples=%0d pauses=%0d resets=%0d hits=%0d strings=%0d", checks, samples, pauses, resets, hits, strings_checked); // 실제 검사와 발생 수 출력
        $finish; // 정상 시뮬레이션 종료
    end // 직접 자극 프로세스 끝
    initial begin #1000000; $fatal(1, "SEQUENCE watchdog"); end // 종료되지 않는 시뮬레이션 제한
endmodule // 순서 검출 테스트벤치 끝
