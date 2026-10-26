`timescale 1ns/1ps // 클록·관측 지연의 시간 단위
module tb; // 문제별 독립 기대값을 가진 테스트벤치
    int checks = 0, vectors = 0; // 실행한 비교와 입력 벡터 수
    logic [7:0] in; // 뒤집을8비트 입력
    wire [7:0] out; // 비트 반전 출력
    top_module dut(.*); // DUT 포트 연결

    task automatic verify(input logic condition, input string message); // X도 실패로 처리할 공통 검사
        checks++; // 실제 비교 횟수 누적
        if (condition !== 1'b1) $fatal(1, "%s vector=%0d %s", "vectorr", vectors, message); // 첫 불일치에서 실패 종료
    endtask // 공통 검사 끝
    initial begin // 재현 가능한 입력과 경계 검사
        for (int value = 0; value < 256; value++) begin // 8비트의 모든 이진 입력
            int remaining, expected; // 나눗셈으로 읽을 입력과 누적 반전값
            remaining = value; expected = 0; in = value[7:0]; // 현재 벡터 준비
            for (int index = 0; index < 8; index++) begin // 낮은 비트부터 반복 추출
                expected = expected * 2 + remaining % 2; // 꺼낸 비트를 반전값의 뒤에 붙이기
                remaining /= 2; // 사용한 원래 낮은 비트 제거
            end // 독립적인 정수 반전 계산 끝
            #1; vectors++; verify(out === expected[7:0], "all bit positions"); // 전체 입력256개 대조
        end // 모든8비트 입력 끝
        $display("PASS id=vectorr checks=%0d vectors=%0d", checks, vectors); // 실제 검사 수 출력
        $finish; // 정상 시뮬레이션 종료
    end // 입력 자극 끝
    initial begin #10000000; $fatal(1, "watchdog"); end // 종료되지 않는 시험의 시간 상한
endmodule // 자체 검사 모듈 끝
