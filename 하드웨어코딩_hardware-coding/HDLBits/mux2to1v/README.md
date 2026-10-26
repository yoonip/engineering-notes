# 100비트 두 후보 중 하나 선택

[하드웨어 코딩 목차](../../README.md) · [공식 문제](https://hdlbits.01xz.net/wiki/mux2to1v)

sel이0이면a,1이면b의100비트 전체를 출력에 연결합니다. [HDLBits mux2to1v](https://hdlbits.01xz.net/wiki/mux2to1v)의 문제 본문과 모듈 선언을 기준으로 직접 구성한 풀이입니다. 공식 문제는 회로 명세의 출처이며 이 문서의 로컬 검사 결과를 보고한 자료는 아닙니다.

## 입출력과 회로 원리

입력 a[99:0]·b[99:0]·sel, 출력 out[99:0]입니다.

조건 연산자 sel ? b : a는 참일 때b, 거짓일 때a를 고릅니다. 두 후보와 결과 폭이 모두100비트이므로 각 위치에서 같은 선택 신호를 공유하는 멀티플렉서가 됩니다.

## 입력부터 결과까지의 흐름

아래는 기능을 설명하기 위해 직접 구성한 입력·관측 흐름입니다. 조합 회로의 행은 서로 다른 입력 예이며, 순차 회로의 행은 해당 에지 또는 명시한 이전 상태를 기준으로 읽습니다.

| 단계·관측 | 입력·조건 | 기대 결과 |
| --- | --- | --- |
| sel=0 | a=0,b=전체1 | out=0 |
| sel=1 | a=0,b=전체1 | out=전체1 |
| sel=0 | a의99번만1,b=0 | out의99번만1 |
| sel=1 | a의99번만1,b=0 | out=0 |

## 실수와 정당성 조건

조건 연산자의 두 후보를 반대로 적으면 선택 신호의 의미가 뒤집힙니다. 99:0은100비트이며99비트가 아닙니다.

100비트 입력 두 개와 선택 신호의 전체2^201조합을 전수 검사한 것은 아닙니다. 이 예제의 기능 비교는 sel과 데이터가0 또는1인 입력을 대상으로 합니다.

## 하드웨어에서의 의미

연산 결과 선택, 레지스터 입력 선택, 경로 전환의 기본 구조입니다. 넓은 데이터 경로에서는 선택 신호의 부하와 배선·논리 지연도 실제 구현에서 확인해야 합니다.

## 독립 로컬 검사

각 비트마다 if로 선택한 기대값을 만들고 전체100비트와 대조합니다. 모든 위치의 원-핫·공통1·선택 방향을 검사합니다.

극단 패턴8개,100개 위치당6개 원-핫 선택, 교대 패턴2개로 총610벡터입니다.

2026-10-26에 실제 Icarus Verilog12.0 devel로 컴파일하고 VVP로 실행했습니다. compile 종료 코드는0, simulation 종료 코드는0입니다. 실제 집계는 비교610회·입력 벡터 또는 샘플610개입니다.

```text
PASS id=mux2to1v checks=610 vectors=610
```

이 집계는 로컬 테스트벤치의 범위이며 온라인 문제 채점과 구분합니다. 합성·STA·formal 증명·실물 보드 시험의 완료를 뜻하지 않습니다. 각 소스의 SHA-256, 실제 명령·종료 코드·표준 출력과 오류는 [problem.json](problem.json)에 기록합니다.

컴파일에는 RTL 모듈의 시간 단위가 명시되지 않았다는 Icarus 경고가 있습니다. RTL에는 `#` 지연이 없고 테스트벤치에는 `timescale 1ns/1ps`를 지정했습니다. 경고 원문을 보존하며 이를 컴파일 실패나 무경고 결과로 바꾸어 적지 않습니다.

## 실행 명령

외부 표준 입력은 없으며 tb.sv가 고정·전수 입력을 생성합니다. 다음 PowerShell 명령은 저장소 루트에서 새 임시 폴더로 소스를 복사해 실행합니다. Icarus가 다른 위치에 있으면 두 실행 파일 경로를 변경합니다.

```powershell
$source = Resolve-Path '하드웨어코딩_hardware-coding/HDLBits/mux2to1v'
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
module top_module(input [99:0] a, b, input sel, output [99:0] out); // 100비트 두 후보와 선택 신호
    assign out = sel ? b : a; // sel1이면b 전체를 고르고0이면a 전체를 연결
endmodule // 벡터 멀티플렉서 끝
```

### tb.sv

```systemverilog
`timescale 1ns/1ps // 클록·관측 지연의 시간 단위
module tb; // 문제별 독립 기대값을 가진 테스트벤치
    int checks = 0, vectors = 0; // 실행한 비교와 입력 벡터 수
    logic [99:0] a, b; // 선택할 두 입력 벡터
    logic sel; // 선택 입력
    wire [99:0] out; // 100비트 출력
    top_module dut(.*); // DUT 포트 연결

    task automatic verify(input logic condition, input string message); // X도 실패로 처리할 공통 검사
        checks++; // 실제 비교 횟수 누적
        if (condition !== 1'b1) $fatal(1, "%s vector=%0d %s", "mux2to1v", vectors, message); // 첫 불일치에서 실패 종료
    endtask // 공통 검사 끝
    task automatic probe(input logic [99:0] first, second, input bit choice); // 벡터 선택 한 건 검사
        logic [99:0] expected; // 비트별 독립 선택 기대값
        a = first; b = second; sel = choice; // 세 입력을 함께 구동
        for (int index = 0; index < 100; index++) begin // 각 출력 비트의 기준 계산
            if (choice == 0) expected[index] = first[index]; // sel0의 개별 비트 기준
            else expected[index] = second[index]; // sel1의 개별 비트 기준
        end // 100비트 기준 완성
        #1; vectors++; verify(out === expected, "whole100bit selection"); // 전체 벡터 폭과 선택 방향 대조
    endtask // 선택 한 건 검사 끝
    initial begin // 재현 가능한 입력과 경계 검사
        for (int first = 0; first < 2; first++) begin // 모든0·모든1의 첫 후보
            for (int second = 0; second < 2; second++) begin // 모든0·모든1의 둘째 후보
                probe({100{first[0]}}, {100{second[0]}}, 0); // 첫 선택 분기 검사
                probe({100{first[0]}}, {100{second[0]}}, 1); // 둘째 선택 분기 검사
            end // 둘째 후보 끝
        end // 극단 패턴 끝
        for (int index = 0; index < 100; index++) begin // 모든 입력 배선 위치
            probe(100'd1 << index, 0, 0); probe(100'd1 << index, 0, 1); // a만 해당 위치가1인 경우
            probe(0, 100'd1 << index, 0); probe(0, 100'd1 << index, 1); // b만 해당 위치가1인 경우
            probe(100'd1 << index, 100'd1 << index, 0); probe(100'd1 << index, 100'd1 << index, 1); // 두 후보의 같은 위치가1인 경우
        end // 모든100개 위치 끝
        probe({50{2'b10}}, {50{2'b01}}, 0); probe({50{2'b10}}, {50{2'b01}}, 1); // 교대 비트와 반대 선택 확인
        $display("PASS id=mux2to1v checks=%0d vectors=%0d", checks, vectors); // 실제 검사 수 출력
        $finish; // 정상 시뮬레이션 종료
    end // 입력 자극 끝
    initial begin #10000000; $fatal(1, "watchdog"); end // 종료되지 않는 시험의 시간 상한
endmodule // 자체 검사 모듈 끝
```

## 근거

- [HDLBits mux2to1v 문제·입출력 명세](https://hdlbits.01xz.net/wiki/mux2to1v)
- [Icarus Verilog의 언어·최상위 모듈·출력 옵션](https://github.com/steveicarus/iverilog/blob/master/Documentation/usage/command_line_flags.rst)

공식 문제의 열람 기준일은2026-10-26입니다.

## 사이트 채점

2026-10-26에 이 폴더의 solution.v를 HDLBits에 직접 제출하여 Success!를 확인했습니다. [채점 화면과 제출 소스 해시](../확인기록_online-grading.md)를 로컬 검사와 별도로 기록합니다.
