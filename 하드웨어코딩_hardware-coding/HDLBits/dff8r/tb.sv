`timescale 1ns/1ps // 클록·관측 지연의 시간 단위
module tb; // 문제별 독립 기대값을 가진 테스트벤치
    int checks = 0, vectors = 0; // 실행한 비교와 입력 벡터 수
    logic clk = 0; // 시작 클록 값
    always #5 clk = ~clk; // 주기10ns의 시뮬레이션 클록
    logic reset = 1; // 시작 동기 리셋
    logic [7:0] d = 0; // 저장할 데이터
    wire [7:0] q; // 관측한 레지스터 출력
    bit initialized = 0; // 초기 X를 상태 유지 검사와 구분
    top_module dut(.*); // 클록·리셋·데이터 연결

    task automatic verify(input logic condition, input string message); // X도 실패로 처리할 공통 검사
        checks++; // 실제 비교 횟수 누적
        if (condition !== 1'b1) $fatal(1, "%s vector=%0d %s", "dff8r", vectors, message); // 첫 불일치에서 실패 종료
    endtask // 공통 검사 끝
    task automatic sample(input bit reset_value, input logic [7:0] value); // 한 상승 에지의 동기 저장 검사
        logic [7:0] held, expected; // 에지 전 보존값과 에지 뒤 기대값
        @(negedge clk); held = q; reset = reset_value; d = value; // 상승 에지 중간에 입력과 리셋 변경
        #1; if (initialized) verify(q === held, "no asynchronous reset or data change"); // 클록 전에는 출력이 바뀌지 않아야 함
        expected = reset_value ? 8'd0 : value; // 입력 선택을 산술 상태와 분리
        @(posedge clk); #1; vectors++; // 실제 저장 에지 뒤 관측
        verify(q === expected, "synchronous register value"); // 데이터 또는 리셋 결과 비교
        initialized = 1; // 이후부터 에지 사이 상태도 검사
    endtask // 한 저장 에지 검사 끝
    initial begin // 재현 가능한 입력과 경계 검사
        sample(1, 8'hff); // 리셋과 입력이 함께 활성인 경우
        for (int value = 0; value < 256; value++) sample(0, value[7:0]); // 모든8비트 데이터 저장
        for (int value = 0; value < 256; value++) sample(1, value[7:0]); // 모든 데이터보다 동기 리셋이 우선
        sample(0, 8'h5a); sample(0, 8'ha5); // 리셋 해제 뒤 데이터 갱신 복구
        $display("PASS id=dff8r checks=%0d vectors=%0d", checks, vectors); // 실제 검사 수 출력
        $finish; // 정상 시뮬레이션 종료
    end // 입력 자극 끝
    initial begin #10000000; $fatal(1, "watchdog"); end // 종료되지 않는 시험의 시간 상한
endmodule // 자체 검사 모듈 끝
