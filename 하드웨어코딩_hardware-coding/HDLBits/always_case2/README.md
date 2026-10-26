# 가장 낮은1을 고르는4비트 우선순위 인코더

[하드웨어 코딩 목차](../../README.md) · [공식 문제](https://hdlbits.01xz.net/wiki/always_case2)

입력16개를 가장 낮은1의 위치별로 나누어 case 문에서 결과를 정합니다. [HDLBits always_case2](https://hdlbits.01xz.net/wiki/always_case2)의 문제 본문과 모듈 선언을 기준으로 직접 구성한 풀이입니다. 공식 문제는 회로 명세의 출처이며 이 문서의 로컬 검사 결과를 보고한 자료는 아닙니다.

## 입출력과 회로 원리

입력 in[3:0], 출력 reg pos[1:0]입니다. 입력0도 pos=0입니다.

모든 홀수는0번 비트가1이므로 pos=0입니다. 0번이0이고1번이1인2·6·10·14는 pos=1입니다.4·12는 pos=2,8은 pos=3입니다. default가 입력0과 그 밖의 값을 처리하므로 모든 조합 경로에서 pos에 값을 할당합니다.

## 입력부터 결과까지의 흐름

아래는 기능을 설명하기 위해 직접 구성한 입력·관측 흐름입니다. 조합 회로의 행은 서로 다른 입력 예이며, 순차 회로의 행은 해당 에지 또는 명시한 이전 상태를 기준으로 읽습니다.

| 단계·관측 | 입력·조건 | 기대 결과 |
| --- | --- | --- |
| 0000 | 활성 비트 없음 | pos=0 |
| 1001 | 0번과3번이1 | pos=0 |
| 1010 | 1번과3번이1 | pos=1 |
| 1100 | 2번과3번이1 | pos=2 |
| 1000 | 3번만1 | pos=3 |

## 실수와 정당성 조건

pos=3을 가장 먼저 우선시키면 명세와 반대입니다. 조합 always에서 default를 빼면 값을 할당하지 않은 경로가 생겨 래치를 추론할 수 있습니다.

입력0과0번만1인 입력은 모두 출력0입니다. 출력에 valid 표시가 없으므로 pos만으로 요청 존재 여부를 구분할 수 없습니다. 이 문제의 우선순위는 가장 높은1이 아니라 가장 낮은1입니다.

## 하드웨어에서의 의미

동시에 여러 요청이 들어왔을 때 정해진 순서로 하나를 고르는 인코더의 기초입니다. 고정 우선순위는 높은 번호의 요청을 오래 미룰 수 있으므로 공정성이 필요한 중재에서는 별도 정책이 필요합니다.

## 독립 로컬 검사

인덱스0부터 선형 탐색해 처음 발견한1만 저장합니다. case의 값 묶음을 복사하지 않습니다.

4비트의 모든16개 이진 입력을 검사합니다.

2026-10-26에 실제 Icarus Verilog12.0 devel로 컴파일하고 VVP로 실행했습니다. compile 종료 코드는0, simulation 종료 코드는0입니다. 실제 집계는 비교16회·입력 벡터 또는 샘플16개입니다.

```text
PASS id=always_case2 checks=16 vectors=16
```

이 집계는 로컬 테스트벤치의 범위이며 온라인 문제 채점과 구분합니다. 합성·STA·formal 증명·실물 보드 시험의 완료를 뜻하지 않습니다. 각 소스의 SHA-256, 실제 명령·종료 코드·표준 출력과 오류는 [problem.json](problem.json)에 기록합니다.

컴파일에는 RTL 모듈의 시간 단위가 명시되지 않았다는 Icarus 경고가 있습니다. RTL에는 `#` 지연이 없고 테스트벤치에는 `timescale 1ns/1ps`를 지정했습니다. 경고 원문을 보존하며 이를 컴파일 실패나 무경고 결과로 바꾸어 적지 않습니다.

## 실행 명령

외부 표준 입력은 없으며 tb.sv가 고정·전수 입력을 생성합니다. 다음 PowerShell 명령은 저장소 루트에서 새 임시 폴더로 소스를 복사해 실행합니다. Icarus가 다른 위치에 있으면 두 실행 파일 경로를 변경합니다.

```powershell
$source = Resolve-Path '하드웨어코딩_hardware-coding/HDLBits/always_case2'
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
module top_module(input [3:0] in, output reg [1:0] pos); // 네 입력 중 가장 낮은1의 위치
    always @(*) begin // 입력 변화마다 조합 결과 다시 계산
        case (in) // 이진 입력16개를 가장 낮은1의 위치별로 묶기
            4'd1, 4'd3, 4'd5, 4'd7, 4'd9, 4'd11, 4'd13, 4'd15: pos = 2'd0; // 홀수는 모두0번 비트가 우선
            4'd2, 4'd6, 4'd10, 4'd14: pos = 2'd1; // 0번이0이고1번이1인 네 경우
            4'd4, 4'd12: pos = 2'd2; // 낮은 두 비트가0이고2번이1인 경우
            4'd8: pos = 2'd3; // 3번 비트만1인 경우
            default: pos = 2'd0; // 입력0도0을 내보내며 미할당 경로 방지
        endcase // 우선 위치별 선택 끝
    end // 모든 경로가 값을 정하는 조합 블록 끝
endmodule // 우선순위 인코더 끝
```

### tb.sv

```systemverilog
`timescale 1ns/1ps // 클록·관측 지연의 시간 단위
module tb; // 문제별 독립 기대값을 가진 테스트벤치
    int checks = 0, vectors = 0; // 실행한 비교와 입력 벡터 수
    logic [3:0] in; // 우선순위 입력
    wire [1:0] pos; // 가장 낮은1의 위치
    top_module dut(.*); // DUT 포트 연결

    task automatic verify(input logic condition, input string message); // X도 실패로 처리할 공통 검사
        checks++; // 실제 비교 횟수 누적
        if (condition !== 1'b1) $fatal(1, "%s vector=%0d %s", "always_case2", vectors, message); // 첫 불일치에서 실패 종료
    endtask // 공통 검사 끝
    initial begin // 재현 가능한 입력과 경계 검사
        for (int value = 0; value < 16; value++) begin // 네 비트의 모든 입력
            int expected; bit found; // 선형 탐색의 위치와 발견 표시
            in = value[3:0]; expected = 0; found = 0; // 입력0의 기본 결과 준비
            for (int index = 0; index < 4; index++) begin // 낮은 인덱스부터 실제1을 찾기
                if (!found && ((value >> index) & 1)) begin // 처음 발견한1만 선택
                    expected = index; found = 1; // 높은 비트가 나중에 덮어쓰지 못하게 표시
                end // 첫1 발견 조건 끝
            end // 모든 비트 탐색 끝
            #1; vectors++; verify(pos === expected[1:0], "lowest set bit priority"); // case 묶음과 독립 탐색 비교
        end // 16개 입력 끝
        $display("PASS id=always_case2 checks=%0d vectors=%0d", checks, vectors); // 실제 검사 수 출력
        $finish; // 정상 시뮬레이션 종료
    end // 입력 자극 끝
    initial begin #10000000; $fatal(1, "watchdog"); end // 종료되지 않는 시험의 시간 상한
endmodule // 자체 검사 모듈 끝
```

## 근거

- [HDLBits always_case2 문제·입출력 명세](https://hdlbits.01xz.net/wiki/always_case2)
- [Icarus Verilog의 언어·최상위 모듈·출력 옵션](https://github.com/steveicarus/iverilog/blob/master/Documentation/usage/command_line_flags.rst)

공식 문제의 열람 기준일은2026-10-26입니다.

## 사이트 채점

2026-10-26에 이 폴더의 solution.v를 HDLBits에 직접 제출하여 Success!를 확인했습니다. [채점 화면과 제출 소스 해시](../확인기록_online-grading.md)를 로컬 검사와 별도로 기록합니다.
