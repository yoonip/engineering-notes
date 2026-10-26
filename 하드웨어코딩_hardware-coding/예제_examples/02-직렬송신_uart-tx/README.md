# 8N1 직렬 송신과 비트 유지 시간

[하드웨어 코딩 목차](../../README.md)

직접 구성한 UART 송신기로 한 바이트를 start0, 데이터8개, stop1 순서로 내보냅니다. 데이터는 LSB부터 전송하고 parity는 사용하지 않습니다. idle 상태의 선은1입니다. [Microchip USART의 프레임 형식](https://onlinedocs.microchip.com/oxy/GUID-7BB81102-57F6-474D-9BFE-B2AF8EA02A1E-en-US-5/GUID-F84E04E8-3235-4E21-89A9-D1911E9B91DD.html)은 start·데이터·선택적 parity·stop의 순서를 설명합니다. [Microchip 비동기 USART 입문 자료](https://ww1.microchip.com/downloads/cn/DeviceDoc/cn_usart.pdf)는 idle high와 start low, LSB 우선 전송을 설명합니다. 여기서는 그중8N1 설정만 구현합니다.

## 요청과 시간 계약

상승 에지 직전에 rst=0,ready=1,send=1이면 data를 한 번 수락합니다. 송신 중 ready는0이며 새 send는 무시합니다. 입력 큐가 없으므로 무시된 요청을 나중에 자동 재전송하지 않습니다. 생산자는 ready가1인 에지에만 새 요청을 전달해야 합니다.

수락 에지 뒤 start가 시작됩니다. 한 비트는 정확히 CLOCKS_PER_BIT개의 클록 주기 동안 유지합니다.10번째 stop 비트가 모두 끝난 상승 에지에서 busy를0으로 바꾸고 done을 한 클록 동안1로 만듭니다. ready는 그 에지 뒤 다시1이므로 새 수락은 다음 상승 에지부터 가능합니다. 따라서 이 구현은 연속 프레임 사이에 최소 한 클록의 idle 간격을 둡니다.

허용 CLOCKS_PER_BIT는2~16이며 기본값은3입니다. 작은 값은 빠른 교육용 시뮬레이션을 위한 것입니다. 실제 전송률은 `f_clk / CLOCKS_PER_BIT`입니다. 주기10ns·기본값3에서는 비트 시간이30ns이며, 이를9600 또는115200 baud라고 부르지 않습니다. 실물 UART 속도에는 적절한 시스템 클록과 분주 비율, 양쪽 오차 허용 범위가 필요합니다.

active-high 동기 리셋은 진행 중 프레임을 즉시 다음 상승 에지에서 취소하고 tx를1로 복귀시킵니다. 취소 시 done은 발생하지 않습니다. 중간에 잘린 프레임이 상대 수신기에서 유효 바이트로 처리된다는 보장은 없습니다.

## A6 바이트의 시간 흐름

아래 상대 클록0은 요청을 수락한 에지 뒤 구간입니다. A6의 비트0~7은0,1,1,0,0,1,0,1입니다.

| 상대 클록 | 종류 | tx |
| --- | --- | --- |
|0~2 | start |0 |
|3~5 | bit0 |0 |
|6~8 | bit1 |1 |
|9~11 | bit2 |1 |
|12~14 | bit3 |0 |
|15~17 | bit4 |0 |
|18~20 | bit5 |1 |
|21~23 | bit6 |0 |
|24~26 | bit7 |1 |
|27~29 | stop |1 |
|30 | 전체 프레임 완료 |1,done=1 |

## 독립 검사와 결함 대조

테스트벤치는 DUT의 내부 frame·ticks·bit_index를 읽지 않습니다. 원래 요청 바이트와 경과 클록 수로 요구되는 직렬 값을 계산해 모든 클록 구간을 비교합니다. 비대칭 바이트 A6, 전체0,전체1,리셋 뒤3C의 네 완성 프레임을 확인합니다. 송신 중 새 요청 네 번을 넣어 원래 프레임이 바뀌지 않는지도 검사합니다.

별도55 프레임은 진행 중 리셋으로 취소합니다. 원래 프레임 길이보다 긴 시간 동안 idle·busy=0·done=0을 확인하여 늦은 완료를 놓치지 않습니다. `BUG_REVERSE_DATA=1`은 MSB 우선으로 뒤집는 의도적인 결함입니다. 정상 결과와 이 결함의 예상 실패를 따로 기록합니다.

## 하드웨어 응용과 한계

같은 클록의 제어 회로가 디버그 바이트를 직렬로 내보내는 송신 경로의 기초 구조입니다. 수신기, oversampling, clock-domain crossing, fractional divider, 송신 FIFO, 흐름 제어는 없습니다. tx는 논리 신호이므로 RS-232의 전압·극성 변환기나 USB 변환 장치를 대체하지 않습니다. ticks는 교육용 integer 레지스터이며 합성 자원 최적화는 수행하지 않았습니다. 논리 시뮬레이션 결과를 물리 타이밍·보드 통신 성공으로 해석하지 않습니다.

## 실행 환경과 명령

별도의 표준 입력은 없으며 tb.sv의 고정 자극으로 검사합니다. Python 기준 모델만 실행한 결과가 아니라 실제 SystemVerilog 컴파일과 VVP 실행 결과입니다. Icarus의 [-g2012·-s·-o 옵션](https://github.com/steveicarus/iverilog/blob/master/Documentation/usage/command_line_flags.rst)으로 언어·최상위 모듈·산출물을 지정하고 [VVP](https://steveicarus.github.io/iverilog/usage/vvp_flags.html)로 실행합니다. 아래 PowerShell 명령은 저장소 루트에서 시작하여 소스를 새 임시 폴더로 복사합니다. 다른 환경에서는 두 도구 경로를 해당 실행 파일로 바꾸면 됩니다.

```powershell
$source = Resolve-Path '하드웨어코딩_hardware-coding/예제_examples/02-직렬송신_uart-tx'
$build = Join-Path ([IO.Path]::GetTempPath()) ('hardware-example-' + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $build | Out-Null
Copy-Item (Join-Path $source 'uart_tx.sv'), (Join-Path $source 'tb.sv') $build
Push-Location $build
& 'C:/iverilog/bin/iverilog.exe' -g2012 -gstrict-expr-width -Wall -s tb_uart_tx -o sim.vvp uart_tx.sv tb.sv
& 'C:/iverilog/bin/vvp.exe' -n sim.vvp
Pop-Location
```

정상 실행은 PASS와 실제 검사 수를 출력합니다. 실패 시 테스트벤치의 `$fatal(1,...)`이 불일치 시점과 이유를 출력하며 종료 코드는0이 아닙니다. 테스트벤치의 `#5` 클록과 `#1` 관측 지연은 시뮬레이션용이며 합성할 회로 지연을 뜻하지 않습니다.

## 실제 로컬 실행 기록

2026-10-26에 설치된 Icarus Verilog12.0 devel과 VVP로 실행했습니다. 아래 수치는 해당 소스와 자극에서 직접 출력된 값이며 새로운 환경의 실행을 대신하지 않습니다. 전체 명령·종료 코드·stdout·stderr와 소스 SHA-256은 [example.json](example.json)에 기록합니다.

| 설정 | 관측 결과 | 실제 집계 |
| --- | --- | --- |
| normal_cpb2 | PASS; compile=0, sim=0 | checks=282, frames=4, serial_samples=80, ignored_requests=4, resets_in_frame=1, clocks_per_bit=2 |
| normal_cpb3 | PASS; compile=0, sim=0 | checks=412, frames=4, serial_samples=120, ignored_requests=4, resets_in_frame=1, clocks_per_bit=3 |
| normal_cpb5 | PASS; compile=0, sim=0 | checks=672, frames=4, serial_samples=200, ignored_requests=4, resets_in_frame=1, clocks_per_bit=5 |
| normal_cpb16 | PASS; compile=0, sim=0 | checks=2102, frames=4, serial_samples=640, ignored_requests=4, resets_in_frame=1, clocks_per_bit=16 |
| negative_reverse_data | EXPECTED_FUNCTIONAL_FAILURE; compile=0, sim=1 | FATAL: tb.sv:13: UART cpb=3 serial level and bit duration |

음성 대조의 예상 실패는 결함이 검출되었다는 뜻이며 결함 회로가 정상 기능 검사를 통과했다는 뜻이 아닙니다. 도구 실행·컴파일 실패는 기능 실패와 별도로 확인합니다. 온라인 문제 채점은 수행하지 않았습니다.

## 줄별 문법과 회로 목적

`logic`는4상태 신호의 자료형이며 그 자체로 플립플롭을 뜻하지 않습니다. 조합 블록·연속 연결·클록 저장 중 어디에서 값을 정하는지에 따라 회로 역할이 달라집니다. `always_comb`는 현재 입력과 상태로 조합 값을 계산하고 모든 경로에 기본값을 둡니다. `always_ff`와 `<=`는 상승 에지 이전 상태를 기준으로 다음 저장값을 예약합니다. 테스트벤치의 blocking `=`는 순서대로 기대값을 계산하는 데 사용합니다. 각 실제 소스 줄의 주석에 문법의 역할과 이 회로의 목적을 함께 적었습니다.

### RTL: uart_tx.sv

```systemverilog
`timescale 1ns/1ps // 시뮬레이션 시간 단위와 정밀도
module uart_tx #( // 한 바이트를8N1로 송신하는 회로
    parameter integer CLOCKS_PER_BIT = 3, // 데이터 비트 한 개를 유지할 클록 수
    parameter bit BUG_REVERSE_DATA = 1'b0 // 음성 대조에서만 켤 데이터 비트 순서 결함
) ( // 포트 목록 시작
    input logic clk, rst, // 단일 클록과 active-high 동기 리셋
    input logic send, // idle 상태에서 한 바이트를 요청하는 표시
    input logic [7:0] data, // 요청과 함께 수락할 바이트
    output logic ready, // 새 바이트를 수락할 수 있는지 표시
    output logic tx, // idle1·start0·LSB 우선 데이터·stop1의 직렬 선
    output logic busy, // 프레임이 진행 중이라는 표시
    output logic done // 프레임 끝에서 한 클록만 나오는 완료 표시
); // 포트 선언 끝
    logic [9:0] frame; // start·데이터8개·stop을 낮은 비트부터 저장
    logic [3:0] bit_index; // 현재 내보내는 프레임 비트0~9
    integer ticks; // 현재 비트에서 지난 클록 수
    always_comb begin // 저장 상태를 외부 신호로 해석
        ready = !rst && !busy; // 리셋이나 송신 중에는 요청 수락 금지
        tx = busy ? frame[bit_index] : 1'b1; // idle은1이고 송신 중에는 현재 비트 연결
    end // 조합 출력 계산 끝
    always_ff @(posedge clk) begin // 상승 에지에서만 프레임 진행
        if (rst) begin // 진행 중인 프레임도 리셋에서 취소
            busy <= 1'b0; // idle 상태로 복귀
            done <= 1'b0; // 취소를 완료로 보고하지 않기
            frame <= 10'h3ff; // 저장된 비트를 idle 수준으로 초기화
            bit_index <= 4'd0; // 다음 프레임은 start부터 시작
            ticks <= 0; // 비트 주기 카운터 초기화
        end else begin // 정상 송신 동작
            done <= 1'b0; // 완료 펄스의 기본값은0
            if (!busy) begin // 진행 중인 프레임이 없는 경우
                if (send) begin // ready가1인 에지의 새 바이트 수락
                    if (BUG_REVERSE_DATA) frame <= {1'b1, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], 1'b0}; // 의도적으로 MSB부터 내보내는 결함
                    else frame <= {1'b1, data, 1'b0}; // 낮은 비트에 start를 두어 LSB부터 전송
                    busy <= 1'b1; // 이번 에지 뒤 start 비트를 내보내기
                    bit_index <= 4'd0; // start 비트 위치 선택
                    ticks <= 0; // start 유지 시간을 처음부터 세기
                end // 요청이 없으면 idle 유지
            end else if (ticks == CLOCKS_PER_BIT - 1) begin // 현재 비트의 마지막 클록 경계
                ticks <= 0; // 다음 비트 주기 시작
                if (bit_index == 9) begin // stop 비트까지 온전히 보낸 경우
                    busy <= 1'b0; // 다음 에지부터 새 요청 허용
                    done <= 1'b1; // 프레임 완료를 한 클록 알리기
                end else bit_index <= bit_index + 1'b1; // 다음 직렬 비트로 이동
            end else ticks <= ticks + 1; // 같은 비트를 한 클록 더 유지
        end // 리셋 또는 정상 동작 분기 끝
    end // 순차 송신 상태 갱신 끝
endmodule // UART 송신기 끝
```

### 자체 검사: tb.sv

```systemverilog
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
```

## 근거와 직접 구성한 부분

- [Microchip USART frame formats](https://onlinedocs.microchip.com/oxy/GUID-7BB81102-57F6-474D-9BFE-B2AF8EA02A1E-en-US-5/GUID-F84E04E8-3235-4E21-89A9-D1911E9B91DD.html)
- [Microchip USART asynchronous operation, idle/start/LSB](https://ww1.microchip.com/downloads/cn/DeviceDoc/cn_usart.pdf)
- [Icarus vvp flags](https://steveicarus.github.io/iverilog/usage/vvp_flags.html)

회로·테스트 입력·기대값 비교기·음성 대조는 이 저장소에서 직접 구성했습니다. 링크한 공식 문서는 언어·도구·인터페이스 규칙의 근거이며 이 예제의 시험 결과를 보고한 자료는 아닙니다. 문서 열람 기준일은2026-10-26입니다.
