# Amaranth 카운터의 회로 생성과 시간 기반 검증

[하드웨어 학습목차](../../README.md) · [언어와 검증 도구](../../언어와검증도구_languages-and-verification.md)

## Python 프로그램과 생성하는 회로

Amaranth는 Python 문법을 이용하여 레지스터와 조합 회로의 연결을 만드는 하드웨어 구성 도구입니다.
이 예제의 [counter.py](counter.py)는 0부터 9까지 순환하는 enable 카운터를 직접 정의합니다.
상승 에지에서 clear가 1이면 0, 아니면 enable이 1일 때 증가하며, 둘 다 0이면 유지합니다.
[test_counter.py](test_counter.py)는 별도의 Python 코드로 시뮬레이션 시간을 진행하고 결과를 검사합니다.
두 파일의 의미 있는 각 줄에는 문법과 목적을 복습 메모로 적었습니다.

| 구문 | 의미 |
| --- | --- |
| Signal(range(10)) | 0..9를 표현할 네 비트 신호; 십진 순환은 별도 회로 필요 |
| Elaboratable.elaborate | Python을 실행하여 하드웨어 구조 구성 |
| Module.If / Elif | 생성할 회로의 우선순위 선택 |
| module.d.sync += ...eq(...) | 상승 에지에서 저장할 레지스터의 다음 값 |
| ClockDomain(reset_less=True) | 숨은 기본 reset 대신 명시적인 clear 포트를 사용하는 클록 영역 |
| Simulator.add_clock | 회로 밖 검증 환경에서 클록 생성 |
| context.set / get | 시뮬레이션의 입력 설정과 신호 관찰 |
| await context.tick() / delay() | 검증 프로세스가 하드웨어 시간에 맞춰 대기 |

일반 Python if로 입력 신호의 현재 값을 분기하는 소프트웨어와, Module.If로 선택 회로를 만드는 단계는 다릅니다.
test_counter.py의 반복문은 80클록을 검증하며, 그 반복문 자체가 카운터 회로로 합성되지는 않습니다.
펌웨어는 프로세서에서 명령을 실행하지만 이 counter.py는 RTL 구조를 생성합니다.

## 같은 입력의 시간 추적

[VHDL 카운터](../04-카운터와범위_vhdl-counter/README.md)와 같은 입력 계약·클록·정수 기준 모델을 사용합니다.
주기 시작에 입력을 설정하고 4ns에 유지, 5ns 상승 뒤 6ns에 결과를 확인하며 다음 주기는 10ns에 시작합니다.
clear는 주기 번호 0,17,18,47,79에서 1이고 enable은 주기 번호 mod 5가 2일 때만 0입니다.

| 주기 | clear | enable | 상승 뒤 count | 이유 |
| ---: | ---: | ---: | ---: | --- |
| 0 | 1 | 1 | 0 | clear가 우선 |
| 1 | 0 | 1 | 1 | 한 단계 증가 |
| 2 | 0 | 0 | 1 | 정지 상태 유지 |
| 11 | 0 | 1 | 9 | 마지막 십진 값 도달 |
| 12 | 0 | 0 | 9 | 경계에서 정지 |
| 13 | 0 | 1 | 0 | 십진 순환 |
| 18 | 1 | 1 | 0 | 중간 초기화 |
| 79 | 1 | 1 | 0 | 마지막 초기화 |

각 클록에 에지 전 유지·에지 후 기대값·0..9 범위의 세 assert를 실행합니다.
기준 모델은 정수 나머지 연산을 사용하며 DUT는 count=9 비교 회로를 사용합니다.

## 실행 환경

확인한 환경은 Python 3.12.14와 Amaranth 0.5.8입니다.
전역 설치 대신 작업용 임시 디렉터리에 의존성을 설치한 뒤 그 경로를 PYTHONPATH로 전달했습니다.
새 환경에서는 선택한 Python 가상환경에 다음 버전을 설치할 수 있습니다.

```sh
python -m pip install amaranth==0.5.8  # 회로 구성기와 시뮬레이터 준비
python -B test_counter.py  # 실제 시간 기반 검증 실행
```

확인한 표준 출력과 종료 상태는 다음과 같습니다.

```text
PASS mod10_counter cycles=80 checks=240
```

80클록·240assert를 통과했고 프로세스 종료 코드는 0입니다.
실행 명령과 파일 해시는 [example.json](example.json)에 기록합니다.
Python의 -O 옵션은 assert를 제거하므로 이 검증 명령에 사용하지 않습니다.

## RTLIL 출력과 확인 범위

```sh
python -B counter.py --rtlil > counter.il  # 회로 구조를 RTLIL 텍스트로 내보내기
```

RTLIL은 합성 도구가 읽는 회로 중간 표현이며 원래 Python 프로그램을 CPU에서 실행하는 바이너리가 아닙니다.
생성 결과에는 clk·clear·enable·4비트 count 포트와 상태를 저장하는 $dff가 포함됩니다.
emit_src=False로 기계별 소스 경로를 제외한 66줄의 RTLIL 출력을 실제 확인했습니다.
이 출력에는 외부 Yosys 실행이 필요하지 않으며, Verilog 변환이나 합성에는 해당 백엔드의 추가 도구가 필요합니다.
검증 범위는 Amaranth Simulator의 기능과 RTLIL 변환 성공입니다.
합성·배치 배선·장치 타이밍·핀 배정·보드 측정은 별도 단계입니다.

## 실수와 장치 사용 조건

range(10)의 신호 폭은 네 비트이므로 10..15라는 비트 패턴 자체가 물리적으로 없어지는 것은 아닙니다.
정상 초기 상태와 현재 다음 상태 논리에서 0..9가 유지되는지를 테스트하고, 실제 시작 절차에서는 동기 clear를 제공합니다.
외부 비동기 입력은 동기화·디바운스 조건을 따로 설계합니다.
입력 신호의 .eq()는 Python 변수의 즉시 대입이 아니라 회로의 다음 상태·연결을 만드는 표현입니다.

## 공식 참고와 라이선스

[Amaranth 0.5.8 시작 문서](https://amaranth-lang.org/docs/amaranth/v0.5.8/start.html)와 [Simulator 문서](https://amaranth-lang.org/docs/amaranth/v0.5.8/simulator.html)의 회로 구성·시간 진행 API를 참고합니다.
회로와 80클록 검증 시나리오는 이 저장소용 원본이며 공식 counter 예제를 복사하지 않았습니다.
사용한 Amaranth 라이브러리는 [BSD-2-Clause 원문](https://github.com/amaranth-lang/amaranth/blob/v0.5.8/LICENSE.txt)에 따라 배포됩니다.
라이브러리 코드의 재배포 조건과 직접 작성한 학습 예제의 출처는 구분합니다.

## counter.py의 전체 코드

```python
import argparse  # RTLIL 출력 모드의 명령줄 선택
from amaranth import ClockDomain, ClockSignal, Elaboratable, Module, Signal  # 하드웨어 신호와 회로 구성
from amaranth.back import rtlil  # 외부 합성 도구 없이 RTLIL 생성

class Mod10Counter(Elaboratable):  # Python으로 정의하는 회로 생성기
    def __init__(self):  # 회로의 포트와 상태 신호 생성
        self.clear = Signal(name="clear")  # enable보다 우선하는 동기 초기화
        self.enable = Signal(name="enable")  # 1인 클록에서만 증가
        self.count = Signal(range(10), name="count", init=0)  # 표현 폭은 네 비트이며 순환은 직접 정의
    def elaborate(self, platform):  # 회로 구조를 구성하는 단계
        module = Module()  # 동시 회로와 동기 회로를 담는 객체
        module.domains += ClockDomain("sync", reset_less=True)  # 별도 숨은 reset 대신 clear 입력 사용
        with module.If(self.clear):  # 하드웨어 우선순위 선택 회로
            module.d.sync += self.count.eq(0)  # 상승 에지의 초기화 값
        with module.Elif(self.enable):  # clear가 0이고 증가가 허용된 경우
            with module.If(self.count == 9):  # 십진 순환 경계
                module.d.sync += self.count.eq(0)  # 9 다음을 0으로 지정
            with module.Else():  # 0부터 8인 상태
                module.d.sync += self.count.eq(self.count + 1)  # 레지스터의 다음 값
        return module  # 완성한 하드웨어 구조 반환

def main():  # 회로를 파일로 내보내는 독립 실행
    parser = argparse.ArgumentParser()  # 명령줄 도움말 구성
    parser.add_argument("--rtlil", action="store_true", help="emit RTLIL to stdout")  # RTLIL 생성 선택
    arguments = parser.parse_args()  # 실행 옵션 읽기
    if arguments.rtlil:  # 명시적으로 요청한 출력 모드
        dut = Mod10Counter()  # 변환할 회로 구성
        print(rtlil.convert(dut, name="mod10_counter", ports=[ClockSignal("sync"), dut.clear, dut.enable, dut.count], emit_src=False), end="")  # 기계별 소스 경로를 빼고 클록과 세 포트의 RTLIL 출력
    else:  # 시험 실행 명령 안내
        parser.error("use --rtlil; run test_counter.py for simulation")  # 모드 없는 실행은 명확히 구분

if __name__ == "__main__":  # 직접 실행할 때만 변환 시작
    main()  # 입력과 회로 변환 처리
```

## test_counter.py의 전체 코드

```python
from amaranth.sim import Simulator  # HDL 회로를 평가하는 시뮬레이터
from counter import Mod10Counter  # 검증할 원본 회로 생성기

async def bench(context):  # 시뮬레이션 시간에 맞춰 실행하는 테스트벤치
    expected = 0  # Python 정수 modulo의 독립 기준
    checks = 0  # 실제로 수행한 assert 수
    for cycle in range(80):  # VHDL과 같은 클록별 자극
        clearing = cycle in (0, 17, 18, 47, 79)  # 초기화와 증가의 우선순위 검사
        enabled = cycle % 5 != 2  # 주기적으로 증가 정지
        context.set(dut.clear, clearing)  # 상승 에지 전에 초기화 입력 변경
        context.set(dut.enable, enabled)  # 상승 에지 전에 enable 변경
        await context.delay(4e-9)  # 5ns 상승 에지보다 앞선 4ns 시각
        assert context.get(dut.count) == expected, "changed before rising edge"  # 에지 없이 입력만 바뀌면 상태 유지
        checks += 1  # 에지 전 유지 검사 집계
        if clearing:  # 기준 모델의 초기화 우선순위
            expected = 0  # 다음 기준 값
        elif enabled:  # 증가가 허용된 클록
            expected = (expected + 1) % 10  # 명시적 if9 대신 정수 나머지로 비교
        await context.tick()  # 상승 에지와 조합 출력 안정화까지 진행
        await context.delay(1e-9)  # VHDL과 같은 상승 뒤 1ns 검사 시각
        assert context.get(dut.count) == expected, "incorrect count after rising edge"  # 회로 다음 상태 비교
        checks += 1  # 기능 검사 집계
        assert 0 <= context.get(dut.count) <= 9, "count outside decimal range"  # 네 비트의 10부터15를 제외
        checks += 1  # 십진 범위 검사 집계
        await context.delay(4e-9)  # 다음 주기의 입력 변경 시점으로 이동
    print(f"PASS mod10_counter cycles=80 checks={checks}")  # 실제 검사 수와 성공 표식

if __name__ == "__main__":  # 독립 시뮬레이션 실행
    dut = Mod10Counter()  # 테스트할 회로 인스턴스
    simulator = Simulator(dut)  # 회로를 시뮬레이터에 전달
    simulator.add_clock(10e-9)  # 주기10ns, 첫 상승 에지5ns
    simulator.add_testbench(bench)  # 입력 생성과 검사 등록
    simulator.run()  # 테스트벤치가 끝날 때까지 실행
```
