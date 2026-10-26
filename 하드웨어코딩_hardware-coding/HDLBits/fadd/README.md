# 올림 입력을 포함한 한 비트 전가산기

[하드웨어 코딩 목차](../../README.md) · [공식 문제](https://hdlbits.01xz.net/wiki/fadd)

세 입력의 XOR로 합 비트를 만들고 두 개 이상이1인지로 올림을 구합니다. [HDLBits fadd](https://hdlbits.01xz.net/wiki/fadd)의 문제 본문과 모듈 선언을 기준으로 직접 구성한 풀이입니다. 공식 문제는 회로 명세의 출처이며 이 문서의 로컬 검사 결과를 보고한 자료는 아닙니다.

## 입출력과 회로 원리

한 비트 입력 a·b·cin, 한 비트 출력 cout·sum입니다.

sum은1의 개수가 홀수일 때1이고 cout은 둘 이상의 입력이1일 때1입니다. 따라서 세 입력의 정수 합은 항상2*cout+sum과 같습니다. cout은 비트별AND 세 쌍의 OR로 구성합니다.

## 입력부터 결과까지의 흐름

아래는 기능을 설명하기 위해 직접 구성한 입력·관측 흐름입니다. 조합 회로의 행은 서로 다른 입력 예이며, 순차 회로의 행은 해당 에지 또는 명시한 이전 상태를 기준으로 읽습니다.

| 단계·관측 | 입력·조건 | 기대 결과 |
| --- | --- | --- |
| a,b,cin=0,0,0 | 정수 합0 | cout,sum=00 |
| a,b,cin=1,0,0 | 정수 합1 | cout,sum=01 |
| a,b,cin=1,1,0 | 정수 합2 | cout,sum=10 |
| a,b,cin=1,1,1 | 정수 합3 | cout,sum=11 |

## 실수와 정당성 조건

반가산기의 a^b만 사용하면 cin이 빠집니다. 세 입력 중 정확히 두 개가1인 경우도 올림이 발생합니다.

오버플로 플래그나 부호 있는 정수의 전체 연산은 다루지 않습니다. sum만 확인하면 올림 오류를 놓칠 수 있으므로 두 출력을 함께 검사합니다.

## 하드웨어에서의 의미

여러 비트 가산기의 한 자리 연산을 이해하는 기본 블록입니다. 올림을 연결하는 구조에 따라 넓은 가산기의 지연이 달라지며 이 한 자리 기능 시험만으로 그 성능을 결정할 수 없습니다.

## 독립 로컬 검사

세 입력을 정수로 더한 뒤 {cout,sum}의 두 비트와 비교합니다. 게이트식과 다른 산술 기준입니다.

a·b·cin의 모든8개 이진 조합을 검사합니다.

2026-10-26에 실제 Icarus Verilog12.0 devel로 컴파일하고 VVP로 실행했습니다. compile 종료 코드는0, simulation 종료 코드는0입니다. 실제 집계는 비교8회·입력 벡터 또는 샘플8개입니다.

```text
PASS id=fadd checks=8 vectors=8
```

이 집계는 로컬 테스트벤치의 범위이며 온라인 문제 채점과 구분합니다. 합성·STA·formal 증명·실물 보드 시험의 완료를 뜻하지 않습니다. 각 소스의 SHA-256, 실제 명령·종료 코드·표준 출력과 오류는 [problem.json](problem.json)에 기록합니다.

컴파일에는 RTL 모듈의 시간 단위가 명시되지 않았다는 Icarus 경고가 있습니다. RTL에는 `#` 지연이 없고 테스트벤치에는 `timescale 1ns/1ps`를 지정했습니다. 경고 원문을 보존하며 이를 컴파일 실패나 무경고 결과로 바꾸어 적지 않습니다.

## 실행 명령

외부 표준 입력은 없으며 tb.sv가 고정·전수 입력을 생성합니다. 다음 PowerShell 명령은 저장소 루트에서 새 임시 폴더로 소스를 복사해 실행합니다. Icarus가 다른 위치에 있으면 두 실행 파일 경로를 변경합니다.

```powershell
$source = Resolve-Path '하드웨어코딩_hardware-coding/HDLBits/fadd'
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
module top_module(input a, b, cin, output cout, sum); // 두 데이터 비트와 이전 자리의 올림
    assign sum = a ^ b ^ cin; // 홀수 개의1이면 합의 낮은 비트가1
    assign cout = (a & b) | (a & cin) | (b & cin); // 둘 이상이1이면 다음 자리로 올림
endmodule // 한 자리 전가산기 끝
```

### tb.sv

```systemverilog
`timescale 1ns/1ps // 클록·관측 지연의 시간 단위
module tb; // 문제별 독립 기대값을 가진 테스트벤치
    int checks = 0, vectors = 0; // 실행한 비교와 입력 벡터 수
    logic a, b, cin; // 전가산기의 세 입력
    wire cout, sum; // 올림과 합 출력
    top_module dut(.*); // DUT 포트 연결

    task automatic verify(input logic condition, input string message); // X도 실패로 처리할 공통 검사
        checks++; // 실제 비교 횟수 누적
        if (condition !== 1'b1) $fatal(1, "%s vector=%0d %s", "fadd", vectors, message); // 첫 불일치에서 실패 종료
    endtask // 공통 검사 끝
    initial begin // 재현 가능한 입력과 경계 검사
        for (int pattern = 0; pattern < 8; pattern++) begin // 세 입력의 모든 조합
            int expected; // 정수로 더한0~3의 기준값
            a = pattern[0]; b = pattern[1]; cin = pattern[2]; // 각 입력 비트 배치
            expected = (pattern & 1) + ((pattern >> 1) & 1) + ((pattern >> 2) & 1); // XOR·다수결과 다른 산술 기대값
            #1; vectors++; verify({cout, sum} === expected[1:0], "sum and carry"); // 올림까지 합친 두 비트 확인
        end // 전체8개 조합 끝
        $display("PASS id=fadd checks=%0d vectors=%0d", checks, vectors); // 실제 검사 수 출력
        $finish; // 정상 시뮬레이션 종료
    end // 입력 자극 끝
    initial begin #10000000; $fatal(1, "watchdog"); end // 종료되지 않는 시험의 시간 상한
endmodule // 자체 검사 모듈 끝
```

## 근거

- [HDLBits fadd 문제·입출력 명세](https://hdlbits.01xz.net/wiki/fadd)
- [Icarus Verilog의 언어·최상위 모듈·출력 옵션](https://github.com/steveicarus/iverilog/blob/master/Documentation/usage/command_line_flags.rst)

공식 문제의 열람 기준일은2026-10-26입니다.

## 사이트 채점

2026-10-26에 이 폴더의 solution.v를 HDLBits에 직접 제출하여 Success!를 확인했습니다. [채점 화면과 제출 소스 해시](../확인기록_online-grading.md)를 로컬 검사와 별도로 기록합니다.
