`timescale 1ns/1ps // 클록·관측 지연의 시간 단위
module tb; // 문제별 독립 기대값을 가진 테스트벤치
    int checks = 0, vectors = 0; // 실행한 비교와 입력 벡터 수
    logic [99:0] a, b; // 선택할 두 입력 벡터
    logic sel; // 선택 입력
    wire [99:0] out; // 100비트 출력
    top_module dut(.*); // DUT 포트 연결

    task automatic verify(input logic condition, input string message); // X도 실패로 처리할 공통 검사
        checks++; // 실제 비교 횟수 누적
        if (condition !== 1'b1) $fatal(1, "%s vector=%0d %s", "mux2to1v", vectors, message); // 첫 불일치에서 실패 종료
    endtask // 공통 검사 끝
    task automatic probe(input logic [99:0] first, second, input bit choice); // 벡터 선택 한 건 검사
        logic [99:0] expected; // 비트별 독립 선택 기대값
        a = first; b = second; sel = choice; // 세 입력을 함께 구동
        for (int index = 0; index < 100; index++) begin // 각 출력 비트의 기준 계산
            if (choice == 0) expected[index] = first[index]; // sel0의 개별 비트 기준
            else expected[index] = second[index]; // sel1의 개별 비트 기준
        end // 100비트 기준 완성
        #1; vectors++; verify(out === expected, "whole100bit selection"); // 전체 벡터 폭과 선택 방향 대조
    endtask // 선택 한 건 검사 끝
    initial begin // 재현 가능한 입력과 경계 검사
        for (int first = 0; first < 2; first++) begin // 모든0·모든1의 첫 후보
            for (int second = 0; second < 2; second++) begin // 모든0·모든1의 둘째 후보
                probe({100{first[0]}}, {100{second[0]}}, 0); // 첫 선택 분기 검사
                probe({100{first[0]}}, {100{second[0]}}, 1); // 둘째 선택 분기 검사
            end // 둘째 후보 끝
        end // 극단 패턴 끝
        for (int index = 0; index < 100; index++) begin // 모든 입력 배선 위치
            probe(100'd1 << index, 0, 0); probe(100'd1 << index, 0, 1); // a만 해당 위치가1인 경우
            probe(0, 100'd1 << index, 0); probe(0, 100'd1 << index, 1); // b만 해당 위치가1인 경우
            probe(100'd1 << index, 100'd1 << index, 0); probe(100'd1 << index, 100'd1 << index, 1); // 두 후보의 같은 위치가1인 경우
        end // 모든100개 위치 끝
        probe({50{2'b10}}, {50{2'b01}}, 0); probe({50{2'b10}}, {50{2'b01}}, 1); // 교대 비트와 반대 선택 확인
        $display("PASS id=mux2to1v checks=%0d vectors=%0d", checks, vectors); // 실제 검사 수 출력
        $finish; // 정상 시뮬레이션 종료
    end // 입력 자극 끝
    initial begin #10000000; $fatal(1, "watchdog"); end // 종료되지 않는 시험의 시간 상한
endmodule // 자체 검사 모듈 끝
