`timescale 1ns/1ps // 클록·관측 지연의 시간 단위
module tb; // 문제별 독립 기대값을 가진 테스트벤치
    int checks = 0, vectors = 0; // 실행한 비교와 입력 벡터 수
    logic [2:0] in; // 세 입력 비트
    wire [1:0] out; // 1의 개수 출력
    top_module dut(.*); // DUT 포트 연결

    task automatic verify(input logic condition, input string message); // X도 실패로 처리할 공통 검사
        checks++; // 실제 비교 횟수 누적
        if (condition !== 1'b1) $fatal(1, "%s vector=%0d %s", "popcount3", vectors, message); // 첫 불일치에서 실패 종료
    endtask // 공통 검사 끝
    initial begin // 재현 가능한 입력과 경계 검사
        for (int value = 0; value < 8; value++) begin // 세 비트의 모든 입력
            int remaining, expected; // 산술 추출 상태와 개수
            remaining = value; expected = 0; in = value[2:0]; // 현재 입력 준비
            while (remaining > 0) begin // 정수의 각 이진 자릿수 읽기
                expected += remaining % 2; // 현재 낮은 비트가1인 경우 더하기
                remaining /= 2; // 다음 자릿수로 이동
            end // 독립적인 개수 계산 끝
            #1; vectors++; verify(out === expected[1:0], "population count"); // 최대값3도 두 비트로 유지되는지 대조
        end // 전체8개 입력 끝
        $display("PASS id=popcount3 checks=%0d vectors=%0d", checks, vectors); // 실제 검사 수 출력
        $finish; // 정상 시뮬레이션 종료
    end // 입력 자극 끝
    initial begin #10000000; $fatal(1, "watchdog"); end // 종료되지 않는 시험의 시간 상한
endmodule // 자체 검사 모듈 끝
