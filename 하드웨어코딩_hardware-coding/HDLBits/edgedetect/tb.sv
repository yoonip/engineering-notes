`timescale 1ns/1ps // 클록·관측 지연의 시간 단위
module tb; // 문제별 독립 기대값을 가진 테스트벤치
    int checks = 0, vectors = 0; // 실행한 비교와 입력 벡터 수
    logic clk = 0; // 시작 클록 값
    always #5 clk = ~clk; // 주기10ns의 시뮬레이션 클록
    logic [7:0] in = 0; // 첫 기준 샘플은 알려진0
    wire [7:0] pedge; // 등록된 상승 변화 출력
    logic [7:0] previous_value = 0, last_output = 0; // 외부 입력 이력과 에지 사이 출력 기준
    top_module dut(.*); // 리셋 없는 문제 인터페이스 연결

    task automatic verify(input logic condition, input string message); // X도 실패로 처리할 공통 검사
        checks++; // 실제 비교 횟수 누적
        if (condition !== 1'b1) $fatal(1, "%s vector=%0d %s", "edgedetect", vectors, message); // 첫 불일치에서 실패 종료
    endtask // 공통 검사 끝
    task automatic sample(input logic [7:0] value); // 입력 이력으로 등록 출력 검사
        logic [7:0] expected; // 비트별 변화 판정 결과
        @(negedge clk); in = value; // 클록 중간에 현재 입력 변경
        #1; verify(pedge === last_output, "registered output holds before clock"); // 조합 변화로 출력이 먼저 바뀌지 않는지 검사
        expected = 0; // 변화가 없는 비트의 기본값
        for (int index = 0; index < 8; index++) begin // 독립된8개 비트의 표 비교
            if (previous_value[index] == 0 && value[index] == 1) expected[index] = 1; // 두 샘플의0→1만 선택
        end // 입력 이력 기준 완성
        @(posedge clk); #1; vectors++; // 레지스터 갱신 이후 관측
        verify(pedge === expected, "previous0 current1"); // 현재·이전 비트 관계 대조
        previous_value = value; last_output = expected; // 다음 에지의 외부 기준 이력 갱신
    endtask // 한 입력 샘플 검사 끝
    initial begin // 재현 가능한 입력과 경계 검사
        @(posedge clk); #1; // 0을 한 번 샘플해 이전 입력 이력 확립
        verify(pedge === 8'd0, "known zero warmup"); // 현재0인 비트에는 상승 변화 없음
        for (int previous = 0; previous < 256; previous++) begin // 이전8비트의 모든 값
            for (int current = 0; current < 256; current++) begin // 현재8비트의 모든 값
                sample(previous[7:0]); // 비교할 이전 입력을 실제 클록에 저장
                sample(current[7:0]); // 65,536개 이전·현재 쌍 대조
            end // 현재 입력 값 끝
        end // 이전 입력 값 끝
        $display("PASS id=edgedetect checks=%0d vectors=%0d", checks, vectors); // 실제 검사 수 출력
        $finish; // 정상 시뮬레이션 종료
    end // 입력 자극 끝
    initial begin #10000000; $fatal(1, "watchdog"); end // 종료되지 않는 시험의 시간 상한
endmodule // 자체 검사 모듈 끝
