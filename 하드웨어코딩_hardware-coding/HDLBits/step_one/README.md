# 입력 없는 상수1 출력

[하드웨어 코딩 목차](../../README.md) · [공식 문제](https://hdlbits.01xz.net/wiki/step_one)

입력과 상태 없이 출력 한 비트를 항상1에 연결합니다. [HDLBits step_one](https://hdlbits.01xz.net/wiki/step_one)의 문제 본문과 모듈 선언을 기준으로 직접 구성한 풀이입니다. 공식 문제는 회로 명세의 출처이며 이 문서의 로컬 검사 결과를 보고한 자료는 아닙니다.

## 입출력과 회로 원리

입력은 없으며 출력 one 하나만 있습니다.

연속 대입 assign은 소프트웨어에서 한 번 실행하는 문장이 아니라 출력의 연결 관계를 정합니다. 1'b1은 폭이1비트인 이진 상수이므로 출력 폭과 같습니다. 클록이나 initial 블록이 필요하지 않습니다.

## 입력부터 결과까지의 흐름

아래는 기능을 설명하기 위해 직접 구성한 입력·관측 흐름입니다. 조합 회로의 행은 서로 다른 입력 예이며, 순차 회로의 행은 해당 에지 또는 명시한 이전 상태를 기준으로 읽습니다.

| 단계·관측 | 입력·조건 | 기대 결과 |
| --- | --- | --- |
| 1ns | 입력 없음 | one=1 |
| 5ns | 시간 경과 | one=1 |
| 25ns | 추가 대기 | one=1 |

## 실수와 정당성 조건

출력 이름 one을 바꾸거나 assign을 생략하면 명세의 외부 포트 또는 연결을 만족하지 못합니다. 단순한 문제라도 모듈명과 포트 계약이 회로 기능의 일부입니다.

이 문제는 출력 수준만 정합니다. 입력 자극이나 저장 상태가 없으므로 여러 시점의 검사는 같은 연결을 다시 관측하는 것입니다. 물리 핀의 전압을 직접 측정한 결과는 아닙니다.

## 하드웨어에서의 의미

상수 연결은 사용하지 않는 제어 입력의 기본값이나 기능을 고정하는 배선의 기초입니다. 실제 소자에서 상수 신호를 구현하는 방식은 합성·배치 도구와 라이브러리에 따릅니다.

## 독립 로컬 검사

1ns·5ns·25ns에 one이 정확히1인지 비교합니다. X나Z도 실패로 처리합니다.

입력 조합이 없는 상수 회로의 세 시점 검사입니다.

2026-10-26에 실제 Icarus Verilog12.0 devel로 컴파일하고 VVP로 실행했습니다. compile 종료 코드는0, simulation 종료 코드는0입니다. 실제 집계는 비교3회·입력 벡터 또는 샘플3개입니다.

```text
PASS id=step_one checks=3 vectors=3
```

이 집계는 로컬 테스트벤치의 범위이며 온라인 문제 채점과 구분합니다. 합성·STA·formal 증명·실물 보드 시험의 완료를 뜻하지 않습니다. 각 소스의 SHA-256, 실제 명령·종료 코드·표준 출력과 오류는 [problem.json](problem.json)에 기록합니다.

컴파일에는 RTL 모듈의 시간 단위가 명시되지 않았다는 Icarus 경고가 있습니다. RTL에는 `#` 지연이 없고 테스트벤치에는 `timescale 1ns/1ps`를 지정했습니다. 경고 원문을 보존하며 이를 컴파일 실패나 무경고 결과로 바꾸어 적지 않습니다.

## 실행 명령

외부 표준 입력은 없으며 tb.sv가 고정·전수 입력을 생성합니다. 다음 PowerShell 명령은 저장소 루트에서 새 임시 폴더로 소스를 복사해 실행합니다. Icarus가 다른 위치에 있으면 두 실행 파일 경로를 변경합니다.

```powershell
$source = Resolve-Path '하드웨어코딩_hardware-coding/HDLBits/step_one'
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
module top_module(output one); // 외부로 내보낼 1비트 출력
    assign one = 1'b1; // 입력 없이 항상 1로 연결
endmodule // 회로 정의 끝
```

### tb.sv

```systemverilog
`timescale 1ns/1ps // 클록·관측 지연의 시간 단위
module tb; // 문제별 독립 기대값을 가진 테스트벤치
    int checks = 0, vectors = 0; // 실행한 비교와 입력 벡터 수
    wire one; // 상수 출력 관측
    top_module dut(.one(one)); // 입력 없는 DUT 연결

    task automatic verify(input logic condition, input string message); // X도 실패로 처리할 공통 검사
        checks++; // 실제 비교 횟수 누적
        if (condition !== 1'b1) $fatal(1, "%s vector=%0d %s", "step_one", vectors, message); // 첫 불일치에서 실패 종료
    endtask // 공통 검사 끝
    initial begin // 재현 가능한 입력과 경계 검사
        #1; verify(one === 1'b1, "constant at1ns"); vectors++; // 최초 안정 출력 확인
        #4; verify(one === 1'b1, "constant at5ns"); vectors++; // 시간 경과 후에도1 유지
        #20; verify(one === 1'b1, "constant at25ns"); vectors++; // 별도 상태 없이 값이 유지되는지 확인
        $display("PASS id=step_one checks=%0d vectors=%0d", checks, vectors); // 실제 검사 수 출력
        $finish; // 정상 시뮬레이션 종료
    end // 입력 자극 끝
    initial begin #10000000; $fatal(1, "watchdog"); end // 종료되지 않는 시험의 시간 상한
endmodule // 자체 검사 모듈 끝
```

## 근거

- [HDLBits step_one 문제·입출력 명세](https://hdlbits.01xz.net/wiki/step_one)
- [Icarus Verilog의 언어·최상위 모듈·출력 옵션](https://github.com/steveicarus/iverilog/blob/master/Documentation/usage/command_line_flags.rst)

공식 문제의 열람 기준일은2026-10-26입니다.

## 사이트 채점

2026-10-26에 이 폴더의 solution.v를 HDLBits에 직접 제출하여 Success!를 확인했습니다. [채점 화면과 제출 소스 해시](../확인기록_online-grading.md)를 로컬 검사와 별도로 기록합니다.
