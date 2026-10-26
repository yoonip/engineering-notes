`timescale 1ns/1ps // 클록·관측 지연의 시간 단위
module tb; // 문제별 독립 기대값을 가진 테스트벤치
    int checks = 0, vectors = 0; // 실행한 비교와 입력 벡터 수
    logic clk = 0; // 시작 클록 값
    always #5 clk = ~clk; // 주기10ns의 시뮬레이션 클록
    logic reset = 1; // 시작 동기 리셋
    wire [3:0] q; // 현재 십진 카운트
    int expected = 0; bit initialized = 0; // 독립 정수 나머지 기준과 초기 표시
    top_module dut(.*); // 클록과 리셋 연결

    task automatic verify(input logic condition, input string message); // X도 실패로 처리할 공통 검사
        checks++; // 실제 비교 횟수 누적
        if (condition !== 1'b1) $fatal(1, "%s vector=%0d %s", "count10", vectors, message); // 첫 불일치에서 실패 종료
    endtask // 공통 검사 끝
    task automatic sample(input bit reset_value); // 한 카운트 에지 검사
        logic [3:0] held; // 클록 전까지 보존할 값
        @(negedge clk); held = q; reset = reset_value; // 에지 중간에 리셋 구동
        #1; if (initialized) verify(q === held, "synchronous reset timing"); // 상승 에지 전에는 리셋도 출력에 영향 없음
        if (reset_value) expected = 0; // 독립 모델의 초기화
        else expected = (expected + 1) % 10; // 상태 분기 대신 정수 나머지로 다음 값 계산
        @(posedge clk); #1; vectors++; // 카운트 저장 뒤 관측
        verify(q === expected[3:0], "modulo10 sequence"); // 전체 순환과 중간 리셋 대조
        verify(q <= 9, "decimal range"); // 정상 궤적에서 잘못된10~15 상태 방지
        initialized = 1; // 이후 에지 사이 유지 검사 허용
    endtask // 한 카운트 에지 검사 끝
    initial begin // 재현 가능한 입력과 경계 검사
        sample(1); // 초기값0 확정
        repeat (35) sample(0); // 9에서0으로 세 번 이상 순환
        sample(1); // 중간 값5에서 동기 리셋
        repeat (20) sample(0); // 리셋 뒤 두 주기 재확인
        $display("PASS id=count10 checks=%0d vectors=%0d", checks, vectors); // 실제 검사 수 출력
        $finish; // 정상 시뮬레이션 종료
    end // 입력 자극 끝
    initial begin #10000000; $fatal(1, "watchdog"); end // 종료되지 않는 시험의 시간 상한
endmodule // 자체 검사 모듈 끝
