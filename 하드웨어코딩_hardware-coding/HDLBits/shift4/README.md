# 비동기 리셋과 병렬 적재를 갖는 우측 시프트

[하드웨어 코딩 목차](../../README.md) · [공식 문제](https://hdlbits.01xz.net/wiki/shift4)

비동기 리셋을 가장 먼저 처리하고 상승 에지에서는load가ena보다 우선하도록 상태를 갱신합니다. [HDLBits shift4](https://hdlbits.01xz.net/wiki/shift4)의 문제 본문과 모듈 선언을 기준으로 직접 구성한 풀이입니다. 공식 문제는 회로 명세의 출처이며 이 문서의 로컬 검사 결과를 보고한 자료는 아닙니다.

## 입출력과 회로 원리

입력 clk·areset·load·ena·data[3:0], 출력 q[3:0]입니다. areset은 비동기 active-high입니다.

posedge areset을 감지 목록에 넣어 클록 없이도0으로 만듭니다. 리셋이 아니면 load를 먼저 확인하고, 그다음 ena일 때 {1'b0,q[3:1]}를 저장합니다. 둘 다0인 에지에는 할당하지 않아 값을 유지합니다.

## 입력부터 결과까지의 흐름

아래는 기능을 설명하기 위해 직접 구성한 입력·관측 흐름입니다. 조합 회로의 행은 서로 다른 입력 예이며, 순차 회로의 행은 해당 에지 또는 명시한 이전 상태를 기준으로 읽습니다.

| 단계·관측 | 입력·조건 | 기대 결과 |
| --- | --- | --- |
| 이전q=D | load=0,ena=0 | q=D 유지 |
| 이전q=D | load=0,ena=1 | q=6; 1101→0110 |
| 이전q=D | load=1,ena=1,data=2 | q=2; 이동보다 적재 우선 |
| 아무 이전값 | areset=1 | 클록 전q=0 |
| 리셋 해제 뒤 | load=0,ena=0 | q=0 유지 |

## 실수와 정당성 조건

ena를 load보다 먼저 검사하면 둘 다1인 입력에서 적재를 놓칩니다. 리셋을 posedge clk 블록에서만 확인하면 비동기 요구를 만족하지 못합니다.

밀려난 q[0]은 보관하지 않습니다. 산술 우측 이동이나 회전 이동이 아니며 q[3]은 항상0으로 채웁니다. 비동기 리셋 해제의 물리적 recovery/removal·동기화 설계는 별도입니다.

## 하드웨어에서의 의미

병렬 입력을 받아 순서대로 비트를 내보내는 저장 구조의 기초입니다. 동시에 활성인 제어의 우선순위를 명시해야 같은 입력에서 하나의 다음 상태가 정해집니다.

## 독립 로컬 검사

이전 상태를 정수로 두고 ena일 때2로 나누어 기대값을 계산합니다. 비동기 리셋은 상승 클록 전에0이 되는지도 확인합니다.

16개 저장 상태와 load·ena의 네 조합을 교차 검사하고 각 조합에서 리셋 우선·해제 후 유지까지 확인합니다. 총257에지·514비교입니다.

2026-10-26에 실제 Icarus Verilog12.0 devel로 컴파일하고 VVP로 실행했습니다. compile 종료 코드는0, simulation 종료 코드는0입니다. 실제 집계는 비교514회·입력 벡터 또는 샘플257개입니다.

```text
PASS id=shift4 checks=514 vectors=257
```

이 집계는 로컬 테스트벤치의 범위이며 온라인 문제 채점과 구분합니다. 합성·STA·formal 증명·실물 보드 시험의 완료를 뜻하지 않습니다. 각 소스의 SHA-256, 실제 명령·종료 코드·표준 출력과 오류는 [problem.json](problem.json)에 기록합니다.

컴파일에는 RTL 모듈의 시간 단위가 명시되지 않았다는 Icarus 경고가 있습니다. RTL에는 `#` 지연이 없고 테스트벤치에는 `timescale 1ns/1ps`를 지정했습니다. 경고 원문을 보존하며 이를 컴파일 실패나 무경고 결과로 바꾸어 적지 않습니다.

## 실행 명령

외부 표준 입력은 없으며 tb.sv가 고정·전수 입력을 생성합니다. 다음 PowerShell 명령은 저장소 루트에서 새 임시 폴더로 소스를 복사해 실행합니다. Icarus가 다른 위치에 있으면 두 실행 파일 경로를 변경합니다.

```powershell
$source = Resolve-Path '하드웨어코딩_hardware-coding/HDLBits/shift4'
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
module top_module(input clk, areset, load, ena, input [3:0] data, output reg [3:0] q); // 비동기 리셋과 적재·이동 제어
    always @(posedge clk or posedge areset) begin // 클록 에지와 리셋 상승을 모두 감지
        if (areset) q <= 4'd0; // 비동기 리셋이 모든 동작보다 우선
        else if (load) q <= data; // load와ena가 함께1이어도 병렬 적재 우선
        else if (ena) q <= {1'b0, q[3:1]}; // 높은 자리에0을 채우며 한 비트 오른쪽 이동
    end // 어떤 제어도 없으면 기존 값을 유지
endmodule // 4비트 우측 시프트 레지스터 끝
```

### tb.sv

```systemverilog
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
```

## 근거

- [HDLBits shift4 문제·입출력 명세](https://hdlbits.01xz.net/wiki/shift4)
- [Icarus Verilog의 언어·최상위 모듈·출력 옵션](https://github.com/steveicarus/iverilog/blob/master/Documentation/usage/command_line_flags.rst)

공식 문제의 열람 기준일은2026-10-26입니다.

## 사이트 채점

2026-10-26에 이 폴더의 solution.v를 HDLBits에 직접 제출하여 Success!를 확인했습니다. [채점 화면과 제출 소스 해시](../확인기록_online-grading.md)를 로컬 검사와 별도로 기록합니다.
