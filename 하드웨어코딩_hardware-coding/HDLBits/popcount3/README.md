# 세 비트에서1의 개수 세기

[하드웨어 코딩 목차](../../README.md) · [공식 문제](https://hdlbits.01xz.net/wiki/popcount3)

세 입력을 각각2비트로 넓혀 더하고0~3의 개수를 두 비트로 출력합니다. [HDLBits popcount3](https://hdlbits.01xz.net/wiki/popcount3)의 문제 본문과 모듈 선언을 기준으로 직접 구성한 풀이입니다. 공식 문제는 회로 명세의 출처이며 이 문서의 로컬 검사 결과를 보고한 자료는 아닙니다.

## 입출력과 회로 원리

입력 in[2:0], 출력 out[1:0]입니다.

각 입력 비트는 정수0이나1의 기여를 갖습니다. {1'b0,in[i]}로 피연산자를2비트로 넓혀 합3까지 유지합니다. 가장 큰 결과3은 이진11이므로 출력 두 비트가 필요합니다.

## 입력부터 결과까지의 흐름

아래는 기능을 설명하기 위해 직접 구성한 입력·관측 흐름입니다. 조합 회로의 행은 서로 다른 입력 예이며, 순차 회로의 행은 해당 에지 또는 명시한 이전 상태를 기준으로 읽습니다.

| 단계·관측 | 입력·조건 | 기대 결과 |
| --- | --- | --- |
| 000 | 1이 없음 | 00=0 |
| 001 | 1 한 개 | 01=1 |
| 101 | 1 두 개 | 10=2 |
| 111 | 1 세 개 | 11=3 |

## 실수와 정당성 조건

결과 폭과 피연산자 폭을 확인하지 않으면 올림이 잘릴 수 있습니다. 이 풀이에서는 덧셈 전에 명시적으로 폭을 넓혀 의도를 드러냅니다.

입력 세 비트의 이진값만을 다루며 X가 섞인 입력의 개수를 별도로 정의하지 않습니다. 작은 개수 회로의 기능 결과를 큰 비트 집계 회로의 타이밍 결과로 일반화하지 않습니다.

## 하드웨어에서의 의미

비트 집합의 개수, 비교 결과의 집계, 다수결 판단 같은 회로의 기초입니다. 더 넓은 입력에서는 가산 트리의 깊이와 비트 폭도 고려해야 합니다.

## 독립 로컬 검사

입력 정수를2로 반복해서 나누며 낮은 비트의 나머지를 합합니다.8개 입력을 전부 비교합니다.

3비트의 모든8개 이진 입력을 검사합니다.

2026-10-26에 실제 Icarus Verilog12.0 devel로 컴파일하고 VVP로 실행했습니다. compile 종료 코드는0, simulation 종료 코드는0입니다. 실제 집계는 비교8회·입력 벡터 또는 샘플8개입니다.

```text
PASS id=popcount3 checks=8 vectors=8
```

이 집계는 로컬 테스트벤치의 범위이며 온라인 문제 채점과 구분합니다. 합성·STA·formal 증명·실물 보드 시험의 완료를 뜻하지 않습니다. 각 소스의 SHA-256, 실제 명령·종료 코드·표준 출력과 오류는 [problem.json](problem.json)에 기록합니다.

컴파일에는 RTL 모듈의 시간 단위가 명시되지 않았다는 Icarus 경고가 있습니다. RTL에는 `#` 지연이 없고 테스트벤치에는 `timescale 1ns/1ps`를 지정했습니다. 경고 원문을 보존하며 이를 컴파일 실패나 무경고 결과로 바꾸어 적지 않습니다.

## 실행 명령

외부 표준 입력은 없으며 tb.sv가 고정·전수 입력을 생성합니다. 다음 PowerShell 명령은 저장소 루트에서 새 임시 폴더로 소스를 복사해 실행합니다. Icarus가 다른 위치에 있으면 두 실행 파일 경로를 변경합니다.

```powershell
$source = Resolve-Path '하드웨어코딩_hardware-coding/HDLBits/popcount3'
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
module top_module(input [2:0] in, output [1:0] out); // 세 입력 비트와0~3을 담는 두 출력 비트
    assign out = {1'b0, in[0]} + {1'b0, in[1]} + {1'b0, in[2]}; // 각 비트를2비트로 넓혀 캐리까지 포함한 개수 합산
endmodule // 1의 개수 회로 끝
```

### tb.sv

```systemverilog
`timescale 1ns/1ps // 클록·관측 지연의 시간 단위
module tb; // 문제별 독립 기대값을 가진 테스트벤치
    int checks = 0, vectors = 0; // 실행한 비교와 입력 벡터 수
    logic [2:0] in; // 세 입력 비트
    wire [1:0] out; // 1의 개수 출력
    top_module dut(.*); // DUT 포트 연결

    task automatic verify(input logic condition, input string message); // X도 실패로 처리할 공통 검사
        checks++; // 실제 비교 횟수 누적
        if (condition !== 1'b1) $fatal(1, "%s vector=%0d %s", "popcount3", vectors, message); // 첫 불일치에서 실패 종료
    endtask // 공통 검사 끝
    initial begin // 재현 가능한 입력과 경계 검사
        for (int value = 0; value < 8; value++) begin // 세 비트의 모든 입력
            int remaining, expected; // 산술 추출 상태와 개수
            remaining = value; expected = 0; in = value[2:0]; // 현재 입력 준비
            while (remaining > 0) begin // 정수의 각 이진 자릿수 읽기
                expected += remaining % 2; // 현재 낮은 비트가1인 경우 더하기
                remaining /= 2; // 다음 자릿수로 이동
            end // 독립적인 개수 계산 끝
            #1; vectors++; verify(out === expected[1:0], "population count"); // 최대값3도 두 비트로 유지되는지 대조
        end // 전체8개 입력 끝
        $display("PASS id=popcount3 checks=%0d vectors=%0d", checks, vectors); // 실제 검사 수 출력
        $finish; // 정상 시뮬레이션 종료
    end // 입력 자극 끝
    initial begin #10000000; $fatal(1, "watchdog"); end // 종료되지 않는 시험의 시간 상한
endmodule // 자체 검사 모듈 끝
```

## 근거

- [HDLBits popcount3 문제·입출력 명세](https://hdlbits.01xz.net/wiki/popcount3)
- [Icarus Verilog의 언어·최상위 모듈·출력 옵션](https://github.com/steveicarus/iverilog/blob/master/Documentation/usage/command_line_flags.rst)

공식 문제의 열람 기준일은2026-10-26입니다.

## 사이트 채점

2026-10-26에 이 폴더의 solution.v를 HDLBits에 직접 제출하여 Success!를 확인했습니다. [채점 화면과 제출 소스 해시](../확인기록_online-grading.md)를 로컬 검사와 별도로 기록합니다.
