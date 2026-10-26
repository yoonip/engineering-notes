`timescale 1ns/1ps // 클록·관측 지연의 시간 단위
module tb; // 문제별 독립 기대값을 가진 테스트벤치
    int checks = 0, vectors = 0; // 실행한 비교와 입력 벡터 수
    logic clk = 0; // 시작 클록 값
    always #5 clk = ~clk; // 주기10ns의 시뮬레이션 클록
    logic reset = 1, in = 1; // 시작 동기 리셋과 유지 입력
    wire out; // B 상태에서1인 Moore 출력
    int zeros = 0; bit initialized = 0; // 리셋 이후0의 개수와 초기 표시
    top_module dut(.*); // 문제 인터페이스 연결

    task automatic verify(input logic condition, input string message); // X도 실패로 처리할 공통 검사
        checks++; // 실제 비교 횟수 누적
        if (condition !== 1'b1) $fatal(1, "%s vector=%0d %s", "fsm1s", vectors, message); // 첫 불일치에서 실패 종료
    endtask // 공통 검사 끝
    task automatic sample(input bit reset_value, input bit value); // 한 입력 에지의 독립 패리티 기준
        logic held; // 동기 리셋 전까지 유지할 출력
        @(negedge clk); held = out; reset = reset_value; in = value; // 상승 에지와 분리해 구동
        #1; if (initialized) verify(out === held, "synchronous Moore output"); // 입력·리셋 변화만으로 상태가 움직이지 않기
        if (reset_value) zeros = 0; // B에서 시작하므로 토글 횟수 초기화
        else if (!value) zeros++; // 입력0만 상태를 바꾸는 사건으로 집계
        @(posedge clk); #1; vectors++; // 상태 저장 뒤 출력 관측
        verify(out === ((zeros % 2) == 0), "parity of zero inputs from stateB"); // FSM 분기표 대신0의 개수 패리티로 비교
        initialized = 1; // 이후 에지 사이 상태도 검사
    endtask // 한 상태 전이 검사 끝
    initial begin // 재현 가능한 입력과 경계 검사
        sample(1, 0); sample(0, 1); sample(0, 0); sample(0, 1); // B 유지·A 전이·A 유지
        sample(1, 0); sample(0, 0); sample(0, 0); // 중간 리셋과 두 번의 토글
        for (int length = 0; length <= 8; length++) begin // 짧은 모든 이진 입력 스트림
            for (int pattern = 0; pattern < (1 << length); pattern++) begin // 해당 길이의 모든 경우
                sample(1, 1); // 매 문자열은B에서 시작
                for (int index = length - 1; index >= 0; index--) sample(0, ((pattern >> index) & 1)); // 가장 높은 자리부터 시간순 입력
            end // 해당 길이의 열거 끝
        end // 총511개 문자열 확인 끝
        $display("PASS id=fsm1s checks=%0d vectors=%0d", checks, vectors); // 실제 검사 수 출력
        $finish; // 정상 시뮬레이션 종료
    end // 입력 자극 끝
    initial begin #10000000; $fatal(1, "watchdog"); end // 종료되지 않는 시험의 시간 상한
endmodule // 자체 검사 모듈 끝
