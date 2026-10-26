# 동기식 active-high 리셋의8비트 레지스터

[하드웨어 코딩 목차](../../README.md) · [공식 문제](https://hdlbits.01xz.net/wiki/dff8r)

상승 에지마다 reset이1이면0을 저장하고 아니면d를 저장합니다. [HDLBits dff8r](https://hdlbits.01xz.net/wiki/dff8r)의 문제 본문과 모듈 선언을 기준으로 직접 구성한 풀이입니다. 공식 문제는 회로 명세의 출처이며 이 문서의 로컬 검사 결과를 보고한 자료는 아닙니다.

## 입출력과 회로 원리

입력 clk·reset·d[7:0], 출력 q[7:0]입니다. reset은 동기식 active-high입니다.

감지 목록에는 posedge clk만 있습니다. 따라서 reset이 에지 사이에서1로 바뀌어도 q는 즉시 바뀌지 않으며 다음 상승 에지에서0이 됩니다. 순차 블록의 nonblocking 대입은 같은 에지 직전 입력을 기준으로 저장을 예약합니다.

## 입력부터 결과까지의 흐름

아래는 기능을 설명하기 위해 직접 구성한 입력·관측 흐름입니다. 조합 회로의 행은 서로 다른 입력 예이며, 순차 회로의 행은 해당 에지 또는 명시한 이전 상태를 기준으로 읽습니다.

| 단계·관측 | 입력·조건 | 기대 결과 |
| --- | --- | --- |
| 첫 리셋 에지 | reset=1,d=FF | q=00 |
| 데이터 순회 | reset=0,d=00..FF | q가 각 입력을 에지 뒤 저장 |
| 다음 리셋 전 | 기존q=FF,reset을1로 변경 | 상승 에지 전에는FF 유지 |
| 다음 리셋 에지 | reset=1,d=00 | q=00 |
| 리셋 뒤 복구 | d=5A,이후A5 | 각 상승 에지 뒤5A, A5 |

## 실수와 정당성 조건

posedge reset을 감지 목록에 추가하면 비동기 리셋이 되어 다른 회로입니다. output reg는 절차 블록에서 할당할 변수 선언이며 그 단어만으로 저장 소자가 결정되는 것은 아닙니다.

초기값이 자동으로0이라는 가정은 하지 않습니다. 실제 초기 상태는 리셋으로 확정합니다. 리셋 해제의 물리 타이밍·FPGA 자원 추론·STA는 로컬 기능 시뮬레이션과 별도입니다.

## 하드웨어에서의 의미

데이터 경로의 파이프라인·상태 저장과 리셋 정책을 구분하는 기초입니다. 동기 리셋은 유효 클록 에지가 있어야 반영되며 시스템의 클록 정지·재시작 정책도 함께 고려해야 합니다.

## 독립 로컬 검사

에지 사이에는 이전 q 유지, 에지 뒤에는 reset에 따른0 또는 입력값을 확인합니다. 모든256개 입력 저장과 모든256개 데이터에서의 리셋 우선을 검사합니다.

총515개 저장 에지와 에지 전·후1029개 비교입니다. 첫 초기화 전 X는 유지 비교에서 제외합니다.

2026-10-26에 실제 Icarus Verilog12.0 devel로 컴파일하고 VVP로 실행했습니다. compile 종료 코드는0, simulation 종료 코드는0입니다. 실제 집계는 비교1029회·입력 벡터 또는 샘플515개입니다.

```text
PASS id=dff8r checks=1029 vectors=515
```

이 집계는 로컬 테스트벤치의 범위이며 온라인 문제 채점과 구분합니다. 합성·STA·formal 증명·실물 보드 시험의 완료를 뜻하지 않습니다. 각 소스의 SHA-256, 실제 명령·종료 코드·표준 출력과 오류는 [problem.json](problem.json)에 기록합니다.

컴파일에는 RTL 모듈의 시간 단위가 명시되지 않았다는 Icarus 경고가 있습니다. RTL에는 `#` 지연이 없고 테스트벤치에는 `timescale 1ns/1ps`를 지정했습니다. 경고 원문을 보존하며 이를 컴파일 실패나 무경고 결과로 바꾸어 적지 않습니다.

## 실행 명령

외부 표준 입력은 없으며 tb.sv가 고정·전수 입력을 생성합니다. 다음 PowerShell 명령은 저장소 루트에서 새 임시 폴더로 소스를 복사해 실행합니다. Icarus가 다른 위치에 있으면 두 실행 파일 경로를 변경합니다.

```powershell
$source = Resolve-Path '하드웨어코딩_hardware-coding/HDLBits/dff8r'
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
module top_module(input clk, reset, input [7:0] d, output reg [7:0] q); // 상승 에지 저장과 동기식 high 리셋
    always @(posedge clk) begin // 클록 상승 에지에서만 출력 갱신
        if (reset) q <= 8'd0; // 리셋이 데이터 저장보다 우선
        else q <= d; // 같은 에지 직전의8비트 입력 저장
    end // nonblocking 대입의 순차 저장 끝
endmodule // 동기 리셋8비트 레지스터 끝
```

### tb.sv

```systemverilog
`timescale 1ns/1ps // 클록·관측 지연의 시간 단위
module tb; // 문제별 독립 기대값을 가진 테스트벤치
    int checks = 0, vectors = 0; // 실행한 비교와 입력 벡터 수
    logic clk = 0; // 시작 클록 값
    always #5 clk = ~clk; // 주기10ns의 시뮬레이션 클록
    logic reset = 1; // 시작 동기 리셋
    logic [7:0] d = 0; // 저장할 데이터
    wire [7:0] q; // 관측한 레지스터 출력
    bit initialized = 0; // 초기 X를 상태 유지 검사와 구분
    top_module dut(.*); // 클록·리셋·데이터 연결

    task automatic verify(input logic condition, input string message); // X도 실패로 처리할 공통 검사
        checks++; // 실제 비교 횟수 누적
        if (condition !== 1'b1) $fatal(1, "%s vector=%0d %s", "dff8r", vectors, message); // 첫 불일치에서 실패 종료
    endtask // 공통 검사 끝
    task automatic sample(input bit reset_value, input logic [7:0] value); // 한 상승 에지의 동기 저장 검사
        logic [7:0] held, expected; // 에지 전 보존값과 에지 뒤 기대값
        @(negedge clk); held = q; reset = reset_value; d = value; // 상승 에지 중간에 입력과 리셋 변경
        #1; if (initialized) verify(q === held, "no asynchronous reset or data change"); // 클록 전에는 출력이 바뀌지 않아야 함
        expected = reset_value ? 8'd0 : value; // 입력 선택을 산술 상태와 분리
        @(posedge clk); #1; vectors++; // 실제 저장 에지 뒤 관측
        verify(q === expected, "synchronous register value"); // 데이터 또는 리셋 결과 비교
        initialized = 1; // 이후부터 에지 사이 상태도 검사
    endtask // 한 저장 에지 검사 끝
    initial begin // 재현 가능한 입력과 경계 검사
        sample(1, 8'hff); // 리셋과 입력이 함께 활성인 경우
        for (int value = 0; value < 256; value++) sample(0, value[7:0]); // 모든8비트 데이터 저장
        for (int value = 0; value < 256; value++) sample(1, value[7:0]); // 모든 데이터보다 동기 리셋이 우선
        sample(0, 8'h5a); sample(0, 8'ha5); // 리셋 해제 뒤 데이터 갱신 복구
        $display("PASS id=dff8r checks=%0d vectors=%0d", checks, vectors); // 실제 검사 수 출력
        $finish; // 정상 시뮬레이션 종료
    end // 입력 자극 끝
    initial begin #10000000; $fatal(1, "watchdog"); end // 종료되지 않는 시험의 시간 상한
endmodule // 자체 검사 모듈 끝
```

## 근거

- [HDLBits dff8r 문제·입출력 명세](https://hdlbits.01xz.net/wiki/dff8r)
- [Icarus Verilog의 언어·최상위 모듈·출력 옵션](https://github.com/steveicarus/iverilog/blob/master/Documentation/usage/command_line_flags.rst)

공식 문제의 열람 기준일은2026-10-26입니다.

## 사이트 채점

2026-10-26에 이 폴더의 solution.v를 HDLBits에 직접 제출하여 Success!를 확인했습니다. [채점 화면과 제출 소스 해시](../확인기록_online-grading.md)를 로컬 검사와 별도로 기록합니다.
