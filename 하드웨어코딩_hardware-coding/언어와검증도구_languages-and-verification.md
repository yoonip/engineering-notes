# 회로 설계 언어·검증 코드·펌웨어의 역할

[하드웨어 학습목차](README.md)

## 같은 프로그램처럼 보여도 다른 실행 대상

회로 설계 코드는 레지스터·조합 논리·연결을 정의합니다.
테스트벤치는 그 회로에 시간에 따른 입력을 주고 출력·프로토콜을 검사합니다.
펌웨어는 이미 존재하는 프로세서가 실행할 명령이며, 주변 장치 레지스터를 읽고 쓰는 프로그램입니다.
한 시스템에서 세 종류가 함께 필요할 수 있지만, 같은 언어 문법이라는 이유로 결과물을 같은 것으로 분류하지 않습니다.

| 언어·도구 | 주된 역할 | 만들어지거나 실행되는 대상 |
| --- | --- | --- |
| Verilog | RTL·구조적 회로 기술과 테스트벤치 | 합성 대상 회로 또는 시뮬레이션 코드 |
| SystemVerilog | Verilog 확장 회로 기술과 검증 | logic·순차/조합 블록, assertion·검증 환경 등 |
| VHDL | 자료형·entity·architecture로 회로 기술과 검증 | 합성 대상 회로 또는 테스트벤치 |
| Amaranth | Python 기반 회로 구성 | 하드웨어 그래프, RTLIL·Verilog 등 |
| Chisel | Scala 기반 회로 생성 | 매개변수화된 하드웨어 구조와 출력 RTL |
| cocotb | Python으로 HDL 시뮬레이터 제어·검사 | 시뮬레이터와 함께 실행되는 테스트벤치 |
| C·C++·Rust·어셈블리 펌웨어 | 프로세서의 동작 정의 | 해당 프로세서가 실행하는 기계어 |

어느 HDL에서도 모든 문법이 합성 가능한 것은 아닙니다.
테스트벤치의 시간 대기·파일 읽기와 실제 회로의 클록·상태 전이를 구분합니다.
시뮬레이션 통과, RTL 변환, 합성, 배치 배선, 보드 측정은 각각 확인한 결과를 따로 기록합니다.

## Verilog·SystemVerilog의 시작 경로

조합 논리의 진리표·비트 폭을 먼저 익힌 뒤 플립플롭·카운터·FSM·메모리 순서로 진행합니다.
블로킹·논블로킹 대입의 효과와 클록 에지에서 상태가 저장되는 시점을 파형으로 확인합니다.
SystemVerilog의 logic나 always_ff 같은 표기는 단순히 소프트웨어 변수를 더 편하게 쓰는 문법이 아니라 회로 의도를 표현하는 도구입니다.
assertion과 검증용 객체·무작위화 기능은 사용하는 시뮬레이터의 지원 범위를 확인합니다.

Project F는 작은 동작을 실제 화면·산술 모듈로 연결하는 원본 설계 프로젝트로 가치가 있습니다.
[공식 강좌 목차](https://projectf.io/tutorials/)에는 보드 입문의 Hello Arty·Hello Nexys와 별도의 그래픽·산술 과정이 있습니다.
처음에는 숫자·벡터·클록의 기본 예제와 보드 없는 테스트벤치를 먼저 다루는 경로를 권합니다.
보드가 있으면 Hello FPGA를 이어서 실행하고, 그래픽은 Beginning FPGA Graphics→Racing the Beam→FPGA Pong 순서로 확장할 수 있습니다.
그 뒤 sprites·framebuffers에서는 메모리·여러 처리 단계·클록 영역의 조건을 함께 읽습니다.
이 순서는 게시된 강좌 구성을 바탕으로 정리한 학습 경로입니다.

[projf-explore 원본 저장소](https://github.com/projf/projf-explore)는 hello·graphics·lib·maths 예제와 지원 환경을 함께 제공합니다.
확인한 저장소 코드는 [MIT 라이선스](https://github.com/projf/projf-explore/blob/main/LICENSE)이며 복사·수정한 상당 부분에는 저작권·허가 고지를 유지합니다.
예를 들어 [고정소수점 나눗셈 div.sv](https://github.com/projf/projf-explore/blob/main/lib/maths/div.sv)도 파일 머리에 MIT를 명시합니다.
강좌 글은 원문 링크로 참조하며, 코드 저장소의 라이선스 범위와 글·그림의 출처를 구분합니다.
보드용 PLL·핀 배정·영상 출력은 해당 보드와 도구에 맞추어야 하며, 산술 모듈의 기능 검사와 별도의 조건입니다.
Project F의 RISC-V 어셈블리 강좌는 프로세서가 실행하는 프로그램 경로로 분류합니다.

## VHDL: 명시적인 자료형과 시간

VHDL에서는 포트를 entity에, 구현을 architecture에 분리하고 signal의 예약 대입과 변수의 즉시 대입을 구분합니다.
[04 카운터 예제](예제_examples/04-카운터와범위_vhdl-counter/README.md)는 같은 클록에서 clear·enable의 우선순위와 9→0 경계를 확인합니다.
첫 진리표 예제는 [GHDL 공식 전가산기·독립 테스트벤치](https://ghdl.github.io/ghdl/quick_start/simulation/adder/index.html)가 적합합니다.
가산기 진리표를 확인한 뒤 카운터·FSM으로 이동하면 조합 출력 안정화와 클록 상태 저장을 비교할 수 있습니다.
GHDL은 실행 도구이며 VHDL이라는 언어 자체의 라이선스를 뜻하지 않습니다.

검증 프로젝트가 커지면 [VUnit 사용자 안내](https://vunit.github.io/user_guide.html)의 테스트별 실행·라이브러리·컴파일 순서 관리를 검토합니다.
VUnit의 Python run.py는 빌드·검사 실행을 조정하고, 테스트벤치는 VHDL 또는 SystemVerilog로 작성합니다.
VUnit 본체는 [MPL-2.0](https://vunit.github.io/)으로 배포되므로 새로 작성한 회로와 외부 검증 라이브러리의 파일을 구분해 관리합니다.
OSVVM을 확장 자료로 사용할 때에는 [유틸리티 코드의 Apache-2.0](https://github.com/OSVVM/OSVVM/blob/master/LICENSE.md)과 [문서의 별도 이용 조건](https://github.com/OSVVM/Documentation)을 구별합니다.
공식 문서 저장소는 번역·슬라이드·웹페이지 같은 파생 문서에 서면 허가를 요구합니다.
학습 본문과 연습 예제는 직접 작성하고 원문은 링크로 연결하는 경로를 사용합니다.

## Amaranth: Python으로 회로 생성

Amaranth의 Python 코드는 실행 시 하드웨어 그래프를 만들고, Simulator나 RTL 출력 백엔드가 그 구조를 사용합니다.
Python 변수의 산술과 Signal에 대한 하드웨어 연산을 구분해야 합니다.
특히 Module.If와 동기 대입은 회로를 정의하고, 테스트벤치의 async·await는 시뮬레이션 시간에 반응합니다.
[05 카운터 예제](예제_examples/05-파이썬회로_amaranth-counter/README.md)는 Python 정수 기준과 실제 Simulator의 신호를 비교합니다.
이어 [0.5.8 공식 시작 문서](https://amaranth-lang.org/docs/amaranth/v0.5.8/start.html)의 구성→시뮬레이션→RTL 변환 흐름을 확인합니다.
Python에 익숙하고 RTL의 신호·에지 개념을 함께 익히려는 학습에 적합합니다.
Python으로 문장을 짧게 썼다고 회로가 자동으로 더 작거나 빠르게 합성되는 것은 아니므로 생성 구조와 도구 결과를 확인합니다.
Amaranth 라이브러리는 [BSD-2-Clause](https://github.com/amaranth-lang/amaranth/blob/v0.5.8/LICENSE.txt)입니다.

## Chisel: 매개변수화된 회로 생성기

Chisel은 Scala 프로그램으로 하드웨어 그래프를 만드는 언어이며, 같은 구조를 폭·개수·연결에 따라 생성하는 데 초점을 둡니다.
Scala 실행 단계의 값과 Chisel의 UInt·레지스터·회로 연결을 구분합니다. [공식 소개](https://www.chisel-lang.org/chisel3/)
공식 [설치·Scala CLI 시작](https://www.chisel-lang.org/docs/installation)과 [조합 회로→순차 회로 설명 순서](https://www.chisel-lang.org/docs/explanations)를 먼저 확인합니다.
[chisel-template](https://github.com/chipsalliance/chisel-template)은 원본 프로젝트 구조와 svsim·Verilator 검사를 살펴볼 수 있는 후보입니다.
Chisel 라이브러리는 [Apache-2.0](https://github.com/chipsalliance/chisel/blob/main/LICENSE), 이 템플릿은 [Unlicense](https://github.com/chipsalliance/chisel-template/blob/main/LICENSE)로 서로 다릅니다.
[Chisel Bootcamp](https://github.com/freechipsproject/chisel-bootcamp)는 Scala·조합·순차·매개변수화 예제의 교육 가치가 있지만, README가 Binder 일부의 노후화와 실행 오류를 명시합니다.
Bootcamp는 Apache-2.0이며 디지털 회로 배경을 전제로 합니다. 현행 도구의 재현 시작점은 현재 공식 설치 문서로 잡습니다.
이 저장소에서는 Chisel을 실행했다고 표시하지 않으며, 관련 원본 프로젝트와 적용 순서를 연결합니다.

## cocotb: 회로를 만드는 Python과 검증하는 Python

cocotb는 VPI·VHPI·FLI 같은 인터페이스로 실행 중인 HDL 시뮬레이터와 연결하는 Python 검증 환경입니다.
HDL로 작성한 DUT를 자극하고 클록·이벤트에 맞춰 신호를 읽는 역할입니다. [공식 개요](https://docs.cocotb.org/en/stable/)
따라서 Amaranth의 RTL 생성과 cocotb의 기존 RTL 검증은 같은 Python을 사용해도 결과물의 역할이 다릅니다.
시작 단계에서는 작은 가산기·플립플롭에 입력과 기대값을 주고, 다음에 clock·reset·ready/valid를 검사하는 경로가 적합합니다.
[현재 First Steps](https://docs.cocotb.org/en/stable/first_steps.html)와 [버전이 고정된 2.0.0 Quickstart](https://docs.cocotb.org/en/v2.0.0/quickstart.html)는 문서 구성이 다릅니다.
예제에 사용할 패키지 버전과 해당 버전의 문서·시뮬레이터 지원을 함께 기록합니다.
cocotb 본체는 [BSD-3-Clause](https://github.com/cocotb/cocotb/blob/master/LICENSE)입니다.
반면 확인한 2.0.0 Quickstart의 [my_design.sv](https://github.com/cocotb/cocotb/blob/v2.0.0/examples/doc_examples/quickstart/my_design.sv)와 [test_my_design.py](https://github.com/cocotb/cocotb/blob/v2.0.0/examples/doc_examples/quickstart/test_my_design.py)는 각각 파일 머리에 CC0-1.0을 표시합니다.
프로젝트의 대표 라이선스와 실제 가져오는 개별 파일의 고지를 함께 기록합니다.

## CPU·검증·아날로그·설계 흐름의 실행 예제

[RISC-V·Rust·cocotb·SPICE·Tcl/SDC·SystemC 실습](언어확장_language-expansion/README.md)에서 CPU 명령과 호출 규약, no_std 프레임 파서, Python 회로 검증, RC 해석, 일반 합성 구조와 제약 생성, FIFO 시간 모형을 읽으실 수 있습니다. 각 예제는 전체 주석 코드·시간 흐름·실제 도구 출력과 한계를 담았습니다. [언어를 고른 기준과 학습 순서](언어확장_language-expansion/검토와학습순서_language-selection.md)는 Chisel·SystemRDL·HLS의 다음 학습 조건도 연결하며 실제 실행한 자료와 조사한 경로를 구분합니다.

## 추천 경로와 확인 결과의 표기

1. 진리표·멀티플렉서·가산기에서 입력과 조합 출력을 비교합니다.
2. 플립플롭·카운터로 클록·초기화·정지·폭·범위를 확인합니다.
3. FSM·메모리·작은 프로토콜에 자기 검사 테스트벤치를 붙입니다.
4. 같은 회로를 다른 기술 방식으로 비교하려면 VHDL 또는 Amaranth의 작은 예제를 선택합니다.
5. 여러 모듈·매개변수화가 실제로 필요해지면 Chisel 같은 생성기를 검토합니다.
6. HDL 검증의 자동화가 필요하면 현재 환경에 맞는 cocotb·VUnit을 선택합니다.
7. 보드와 프로세서 제어를 연결할 때 펌웨어·핀·클록·전압·시간 제약을 별도로 다룹니다.

학습 범위를 늘리기 위해 모든 언어를 동시에 설치하거나 같은 회로를 대규모로 복제할 필요는 없습니다.
이 글의 외부 자료는 공식 출처를 조사해 연결한 학습 경로입니다.
실제로 실행한 로컬 검사는 각 예제의 example.json에 도구·버전·명령·검사 수와 함께 기록합니다.
