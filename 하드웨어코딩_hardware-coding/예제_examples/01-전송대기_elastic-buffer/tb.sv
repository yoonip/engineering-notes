`timescale 1ns/1ps // 클록과 관측 지연의 시간 단위
module tb_elastic_buffer; // 자체 검사 테스트벤치
    parameter bit BUG_DROP_ON_STALL = 1'b0; // 정상 실행과 결함 실행의 선택
    logic clk = 1'b0, rst = 1'b1, in_valid = 1'b0, out_ready = 1'b0; // 시작 전 제어 신호
    logic [7:0] in_data = 8'd0, out_data; // 입력과 관측 출력 값
    logic in_ready, out_valid; // DUT가 내보내는 핸드셰이크
    byte unsigned expected[2048]; // 수락 순서만 기록하는 독립 기대값 큐
    int head = 0, tail = 0, checks = 0, cycles = 0; // 큐 경계와 실제 검사 수
    int accepted = 0, consumed = 0, cancelled = 0, stalls = 0; // 전송·취소·정체 관측 수
    int replaces = 0; // 같은 에지의 소비와 새 입력 수락 수
    elastic_buffer #(.BUG_DROP_ON_STALL(BUG_DROP_ON_STALL)) dut (.*); // 같은 포트 이름으로 DUT 연결
    always #5 clk = ~clk; // 주기10ns의 단일 클록
    task automatic verify(input logic condition, input string message); // X도 실패시키는 검사 공통 함수
        checks++; // 실행된 검사를 실제로 집계
        if (condition !== 1'b1) $fatal(1, "ELASTIC cycle=%0d %s", cycles, message); // 불일치 즉시 실패 종료
    endtask // 검사 함수 끝
    task automatic step(input bit reset_value, input bit valid_value, input byte unsigned data_value, input bit ready_value); // 한 에지의 입력 자극
        @(negedge clk); // DUT의 수락 에지와 분리해 구동
        rst = reset_value; in_valid = valid_value; in_data = data_value; out_ready = ready_value; // 이번 입력 배치
        #1; // 조합 출력이 안정될 시간 확보
        cycles++; // 이번 검사 에지 번호
        verify(in_ready === (!rst && (head == tail || out_ready)), "input readiness"); // 큐의 빈자리와 소비 여부로 준비 신호 검사
        verify(out_valid === (!rst && head != tail), "output validity before edge"); // 기존 미소비 항목이 있는지 검사
        if (out_valid) verify(out_data === expected[head], "ordered data before edge"); // 포인터 상태 대신 수락된 값과 비교
        if (out_valid && !out_ready) stalls++; // 출력 정체를 실제 관측
        if (out_valid && out_ready && in_valid && in_ready) replaces++; // 동시 소비·교체를 실제 관측
        @(posedge clk); // 현재 입력을 수락하는 상승 에지
        if (rst) begin // 리셋이면 남은 기대 항목 취소
            cancelled += tail - head; // 취소된 항목 수 기록
            head = tail; // 독립 큐 비우기
        end else begin // 정상 핸드셰이크 처리
            if (out_valid && out_ready) begin head++; consumed++; end // 이전 출력부터 소비
            if (in_valid && in_ready) begin expected[tail++] = in_data; accepted++; end // 수락된 새 입력만 큐에 추가
        end // 기대 전송 갱신 끝
        #1; // nonblocking 갱신 뒤 상태 관측
        verify(tail - head <= 1, "queue capacity"); // 한 칸 버퍼의 점유 상한
        verify(out_valid === (!rst && head != tail), "output validity after edge"); // 갱신 뒤 유효 상태 검사
        if (out_valid) verify(out_data === expected[head], "ordered data after edge"); // 새 출력이나 유지된 출력의 값 검사
    endtask // 한 에지 검사 끝
    initial begin // 재현 가능한 직접 자극과 규칙 자극
        step(1, 1, 8'hff, 1); // 리셋 중 입력을 수락하지 않는 경계
        step(0, 1, 8'h11, 0); // 빈 버퍼는 소비자가 멈춰도 한 항목 수락
        step(0, 0, 8'h11, 0); // 저장한11을 정체 중 유지
        step(0, 1, 8'h22, 0); // 준비가 없을 때 두 번째 항목은 수락하지 않기
        step(0, 1, 8'h22, 1); // 기존11 소비와22 수락을 같은 에지에 실행
        step(0, 0, 8'h00, 1); // 마지막22를 소비해 비우기
        step(0, 1, 8'h33, 0); // 취소 시험용 항목 저장
        step(1, 1, 8'h44, 1); // 미소비33을 취소하고44도 수락하지 않기
        for (int i = 0; i < 64; i++) begin // 고정 규칙으로 생산·소비 속도 조합 변경
            step(i == 31, (i % 4) != 0, i[7:0], (i % 5) >= 2); // 같은 입력에서 재현 가능한 정체·리셋
        end // 규칙 자극 끝
        step(0, 0, 8'h00, 1); // 남은 항목을 모두 소비
        step(0, 0, 8'h00, 1); // 빈 출력에서 가짜 항목이 없는지 확인
        verify(head == tail, "final queue empty"); // 마지막 기대 항목 누락 검사
        verify(accepted == consumed + cancelled, "transaction accounting"); // 수락·소비·취소의 개수 보존
        verify(stalls > 0 && replaces > 0 && cancelled > 0, "required scenarios reached"); // 중요한 경계를 실제로 지났는지 확인
        $display("PASS checks=%0d cycles=%0d accepted=%0d consumed=%0d cancelled=%0d stalls=%0d replacements=%0d", checks, cycles, accepted, consumed, cancelled, stalls, replaces); // 실제 관측 수 출력
        $finish; // 정상 시뮬레이션 종료
    end // 직접 자극 프로세스 끝
    initial begin #100000; $fatal(1, "ELASTIC watchdog"); end // 멈춘 테스트를 무한 대기로 처리하지 않기
endmodule // 전송 버퍼 테스트벤치 끝
