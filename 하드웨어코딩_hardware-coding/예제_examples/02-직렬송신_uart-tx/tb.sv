`timescale 1ns/1ps // 클록과 출력 관측의 시간 단위
module tb_uart_tx; // 내부 프레임을 읽지 않는 직렬 출력 검사
    parameter integer CLOCKS_PER_BIT = 3; // 2·3·5·16클록 조건을 별도 실행
    parameter bit BUG_REVERSE_DATA = 1'b0; // 비트 순서 결함의 음성 대조 선택
    logic clk = 1'b0, rst = 1'b1, send = 1'b0; // 시작 전 제어 신호
    logic [7:0] data = 8'd0; // 요청할 바이트
    logic ready, tx, busy, done; // DUT의 관측 출력
    int checks = 0, frames = 0, serial_samples = 0, ignored_requests = 0, resets_in_frame = 0; // 실제 검사·관측 개수
    uart_tx #(.CLOCKS_PER_BIT(CLOCKS_PER_BIT), .BUG_REVERSE_DATA(BUG_REVERSE_DATA)) dut (.*); // 명세 파라미터로 DUT 연결
    always #5 clk = ~clk; // 주기10ns의 클록
    task automatic verify(input logic condition, input string message); // 알 수 없는 값도 거절하는 검사
        checks++; // 실행된 검사 집계
        if (condition !== 1'b1) $fatal(1, "UART cpb=%0d %s", CLOCKS_PER_BIT, message); // 불일치 즉시 실패 종료
    endtask // 공통 검사 끝
    task automatic send_and_check(input byte unsigned value); // 한 프레임을 외부 직렬 선에서 검사
        bit expected_bit; // 시간표가 요구하는 직렬 값
        int position; // start·데이터·stop의 외부 시간 위치
        @(negedge clk); rst = 0; send = 1; data = value; // idle에서 요청 바이트 구동
        #1; verify(ready === 1'b1, "ready before acceptance"); // 수락 가능한 상태인지 먼저 확인
        @(posedge clk); #1; // 바이트 수락과 nonblocking 갱신 대기
        for (int elapsed = 0; elapsed < 10 * CLOCKS_PER_BIT; elapsed++) begin // 전체10비트 구간의 모든 클록 검사
            if (elapsed > 0) begin @(posedge clk); #1; end // 첫 구간 이후에는 다음 클록 관측
            position = elapsed / CLOCKS_PER_BIT; // 경과 시간으로 현재 비트 종류 결정
            if (position == 0) expected_bit = 0; // 첫 비트는 start
            else if (position == 9) expected_bit = 1; // 마지막 비트는 stop
            else expected_bit = (value >> (position - 1)) & 1; // 원래 요청 바이트를 LSB부터 해석
            verify(tx === expected_bit, "serial level and bit duration"); // DUT의 카운터·frame 없이 외부 시간표와 대조
            verify(busy === 1'b1 && ready === 1'b0, "busy throughout frame"); // stop 끝까지 새 요청 차단
            verify(done === 1'b0, "no early completion"); // 10비트가 끝나기 전 완료 금지
            serial_samples++; // 실제로 비교한 직렬 구간 집계
            @(negedge clk); // 다음 상승 에지와 분리한 요청 자극
            send = (elapsed == CLOCKS_PER_BIT); data = ~value; // 송신 중 한 번 다른 바이트 요청
            if (send) ignored_requests++; // 무시되어야 할 요청 횟수 기록
        end // 프레임 유지 시간 검사 끝
        @(posedge clk); #1; // 마지막 stop 구간이 끝나는 경계
        verify(tx === 1'b1 && busy === 1'b0 && ready === 1'b1, "idle after stop"); // 전체 프레임 뒤 idle 복귀
        verify(done === 1'b1, "single completion edge"); // 정확한 끝 경계에서 완료 확인
        frames++; // 끝까지 확인한 프레임 집계
        @(negedge clk); send = 0; // 새 송신 요청 없이 대기
        @(posedge clk); #1; verify(done === 1'b0 && busy === 1'b0, "completion pulse clears"); // 완료가 한 클록뿐인지 검사
    endtask // 한 프레임 외부 검사 끝
    initial begin // 직접 구성한 바이트와 리셋 경계 자극
        repeat (2) @(posedge clk); // 시작 리셋을 두 상승 에지에 적용
        #1; verify(tx === 1'b1 && busy === 1'b0 && done === 1'b0, "initial reset"); // 초기 idle 확인
        send_and_check(8'ha6); // 비트 순서가 뒤집히면 다른 비대칭 바이트
        send_and_check(8'h00); // 데이터 비트가 모두0인 경계
        send_and_check(8'hff); // 데이터 비트가 모두1인 경계
        @(negedge clk); send = 1; data = 8'h55; // 취소 시험용 프레임 시작
        @(posedge clk); #1; verify(busy === 1'b1, "abort frame started"); // 프레임 수락 확인
        @(negedge clk); send = 0; // 시작 요청 해제
        repeat (CLOCKS_PER_BIT + 1) @(posedge clk); // start와 첫 데이터 일부가 지나도록 대기
        @(negedge clk); rst = 1; send = 1; // 진행 중 리셋과 새 요청을 함께 구동
        @(posedge clk); #1; // 리셋이 적용된 뒤 관측
        verify(tx === 1'b1 && busy === 1'b0 && done === 1'b0, "reset cancels frame"); // 취소를 정상 완료로 세지 않기
        resets_in_frame++; // 진행 중 리셋 경계 집계
        @(negedge clk); rst = 0; send = 0; // 리셋 해제 뒤 요청 없이 대기
        repeat (10 * CLOCKS_PER_BIT + 2) begin // 취소된 프레임의 원래 길이보다 오래 관측
            @(posedge clk); #1; verify(tx === 1'b1 && busy === 1'b0 && done === 1'b0, "no delayed aborted frame"); // 취소 프레임의 재등장·늦은 완료 방지
        end // 취소 후 대기 검사 끝
        send_and_check(8'h3c); // 리셋 뒤 새 프레임의 정상 복구
        verify(frames == 4 && ignored_requests == 4 && resets_in_frame == 1, "scenario accounting"); // 필수 시나리오 실행 수 확인
        $display("PASS checks=%0d frames=%0d serial_samples=%0d ignored_requests=%0d resets_in_frame=%0d clocks_per_bit=%0d", checks, frames, serial_samples, ignored_requests, resets_in_frame, CLOCKS_PER_BIT); // 실제 검사 수 출력
        $finish; // 정상 시뮬레이션 종료
    end // 직접 자극 프로세스 끝
    initial begin #1000000; $fatal(1, "UART watchdog"); end // 종료되지 않는 회귀의 시간 상한
endmodule // UART 직렬 출력 검사 끝
