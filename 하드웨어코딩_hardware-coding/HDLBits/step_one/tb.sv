`timescale 1ns/1ps // 클록·관측 지연의 시간 단위
module tb; // 문제별 독립 기대값을 가진 테스트벤치
    int checks = 0, vectors = 0; // 실행한 비교와 입력 벡터 수
    wire one; // 상수 출력 관측
    top_module dut(.one(one)); // 입력 없는 DUT 연결

    task automatic verify(input logic condition, input string message); // X도 실패로 처리할 공통 검사
        checks++; // 실제 비교 횟수 누적
        if (condition !== 1'b1) $fatal(1, "%s vector=%0d %s", "step_one", vectors, message); // 첫 불일치에서 실패 종료
    endtask // 공통 검사 끝
    initial begin // 재현 가능한 입력과 경계 검사
        #1; verify(one === 1'b1, "constant at1ns"); vectors++; // 최초 안정 출력 확인
        #4; verify(one === 1'b1, "constant at5ns"); vectors++; // 시간 경과 후에도1 유지
        #20; verify(one === 1'b1, "constant at25ns"); vectors++; // 별도 상태 없이 값이 유지되는지 확인
        $display("PASS id=step_one checks=%0d vectors=%0d", checks, vectors); // 실제 검사 수 출력
        $finish; // 정상 시뮬레이션 종료
    end // 입력 자극 끝
    initial begin #10000000; $fatal(1, "watchdog"); end // 종료되지 않는 시험의 시간 상한
endmodule // 자체 검사 모듈 끝
