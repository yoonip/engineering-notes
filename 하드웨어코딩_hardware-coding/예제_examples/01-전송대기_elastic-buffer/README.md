# 한 칸 버퍼의 정체·교체·리셋

[하드웨어 코딩 목차](../../README.md)

이 예제는 직접 구성한8비트·한 칸 전송 버퍼입니다. 입력과 출력의 `valid && ready`가 상승 에지에서 참일 때만 해당 항목을 수락하거나 소비합니다. 한 항목을 보관하므로 소비자가 잠시 멈춰도 생산자가 보낸 값 하나를 보존할 수 있습니다. 전체 AXI 버스나 특정 공급사의 register slice를 구현한 것은 아닙니다.

## 문제와 인터페이스

`in_valid`는 보낼 항목의 존재, `in_ready`는 이번 에지의 수락 가능 여부입니다. `out_valid`는 저장 항목의 존재, `out_ready`는 소비 가능 여부입니다. 생산자는 유효한 항목이 수락될 때까지 그 값과 valid를 유지해야 합니다. 테스트벤치의 규칙 자극 중에는 수락되지 않은 입력을 바꾸는 경우도 있으며, 그 항목의 전달을 기대하지는 않습니다. 생산자 프로토콜 준수 검사와 이 버퍼의 저장 기능 검사는 구분합니다.

`rst`는 active-high이며 저장 상태의 제거는 상승 에지에서 일어납니다. 조합 출력은 rst가1인 동안 valid와 ready를0으로 가립니다. 미소비 항목은 리셋에서 취소하며, 그 에지의 새 입력도 받지 않습니다. `out_data`는 out_valid가1일 때만 의미가 있습니다.

입력 수락 직후 레지스터의 값이 출력에 보이며 최초 소비는 다음 상승 에지부터 가능합니다. 빈 버퍼를 바로 통과하는 조합 bypass는 없습니다. 가득 찼더라도 기존 출력을 이번 에지에 소비한다면 같은 에지에 새 입력으로 교체할 수 있습니다.

## 준비 신호의 원리

`!full || out_ready`는 빈자리가 있거나 현재 항목이 빠져나갈 조건입니다. 이때 `full <= in_valid`로 다음 점유 상태를 정합니다. 가득 찬 상태에서 out_ready가0이면 순차 블록이 저장값과 full에 할당하지 않으므로 이전 값을 유지합니다. Arm의 [AXI 채널 핸드셰이크 규칙, IHI0022H A3.2](https://developer.arm.com/-/media/Arm%20Developer%20Community/PDF/IHI0022H_amba_axi_protocol_spec.pdf)와 AMD의 [WDATA 정체 중 안정성 검사, PG101](https://docs.amd.com/r/en-US/pg101-axi-protocol-checker/AXI-Protocol-Checks-and-Descriptions)는 전송 수락과 대기 중 값 유지의 근거입니다. 이 예제의 리셋·저장 용량·지연은 별도로 정한 교육 계약입니다.

## 입력부터 출력까지의 흐름

| 검사 에지 | 입력·소비 조건 | 에지 뒤 상태 |
| --- | --- | --- |
| 1 | reset=1, 입력ff | 입력을 받지 않으며 비어 있습니다. |
| 2 | 입력11, 소비 준비0 | 빈 한 칸에11을 저장합니다. |
| 3 | 새 유효 입력 없음, 소비 준비0 |11과 out_valid를 유지합니다. |
| 4 | 입력22, 소비 준비0 | in_ready가0이므로22를 받지 않습니다. |
| 5 | 입력22, 소비 준비1 |11을 소비하고22를 저장합니다. |
| 6 | 새 유효 입력 없음, 소비 준비1 |22를 소비하고 비웁니다. |
| 7~8 |33 저장 뒤 reset=1 |33을 취소하며44도 받지 않습니다. |

## 독립 검사와 결함 대조

테스트벤치는 DUT의 내부 full이나 stored를 읽지 않습니다. 수락된 입력값만 큐에 넣고 소비된 출력과 비교합니다. 하강 에지에 입력을 바꾸고 다음 상승 에지 직전의 핸드셰이크를 처리한 뒤 `#1`에서 nonblocking 갱신 결과를 확인합니다. 수락한 수는 소비한 수와 리셋으로 취소한 수의 합이어야 하며 마지막 큐도 비어야 합니다.

`BUG_DROP_ON_STALL=1`은 정체 중 저장 항목을 지우는 의도적인 결함입니다. 정상 모드의 기능이 아니며, 같은 테스트벤치가 실제로 오류를 잡는지 확인하는 음성 대조입니다. 정상 PASS와 결함의 예상 실패를 서로 다른 결과로 기록합니다.

## 응용과 한계

같은 클록 도메인의 스트리밍 연산 단계 사이에서 짧은 소비 정체를 흡수하는 기본 구조로 사용할 수 있습니다. 단 한 칸이므로 긴 정체를 저장할 수 없으며 준비 신호가 뒤에서 앞으로 조합 경로를 만듭니다. 이 구조만으로 타이밍 경로를 끊었다고 할 수 없습니다. 비동기 클록 전달, 메타안정성, FPGA 자원 사용량·STA·전력·실물 보드 시험은 이 시뮬레이션의 확인 범위에 포함하지 않습니다.

## 실행 환경과 명령

별도의 표준 입력은 없으며 tb.sv의 고정 자극으로 검사합니다. Python 기준 모델만 실행한 결과가 아니라 실제 SystemVerilog 컴파일과 VVP 실행 결과입니다. Icarus의 [-g2012·-s·-o 옵션](https://github.com/steveicarus/iverilog/blob/master/Documentation/usage/command_line_flags.rst)으로 언어·최상위 모듈·산출물을 지정하고 [VVP](https://steveicarus.github.io/iverilog/usage/vvp_flags.html)로 실행합니다. 아래 PowerShell 명령은 저장소 루트에서 시작하여 소스를 새 임시 폴더로 복사합니다. 다른 환경에서는 두 도구 경로를 해당 실행 파일로 바꾸면 됩니다.

```powershell
$source = Resolve-Path '하드웨어코딩_hardware-coding/예제_examples/01-전송대기_elastic-buffer'
$build = Join-Path ([IO.Path]::GetTempPath()) ('hardware-example-' + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $build | Out-Null
Copy-Item (Join-Path $source 'elastic_buffer.sv'), (Join-Path $source 'tb.sv') $build
Push-Location $build
& 'C:/iverilog/bin/iverilog.exe' -g2012 -gstrict-expr-width -Wall -s tb_elastic_buffer -o sim.vvp elastic_buffer.sv tb.sv
& 'C:/iverilog/bin/vvp.exe' -n sim.vvp
Pop-Location
```

정상 실행은 PASS와 실제 검사 수를 출력합니다. 실패 시 테스트벤치의 `$fatal(1,...)`이 불일치 시점과 이유를 출력하며 종료 코드는0이 아닙니다. 테스트벤치의 `#5` 클록과 `#1` 관측 지연은 시뮬레이션용이며 합성할 회로 지연을 뜻하지 않습니다.

## 실제 로컬 실행 기록

2026-10-26에 설치된 Icarus Verilog12.0 devel과 VVP로 실행했습니다. 아래 수치는 해당 소스와 자극에서 직접 출력된 값이며 새로운 환경의 실행을 대신하지 않습니다. 전체 명령·종료 코드·stdout·stderr와 소스 SHA-256은 [example.json](example.json)에 기록합니다.

| 설정 | 관측 결과 | 실제 집계 |
| --- | --- | --- |
| normal | PASS; compile=0, sim=0 | checks=413, cycles=74, accepted=36, consumed=34, cancelled=2, stalls=22, replacements=24 |
| negative_drop_on_stall | EXPECTED_FUNCTIONAL_FAILURE; compile=0, sim=1 | FATAL: tb.sv:15: ELASTIC cycle=3 output validity after edge |

음성 대조의 예상 실패는 결함이 검출되었다는 뜻이며 결함 회로가 정상 기능 검사를 통과했다는 뜻이 아닙니다. 도구 실행·컴파일 실패는 기능 실패와 별도로 확인합니다. 온라인 문제 채점은 수행하지 않았습니다.

## 줄별 문법과 회로 목적

`logic`는4상태 신호의 자료형이며 그 자체로 플립플롭을 뜻하지 않습니다. 조합 블록·연속 연결·클록 저장 중 어디에서 값을 정하는지에 따라 회로 역할이 달라집니다. `always_comb`는 현재 입력과 상태로 조합 값을 계산하고 모든 경로에 기본값을 둡니다. `always_ff`와 `<=`는 상승 에지 이전 상태를 기준으로 다음 저장값을 예약합니다. 테스트벤치의 blocking `=`는 순서대로 기대값을 계산하는 데 사용합니다. 각 실제 소스 줄의 주석에 문법의 역할과 이 회로의 목적을 함께 적었습니다.

### RTL: elastic_buffer.sv

```systemverilog
`timescale 1ns/1ps // 시뮬레이션 시간 단위와 정밀도
module elastic_buffer #( // 한 항목을 보관하는 전송 버퍼
    parameter bit BUG_DROP_ON_STALL = 1'b0 // 음성 대조에서만 켤 의도적인 정체 중 유실
) ( // 포트 목록 시작
    input logic clk, rst, // 단일 클록과 active-high 동기 상태 리셋
    input logic in_valid, // 입력 항목이 유효하다는 표시
    input logic [7:0] in_data, // 입력 항목의8비트 값
    output logic in_ready, // 이번 에지에 입력을 받을 수 있는지 표시
    output logic out_valid, // 보관한 출력 항목의 유효 표시
    output logic [7:0] out_data, // 보관한 출력 값
    input logic out_ready // 소비자가 이번 에지에 받을 수 있는지 표시
); // 포트 선언 끝
    logic full; // 한 칸의 점유 여부
    logic [7:0] stored; // 다음 소비 때까지 보존할 항목
    always_comb begin // 현재 상태와 소비 준비로 조합 출력 계산
        in_ready = !rst && (!full || out_ready); // 빈 칸이 있거나 이번 항목을 비우면 새 입력 허용
        out_valid = !rst && full; // 리셋 중에는 이전 항목을 전송하지 않기
        out_data = stored; // 유효할 때만 의미가 있는 저장 값 연결
    end // 모든 조합 출력을 항상 할당해 래치 방지
    always_ff @(posedge clk) begin // 상승 에지에서만 저장 상태 변경
        if (rst) begin // 리셋이 입력·출력 전송보다 우선
            full <= 1'b0; // 보관 중인 항목 취소
            stored <= 8'd0; // 리셋 뒤 관측할 값을 정해두기
        end else if (BUG_DROP_ON_STALL && full && !out_ready) begin // 잘못된 정체 처리의 음성 대조
            full <= 1'b0; // 의도적으로 미소비 항목을 버리기
        end else if (in_ready) begin // 칸을 채우거나 비울 수 있는 에지
            full <= in_valid; // 새 입력이 있으면 점유하고 없으면 비우기
            if (in_valid) stored <= in_data; // 수락한 항목만 저장 값으로 반영
        end // 정체 중에는 할당 없이 이전 값 유지
    end // 순차 상태 갱신 끝
endmodule // 전송 대기 버퍼 끝
```

### 자체 검사: tb.sv

```systemverilog
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
```

## 근거와 직접 구성한 부분

- [Arm AXI IHI0022H, A3.2 handshake](https://developer.arm.com/-/media/Arm%20Developer%20Community/PDF/IHI0022H_amba_axi_protocol_spec.pdf)
- [AMD PG101 stable WDATA check](https://docs.amd.com/r/en-US/pg101-axi-protocol-checker/AXI-Protocol-Checks-and-Descriptions)
- [Icarus command-line flags](https://github.com/steveicarus/iverilog/blob/master/Documentation/usage/command_line_flags.rst)

회로·테스트 입력·기대값 비교기·음성 대조는 이 저장소에서 직접 구성했습니다. 링크한 공식 문서는 언어·도구·인터페이스 규칙의 근거이며 이 예제의 시험 결과를 보고한 자료는 아닙니다. 문서 열람 기준일은2026-10-26입니다.
