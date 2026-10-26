`timescale 1ns/1ps // 클록·관측 지연의 시간 단위
module tb; // 문제별 독립 기대값을 가진 테스트벤치
    int checks = 0, vectors = 0; // 실행한 비교와 입력 벡터 수
    logic [31:0] in; // 바이트 순서를 바꿀 입력
    wire [31:0] out; // 변환 출력 관측
    logic [31:0] sequence_value = 32'h12345678; // 재현 가능한 비트 패턴 생성 상태
    top_module dut(.*); // 같은 이름의 입력·출력 연결

    task automatic verify(input logic condition, input string message); // X도 실패로 처리할 공통 검사
        checks++; // 실제 비교 횟수 누적
        if (condition !== 1'b1) $fatal(1, "%s vector=%0d %s", "vector2", vectors, message); // 첫 불일치에서 실패 종료
    endtask // 공통 검사 끝
    task automatic probe(input logic [31:0] value); // 한32비트 값을 독립 산술로 해석
        logic [31:0] expected; // 네 바이트를 역순으로 누적한 기대값
        in = value; expected = 0; // 입력과 산술 누적값 준비
        for (int index = 0; index < 4; index++) expected = expected * 256 + ((value >> (8 * index)) & 255); // 낮은 바이트부터256진수 숫자로 다시 조립
        #1; vectors++; verify(out === expected, "byte order"); // 배선식과 다른 반복 산술 기준으로 대조
    endtask // 바이트 한 벡터 검사 끝
    initial begin // 재현 가능한 입력과 경계 검사
        probe(32'h00000000); probe(32'hffffffff); probe(32'h12345678); // 모든0·모든1·서로 다른 바이트
        for (int bit_index = 0; bit_index < 32; bit_index++) probe(32'd1 << bit_index); // 각 배선의 원-핫 위치 확인
        for (int i = 0; i < 1000; i++) begin // 고정 시드의 추가 입력
            sequence_value ^= sequence_value << 13; // 상위 비트로 섞기
            sequence_value ^= sequence_value >> 17; // 하위 비트로 섞기
            sequence_value ^= sequence_value << 5; // 32비트 안의 다음 패턴 완성
            probe(sequence_value); // 바이트 산술 기준과 비교
        end // 추가 패턴 끝
        $display("PASS id=vector2 checks=%0d vectors=%0d", checks, vectors); // 실제 검사 수 출력
        $finish; // 정상 시뮬레이션 종료
    end // 입력 자극 끝
    initial begin #10000000; $fatal(1, "watchdog"); end // 종료되지 않는 시험의 시간 상한
endmodule // 자체 검사 모듈 끝
