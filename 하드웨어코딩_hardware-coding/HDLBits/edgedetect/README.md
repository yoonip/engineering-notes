# 이전0·현재1을 등록 출력으로 검출

[하드웨어 코딩 목차](../../README.md) · [공식 문제](https://hdlbits.01xz.net/wiki/edgedetect)

직전 입력과 현재 입력을 비교하고0에서1로 바뀐 비트만pedge 레지스터에 저장합니다. [HDLBits edgedetect](https://hdlbits.01xz.net/wiki/edgedetect)의 문제 본문과 모듈 선언을 기준으로 직접 구성한 풀이입니다. 공식 문제는 회로 명세의 출처이며 이 문서의 로컬 검사 결과를 보고한 자료는 아닙니다.

## 입출력과 회로 원리

입력 clk·in[7:0], 출력 pedge[7:0]입니다. 리셋 포트는 없습니다.

previous와pedge를 같은 상승 에지에서 nonblocking 대입하므로 pedge 계산은 갱신 전 previous를 읽습니다. 에지k 뒤의 출력은 에지k 입력과 에지k−1 입력의0→1 관계입니다. 클록 사이의 입력 변화만으로 pedge가 즉시 바뀌지는 않습니다.

## 입력부터 결과까지의 흐름

아래는 기능을 설명하기 위해 직접 구성한 입력·관측 흐름입니다. 조합 회로의 행은 서로 다른 입력 예이며, 순차 회로의 행은 해당 에지 또는 명시한 이전 상태를 기준으로 읽습니다.

| 단계·관측 | 입력·조건 | 기대 결과 |
| --- | --- | --- |
| 기준 샘플 | in=00 | 이전 입력 이력=00 |
| 다음 상승 에지 | in=03 | pedge=03 |
| 다음 상승 에지 | in=07,이전03 | pedge=04 |
| 다음 상승 에지 | in=02,이전07 | pedge=00; 하강은 제외 |
| 다음 상승 에지 | in=0A,이전02 | pedge=08 |

## 실수와 정당성 조건

previous를 blocking 대입으로 먼저 바꾸면 같은 입력끼리 비교해 검출이 사라집니다. 출력도 레지스터에 저장해야 하며 단순 assign의 조합 변화와 구분합니다.

리셋과 initial 초기값을 추가하지 않습니다. 처음에는 previous가 알려져 있지 않으므로 일반 입력의 첫 출력 전체를 임의로0이라고 보장할 수 없습니다. 테스트는 입력0을 한 번 샘플해 이력을 정한 뒤 비교합니다. 현재 입력이0인 비트는 이전값과 관계없이 상승 표시가0입니다.

## 하드웨어에서의 의미

동일 클록에 이미 동기화된 상태 비트에서 새 사건을 한 주기로 표시하는 기본입니다. 비동기 외부 신호나 짧은 펄스는 이 회로만으로 안정적으로 수집할 수 없으므로 동기화·펄스 수락 계약이 따로 필요합니다.

## 독립 로컬 검사

테스트벤치는 외부에서 보관한 이전 입력을 비트별 if로 비교합니다. 등록 출력이 클록 사이에 유지되는지와 에지 뒤의 판정을 모두 확인합니다.

알려진0 워밍업 뒤 가능한 이전·현재8비트 쌍65,536개를 전수 검사합니다. 각 쌍을 두 실제 샘플로 넣어 총131,072샘플·262,145비교입니다.

2026-10-26에 실제 Icarus Verilog12.0 devel로 컴파일하고 VVP로 실행했습니다. compile 종료 코드는0, simulation 종료 코드는0입니다. 실제 집계는 비교262145회·입력 벡터 또는 샘플131072개입니다.

```text
PASS id=edgedetect checks=262145 vectors=131072
```

이 집계는 로컬 테스트벤치의 범위이며 온라인 문제 채점과 구분합니다. 합성·STA·formal 증명·실물 보드 시험의 완료를 뜻하지 않습니다. 각 소스의 SHA-256, 실제 명령·종료 코드·표준 출력과 오류는 [problem.json](problem.json)에 기록합니다.

컴파일에는 RTL 모듈의 시간 단위가 명시되지 않았다는 Icarus 경고가 있습니다. RTL에는 `#` 지연이 없고 테스트벤치에는 `timescale 1ns/1ps`를 지정했습니다. 경고 원문을 보존하며 이를 컴파일 실패나 무경고 결과로 바꾸어 적지 않습니다.

## 실행 명령

외부 표준 입력은 없으며 tb.sv가 고정·전수 입력을 생성합니다. 다음 PowerShell 명령은 저장소 루트에서 새 임시 폴더로 소스를 복사해 실행합니다. Icarus가 다른 위치에 있으면 두 실행 파일 경로를 변경합니다.

```powershell
$source = Resolve-Path '하드웨어코딩_hardware-coding/HDLBits/edgedetect'
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
module top_module(input clk, input [7:0] in, output reg [7:0] pedge); // 각 입력 비트의 등록된 상승 변화 표시
    reg [7:0] previous; // 직전 상승 에지에 관측한 입력
    always @(posedge clk) begin // 같은 에지의 이전값과 현재 입력을 비교
        previous <= in; // 다음 비교를 위해 현재 입력 보관
        pedge <= in & ~previous; // 이전0·현재1인 비트만 출력 레지스터에 표시
    end // 두 nonblocking 대입 모두 에지 직전 previous를 사용
endmodule // 8비트 상승 변화 검출기 끝
```

### tb.sv

```systemverilog
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
```

## 근거

- [HDLBits edgedetect 문제·입출력 명세](https://hdlbits.01xz.net/wiki/edgedetect)
- [Icarus Verilog의 언어·최상위 모듈·출력 옵션](https://github.com/steveicarus/iverilog/blob/master/Documentation/usage/command_line_flags.rst)

공식 문제의 열람 기준일은2026-10-26입니다.

## 사이트 채점

2026-10-26에 이 폴더의 solution.v를 HDLBits에 직접 제출하여 Success!를 확인했습니다. [채점 화면과 제출 소스 해시](../확인기록_online-grading.md)를 로컬 검사와 별도로 기록합니다.
