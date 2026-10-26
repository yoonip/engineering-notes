# 8비트 입력의 비트 순서 반전

[하드웨어 코딩 목차](../../README.md) · [공식 문제](https://hdlbits.01xz.net/wiki/vectorr)

입력의0번 비트를 출력의7번에 보내며 여덟 위치를 역순으로 연결합니다. [HDLBits vectorr](https://hdlbits.01xz.net/wiki/vectorr)의 문제 본문과 모듈 선언을 기준으로 직접 구성한 풀이입니다. 공식 문제는 회로 명세의 출처이며 이 문서의 로컬 검사 결과를 보고한 자료는 아닙니다.

## 입출력과 회로 원리

입력 in[7:0], 출력 out[7:0]의 조합 회로입니다.

출력 out[7-i]는 입력 in[i]와 같습니다. 연결 연산자의 첫 원소를 in[0]으로 적으면 그 비트가 가장 높은 출력 자리에 놓입니다. 각 원소는 원래0이나1을 유지합니다.

## 입력부터 결과까지의 흐름

아래는 기능을 설명하기 위해 직접 구성한 입력·관측 흐름입니다. 조합 회로의 행은 서로 다른 입력 예이며, 순차 회로의 행은 해당 에지 또는 명시한 이전 상태를 기준으로 읽습니다.

| 단계·관측 | 입력·조건 | 기대 결과 |
| --- | --- | --- |
| 입력01 | 00000001 | 10000000=80 |
| 입력80 | 10000000 | 00000001=01 |
| 입력D2 | 11010010 | 01001011=4B |
| 입력81 | 10000001 | 10000001=81 |

## 실수와 정당성 조건

in[0:7]처럼 선언과 반대 방향의 부분 선택으로 순서를 바꾸려고 하면 허용되지 않는 범위가 됩니다. 각 비트나 올바른 조각을 연결해야 합니다.

비트의 위치를 바꾸는 것이며0을1로 바꾸는 논리 부정이 아닙니다. 조합 배선의 기능 검사이며 지연이나 보드 신호 품질은 측정하지 않습니다.

## 하드웨어에서의 의미

직렬 데이터의 비트 순서와 병렬 표현을 맞추는 배선의 기본입니다. LSB 우선과 MSB 우선을 구분할 때 도움이 되지만 실제 직렬 전송에는 별도의 시간 제어도 필요합니다.

## 독립 로컬 검사

입력을 정수로 보고2로 나눈 나머지를 차례로 꺼내 기대값에 붙입니다. 직접 연결식 대신 산술 기준을 사용합니다.

8비트의 모든256개 이진 입력을 검사합니다.

2026-10-26에 실제 Icarus Verilog12.0 devel로 컴파일하고 VVP로 실행했습니다. compile 종료 코드는0, simulation 종료 코드는0입니다. 실제 집계는 비교256회·입력 벡터 또는 샘플256개입니다.

```text
PASS id=vectorr checks=256 vectors=256
```

이 집계는 로컬 테스트벤치의 범위이며 온라인 문제 채점과 구분합니다. 합성·STA·formal 증명·실물 보드 시험의 완료를 뜻하지 않습니다. 각 소스의 SHA-256, 실제 명령·종료 코드·표준 출력과 오류는 [problem.json](problem.json)에 기록합니다.

컴파일에는 RTL 모듈의 시간 단위가 명시되지 않았다는 Icarus 경고가 있습니다. RTL에는 `#` 지연이 없고 테스트벤치에는 `timescale 1ns/1ps`를 지정했습니다. 경고 원문을 보존하며 이를 컴파일 실패나 무경고 결과로 바꾸어 적지 않습니다.

## 실행 명령

외부 표준 입력은 없으며 tb.sv가 고정·전수 입력을 생성합니다. 다음 PowerShell 명령은 저장소 루트에서 새 임시 폴더로 소스를 복사해 실행합니다. Icarus가 다른 위치에 있으면 두 실행 파일 경로를 변경합니다.

```powershell
$source = Resolve-Path '하드웨어코딩_hardware-coding/HDLBits/vectorr'
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
module top_module(input [7:0] in, output [7:0] out); // 8비트 입력과 비트 순서를 바꾼 출력
    assign out = {in[0], in[1], in[2], in[3], in[4], in[5], in[6], in[7]}; // 낮은 입력 비트부터 높은 출력 자리에 연결
endmodule // 비트 순서 반전 회로 끝
```

### tb.sv

```systemverilog
`timescale 1ns/1ps // 클록·관측 지연의 시간 단위
module tb; // 문제별 독립 기대값을 가진 테스트벤치
    int checks = 0, vectors = 0; // 실행한 비교와 입력 벡터 수
    logic [7:0] in; // 뒤집을8비트 입력
    wire [7:0] out; // 비트 반전 출력
    top_module dut(.*); // DUT 포트 연결

    task automatic verify(input logic condition, input string message); // X도 실패로 처리할 공통 검사
        checks++; // 실제 비교 횟수 누적
        if (condition !== 1'b1) $fatal(1, "%s vector=%0d %s", "vectorr", vectors, message); // 첫 불일치에서 실패 종료
    endtask // 공통 검사 끝
    initial begin // 재현 가능한 입력과 경계 검사
        for (int value = 0; value < 256; value++) begin // 8비트의 모든 이진 입력
            int remaining, expected; // 나눗셈으로 읽을 입력과 누적 반전값
            remaining = value; expected = 0; in = value[7:0]; // 현재 벡터 준비
            for (int index = 0; index < 8; index++) begin // 낮은 비트부터 반복 추출
                expected = expected * 2 + remaining % 2; // 꺼낸 비트를 반전값의 뒤에 붙이기
                remaining /= 2; // 사용한 원래 낮은 비트 제거
            end // 독립적인 정수 반전 계산 끝
            #1; vectors++; verify(out === expected[7:0], "all bit positions"); // 전체 입력256개 대조
        end // 모든8비트 입력 끝
        $display("PASS id=vectorr checks=%0d vectors=%0d", checks, vectors); // 실제 검사 수 출력
        $finish; // 정상 시뮬레이션 종료
    end // 입력 자극 끝
    initial begin #10000000; $fatal(1, "watchdog"); end // 종료되지 않는 시험의 시간 상한
endmodule // 자체 검사 모듈 끝
```

## 근거

- [HDLBits vectorr 문제·입출력 명세](https://hdlbits.01xz.net/wiki/vectorr)
- [Icarus Verilog의 언어·최상위 모듈·출력 옵션](https://github.com/steveicarus/iverilog/blob/master/Documentation/usage/command_line_flags.rst)

공식 문제의 열람 기준일은2026-10-26입니다.

## 사이트 채점

2026-10-26에 이 폴더의 solution.v를 HDLBits에 직접 제출하여 Success!를 확인했습니다. [채점 화면과 제출 소스 해시](../확인기록_online-grading.md)를 로컬 검사와 별도로 기록합니다.
