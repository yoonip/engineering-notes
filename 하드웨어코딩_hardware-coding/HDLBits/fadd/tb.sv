`timescale 1ns/1ps // 클록·관측 지연의 시간 단위
module tb; // 문제별 독립 기대값을 가진 테스트벤치
    int checks = 0, vectors = 0; // 실행한 비교와 입력 벡터 수
    logic a, b, cin; // 전가산기의 세 입력
    wire cout, sum; // 올림과 합 출력
    top_module dut(.*); // DUT 포트 연결

    task automatic verify(input logic condition, input string message); // X도 실패로 처리할 공통 검사
        checks++; // 실제 비교 횟수 누적
        if (condition !== 1'b1) $fatal(1, "%s vector=%0d %s", "fadd", vectors, message); // 첫 불일치에서 실패 종료
    endtask // 공통 검사 끝
    initial begin // 재현 가능한 입력과 경계 검사
        for (int pattern = 0; pattern < 8; pattern++) begin // 세 입력의 모든 조합
            int expected; // 정수로 더한0~3의 기준값
            a = pattern[0]; b = pattern[1]; cin = pattern[2]; // 각 입력 비트 배치
            expected = (pattern & 1) + ((pattern >> 1) & 1) + ((pattern >> 2) & 1); // XOR·다수결과 다른 산술 기대값
            #1; vectors++; verify({cout, sum} === expected[1:0], "sum and carry"); // 올림까지 합친 두 비트 확인
        end // 전체8개 조합 끝
        $display("PASS id=fadd checks=%0d vectors=%0d", checks, vectors); // 실제 검사 수 출력
        $finish; // 정상 시뮬레이션 종료
    end // 입력 자극 끝
    initial begin #10000000; $fatal(1, "watchdog"); end // 종료되지 않는 시험의 시간 상한
endmodule // 자체 검사 모듈 끝
