`timescale 1ns/1ps // 클록·관측 지연의 시간 단위
module tb; // 문제별 독립 기대값을 가진 테스트벤치
    int checks = 0, vectors = 0; // 실행한 비교와 입력 벡터 수
    logic clk = 0; // 시작 클록 값
    always #5 clk = ~clk; // 주기10ns의 시뮬레이션 클록
    logic areset = 0, load = 0, ena = 0; // 비동기 리셋과 두 동기 제어
    logic [3:0] data = 0; // 병렬 적재 값
    wire [3:0] q; // 시프트 레지스터 출력
    int expected = 0; bit initialized = 0; // 독립 정수 상태와 초기 표시
    top_module dut(.*); // 문제 인터페이스 연결

    task automatic verify(input logic condition, input string message); // X도 실패로 처리할 공통 검사
        checks++; // 실제 비교 횟수 누적
        if (condition !== 1'b1) $fatal(1, "%s vector=%0d %s", "shift4", vectors, message); // 첫 불일치에서 실패 종료
    endtask // 공통 검사 끝
    task automatic sample(input bit reset_value, input bit load_value, input bit enable_value, input logic [3:0] value); // 한 비동기·동기 제어 조합
        logic [3:0] held; // 제어 변경 전 출력
        @(negedge clk); held = q; areset = reset_value; load = load_value; ena = enable_value; data = value; // 상승 에지와 분리한 구동
        #1; // 비동기 리셋이 반영될 시간
        if (reset_value) verify(q === 4'd0, "asynchronous clear before clock"); // 클록을 기다리지 않는 리셋 확인
        else if (initialized) verify(q === held, "load and enable wait for clock"); // 적재와 시프트는 아직 실행하지 않기
        if (reset_value) expected = 0; // 독립 모델에서도 리셋 우선
        else if (load_value) expected = value; // load와ena가 동시에1이어도 적재
        else if (enable_value) expected /= 2; // 비트 연결 대신 정수 나눗셈으로 우측 이동
        @(posedge clk); #1; vectors++; // 저장 에지 뒤 결과 관측
        verify(q === expected[3:0], "reset load enable priority"); // 우선순위와 홀드 결과 대조
        initialized = 1; // 이후부터 에지 사이 상태 유지 검사
    endtask // 한 제어 조합 검사 끝
    initial begin // 재현 가능한 입력과 경계 검사
        sample(1, 1, 1, 4'hf); // 리셋·load·ena가 함께 활성인 우선순위
        for (int seed = 0; seed < 16; seed++) begin // 가능한 모든 저장 상태
            for (int load_value = 0; load_value < 2; load_value++) begin // load의 두 값
                for (int enable_value = 0; enable_value < 2; enable_value++) begin // ena의 두 값
                    sample(0, 1, 0, seed[3:0]); // 검사할 이전 상태를 먼저 적재
                    sample(0, load_value[0], enable_value[0], ~seed[3:0]); // 두 제어의 네 조합에서 다음 상태 확인
                    sample(1, load_value[0], enable_value[0], 4'hf); // 각 제어 조합보다 비동기 리셋이 우선
                    sample(0, 0, 0, 0); // 리셋 해제 뒤 활성 제어가 없으면0 유지
                end // ena 조합 끝
            end // load 조합 끝
        end // 16개 상태 대조 끝
        $display("PASS id=shift4 checks=%0d vectors=%0d", checks, vectors); // 실제 검사 수 출력
        $finish; // 정상 시뮬레이션 종료
    end // 입력 자극 끝
    initial begin #10000000; $fatal(1, "watchdog"); end // 종료되지 않는 시험의 시간 상한
endmodule // 자체 검사 모듈 끝
