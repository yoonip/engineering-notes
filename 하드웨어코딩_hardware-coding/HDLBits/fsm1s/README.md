# B에서 리셋하고0에서 토글하는 두 상태 FSM

[하드웨어 코딩 목차](../../README.md) · [공식 문제](https://hdlbits.01xz.net/wiki/fsm1s)

동기 리셋에서B로 들어가며 입력0은 상태를 바꾸고 입력1은 유지합니다. [HDLBits fsm1s](https://hdlbits.01xz.net/wiki/fsm1s)의 문제 본문과 모듈 선언을 기준으로 직접 구성한 풀이입니다. 공식 문제는 회로 명세의 출처이며 이 문서의 로컬 검사 결과를 보고한 자료는 아닙니다.

## 입출력과 회로 원리

입력 clk·동기식 reset·in, 출력 out입니다. A의 출력은0, B의 출력은1입니다.

A=0,B=1의 한 비트 상태를 사용하므로 입력0의 전이는 상태 비트 반전으로 표현할 수 있습니다. 입력1에서는 할당하지 않아 유지합니다. out은 현재 상태가B인지로 정하는 Moore 출력입니다. 따라서 리셋 뒤 입력0이 나온 횟수가 짝수이면B, 홀수이면A입니다.

## 입력부터 결과까지의 흐름

아래는 기능을 설명하기 위해 직접 구성한 입력·관측 흐름입니다. 조합 회로의 행은 서로 다른 입력 예이며, 순차 회로의 행은 해당 에지 또는 명시한 이전 상태를 기준으로 읽습니다.

| 단계·관측 | 입력·조건 | 기대 결과 |
| --- | --- | --- |
| reset 에지 | 입력과 무관 | B,out=1 |
| in=1 | B에서 유지 | B,out=1 |
| in=0 | B에서 전이 | A,out=0 |
| in=1 | A에서 유지 | A,out=0 |
| reset 에지 | A에서 초기화 | B,out=1 |

## 실수와 정당성 조건

리셋을A로 잡거나 입력1에서 토글하면 공식 그림과 반대입니다. 출력이1이라는 사실만으로 별도의 추가 출력 지연 레지스터를 넣지 않습니다.

공식 본문은 동기식 리셋을 요구합니다. 페이지의 공용 상태 그림에 있는 areset 표기를 비동기 감지 목록의 요구로 해석하지 않습니다. 초기 상태를 확정하려면 실제 리셋 에지가 필요합니다. 임의의 X 입력에 대한 복구 정책은 추가하지 않습니다.

## 하드웨어에서의 의미

상태 전이와 출력의 관계, Moore 출력의 저장 시점, 동기 리셋을 구분하는 기본입니다. 실제 프로토콜 제어기에서도 입력 조건과 리셋 상태를 명세대로 해석해야 합니다.

## 독립 로컬 검사

DUT의 state를 읽지 않고 리셋 뒤0 입력의 개수 패리티로 out을 계산합니다. 에지 전 출력 유지도 확인합니다.

직접 리셋·유지·토글 흐름과 길이0~8의 모든 이진 문자열511개를 독립 리셋에서 검사합니다. 총4104에지·8207비교입니다.

2026-10-26에 실제 Icarus Verilog12.0 devel로 컴파일하고 VVP로 실행했습니다. compile 종료 코드는0, simulation 종료 코드는0입니다. 실제 집계는 비교8207회·입력 벡터 또는 샘플4104개입니다.

```text
PASS id=fsm1s checks=8207 vectors=4104
```

이 집계는 로컬 테스트벤치의 범위이며 온라인 문제 채점과 구분합니다. 합성·STA·formal 증명·실물 보드 시험의 완료를 뜻하지 않습니다. 각 소스의 SHA-256, 실제 명령·종료 코드·표준 출력과 오류는 [problem.json](problem.json)에 기록합니다.

컴파일에는 RTL 모듈의 시간 단위가 명시되지 않았다는 Icarus 경고가 있습니다. RTL에는 `#` 지연이 없고 테스트벤치에는 `timescale 1ns/1ps`를 지정했습니다. 경고 원문을 보존하며 이를 컴파일 실패나 무경고 결과로 바꾸어 적지 않습니다.

## 실행 명령

외부 표준 입력은 없으며 tb.sv가 고정·전수 입력을 생성합니다. 다음 PowerShell 명령은 저장소 루트에서 새 임시 폴더로 소스를 복사해 실행합니다. Icarus가 다른 위치에 있으면 두 실행 파일 경로를 변경합니다.

```powershell
$source = Resolve-Path '하드웨어코딩_hardware-coding/HDLBits/fsm1s'
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
module top_module(input clk, reset, in, output out); // 두 상태 Moore 기계의 입력과 상태 출력
    localparam A = 1'b0, B = 1'b1; // 출력0의A와 출력1의B를 한 비트로 구분
    reg state; // 현재 상태를 저장할 플립플롭
    always @(posedge clk) begin // 동기 리셋과 상태 전이를 상승 에지에서 처리
        if (reset) state <= B; // 공식 명세의 리셋 상태는B
        else if (!in) state <= ~state; // 입력0이면A와B 사이를 이동
    end // 입력1이면 할당 없이 현재 상태 유지
    assign out = (state == B); // 현재 상태가B인 동안만 출력1
endmodule // 동기 리셋 두 상태 기계 끝
```

### tb.sv

```systemverilog
`timescale 1ns/1ps // 클록·관측 지연의 시간 단위
module tb; // 문제별 독립 기대값을 가진 테스트벤치
    int checks = 0, vectors = 0; // 실행한 비교와 입력 벡터 수
    logic clk = 0; // 시작 클록 값
    always #5 clk = ~clk; // 주기10ns의 시뮬레이션 클록
    logic reset = 1, in = 1; // 시작 동기 리셋과 유지 입력
    wire out; // B 상태에서1인 Moore 출력
    int zeros = 0; bit initialized = 0; // 리셋 이후0의 개수와 초기 표시
    top_module dut(.*); // 문제 인터페이스 연결

    task automatic verify(input logic condition, input string message); // X도 실패로 처리할 공통 검사
        checks++; // 실제 비교 횟수 누적
        if (condition !== 1'b1) $fatal(1, "%s vector=%0d %s", "fsm1s", vectors, message); // 첫 불일치에서 실패 종료
    endtask // 공통 검사 끝
    task automatic sample(input bit reset_value, input bit value); // 한 입력 에지의 독립 패리티 기준
        logic held; // 동기 리셋 전까지 유지할 출력
        @(negedge clk); held = out; reset = reset_value; in = value; // 상승 에지와 분리해 구동
        #1; if (initialized) verify(out === held, "synchronous Moore output"); // 입력·리셋 변화만으로 상태가 움직이지 않기
        if (reset_value) zeros = 0; // B에서 시작하므로 토글 횟수 초기화
        else if (!value) zeros++; // 입력0만 상태를 바꾸는 사건으로 집계
        @(posedge clk); #1; vectors++; // 상태 저장 뒤 출력 관측
        verify(out === ((zeros % 2) == 0), "parity of zero inputs from stateB"); // FSM 분기표 대신0의 개수 패리티로 비교
        initialized = 1; // 이후 에지 사이 상태도 검사
    endtask // 한 상태 전이 검사 끝
    initial begin // 재현 가능한 입력과 경계 검사
        sample(1, 0); sample(0, 1); sample(0, 0); sample(0, 1); // B 유지·A 전이·A 유지
        sample(1, 0); sample(0, 0); sample(0, 0); // 중간 리셋과 두 번의 토글
        for (int length = 0; length <= 8; length++) begin // 짧은 모든 이진 입력 스트림
            for (int pattern = 0; pattern < (1 << length); pattern++) begin // 해당 길이의 모든 경우
                sample(1, 1); // 매 문자열은B에서 시작
                for (int index = length - 1; index >= 0; index--) sample(0, ((pattern >> index) & 1)); // 가장 높은 자리부터 시간순 입력
            end // 해당 길이의 열거 끝
        end // 총511개 문자열 확인 끝
        $display("PASS id=fsm1s checks=%0d vectors=%0d", checks, vectors); // 실제 검사 수 출력
        $finish; // 정상 시뮬레이션 종료
    end // 입력 자극 끝
    initial begin #10000000; $fatal(1, "watchdog"); end // 종료되지 않는 시험의 시간 상한
endmodule // 자체 검사 모듈 끝
```

## 근거

- [HDLBits fsm1s 문제·입출력 명세](https://hdlbits.01xz.net/wiki/fsm1s)
- [Icarus Verilog의 언어·최상위 모듈·출력 옵션](https://github.com/steveicarus/iverilog/blob/master/Documentation/usage/command_line_flags.rst)

공식 문제의 열람 기준일은2026-10-26입니다.

## 사이트 채점

2026-10-26에 이 폴더의 solution.v를 HDLBits에 직접 제출하여 Success!를 확인했습니다. [채점 화면과 제출 소스 해시](../확인기록_online-grading.md)를 로컬 검사와 별도로 기록합니다.
