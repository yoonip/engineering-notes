`timescale 1ns/1ps // 클록·관측 지연의 시간 단위
module tb; // 문제별 독립 기대값을 가진 테스트벤치
    int checks = 0, vectors = 0; // 실행한 비교와 입력 벡터 수
    logic [3:0] in; // 우선순위 입력
    wire [1:0] pos; // 가장 낮은1의 위치
    top_module dut(.*); // DUT 포트 연결

    task automatic verify(input logic condition, input string message); // X도 실패로 처리할 공통 검사
        checks++; // 실제 비교 횟수 누적
        if (condition !== 1'b1) $fatal(1, "%s vector=%0d %s", "always_case2", vectors, message); // 첫 불일치에서 실패 종료
    endtask // 공통 검사 끝
    initial begin // 재현 가능한 입력과 경계 검사
        for (int value = 0; value < 16; value++) begin // 네 비트의 모든 입력
            int expected; bit found; // 선형 탐색의 위치와 발견 표시
            in = value[3:0]; expected = 0; found = 0; // 입력0의 기본 결과 준비
            for (int index = 0; index < 4; index++) begin // 낮은 인덱스부터 실제1을 찾기
                if (!found && ((value >> index) & 1)) begin // 처음 발견한1만 선택
                    expected = index; found = 1; // 높은 비트가 나중에 덮어쓰지 못하게 표시
                end // 첫1 발견 조건 끝
            end // 모든 비트 탐색 끝
            #1; vectors++; verify(pos === expected[1:0], "lowest set bit priority"); // case 묶음과 독립 탐색 비교
        end // 16개 입력 끝
        $display("PASS id=always_case2 checks=%0d vectors=%0d", checks, vectors); // 실제 검사 수 출력
        $finish; // 정상 시뮬레이션 종료
    end // 입력 자극 끝
    initial begin #10000000; $fatal(1, "watchdog"); end // 종료되지 않는 시험의 시간 상한
endmodule // 자체 검사 모듈 끝
