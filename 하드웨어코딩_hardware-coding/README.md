# 하드웨어 코딩 문제와 실행 예제 | Hardware coding practice

Verilog 회로를 제출하는 온라인 문제, 직접 설계한 SystemVerilog 회로, VHDL과 Amaranth 예제를 연결합니다. 각 풀이에는 주석을 단 소스와 테스트벤치, 입력에서 출력까지의 시간 흐름, 실무에서 쓰이는 위치와 검증 범위를 적었습니다.

[처음으로](../README.md) · [학습 사이트와 코드 출처](학습사이트와코드출처_hardware-resources.md) · [언어와 검증 도구](언어와검증도구_languages-and-verification.md) · [실행·채점 기록](확인기록_validation.md)

## CPU 실행·아날로그·검증·설계 자동화

[언어와 도구의 확장 실습](언어확장_language-expansion/README.md)은 RISC-V 어셈블리·Rust·cocotb·SPICE·Tcl/SDC·SystemC를 연결합니다. [선정 이유와 학습 순서](언어확장_language-expansion/검토와학습순서_language-selection.md)에서 각 도구가 다루는 대상과 기존 HDL 학습에서 이어갈 지점을 설명합니다. 확장 실습은 각 폴더의 별도 명령으로 실행하며, [실행 기록](언어확장_language-expansion/확인기록_validation.md)에서 확인한 범위를 구분합니다.

## 무엇부터 공부할지

| 목표 | 시작할 자료 | 다음 단계 |
| --- | --- | --- |
| 프로그래머스처럼 작은 회로를 제출하고 결과 확인 | [HDLBits 풀이](HDLBits/README.md) | 조합회로 → 레지스터 → 리셋·활성화 → 상태기계 |
| 클록마다 데이터가 움직이는 과정 이해 | [전송 대기 버퍼](예제_examples/01-전송대기_elastic-buffer/README.md) | 정체와 동시 입출력, 데이터 취소 조건 |
| 주변 장치와 비트 단위로 통신 | [UART 송신기](예제_examples/02-직렬송신_uart-tx/README.md) | 시작·데이터·정지 비트와 비트당 클록 수 |
| 과거 입력을 기억해 조건 검출 | [1011 순서 검출기](예제_examples/03-순서검출_sequence-detector/README.md) | 상태 전이와 겹치는 입력 패턴 |
| 같은 회로를 다른 언어로 표현 | [VHDL 카운터](예제_examples/04-카운터와범위_vhdl-counter/README.md), [Amaranth 카운터](예제_examples/05-파이썬회로_amaranth-counter/README.md) | 같은 자극·시간·기대값을 사용한 비교 |
| FPGA 그래픽·프로세서·칩 제작으로 확장 | [외부 자료의 형태와 학습 순서](학습사이트와코드출처_hardware-resources.md) | Project F·Tiny Tapeout 등의 공식 프로젝트 |

HDLBits는 [공식 소개](https://hdlbits.01xz.net/wiki/Main_Page)에서 Verilog 회로를 참조회로와 비교하는 온라인 채점을 설명합니다. EDA Playground처럼 코드를 실행할 수 있는 도구와, 문제마다 정답을 판정하는 사이트는 기능이 다릅니다. 각 자료의 형태는 출처 안내에서 구분합니다.

## 소프트웨어 문제 풀이와 다른 점

프로그램에서 `for`를 실행하면 보통 반복할 시간이 필요합니다. 합성할 회로의 고정 범위 반복문은 여러 연결과 연산기를 만드는 표현이 될 수 있습니다. 문장 수보다 어떤 조합논리와 레지스터가 만들어지는지 먼저 확인합니다. Python 기반 Amaranth에서도 Python은 회로를 구성하는 언어이고, 만들어진 레지스터는 클록에 맞춰 동작합니다. [언어별 역할](언어와검증도구_languages-and-verification.md)에서 예제를 비교합니다.

```mermaid
flowchart LR
    A[입력·리셋·클록 조건] --> B[조합논리로 다음 값 계산]
    B --> C[클록 에지에서 레지스터 갱신]
    C --> D[출력·전송 여부 확인]
    C --> B
    E[독립 기대값과 입력 시나리오] --> D
```

조합회로는 입력을 바꾼 뒤 출력이 안정된 시점을 확인합니다. 순차회로는 에지 전 값과 에지 후 값을 나누고, 동기식·비동기식 리셋의 차이도 검사합니다. 테스트벤치의 `#` 지연이나 파일 출력은 시뮬레이션을 위한 코드이므로 그대로 회로 소자가 되는 것으로 읽지 않습니다.

## 회로를 푸는 순서

1. 포트의 방향·폭·부호와 출력이 유효한 시점을 적습니다.
2. 조합논리인지, 과거를 기억할 상태가 필요한지 나눕니다.
3. 리셋·로드·활성화가 동시에 들어올 때의 우선순위를 정합니다.
4. 진리표나 상태 전이표에서 회로를 만들고, 모든 조합 경로에 값을 할당합니다.
5. 작은 값의 전 조합, 경계값, 중간 리셋, 입력 정체를 독립 기대값과 비교합니다.
6. 파형에서 입력 → 에지 → 레지스터 → 출력의 순서를 확인합니다.

전송 버퍼에서는 `valid`가 있다는 것과 실제 전송이 일어났다는 것을 구분해야 합니다. UART에서는 출력 비트의 값뿐 아니라 유지한 클록 수도 맞아야 합니다. 이런 조건을 명세와 테스트벤치에 함께 넣어야 회로가 겉보기에만 맞는 상황을 줄일 수 있습니다.

## 검증과 재실행

문제별 사이트 채점 화면은 [HDLBits 채점 기록](HDLBits/확인기록_online-grading.md)에 연결합니다. 로컬 시뮬레이션은 [통합 실행 기록](확인기록_validation.md)과 각 폴더의 메타데이터에서 확인합니다. 정상 회로의 통과와 의도적으로 결함을 넣은 회로의 검출도 구분합니다.

저장소 루트에서 다음 명령을 사용합니다. 도구가 PATH에 없으면 해당 실행 파일을 지정합니다. Amaranth는 예제에서 사용한 판본 `0.5.8`을 별도 Python 환경에 설치하거나 `--python-deps`로 설치 위치를 전달합니다.

```bash
python 하드웨어코딩_hardware-coding/check_hardware.py --help
python 하드웨어코딩_hardware-coding/check_hardware.py --iverilog /path/to/iverilog --vvp /path/to/vvp --ghdl /path/to/ghdl --build-dir /path/to/new-build --out /path/to/new-report.json
```

기능 시뮬레이션의 통과는 특정 FPGA의 배치·배선, 정적 타이밍 분석, 핀 전압, 실제 보드 동작을 확인한 결과와 구분합니다. Amaranth의 RTLIL 생성도 변환된 회로를 별도 도구로 다시 시험한 결과와 구분합니다.

## 기존 자료와 연결

- [RTL 설계](../전자컴퓨터공학_ece/13-RTL설계_verilog-systemverilog/README.md): 조합·순차논리, FSM·FIFO의 기본 개념
- [하드웨어 검증](../전자컴퓨터공학_ece/14-하드웨어검증_hardware-verification/README.md): 검증 계획과 기준 모델
- [FPGA·ASIC 설계](../전자컴퓨터공학_ece/15-FPGA-ASIC설계_fpga-asic/README.md): 구현 도구와 물리 조건
- [RTL·CDC·DDR 오류 재현](../예제_examples/실무검증_practical-validation/README.md): 잘못된 조건과 해결한 조건의 비교
- [임베디드 디버깅 실습](../예제_examples/임베디드디버깅_embedded-debug-labs/README.md): CPU에서 실행하는 펌웨어와 장치 디버깅

외부 문제의 원문·도표와 공개 예제의 코드는 이용 조건이 다를 수 있습니다. 이 폴더의 풀이와 회로는 직접 작성하고, 원문은 공식 링크로 연결합니다. 외부 자료를 읽는 경로와 직접 실행한 범위는 각각 출처 안내와 확인 기록에 적습니다.

## English

Verilog exercises with recorded HDLBits results, original SystemVerilog circuits with self-checking testbenches, and VHDL/Amaranth counter examples. Each example documents its interface, cycle trace, annotated source, independent checks and limits. Local functional simulation, online judging, RTL generation and physical hardware validation are recorded separately. The resource guide links to official practice platforms, tutorials and licensed example projects.
