# Python 테스트와 Icarus의 카운터·전송 버퍼 연동

[하드웨어 코딩 목차](../../README.md)

cocotb는 Python으로 HDL 시뮬레이터의 입력을 구동하고 출력을 비교하는 검증 도구입니다. 이 예제에서는 SystemVerilog 회로를 실제 Icarus로 컴파일하고, VVP에 VPI 모듈을 연결하여 Python 테스트를 실행합니다. Python에서 정수 모델만 계산한 결과와 구분합니다. [공식 실행기 설명](https://docs.cocotb.org/en/v2.0.0/runner.html)은 HDL 빌드와 테스트 실행의 역할을 설명합니다.

## 회로와 언어의 역할

counter.sv는 enable이 켜진 상승 에지에 0부터 9까지 증가하는 회로입니다. clear가 증가보다 우선하며 리셋 전 초기 레지스터 값은 정하지 않습니다. 카운터 RTL과 두 Python 테스트·실행기는 이 예제를 위해 직접 작성했습니다.

elastic_buffer.sv는 [기존 한 칸 버퍼](../../예제_examples/01-전송대기_elastic-buffer/README.md)의 소스를 바이트 그대로 복사했습니다. 원본을 수정하지 않았으며 원본·복사본 해시를 [example.json](example.json)에 기록합니다. 버퍼의 rst는 저장 취소를 상승 에지에 반영하며, rst가 1인 동안 ready·valid 조합 출력도 0으로 가립니다.

SystemVerilog의 always_ff와 nonblocking 대입이 저장 회로를 정의합니다. Python의 deque와 정수는 기대값을 계산하는 소프트웨어 상태입니다. cocotb Python 테스트 자체를 합성하거나 FPGA에 올린 것은 아닙니다.

## Windows 실행 환경

cocotb 2.0.0을 고정했습니다. 공식 [플랫폼 지원 표](https://docs.cocotb.org/en/v2.0.0/platform_support.html)는 Windows 10·11 x86_64와 CPython 3.12를 포함합니다. [시뮬레이터 지원](https://docs.cocotb.org/en/v2.0.0/simulator_support.html)은 Icarus 11 이상을 명시합니다. 이 기록은 Windows에서 64비트 Icarus 12와 CPython 3.12.14를 사용한 native 실행입니다.

패키지는 임시 --target 폴더에 설치했으며 기존 Python 환경의 패키지를 교체하지 않았습니다. 공식 Python runner API는 실험적 API로 설명되어 있어 이 예제는 2.0.0의 인터페이스에 맞춥니다. Makefile 대신 이 API를 직접 호출합니다. 선택적인 pytest가 없다는 안내는 실패가 아니며 실제 assert와 XML 결과는 동작했습니다.

## 한 주기의 관측 순서

클록 주기는 10ns입니다. 0ns에 입력을 구동하고 4ns에 에지 전 출력을 확인하며, 5ns에 clk를 1로 올립니다. 6ns에는 레지스터 갱신 결과를 확인하고 10ns에 낮춰 다음 주기를 준비합니다.

Timer는 다음 시각으로 이동하고 ReadOnly는 같은 시각의 HDL 계산이 안정된 뒤 읽도록 합니다. RisingEdge에 도달했다는 사실만으로 downstream nonblocking 출력까지 갱신되었다고 가정하지 않는 것이 핵심입니다. 이 시각 구분의 근거는 [공식 timing model](https://docs.cocotb.org/en/v2.0.0/timing_model.html)입니다.

| 카운터 주기 | clear·enable | 에지 전 → 에지 뒤 |
| --- | --- | --- |
| 0 | 1·1 | 초기값은 비교하지 않으며 에지 뒤 0입니다. |
| 1 | 0·1 | 0 → 1입니다. |
| 2 | 0·0 | 1 → 1로 유지합니다. |
| 11 | 0·1 | 8 → 9입니다. |
| 12 | 0·0 | 9 → 9로 유지합니다. |
| 13 | 0·1 | 9 → 0으로 순환합니다. |
| 17·18 | 1·각 주기의 enable | 연속 clear 에지에서 0입니다. |

카운터는 첫 초기화 전 비교를 제외한 에지 전 79회, 에지 뒤 값·범위 각 80회, 순환 횟수 1회로 240개 assert를 실행합니다. 순환 경계를 실제로 다섯 번 지나야 종료합니다.

버퍼는 내부 full·stored를 읽지 않습니다. 실제로 수락한 값만 Python 큐에 넣고 소비된 출력과 비교합니다. 빈 버퍼의 첫 수락, 정체 중 0x11 유지, 같은 에지에 0x11 소비와 0x22 교체, 남은 0x33의 리셋 취소를 직접 자극합니다. 뒤의 규칙 자극과 마지막 배출까지 총 74주기입니다.

## 실제 결과와 결함 대조

2026-10-26에 두 정상 테스트가 실제 Icarus/VVP 안에서 통과했습니다.

| 대상 | 실제 완료 표시 | 범위 |
| --- | --- | --- |
| 카운터 | PASS counter cycles=80 checks=240 wraps=5 | 동기 초기화·정지·순환입니다. |
| 버퍼 | PASS buffer cycles=74 checks=413 | 수락 36·소비 34·취소 2·정체 22·교체 24입니다. |
| 정체 유실 결함 | AssertionError: valid-after cycle=2 | 의도한 잘못된 버퍼를 Python 기준이 검출했습니다. |

--drop-on-stall은 복사본에 이미 있는 의도적 BUG_DROP_ON_STALL 파라미터를 켭니다. 정상 회로의 옵션으로 사용하지 않습니다. 이 음성 대조에서도 카운터는 통과하고 버퍼의 XML에 실제 테스트 실패가 남으며 실행기는 종료 코드 1을 반환했습니다. 컴파일 실패를 결함 검출로 세지 않습니다. 정상 실행은 두 테스트의 XML 행과 failure·error 부재까지 확인합니다.

생산자가 ready=0일 때 valid·data를 유지하는 프로토콜 자체는 이 테스트의 검사 대상이 아닙니다. 규칙 자극에는 수락되지 않은 값을 바꾸는 경우가 있으며, 큐는 수락된 항목만 기대합니다. 소비자가 임의로 오래 멈추는 모든 길이의 흐름이나 CDC·STA·합성·formal 증명·실물 보드 동작을 확인한 기록은 아닙니다.

## 재현 명령

저장소 루트에서 아래 PowerShell 명령을 실행합니다. $py는 사용할 64비트 CPython, Icarus 경로는 해당 설치로 지정합니다. -O를 사용하면 assert가 제거되므로 실행기가 거절합니다.

```powershell
$py = 'C:/path/to/python.exe'
$work = Join-Path (Get-Location) 'tmp/cocotb-example'
& $py -B -m pip install --target (Join-Path $work 'python-deps') 'cocotb==2.0.0'
$env:PYTHONPATH = Join-Path $work 'python-deps'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONDONTWRITEBYTECODE = '1'
& $py -B '하드웨어코딩_hardware-coding/언어확장_language-expansion/02-Python회로검증_cocotb/run.py' --build-dir (Join-Path $work 'normal') --iverilog-bin 'C:/iverilog/bin'
& $py -B '하드웨어코딩_hardware-coding/언어확장_language-expansion/02-Python회로검증_cocotb/run.py' --build-dir (Join-Path $work 'negative') --iverilog-bin 'C:/iverilog/bin' --drop-on-stall
```

마지막 명령은 의도한 실패이며 정상 통과 명령과 구분합니다. 실행 로그의 실제 컴파일·VVP 명령, Python 환경, 종료 코드와 원본 XML은 example.json에 기록합니다. 생성물은 지정한 빌드 폴더에 저장하며 게시 소스를 고치지 않습니다.

## 전체 소스와 줄별 메모

### counter.sv

```systemverilog
`timescale 1ns/1ps // 테스트와 맞출 시뮬레이션 시간 단위
module mod10_counter ( // 0부터 9까지 순환하는 enable 카운터
    input logic clk, clear, enable, // 상승 에지 클록과 우선 초기화·증가 허용
    output logic [3:0] count // 십진 상태를 담는 네 비트
); // 포트 선언 끝
    always_ff @(posedge clk) begin // 상태 변화는 상승 에지에만 반영
        if (clear) count <= 4'd0; // 증가보다 동기 초기화 우선
        else if (enable) begin // 허용한 에지에서만 한 단계 진행
            if (count == 4'd9) count <= 4'd0; // 9 다음은 0
            else count <= count + 4'd1; // 0부터 8은 1씩 증가
        end // enable이 0이면 기존 상태 유지
    end // nonblocking 순차 갱신 끝
endmodule // 직접 구성한 카운터 끝
```

### elastic_buffer.sv

```systemverilog
`timescale 1ns/1ps // 시뮬레이션 시간 단위와 정밀도
module elastic_buffer #( // 한 항목을 보관하는 전송 버퍼
    parameter bit BUG_DROP_ON_STALL = 1'b0 // 음성 대조에서만 켤 의도적인 정체 중 유실
) ( // 포트 목록 시작
    input logic clk, rst, // 단일 클록과 active-high 동기 상태 리셋
    input logic in_valid, // 입력 항목이 유효하다는 표시
    input logic [7:0] in_data, // 입력 항목의8비트 값
    output logic in_ready, // 이번 에지에 입력을 받을 수 있는지 표시
    output logic out_valid, // 보관한 출력 항목의 유효 표시
    output logic [7:0] out_data, // 보관한 출력 값
    input logic out_ready // 소비자가 이번 에지에 받을 수 있는지 표시
); // 포트 선언 끝
    logic full; // 한 칸의 점유 여부
    logic [7:0] stored; // 다음 소비 때까지 보존할 항목
    always_comb begin // 현재 상태와 소비 준비로 조합 출력 계산
        in_ready = !rst && (!full || out_ready); // 빈 칸이 있거나 이번 항목을 비우면 새 입력 허용
        out_valid = !rst && full; // 리셋 중에는 이전 항목을 전송하지 않기
        out_data = stored; // 유효할 때만 의미가 있는 저장 값 연결
    end // 모든 조합 출력을 항상 할당해 래치 방지
    always_ff @(posedge clk) begin // 상승 에지에서만 저장 상태 변경
        if (rst) begin // 리셋이 입력·출력 전송보다 우선
            full <= 1'b0; // 보관 중인 항목 취소
            stored <= 8'd0; // 리셋 뒤 관측할 값을 정해두기
        end else if (BUG_DROP_ON_STALL && full && !out_ready) begin // 잘못된 정체 처리의 음성 대조
            full <= 1'b0; // 의도적으로 미소비 항목을 버리기
        end else if (in_ready) begin // 칸을 채우거나 비울 수 있는 에지
            full <= in_valid; // 새 입력이 있으면 점유하고 없으면 비우기
            if (in_valid) stored <= in_data; // 수락한 항목만 저장 값으로 반영
        end // 정체 중에는 할당 없이 이전 값 유지
    end // 순차 상태 갱신 끝
endmodule // 전송 대기 버퍼 끝
```

### test_counter.py

```python
import cocotb  # HDL 시뮬레이터 안에서 Python 테스트 등록
import sys  # 내장 Python의 실제 실행 버전 확인
from cocotb.triggers import ReadOnly, Timer  # 시간 이동과 안정된 출력 관측

@cocotb.test()  # 이 코루틴을 실제 시뮬레이션 테스트로 등록
async def counter_boundaries(dut):  # DUT 핸들로 외부 포트만 사용
    print(f"RUNTIME python={sys.version.split()[0]}")  # 도구 빌드 배너와 실제 런타임 버전 구분
    expected = 0  # 첫 clear 뒤부터 사용할 독립 정수 기준
    checks = 0  # 실제 실행한 assert 수
    wraps = 0  # enable이 켜진 9에서 0으로의 전이 수
    dut.clk.value = 0  # 첫 상승 에지 전의 낮은 클록
    for cycle in range(80):  # 재현 가능한 80주기 자극
        clear = int(cycle in (0, 17, 18, 47, 79))  # 시작·연속·중간·마지막 초기화
        enable = int(cycle % 5 != 2)  # 매 다섯 주기마다 한 번 정지
        dut.clear.value = clear  # 초기화 입력 구동
        dut.enable.value = enable  # 증가 허용 입력 구동
        await Timer(4, unit="ns")  # 주기의 4ns 위치로 이동
        await ReadOnly()  # 해당 시각의 HDL 평가가 끝난 뒤 읽기
        if cycle > 0:  # 리셋 전 첫 레지스터 값은 가정하지 않기
            assert int(dut.count.value) == expected, f"pre-edge cycle={cycle}"  # 클록 전 값 유지
            checks += 1  # 실제 비교 한 건 집계
        if clear:  # 모델도 clear 우선
            expected = 0  # 리셋 후 기준값
        elif enable:  # 정지 주기에는 기준도 유지
            wraps += int(expected == 9)  # 실제 순환 경계 집계
            expected = (expected + 1) % 10  # RTL 조건식 대신 정수 나머지 기준
        await Timer(1, unit="ns")  # 주기의 5ns 상승 에지 위치
        dut.clk.value = 1  # 실제 HDL 플립플롭 구동
        await Timer(1, unit="ns")  # nonblocking 갱신 이후의 6ns 위치
        await ReadOnly()  # 안정된 레지스터 출력 읽기
        actual = int(dut.count.value)  # X가 남으면 정수 변환도 실패
        assert actual == expected, f"post-edge cycle={cycle}"  # 계산한 다음 상태와 대조
        assert 0 <= actual <= 9, f"decimal range cycle={cycle}"  # 십진 범위 유지
        checks += 2  # 값·범위 두 비교 집계
        await Timer(4, unit="ns")  # 다음 주기의 0ns 위치
        dut.clk.value = 0  # 다음 상승 에지를 위한 하강
    assert wraps == 5  # 순환 경계를 실제로 다섯 번 통과했는지 확인
    checks += 1  # 시나리오 검사도 실제 개수에 포함
    print(f"PASS counter cycles=80 checks={checks} wraps={wraps}")  # 완료 근거를 로그에 남기기
```

### test_buffer.py

```python
from collections import deque  # 수락 순서만 저장하는 독립 기준 큐
import cocotb  # HDL 시뮬레이터 안의 테스트 등록
import sys  # 내장 Python의 실제 실행 버전 확인
from cocotb.triggers import ReadOnly, Timer  # 시간과 안정된 관측 시점 제어

@cocotb.test()  # 버퍼 한 개의 기능 테스트 등록
async def stalls_replacement_and_reset(dut):  # DUT 내부 full·stored는 읽지 않기
    print(f"RUNTIME python={sys.version.split()[0]}")  # 내장 Python의 실제 런타임 버전 기록
    queue = deque()  # 아직 소비되지 않은 외부 항목
    accepted = consumed = cancelled = stalls = replacements = checks = 0  # 실제 사건 집계
    stimuli = [(1, 1, 255, 1), (0, 1, 17, 0), (0, 0, 17, 0), (0, 1, 34, 0), (0, 1, 34, 1), (0, 0, 0, 1), (0, 1, 51, 0), (1, 1, 68, 1)]  # 직접 구성한 핵심 경계
    stimuli += [(int(i == 31), int(i % 4 != 0), i, int(i % 5 >= 2)) for i in range(64)]  # 속도 차이와 중간 리셋
    stimuli += [(0, 0, 0, 1), (0, 0, 0, 1)]  # 마지막 항목 소비와 가짜 출력 검사
    dut.clk.value = 0  # 첫 클록 전의 기준 수준
    for cycle, (reset, valid, data, ready) in enumerate(stimuli):  # 고정된 74주기 자극
        dut.rst.value = reset  # 리셋은 출력 마스킹과 에지 취소에 사용
        dut.in_valid.value = valid  # 이번에 제시한 입력의 유효 표시
        dut.in_data.value = data  # 8비트 입력 값
        dut.out_ready.value = ready  # 소비자가 받을 수 있는지 표시
        await Timer(4, unit="ns")  # 상승 에지 이전의 관측 위치
        await ReadOnly()  # ready·valid 조합 출력이 안정된 뒤 읽기
        can_accept = not reset and (not queue or ready)  # 빈자리 또는 같은 에지의 소비
        has_output = not reset and bool(queue)  # 리셋 중에는 출력 전송 없음
        assert int(dut.in_ready.value) == can_accept, f"ready cycle={cycle}"  # 수락 가능 여부 대조
        assert int(dut.out_valid.value) == has_output, f"valid-before cycle={cycle}"  # 에지 전 항목 존재 대조
        checks += 2  # 두 제어 신호 비교 집계
        if has_output:  # 유효할 때만 데이터에 의미 부여
            assert int(dut.out_data.value) == queue[0], f"data-before cycle={cycle}"  # 값과 순서 유지
            checks += 1  # 데이터 비교 집계
        stalls += int(has_output and not ready)  # 정체를 실제 관측
        replacements += int(has_output and ready and valid and can_accept)  # 동시 소비와 교체 관측
        if reset:  # 리셋 에지에서는 수락과 소비 대신 취소
            cancelled += len(queue)  # 취소한 항목 개수
            queue.clear()  # 이전 구간의 항목 제거
        else:  # 정상 에지의 외부 전송 계약
            if has_output and ready:  # 이전 출력부터 소비
                queue.popleft()  # 앞 항목 제거
                consumed += 1  # 실제 소비 집계
            if valid and can_accept:  # 수락한 입력만 기대 큐에 추가
                queue.append(data)  # 새 항목의 순서 보관
                accepted += 1  # 실제 수락 집계
        await Timer(1, unit="ns")  # 주기의 5ns 위치
        dut.clk.value = 1  # DUT의 저장 에지 발생
        await Timer(1, unit="ns")  # 순차 갱신이 끝난 6ns 위치
        await ReadOnly()  # 갱신된 출력 관측
        assert len(queue) <= 1, f"capacity cycle={cycle}"  # 한 칸의 기대 점유 상한
        assert int(dut.out_valid.value) == (not reset and bool(queue)), f"valid-after cycle={cycle}"  # 에지 뒤 유효 상태
        checks += 2  # 용량·유효 상태 비교 집계
        if not reset and queue:  # 새 출력 또는 정체로 보존한 항목
            assert int(dut.out_data.value) == queue[0], f"data-after cycle={cycle}"  # 내용이 유실되거나 바뀌지 않기
            checks += 1  # 에지 뒤 데이터 비교 집계
        await Timer(4, unit="ns")  # 다음 주기로 이동
        dut.clk.value = 0  # 다음 상승 에지 준비
    assert not queue  # 마지막 항목이 남지 않아야 종료
    assert accepted == consumed + cancelled  # 수락 항목의 개수 보존
    assert stalls > 0 and replacements > 0 and cancelled > 0  # 핵심 시나리오가 실제로 실행됨
    checks += 3  # 마지막 세 조건도 집계
    print(f"PASS buffer cycles={len(stimuli)} checks={checks} accepted={accepted} consumed={consumed} cancelled={cancelled} stalls={stalls} replacements={replacements}")  # 실제 결과 출력
```

### run.py

```python
import argparse  # 도구와 빌드 위치 선택
import logging  # 실제 컴파일·VVP 명령을 실행 로그에 표시
import os  # Icarus 실행 경로와 Python 환경 연결
from pathlib import Path  # 원본과 임시 경로 구분
import shutil  # 원본을 바이트 그대로 복사
import sys  # 시뮬레이터의 Python 모듈 검색 경로
import xml.etree.ElementTree as ET  # cocotb의 실제 테스트 결과 확인
from cocotb_tools.runner import get_runner  # 고정 버전의 공식 Python 실행기

def main():  # 두 회로의 실제 Icarus 연동 실행
    parser = argparse.ArgumentParser()  # 명령줄 인자 구성
    parser.add_argument("--build-dir", type=Path, required=True)  # 생성물은 명시한 임시 폴더로 한정
    parser.add_argument("--iverilog-bin", type=Path)  # PATH에 없는 Icarus 설치도 선택
    parser.add_argument("--drop-on-stall", action="store_true")  # 음성 대조에서만 기존 DUT의 의도한 결함 선택
    args = parser.parse_args()  # 사용자 입력 읽기
    if sys.flags.optimize:  # assert가 지워진 Python 실행 거절
        parser.error("run without -O")  # 검사 생략을 통과로 기록하지 않기
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")  # 실제 도구 명령을 보존할 로거
    if args.iverilog_bin:  # 두 실행 파일을 같은 설치에서 찾기
        os.environ["PATH"] = str(args.iverilog_bin.resolve()) + os.pathsep + os.environ["PATH"]  # 도구 경로 우선
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"  # 게시 소스에 캐시를 만들지 않기
    os.environ.pop("PYTHONOPTIMIZE", None)  # 내장 Python에서도 assert 유지
    source = Path(__file__).resolve().parent  # 이 예제의 소스 폴더
    base = args.build_dir.resolve()  # 기존 파일을 지우지 않는 생성물 위치
    base.mkdir(parents=True, exist_ok=True)  # 빌드 부모 폴더 준비
    for name, rtl, top, test in [("counter", "counter.sv", "mod10_counter", "test_counter"), ("buffer", "elastic_buffer.sv", "elastic_buffer", "test_buffer")]:  # DUT별 독립 빌드
        work = base / name  # 두 회로의 결과 충돌 방지
        work.mkdir(exist_ok=True)  # 해당 작업 공간 준비
        for filename in (rtl, test + ".py"):  # 필요한 RTL과 테스트만 복사
            shutil.copyfile(source / filename, work / filename)  # 개행·인코딩을 바꾸지 않는 복사
        sys.path.insert(0, str(work))  # 시뮬레이터 안에서 테스트 모듈 찾기
        runner = get_runner("icarus")  # 실제 Icarus/VPI 실행기 선택
        parameters = {"BUG_DROP_ON_STALL": 1} if name == "buffer" and args.drop_on_stall else {}  # 정상 DUT와 명시한 결함 대조 분리
        runner.build(sources=[work / rtl], hdl_toplevel=top, build_dir=work, always=True, build_args=["-g2012"], parameters=parameters)  # SystemVerilog 회로 컴파일
        results = runner.test(hdl_toplevel=top, test_module=test, build_dir=work, test_dir=work, results_xml="results.xml", seed=20261026)  # 고정 시드의 내장 Python 테스트
        root = ET.parse(results).getroot()  # 종료 코드 외에 실제 테스트 행 확인
        cases = list(root.iter("testcase"))  # 완료한 cocotb 테스트 목록
        assert len(cases) == 1 and not any(list(root.iter(tag)) for tag in ("failure", "error", "skipped")), name  # 실패·오류·건너뜀 없는 한 테스트 완료
        print(f"PASS integration dut={name} tests={len(cases)}")  # 회로별 통합 완료 표시

if __name__ == "__main__":  # import로 빌드를 시작하지 않기
    main()  # 명시적으로 실행한 경우만 도구 호출
```

## 출처와 라이선스

- [cocotb 2.0.0 설치](https://docs.cocotb.org/en/v2.0.0/install.html)·[플랫폼](https://docs.cocotb.org/en/v2.0.0/platform_support.html)·[시뮬레이터](https://docs.cocotb.org/en/v2.0.0/simulator_support.html)는 실제 조합을 선택한 근거입니다.
- [cocotb timing model](https://docs.cocotb.org/en/v2.0.0/timing_model.html)·[Python runner](https://docs.cocotb.org/en/v2.0.0/runner.html)는 API와 관측 단계의 근거입니다. 공식 예제 코드를 복사한 것은 아닙니다.
- [cocotb 라이선스](https://raw.githubusercontent.com/cocotb/cocotb/v2.0.0/LICENSE)는 BSD 3-Clause이며, [Icarus의 COPYING](https://raw.githubusercontent.com/steveicarus/iverilog/master/COPYING)은 GPLv2를 제시합니다. 이 폴더에는 도구 바이너리나 라이브러리 소스를 재배포하지 않습니다. 회로·테스트 소스와 사용한 도구의 라이선스는 별개입니다.

공식 자료 열람과 로컬 실행 기준일은 2026-10-26입니다.
