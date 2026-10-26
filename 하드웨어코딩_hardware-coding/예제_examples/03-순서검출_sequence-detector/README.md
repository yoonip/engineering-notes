# 겹치는1011을 검출하는 접미사 FSM

[하드웨어 코딩 목차](../../README.md)

직접 구성한 순서 검출 문제입니다. 유효 입력 비트의 흐름에서1011이 끝나는 순간마다 hit를 한 클록 출력합니다.1011011에는 네 번째와 일곱 번째 비트에서 두 발생이 있으며 마지막1을 다음 패턴의 첫1로 다시 사용할 수 있습니다.

## 입력 소비와 출력 시점

상승 에지에서 rst=0이고 sample_enable=1일 때만 bit_in을 소비합니다. enable이0이면 입력을 버리는 것이 아니라 아직 소비하지 않는 계약입니다. 접미사 상태는 유지하고 hit는0으로 갱신합니다. 외부 신호가 비동기라면 별도 동기화와 비트 수락 방식이 필요하며 이 예제는 단일 클록의 이미 안정된 입력만 다룹니다.

rst는 active-high 동기 리셋이며 유효 입력보다 우선합니다. 리셋에서 이전 접미사를 지우므로 서로 다른 리셋 구간의 비트를 이어 붙여 검출하지 않습니다. hit는 조합 출력이 아니라 마지막 비트를 소비한 에지 뒤의 레지스터 출력입니다.

## 상태의 의미와 전이

상태는 패턴1011의 접두사이면서 지금까지 읽은 비트의 접미사인 가장 긴 문자열입니다. 전체 이력을 기억하지 않고 다음 일치에 필요한 정보만 남깁니다.

| 현재 접미사 | 입력0 | 입력1 |
| --- | --- | --- |
| EMPTY | EMPTY | SEEN_1 |
|1 | SEEN_10 | SEEN_1 |
|10 | EMPTY | SEEN_101 |
|101 | SEEN_10 | hit=1,SEEN_1 |

101 뒤0이 오면1010의 마지막10을 남깁니다.101 뒤1이면 전체 패턴을 보고한 뒤 마지막1을 남깁니다. 완성 후 무조건 EMPTY로 돌아가면1011011의 두 번째 발생을 놓칩니다. 각 전이는 새 문자열의 접미사를 직접 살펴 구성했습니다. [Intel의 SystemVerilog FSM 예제](https://www.intel.com/content/www/us/en/docs/programmable/683323/current/systemverilog-state-machine-coding-example.html)와 [Berkeley EECS151의 FSM 스타일 안내](https://eecs151.org/asic/lab3/docs/fsm-style-guide/)는 이름 있는 상태와 조합 전이·순차 저장의 분리를 설명합니다. 이 패턴과 전이표는 이 자료에서 직접 구성했습니다.

## 입력부터 검출까지의 흐름

| 소비 비트 번호 | 입력 | 에지 뒤 접미사 | hit |
| --- | --- | --- | --- |
|1 |1 |1 |0 |
|2 |0 |10 |0 |
|3 |1 |101 |0 |
| 대기2에지 | enable=0 |101 유지 |0 |
|4 |1 |1 |1 |
|5 |0 |10 |0 |
|6 |1 |101 |0 |
|7 |1 |1 |1 |

대기 에지에는 bit_in이0이나1로 바뀌어도 소비하지 않습니다. 따라서 비트 번호는 실제 소비 에지에만 붙입니다. 각 hit는 가장 최근 네 소비 비트가1011인지와 같습니다.

## 독립 검사와 음성 대조

테스트벤치는 DUT의 enum 상태를 읽지 않고 최근 네 유효 비트의 이동 창과 길이만 유지합니다. 소비한 비트가 네 개 이상이고 창이1011이면 검출을 기대합니다. FSM 전이표를 테스트벤치에 복사하지 않아 같은 전이 오류를 공유할 가능성을 줄입니다.

겹침·중간 대기·접두사 도중 리셋을 직접 검사한 뒤 길이0~8인 모든 이진 문자열511개를 각각 새 리셋에서 검사합니다. 짧은 입력의 전수 검사이며 임의 길이에 대한 formal 증명은 아닙니다. `BUG_NO_OVERLAP=1`은 완성 후 EMPTY로 돌아가는 의도적 결함으로 같은 검사에서 실패해야 합니다.

## 하드웨어 응용과 한계

유효한 비트 스트림의 짧은 동기어·제어 시퀀스 탐지에 접미사 FSM 구조를 적용할 수 있습니다. 실제 프레임 수신에서는 잘못된 동기어 발생 가능성, 프레임 길이·CRC·오류 복구도 함께 정해야 합니다. 이 회로는 문자열 메모리 검색기나 임의 패턴 프로그래밍 회로가 아니며 패턴을 바꾸려면 상태와 전이를 다시 구성해야 합니다. 합성,STA,보드 입력의 메타안정성·디바운싱 시험은 수행하지 않습니다.

## 실행 환경과 명령

별도의 표준 입력은 없으며 tb.sv의 고정 자극으로 검사합니다. Python 기준 모델만 실행한 결과가 아니라 실제 SystemVerilog 컴파일과 VVP 실행 결과입니다. Icarus의 [-g2012·-s·-o 옵션](https://github.com/steveicarus/iverilog/blob/master/Documentation/usage/command_line_flags.rst)으로 언어·최상위 모듈·산출물을 지정하고 [VVP](https://steveicarus.github.io/iverilog/usage/vvp_flags.html)로 실행합니다. 아래 PowerShell 명령은 저장소 루트에서 시작하여 소스를 새 임시 폴더로 복사합니다. 다른 환경에서는 두 도구 경로를 해당 실행 파일로 바꾸면 됩니다.

```powershell
$source = Resolve-Path '하드웨어코딩_hardware-coding/예제_examples/03-순서검출_sequence-detector'
$build = Join-Path ([IO.Path]::GetTempPath()) ('hardware-example-' + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $build | Out-Null
Copy-Item (Join-Path $source 'sequence_detector.sv'), (Join-Path $source 'tb.sv') $build
Push-Location $build
& 'C:/iverilog/bin/iverilog.exe' -g2012 -gstrict-expr-width -Wall -s tb_sequence_detector -o sim.vvp sequence_detector.sv tb.sv
& 'C:/iverilog/bin/vvp.exe' -n sim.vvp
Pop-Location
```

정상 실행은 PASS와 실제 검사 수를 출력합니다. 실패 시 테스트벤치의 `$fatal(1,...)`이 불일치 시점과 이유를 출력하며 종료 코드는0이 아닙니다. 테스트벤치의 `#5` 클록과 `#1` 관측 지연은 시뮬레이션용이며 합성할 회로 지연을 뜻하지 않습니다.

## 실제 로컬 실행 기록

2026-10-26에 설치된 Icarus Verilog12.0 devel과 VVP로 실행했습니다. 아래 수치는 해당 소스와 자극에서 직접 출력된 값이며 새로운 환경의 실행을 대신하지 않습니다. 전체 명령·종료 코드·stdout·stderr와 소스 SHA-256은 [example.json](example.json)에 기록합니다.

| 설정 | 관측 결과 | 실제 집계 |
| --- | --- | --- |
| normal | PASS; compile=0, sim=0 | checks=4112, samples=3597, pauses=2, resets=513, hits=131, strings=511 |
| negative_no_overlap | EXPECTED_FUNCTIONAL_FAILURE; compile=0, sim=1 | FATAL: tb.sv:24: SEQUENCE sample=7 history=1011 expected=1 actual=0 |

음성 대조의 예상 실패는 결함이 검출되었다는 뜻이며 결함 회로가 정상 기능 검사를 통과했다는 뜻이 아닙니다. 도구 실행·컴파일 실패는 기능 실패와 별도로 확인합니다. 온라인 문제 채점은 수행하지 않았습니다.

## 줄별 문법과 회로 목적

`logic`는4상태 신호의 자료형이며 그 자체로 플립플롭을 뜻하지 않습니다. 조합 블록·연속 연결·클록 저장 중 어디에서 값을 정하는지에 따라 회로 역할이 달라집니다. `always_comb`는 현재 입력과 상태로 조합 값을 계산하고 모든 경로에 기본값을 둡니다. `always_ff`와 `<=`는 상승 에지 이전 상태를 기준으로 다음 저장값을 예약합니다. 테스트벤치의 blocking `=`는 순서대로 기대값을 계산하는 데 사용합니다. 각 실제 소스 줄의 주석에 문법의 역할과 이 회로의 목적을 함께 적었습니다.

### RTL: sequence_detector.sv

```systemverilog
`timescale 1ns/1ps // 시뮬레이션 시간 단위와 정밀도
module sequence_detector #( // 겹침을 허용하는1011 순서 검출기
    parameter bit BUG_NO_OVERLAP = 1'b0 // 음성 대조에서만 켤 접미사 유실 결함
) ( // 포트 목록 시작
    input logic clk, rst, // 단일 클록과 active-high 동기 리셋
    input logic sample_enable, // 이번 에지에 입력 비트를 소비할지 표시
    input logic bit_in, // 소비할 직렬 입력 비트
    output logic hit // 이번에 소비한 비트로1011이 완성된 표시
); // 포트 선언 끝
    typedef enum logic [1:0] {EMPTY, SEEN_1, SEEN_10, SEEN_101} state_t; // 남아 있는 최장 접미사의 네 상태
    state_t state, next_state; // 현재 상태와 다음 에지의 후보 상태
    logic next_hit; // 이번 입력이 패턴을 완성하는지 계산한 값
    always_comb begin // 현재 접미사와 새 비트의 조합 전이
        next_state = state; // 소비하지 않으면 접미사 상태 유지
        next_hit = 1'b0; // 완성한 에지에서만 검출 표시
        if (sample_enable) begin // 유효한 입력 비트가 있는 경우에만 전이
            case (state) // 지금까지의 최장 일치 접미사 구분
                EMPTY: begin // 아직 남길 접두사가 없는 상태
                    if (bit_in) next_state = SEEN_1; // 1은 새 패턴의 시작
                    else next_state = EMPTY; // 0만으로는 시작 접두사 없음
                end // 빈 접미사의 전이 끝
                SEEN_1: begin // 최근 접미사가1인 상태
                    if (bit_in) next_state = SEEN_1; // 11의 마지막1을 새 시작으로 보존
                    else next_state = SEEN_10; // 0을 붙여10까지 일치
                end // 1 접미사의 전이 끝
                SEEN_10: begin // 최근 접미사가10인 상태
                    if (bit_in) next_state = SEEN_101; // 1을 붙여101까지 일치
                    else next_state = EMPTY; // 100에는 시작 접두사 접미사가 없음
                end // 10 접미사의 전이 끝
                SEEN_101: begin // 다음1이면 전체 패턴이 완성되는 상태
                    if (bit_in) begin // 1011 완성
                        next_hit = 1'b1; // 이번 에지의 검출 표시
                        if (BUG_NO_OVERLAP) next_state = EMPTY; // 의도적으로 마지막1의 재사용을 잃는 결함
                        else next_state = SEEN_1; // 마지막1을 다음 패턴의 시작으로 보존
                    end else next_state = SEEN_10; // 1010의 마지막10을 재사용
                end // 101 접미사의 전이 끝
                default: next_state = EMPTY; // 정의되지 않은 상태의 복귀 후보
            endcase // 모든 상태의 전이 계산 끝
        end // 입력 소비 조건 끝
    end // 기본값으로 조합 출력의 래치 방지
    always_ff @(posedge clk) begin // 상승 에지에서 상태와 검출 펄스 저장
        if (rst) begin // 리셋은 입력 소비보다 우선
            state <= EMPTY; // 이전 비트의 접미사 취소
            hit <= 1'b0; // 리셋을 검출로 보고하지 않기
        end else begin // 정상 입력 진행
            state <= next_state; // 조합 전이가 정한 접미사 저장
            hit <= next_hit; // 해당 소비 에지 뒤 한 클록 검출 표시
        end // 리셋과 정상 갱신 분기 끝
    end // 순차 상태 갱신 끝
endmodule // 순서 검출기 끝
```

### 자체 검사: tb.sv

```systemverilog
`timescale 1ns/1ps // 클록과 관측 지연의 시간 단위
module tb_sequence_detector; // 최근 네 비트 기준으로 검사하는 테스트벤치
    parameter bit BUG_NO_OVERLAP = 1'b0; // 겹침 유실 결함의 음성 대조 선택
    logic clk = 0, rst = 1, sample_enable = 0, bit_in = 0, hit; // 시작 전 제어와 관측 출력
    logic [3:0] history = 0; // 유효 입력만 담는 독립 이동 창
    int seen = 0, checks = 0, samples = 0, pauses = 0, resets = 0, hits = 0, strings_checked = 0; // 실제 입력과 검사 수
    sequence_detector #(.BUG_NO_OVERLAP(BUG_NO_OVERLAP)) dut (.*); // 선택한 DUT 설정 연결
    always #5 clk = ~clk; // 주기10ns의 클록
    task automatic step(input bit reset_value, input bit enabled, input bit value); // 입력 비트 한 개 또는 대기 에지 실행
        bit expected_hit; // 내부 FSM 없이 계산할 검출 기대값
        @(negedge clk); rst = reset_value; sample_enable = enabled; bit_in = value; // 상승 에지와 분리해 입력 배치
        @(posedge clk); // 입력을 소비하는 기준 에지
        expected_hit = 0; // 비활성·리셋 에지는 검출 없음
        if (rst) begin // 리셋에서 독립 입력 이력도 지우기
            history = 0; seen = 0; resets++; // 이전 입력과 구분되는 새 스트림
        end else if (sample_enable) begin // 실제로 소비한 비트만 이동 창에 추가
            history = {history[2:0], bit_in}; // 최근 네 비트의 단순 이동
            if (seen < 4) seen++; // 네 비트가 모이기 전의 길이 기록
            expected_hit = seen == 4 && history == 4'b1011; // 완성된 네 비트와 상수 패턴 비교
            samples++; // 소비한 비트 수 집계
        end else pauses++; // 입력 대기 에지 집계
        #1; // DUT의 nonblocking 상태·출력 갱신 후 관측
        checks++; // 실제 출력 비교 수
        if (hit !== expected_hit) $fatal(1, "SEQUENCE sample=%0d history=%04b expected=%0b actual=%0b", samples, history, expected_hit, hit); // 겹침·리셋·대기 차이 검출
        if (hit) hits++; // 실제 패턴 발생 수 기록
    endtask // 한 에지 검사 끝
    initial begin // 직접 흐름과 짧은 문자열 전수 검사
        step(1, 1, 1); // reset과 유효 입력이 함께 와도 이전 이력 삭제
        step(0, 1, 1); step(0, 1, 0); step(0, 1, 1); // 첫 세 비트101
        step(0, 0, 0); step(0, 0, 1); // 중간 대기에서는 입력 값을 소비하지 않기
        step(0, 1, 1); // 첫1011 검출
        step(0, 1, 0); step(0, 1, 1); step(0, 1, 1); // 마지막1을 재사용한 두 번째1011
        if (hits != 2) $fatal(1, "SEQUENCE directed overlap count"); // 겹친 두 발생을 실제로 지났는지 확인
        step(0, 1, 1); step(0, 1, 0); // 리셋 전 접미사10 만들기
        step(1, 1, 1); step(0, 1, 1); step(0, 1, 1); // 리셋 뒤11은 이전10과 결합하지 않기
        for (int length = 0; length <= 8; length++) begin // 길이0~8의 모든 이진 문자열
            for (int pattern = 0; pattern < (1 << length); pattern++) begin // 고정 길이의 모든 값 열거
                step(1, 0, 0); // 각 문자열은 독립 리셋 상태에서 시작
                for (int index = length - 1; index >= 0; index--) begin // 왼쪽 비트부터 시간순 입력
                    step(0, 1, (pattern >> index) & 1); // 열거한 입력을 한 비트씩 소비
                end // 문자열의 모든 비트 입력 끝
                strings_checked++; // 실제로 완료한 문자열 수
            end // 현재 길이의 모든 문자열 끝
        end // 짧은 문자열 전수 검사 끝
        if (strings_checked != 511 || pauses < 2) $fatal(1, "SEQUENCE scenario accounting"); // 전수 범위와 대기 경계 확인
        $display("PASS checks=%0d samples=%0d pauses=%0d resets=%0d hits=%0d strings=%0d", checks, samples, pauses, resets, hits, strings_checked); // 실제 검사와 발생 수 출력
        $finish; // 정상 시뮬레이션 종료
    end // 직접 자극 프로세스 끝
    initial begin #1000000; $fatal(1, "SEQUENCE watchdog"); end // 종료되지 않는 시뮬레이션 제한
endmodule // 순서 검출 테스트벤치 끝
```

## 근거와 직접 구성한 부분

- [Intel SystemVerilog FSM coding example, enum and two processes](https://www.intel.com/content/www/us/en/docs/programmable/683323/current/systemverilog-state-machine-coding-example.html)
- [Berkeley EECS151 FSM style guide](https://eecs151.org/asic/lab3/docs/fsm-style-guide/)
- [Icarus command-line flags](https://github.com/steveicarus/iverilog/blob/master/Documentation/usage/command_line_flags.rst)

회로·테스트 입력·기대값 비교기·음성 대조는 이 저장소에서 직접 구성했습니다. 링크한 공식 문서는 언어·도구·인터페이스 규칙의 근거이며 이 예제의 시험 결과를 보고한 자료는 아닙니다. 문서 열람 기준일은2026-10-26입니다.
