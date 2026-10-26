# 32비트 단어의 네 바이트 순서 바꾸기

[하드웨어 코딩 목차](../../README.md) · [공식 문제](https://hdlbits.01xz.net/wiki/vector2)

각 바이트 내부의 비트는 보존하고 네 바이트의 위치만 역순으로 연결합니다. [HDLBits vector2](https://hdlbits.01xz.net/wiki/vector2)의 문제 본문과 모듈 선언을 기준으로 직접 구성한 풀이입니다. 공식 문제는 회로 명세의 출처이며 이 문서의 로컬 검사 결과를 보고한 자료는 아닙니다.

## 입출력과 회로 원리

입력 in[31:0], 출력 out[31:0]의 조합 회로입니다.

중괄호 연결 연산자는 왼쪽 항목을 결과의 높은 비트에 놓습니다. 입력의 가장 낮은 바이트 in[7:0]을 출력의 가장 높은 바이트로 보내고 나머지도 역순으로 배치합니다. 각 조각이8비트이므로 전체 폭은32비트입니다.

## 입력부터 결과까지의 흐름

아래는 기능을 설명하기 위해 직접 구성한 입력·관측 흐름입니다. 조합 회로의 행은 서로 다른 입력 예이며, 순차 회로의 행은 해당 에지 또는 명시한 이전 상태를 기준으로 읽습니다.

| 단계·관측 | 입력·조건 | 기대 결과 |
| --- | --- | --- |
| out[31:24] | in[7:0]=78 | 78 |
| out[23:16] | in[15:8]=56 | 56 |
| out[15:8] | in[23:16]=34 | 34 |
| out[7:0] | in[31:24]=12 | 12; 전체78563412 |

## 실수와 정당성 조건

12345678을78563412로 바꾸는 작업과 각 비트 순서를 반전하는 작업은 다릅니다. 슬라이스 경계를 한 칸 잘못 쓰면 전체 폭이나 특정 배선이 틀어집니다.

바이트 내부 비트를 뒤집는 기능이 아니며 숫자의 부호나 값을 산술 변환하지 않습니다. 32비트의2^32가지 입력 전부를 검사하지는 않았습니다.

## 하드웨어에서의 의미

서로 다른 바이트 순서를 사용하는 데이터 형식 사이의 변환에 적용할 수 있습니다. 단어의 비트 번호와 메모리 주소의 바이트 배치는 구분해야 하며 실제 프로토콜의 바이트 순서를 먼저 정해야 합니다.

## 독립 로컬 검사

테스트벤치는 낮은 바이트부터 나눠 읽어256진수 누적 산술로 기대값을 만듭니다. 연결식을 그대로 복사하지 않습니다.

전체0·전체1·12345678,32개 원-핫 입력, 고정 시드의 xorshift 입력1000개로 총1035벡터입니다.

2026-10-26에 실제 Icarus Verilog12.0 devel로 컴파일하고 VVP로 실행했습니다. compile 종료 코드는0, simulation 종료 코드는0입니다. 실제 집계는 비교1035회·입력 벡터 또는 샘플1035개입니다.

```text
PASS id=vector2 checks=1035 vectors=1035
```

이 집계는 로컬 테스트벤치의 범위이며 온라인 문제 채점과 구분합니다. 합성·STA·formal 증명·실물 보드 시험의 완료를 뜻하지 않습니다. 각 소스의 SHA-256, 실제 명령·종료 코드·표준 출력과 오류는 [problem.json](problem.json)에 기록합니다.

컴파일에는 RTL 모듈의 시간 단위가 명시되지 않았다는 Icarus 경고가 있습니다. RTL에는 `#` 지연이 없고 테스트벤치에는 `timescale 1ns/1ps`를 지정했습니다. 경고 원문을 보존하며 이를 컴파일 실패나 무경고 결과로 바꾸어 적지 않습니다.

## 실행 명령

외부 표준 입력은 없으며 tb.sv가 고정·전수 입력을 생성합니다. 다음 PowerShell 명령은 저장소 루트에서 새 임시 폴더로 소스를 복사해 실행합니다. Icarus가 다른 위치에 있으면 두 실행 파일 경로를 변경합니다.

```powershell
$source = Resolve-Path '하드웨어코딩_hardware-coding/HDLBits/vector2'
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
module top_module(input [31:0] in, output [31:0] out); // 32비트 입력과 바이트 순서를 바꾼 출력
    assign out = {in[7:0], in[15:8], in[23:16], in[31:24]}; // 네 바이트의 위치만 뒤집어 연결
endmodule // 바이트 순서 변환 회로 끝
```

### tb.sv

```systemverilog
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
```

## 근거

- [HDLBits vector2 문제·입출력 명세](https://hdlbits.01xz.net/wiki/vector2)
- [Icarus Verilog의 언어·최상위 모듈·출력 옵션](https://github.com/steveicarus/iverilog/blob/master/Documentation/usage/command_line_flags.rst)

공식 문제의 열람 기준일은2026-10-26입니다.

## 사이트 채점

2026-10-26에 이 폴더의 solution.v를 HDLBits에 직접 제출하여 Success!를 확인했습니다. [채점 화면과 제출 소스 해시](../확인기록_online-grading.md)를 로컬 검사와 별도로 기록합니다.
