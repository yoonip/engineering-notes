# 0부터9까지 순환하는 십진 카운터

[하드웨어 코딩 목차](../../README.md) · [공식 문제](https://hdlbits.01xz.net/wiki/count10)

동기 리셋 또는 현재9인 에지에서0으로 돌아가며 나머지 정상 상태는1씩 증가합니다. [HDLBits count10](https://hdlbits.01xz.net/wiki/count10)의 문제 본문과 모듈 선언을 기준으로 직접 구성한 풀이입니다. 공식 문제는 회로 명세의 출처이며 이 문서의 로컬 검사 결과를 보고한 자료는 아닙니다.

## 입출력과 회로 원리

입력 clk·동기식 active-high reset, 출력 q[3:0]입니다.

정상 궤적은0,1,...,9,0입니다. 네 비트의 자연스러운 넘침은15에서0으로 돌아가므로9에서 직접0을 저장해야 주기가10이 됩니다. 리셋은 현재 값과 관계없이0을 선택합니다.

## 입력부터 결과까지의 흐름

아래는 기능을 설명하기 위해 직접 구성한 입력·관측 흐름입니다. 조합 회로의 행은 서로 다른 입력 예이며, 순차 회로의 행은 해당 에지 또는 명시한 이전 상태를 기준으로 읽습니다.

| 단계·관측 | 입력·조건 | 기대 결과 |
| --- | --- | --- |
| 리셋 | reset=1 | q=0 |
| 정상 증가 | 연속9에지 | q=1..9 |
| 그다음 에지 | 기존q=9 | q=0 |
| 35회 증가 뒤 | 초기0에서35mod10 | q=5 |
| 중간 리셋 | 기존q=5,reset=1 | 다음 상승 에지에q=0 |

## 실수와 정당성 조건

q의 폭만4비트로 정하면 모듈로16 카운터입니다. 비트 폭과 원하는 상태 개수는 별도로 결정해야 합니다.

리셋 뒤 도달하는 정상 상태의 기능을 검사합니다. 외부 오류로10~15 상태가 된 경우의 복구 동작은 이 문제의 명세로 추가하지 않습니다. RTL 초기값을 임의로 강제하지 않습니다.

## 하드웨어에서의 의미

10진 자리수·정해진 주기의 사건 수 계산을 이해하는 기본입니다. 실제 시간 간격은 클록 주기와 함께 정해야 하며 카운터 출력이 곧 별도 클록으로 안전하게 사용된다는 뜻은 아닙니다.

## 독립 로컬 검사

테스트벤치는 q==9 분기 대신 정수 (expected+1)%10으로 기준을 만듭니다. 에지 사이의 동기 리셋 시점과 중간 상태의 초기화도 비교합니다.

첫 리셋,35회 증가, 값5에서 중간 리셋,20회 증가의57에지·170비교입니다.

2026-10-26에 실제 Icarus Verilog12.0 devel로 컴파일하고 VVP로 실행했습니다. compile 종료 코드는0, simulation 종료 코드는0입니다. 실제 집계는 비교170회·입력 벡터 또는 샘플57개입니다.

```text
PASS id=count10 checks=170 vectors=57
```

이 집계는 로컬 테스트벤치의 범위이며 온라인 문제 채점과 구분합니다. 합성·STA·formal 증명·실물 보드 시험의 완료를 뜻하지 않습니다. 각 소스의 SHA-256, 실제 명령·종료 코드·표준 출력과 오류는 [problem.json](problem.json)에 기록합니다.

컴파일에는 RTL 모듈의 시간 단위가 명시되지 않았다는 Icarus 경고가 있습니다. RTL에는 `#` 지연이 없고 테스트벤치에는 `timescale 1ns/1ps`를 지정했습니다. 경고 원문을 보존하며 이를 컴파일 실패나 무경고 결과로 바꾸어 적지 않습니다.

## 실행 명령

외부 표준 입력은 없으며 tb.sv가 고정·전수 입력을 생성합니다. 다음 PowerShell 명령은 저장소 루트에서 새 임시 폴더로 소스를 복사해 실행합니다. Icarus가 다른 위치에 있으면 두 실행 파일 경로를 변경합니다.

```powershell
$source = Resolve-Path '하드웨어코딩_hardware-coding/HDLBits/count10'
$build = Join-Path ([IO.Path]::GetTempPath()) ('hdlbits-' + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $build | Out-Null
Copy-Item (Join-Path $source 'solution.v'), (Join-Path $source 'tb.sv') $build
Push-Location $build
& 'C:/iverilog/bin/iverilog.exe' -g2012 -gstrict-expr-width -Wall -s tb -o sim.vvp solution.v tb.sv
& 'C:/iverilog/bin/vvp.exe' -n sim.vvp
Pop-Location
```

## 풀이와 줄별 메모

연결·조건·저장 시점의 문법과 목적은 실제 실행 줄의 주석에 함께 적었습니다. solution.v는 제출 회로이고 tb.sv는 로컬 검사 전용입니다. 테스트벤치의 지연·반복 열거·검사 함수는 제출 회로에 포함하지 않습니다.

### solution.v

```verilog
module top_module(input clk, reset, output reg [3:0] q); // 0~9를 담는 네 비트 카운터
    always @(posedge clk) begin // 상승 에지마다 한 번 상태 변경
        if (reset || q == 4'd9) q <= 4'd0; // 동기 리셋 또는9의 다음은0
        else q <= q + 4'd1; // 나머지 정상 상태는 한 단계 증가
    end // 십진 주기의 상태 갱신 끝
endmodule // 모듈로10 카운터 끝
```

### tb.sv

```systemverilog
`timescale 1ns/1ps // 클록·관측 지연의 시간 단위
module tb; // 문제별 독립 기대값을 가진 테스트벤치
    int checks = 0, vectors = 0; // 실행한 비교와 입력 벡터 수
    logic clk = 0; // 시작 클록 값
    always #5 clk = ~clk; // 주기10ns의 시뮬레이션 클록
    logic reset = 1; // 시작 동기 리셋
    wire [3:0] q; // 현재 십진 카운트
    int expected = 0; bit initialized = 0; // 독립 정수 나머지 기준과 초기 표시
    top_module dut(.*); // 클록과 리셋 연결

    task automatic verify(input logic condition, input string message); // X도 실패로 처리할 공통 검사
        checks++; // 실제 비교 횟수 누적
        if (condition !== 1'b1) $fatal(1, "%s vector=%0d %s", "count10", vectors, message); // 첫 불일치에서 실패 종료
    endtask // 공통 검사 끝
    task automatic sample(input bit reset_value); // 한 카운트 에지 검사
        logic [3:0] held; // 클록 전까지 보존할 값
        @(negedge clk); held = q; reset = reset_value; // 에지 중간에 리셋 구동
        #1; if (initialized) verify(q === held, "synchronous reset timing"); // 상승 에지 전에는 리셋도 출력에 영향 없음
        if (reset_value) expected = 0; // 독립 모델의 초기화
        else expected = (expected + 1) % 10; // 상태 분기 대신 정수 나머지로 다음 값 계산
        @(posedge clk); #1; vectors++; // 카운트 저장 뒤 관측
        verify(q === expected[3:0], "modulo10 sequence"); // 전체 순환과 중간 리셋 대조
        verify(q <= 9, "decimal range"); // 정상 궤적에서 잘못된10~15 상태 방지
        initialized = 1; // 이후 에지 사이 유지 검사 허용
    endtask // 한 카운트 에지 검사 끝
    initial begin // 재현 가능한 입력과 경계 검사
        sample(1); // 초기값0 확정
        repeat (35) sample(0); // 9에서0으로 세 번 이상 순환
        sample(1); // 중간 값5에서 동기 리셋
        repeat (20) sample(0); // 리셋 뒤 두 주기 재확인
        $display("PASS id=count10 checks=%0d vectors=%0d", checks, vectors); // 실제 검사 수 출력
        $finish; // 정상 시뮬레이션 종료
    end // 입력 자극 끝
    initial begin #10000000; $fatal(1, "watchdog"); end // 종료되지 않는 시험의 시간 상한
endmodule // 자체 검사 모듈 끝
```

## 근거

- [HDLBits count10 문제·입출력 명세](https://hdlbits.01xz.net/wiki/count10)
- [Icarus Verilog의 언어·최상위 모듈·출력 옵션](https://github.com/steveicarus/iverilog/blob/master/Documentation/usage/command_line_flags.rst)

공식 문제의 열람 기준일은2026-10-26입니다.

## 사이트 채점

2026-10-26에 이 폴더의 solution.v를 HDLBits에 직접 제출하여 Success!를 확인했습니다. [채점 화면과 제출 소스 해시](../확인기록_online-grading.md)를 로컬 검사와 별도로 기록합니다.
