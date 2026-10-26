# 하드웨어 코딩 학습 사이트와 코드 출처

Verilog·SystemVerilog·VHDL 회로 설계, Python 기반 HDL, 어셈블리 실습에 사용할 수 있는 자료를 비교합니다. 확인일은 2026년 10월 26일입니다. 사이트의 문제 전체를 풀었다는 목록이 아니며, 이 저장소에서 다룬 일부 직접 풀이와 로컬 예제의 출처를 찾기 위한 문서입니다. 실제 사이트 채점 통과 여부와 로컬 테스트 결과는 각 풀이의 기록으로 구분합니다.

공식 설명과 저자 저장소에서 확인한 내용은 아래에 연결합니다. 기계 판독용 확인 범위와 미확인 항목은 [sources.json](sources.json)에 있습니다. 로그인 정책·도구 제공 범위·제작 비용은 이후 바뀔 수 있습니다.

## 실습 방식 비교

| 자료 | 주된 언어·대상 | 실습과 판정 방식 | 비용·로그인 | 권장 용도 |
|---|---|---|---|---|
| [HDLBits](https://hdlbits.01xz.net/wiki/Main_Page) | Verilog | 제출한 회로를 테스트 벡터로 시뮬레이션하고 기준 회로와 비교합니다. | 공개 웹 연습이며, 계정은 진행 기록을 다른 브라우저로 옮기는 데 사용합니다. | 문법과 작은 조합·순차 회로를 처음 연습합니다. |
| [ASMBits](https://asmbits.01xz.net/wiki/Main_Page) | ARMv7·Nios II 어셈블리 | 함수 실행 결과를 기준 해답과 비교합니다. | 공개 웹 연습이며, 계정은 진행 기록용으로 안내합니다. | 레지스터·함수 호출·메모리 접근을 익힙니다. |
| [CPUlator](https://cpulator.01xz.net/doc/) | Nios II·ARMv7·RISC-V·MIPS | CPU·메모리·입출력 장치를 시뮬레이션하고 디버깅합니다. 정답 비교 문제은행은 아닙니다. | 공개 브라우저 도구입니다. 확인한 시작 안내에는 계정 요구가 없습니다. | ASMBits 풀이를 단일 단계로 실행하며 상태를 관찰합니다. |
| [Nand2Tetris](https://www.nand2tetris.org/course) | 교육용 Hack HDL·어셈블리 등 | 제공된 시뮬레이터에서 테스트 스크립트와 비교 파일로 검사합니다. | 비영리 학습용 자료를 공개합니다. 외부 강좌·인증서와는 구분합니다. | 게이트에서 CPU로 이어지는 구조를 비공개 개인 실습으로 공부합니다. |
| [Nandland](https://nandland.com/) | Verilog·VHDL | 설명과 완성 모듈을 읽고 로컬 시뮬레이터·FPGA에서 실습합니다. | 공개 튜토리얼과 유료 책·보드는 별개입니다. | 두 HDL의 문법과 기본 회로를 비교합니다. |
| [Project F](https://projectf.io/verilog-lib/) | Verilog 계열 RTL·FPGA | 모듈·테스트벤치·문서를 이용한 로컬 실습입니다. | 공개 문서·저장소이며, 실제 보드 실습에는 별도 하드웨어가 필요할 수 있습니다. | 수 표현을 익힌 뒤 화면 출력·메모리·UART로 확장합니다. |
| [EDA Playground](https://eda-playground.readthedocs.io/en/latest/intro.html) | Verilog·SystemVerilog·VHDL·SystemC 등 | 브라우저에서 시뮬레이션·합성·파형을 실행합니다. 판정은 작성한 테스트벤치에 달려 있습니다. | 실행에는 로그인이 필요합니다. 일부 상용 도구는 추가 신원 확인과 제한 이용 조건이 있습니다. | 설치 전에 작은 언어 예제와 테스트벤치를 실행합니다. |
| [VHDLweb](https://vhdlweb.com/) | VHDL | 브라우저 예제·연습 도구입니다. 이번 확인에서는 실제 문제의 최종 채점 화면을 확인하지 못했습니다. | 공식 안내에는 일반 방문자의 연습과 Tufts 수강생의 학점용 로그인을 구분합니다. 현재 실행 가능 여부는 별도 확인이 필요합니다. | VHDL 웹 연습 후보로 살펴봅니다. |
| [Tiny Tapeout](https://tinytapeout.com/hdl/) | HDL 기반 ASIC 설계 | 템플릿·cocotb 테스트·CI·물리 설계 흐름을 제공합니다. 알고리즘 정답 채점 사이트는 아닙니다. | 문서는 공개합니다. GitHub 연동과 실제 칩 제작·구매는 별도 절차·비용이 있습니다. | 작은 RTL과 테스트벤치를 익힌 뒤 ASIC 흐름으로 연결합니다. |
| [cocotb](https://docs.cocotb.org/en/v2.0.0/quickstart.html) | Python 테스트벤치와 Verilog·VHDL DUT | 외부 HDL 시뮬레이터에서 Python의 검사식으로 자동 테스트합니다. | 오픈소스 로컬 도구이며 계정이 필요하지 않습니다. 시뮬레이터의 이용 조건은 별도입니다. | 클록·리셋·경계 입력을 반복 검사합니다. |
| [Amaranth](https://amaranth-lang.org/docs/amaranth/v0.5.8/start.html) | Python 기반 HDL | 회로를 생성하고 시뮬레이션하거나 Verilog로 변환합니다. | 오픈소스 로컬 도구이며 계정이 필요하지 않습니다. | Python 문법으로 조합·동기 회로를 기술합니다. |
| [Amaranth exercises](https://github.com/XekriRedmane/amaranth-exercises) | Amaranth·형식 검증 | 저자 연습 문제를 로컬에서 풀고 SymbiYosys의 cover·BMC 등으로 검사합니다. | 공개 저자 저장소입니다. 읽기에는 GitHub 계정이 필요하지 않습니다. | Amaranth 기초 뒤에 속성 작성과 반례 추적을 연습합니다. |

## 처음 시작할 때의 순서

1. Verilog를 처음 사용한다면 [HDLBits 문제 목록](https://hdlbits.01xz.net/wiki/Problem_sets)의 Getting Started부터 시작합니다. wire·vector·조합 회로를 연습한 뒤 D 플립플롭·카운터·상태 기계로 진행합니다. 공식 안내처럼 언어 항목과 회로 항목을 함께 공부합니다.
2. 같은 회로를 Verilog와 VHDL로 비교하려면 Nandland의 기본 문법과 가산기·멀티플렉서 예제를 참고합니다. 실행 환경은 로컬 시뮬레이터 또는 EDA Playground에서 선택합니다.
3. 클록과 리셋을 다룰 수 있게 되면 직접 작성한 테스트벤치 또는 cocotb로 정상 입력·경계 입력·연속 동작을 검사합니다. 파형이 그려졌다는 사실과 검사식을 모두 통과했다는 사실은 구분합니다.
4. 작은 회로를 연결하는 단계에서는 Project F의 모듈과 테스트벤치를 참고합니다. Python 기반 HDL을 원한다면 Amaranth의 버전을 고정한 Getting started 예제를 먼저 실행합니다.
5. 디지털 회로와 소프트웨어의 연결을 공부하려면 ASMBits와 CPUlator를 함께 사용합니다. ASIC 제작 흐름은 이후 Tiny Tapeout 템플릿으로 살펴봅니다. Nand2Tetris는 저자의 공개 해답 게시 자제 요청을 지키며 별도 개인 실습으로 진행합니다.

## 사이트별 출처와 이용 조건

### 1. HDLBits: 기준 회로와 비교하는 Verilog 연습

[공식 첫 문제](https://hdlbits.01xz.net/wiki/Step_one)는 `top_module`의 이름과 포트를 유지하고 회로 본문을 작성하는 방법을 설명합니다. 컴파일 실패·시뮬레이션 실패·출력 불일치·성공을 구분하며, 불일치가 생기면 제출 회로와 기준 회로의 파형을 비교할 수 있습니다. [일반 Icarus Verilog 실행 페이지](https://hdlbits.01xz.net/wiki/Iverilog)는 임의 코드를 실행하는 기능으로, 문제별 기준 해답 채점과는 용도가 다릅니다.

[소개](https://hdlbits.01xz.net/wiki/Project:About)와 확인한 문제·안내 페이지에서는 문제 본문·그림·채점용 테스트의 일괄 재배포를 허용하는 명시적 라이선스를 확인하지 못했습니다. 이 저장소에는 문제 링크와 직접 작성한 회로·설명을 남기며, 사이트의 문제 본문·그림·비공개 테스트를 모아 복제하지 않습니다. `hdlbits.01xz.net`을 이 문서의 HDLBits 주소로 사용합니다.

### 2. ASMBits: 함수 단위 어셈블리 채점

[공식 안내](https://asmbits.01xz.net/wiki/Main_Page)는 ARMv7 또는 Nios II를 선택하고 짧은 함수를 작성해 제출하는 흐름을 설명합니다. 테스트 입력에 대한 실행 결과를 기준 해답과 비교하므로, 회로 합성 문제와는 구분되는 컴퓨터 구조 연습입니다. 처음에는 함수 반환과 산술부터 시작하고 분기·반복·메모리 처리로 넓히는 경로를 권합니다.

확인한 공식 안내에서 문제와 예제의 재배포 라이선스는 확인하지 못했습니다. 문제 링크와 직접 작성한 풀이를 사용하며, 원문이나 제공 코드를 재사용할 때에는 해당 파일의 조건을 따로 확인합니다.

### 3. CPUlator: 레지스터와 메모리를 관찰하는 디버거

[공식 문서의 Features·Quick Start·Compiling Code](https://cpulator.01xz.net/doc/)는 지원 CPU, 단일 단계 실행, 중단점, 레지스터·메모리 관찰, 어셈블리와 ELF 입력을 설명합니다. 내장 편집기는 단일 어셈블리 소스를 조립하며, C나 여러 파일로 구성한 프로그램은 별도 컴파일한 ELF를 불러옵니다. 보드가 없어도 입출력 장치를 포함한 프로그램을 디버깅할 수 있습니다.

이 도구의 실행 성공이나 디버그 경고가 없다는 사실은 특정 문제의 정답 판정이 아닙니다. 확인한 문서에서는 CPUlator 자체의 재배포 라이선스를 찾지 못했으며, 내부 GNU 도구의 라이선스를 사이트 전체의 라이선스로 간주하지 않습니다.

### 4. Nand2Tetris: 게이트에서 컴퓨터로 이어지는 개인 프로젝트

[공식 강좌](https://www.nand2tetris.org/course)와 [HDL 안내](https://www.nand2tetris.org/software/HDL)는 교육용 Hack HDL과 하드웨어 시뮬레이터를 제공합니다. 이 HDL은 Verilog나 VHDL과 다른 언어입니다. 제공된 `.tst`·`.cmp`를 이용한 로컬 검사와 [공식 Web IDE](https://nand2tetris.github.io/web-ide/)의 실행을 온라인 공개 정답 제출 기록과 구분합니다.

[공식 License 페이지](https://www.nand2tetris.org/license)는 사이트 자료에 CC BY-NC-SA 3.0을 표시하며, 완성 해답을 블로그·포럼·GitHub 등에 공개하지 말아 달라는 저자의 요청을 별도로 적고 있습니다. 이 저장소에서는 이 요청을 존중하여 완성 프로젝트 해답을 공개 예제로 채우지 않고 학습 경로와 개념을 연결합니다. [공식 projects 저장소의 MIT LICENSE](https://github.com/nand2tetris/projects/blob/main/LICENSE)는 그 저장소에서 확인한 소프트웨어의 조건이며, 사이트 전체나 책의 이용 조건과 섞지 않습니다.

### 5. Nandland: Verilog와 VHDL 기본 회로 비교

[모듈 목록](https://nandland.com/lots-more-vhdl-and-verilog-modules/)에는 가산기·FIFO·UART·BCD 변환·7세그먼트·멀티플렉서 등이 있습니다. 기준 해답으로 제출을 판정하는 사이트가 아니라, 설명과 코드를 참고하여 시뮬레이션과 보드 실습을 하는 자료입니다. 기본 게이트와 플립플롭을 익힌 뒤 테스트벤치·카운터·FIFO·UART 순으로 진행할 수 있습니다.

해당 모듈 페이지는 코드를 내려받아 수정할 수 있으며 Nandland 출처를 표시하라고 안내합니다. 같은 페이지의 푸터는 저자 허락 없는 웹 콘텐츠 재호스팅을 제한합니다. [책의 보조 코드 저장소 LICENSE](https://github.com/nandland/getting-started-with-fpgas/blob/main/LICENSE)는 MIT이지만 이를 모든 웹 문서·그림의 라이선스로 확대하지 않습니다. 본문을 복사하기보다 링크와 직접 작성한 설명을 사용합니다.

### 6. Project F: 테스트벤치가 있는 FPGA 모듈

[Verilog Library](https://projectf.io/verilog-lib/)는 클록·디스플레이·그래픽·수학·메모리·UART 모듈을 문서와 테스트벤치에 연결합니다. [Project F 홈](https://projectf.io/)에서 수와 벡터를 익힌 뒤 화면 타이밍과 도형 출력으로 진행할 수 있습니다. 예제별 사용 언어와 시뮬레이터·보드 요구 조건을 확인합니다.

[projf-explore LICENSE](https://github.com/projf/projf-explore/blob/main/LICENSE)는 MIT입니다. 해당 코드의 전부 또는 상당 부분을 재사용한다면 저작권·허락 고지를 유지합니다. 이 확인 결과를 별도의 웹 글·그림 전체에 일괄 적용하지 않습니다. 사이트에서 정답을 제출받는 방식이 아니므로 로컬 테스트 통과 범위를 기록합니다.

### 7. EDA Playground: 브라우저 시뮬레이션과 파형

[공식 Quick Start](https://eda-playground.readthedocs.io/en/latest/intro.html)는 로그인 후 언어·시뮬레이터를 선택하고 Run으로 실행하는 흐름을 설명합니다. [등록 페이지](https://www.edaplayground.com/register)는 Google 계정 사용과 추가 검증 계정을 구분하며, 일부 도구에는 회사·기관·학교 정보와 제한 이용 조건이 필요하다고 안내합니다. 해당 상용 도구의 교육·개인 이용 범위와 계정 검증 조건은 실행 전에 확인합니다.

테스트벤치의 assertion으로 통과·실패를 표시할 수 있지만, EDA Playground가 모든 코드에 기준 해답을 제공하는 것은 아닙니다. 공개된 playground를 볼 수 있다는 사실만으로 타인의 코드 재배포 허락이 생기지는 않습니다. 코드의 저자·파일별 조건과 시뮬레이터 이용 조건을 구분합니다.

### 8. VHDLweb: 웹 기반 VHDL 연습 후보

[공식 사이트](https://vhdlweb.com/)는 VHDL 예제와 연습을 제공하며, 일반 방문자의 연습과 Tufts 수강생의 학점 기록용 로그인을 구분합니다. [저자 저장소 README](https://github.com/stevenbell/vhdlweb)는 Tufts ES 4·EE 201용 도구임을 밝히고 GHDL·Docker 기반 설치를 설명합니다. 이번 조사에서는 공식 사이트의 응답 지연으로 실제 문제의 실행 결과·최종 판정 화면을 확인하지 못했습니다. 따라서 이 문서에서는 현재 온라인 자동 채점이 검증된 사이트로 표시하지 않습니다.

[플랫폼 저장소 LICENSE](https://github.com/stevenbell/vhdlweb/blob/master/LICENSE)는 GPL v3입니다. 플랫폼 코드의 조건과 사이트의 모든 문제·제출 코드의 조건을 동일하게 간주하지 않습니다. 현재 사용할 문제와 실행 환경은 직접 접속하여 확인합니다.

### 9. Tiny Tapeout: 테스트에서 칩 설계 흐름으로 확장

[HDL 안내](https://tinytapeout.com/hdl/), [템플릿](https://tinytapeout.com/hdl/templates/), [테스트 안내](https://tinytapeout.com/hdl/testing/)는 작은 설계를 테스트하고 자동화된 설계 흐름으로 넘기는 과정을 연결합니다. 테스트벤치와 CI를 통과했다는 사실은 모든 회로 동작이나 실제 제조 칩이 검증됐다는 뜻은 아닙니다. 실제 제작·구매 조건과 비용은 [공식 FAQ](https://tinytapeout.com/faq/)에서 별도로 확인합니다.

확인한 [IHP Verilog 템플릿 LICENSE](https://github.com/TinyTapeout/ttihp-verilog-template/blob/main/LICENSE)는 Apache-2.0입니다. 재사용할 템플릿의 라이선스·NOTICE·개별 파일 고지를 확인하며, 이 결과를 다른 사용자의 설계나 모든 문서에 확대하지 않습니다.

### 10. cocotb: Python으로 회로 자동 검사

[2.0.0 Quickstart](https://docs.cocotb.org/en/v2.0.0/quickstart.html)는 Python 비동기 테스트, 신호 접근, assertion, Makefile·runner를 이용한 실행을 설명합니다. cocotb는 회로 자체를 대체하는 언어가 아니라 HDL 시뮬레이터의 DUT를 구동하고 검사하는 테스트 도구입니다. 클록·리셋을 제어하고 경계 입력을 검사하는 용도로 사용합니다.

[cocotb 본체의 2.0.0 LICENSE](https://github.com/cocotb/cocotb/blob/v2.0.0/LICENSE)는 BSD-3-Clause입니다. 반면 확인한 [Quickstart의 my_design.sv](https://github.com/cocotb/cocotb/blob/v2.0.0/examples/doc_examples/quickstart/my_design.sv)는 CC0-1.0 고지를 포함합니다. 본체와 예제 파일의 조건을 구분하며, 문서·API 재현에는 버전을 기록합니다.

### 11. Amaranth: Python으로 생성하는 디지털 회로

[0.5.8 Getting started](https://amaranth-lang.org/docs/amaranth/v0.5.8/start.html)는 카운터의 조합·동기 논리, 비동기 테스트벤치, VCD 출력, Verilog 변환을 한 흐름으로 설명합니다. Python 프로그램이 회로를 기술하고 생성하는 방식이므로 일반 Python 함수 실행과 클록에 따른 하드웨어 상태 변화를 구분해야 합니다. 예제와 설치 버전을 맞춘 뒤 회로 생성·시뮬레이션·변환 단계를 확인합니다.

[Amaranth 저장소 LICENSE](https://github.com/amaranth-lang/amaranth/blob/main/LICENSE.txt)는 BSD-2-Clause입니다. 다른 합성 도구·보드 지원 패키지·커뮤니티 교재의 조건은 별도입니다. [공식 Tutorial 페이지](https://amaranth-lang.org/docs/amaranth/latest/tutorial.html)는 확인 시점에 작성 중이며 커뮤니티 자료를 연결하므로, 완성된 공식 기초 튜토리얼이 모두 제공된다고 표현하지 않습니다.

### 12. Amaranth exercises: 로컬 형식 검증 연습

[공식 Amaranth Tutorial의 커뮤니티 목록](https://amaranth-lang.org/docs/amaranth/latest/tutorial.html)에서 연결하는 저자 연습 자료입니다. 기존 Robert Baruch 주소는 현재 [XekriRedmane/amaranth-exercises](https://github.com/XekriRedmane/amaranth-exercises)로 연결됩니다. [첫 연습](https://github.com/XekriRedmane/amaranth-exercises/blob/main/01_input.md)은 회로 작성 뒤 SymbiYosys로 cover 도달과 bounded model checking을 실행하고 반례 파형을 읽는 과정을 설명합니다. 웹사이트에 제출하여 받는 정답 판정은 아닙니다.

[소개](https://github.com/XekriRedmane/amaranth-exercises/blob/main/00_intro.md)는 작성 중인 자료임을 밝힙니다. 확인한 저장소 루트에서 재배포 조건을 정한 LICENSE를 찾지 못했으므로, Amaranth 라이브러리의 BSD 라이선스를 이 교재에 적용하지 않습니다. 링크와 자체 작성한 회로·속성 설명을 사용하며, 과거 버전 API가 있으면 현재 설치 버전과 대조합니다.

## 코드와 설명을 남기는 기준

- 문제 제목·공식 링크·입출력 또는 회로 인터페이스의 필요한 조건을 적고, 회로와 테스트벤치는 직접 작성합니다. 문제 본문·그림·제공 테스트를 통째로 옮기지 않습니다.
- 외부 코드를 실제로 재사용한 경우에는 원본 파일·버전·라이선스·저작권 고지를 기록합니다. 사이트가 공개돼 있다는 사실과 재배포 허락은 구분합니다.
- 사이트 채점은 해당 문제의 실제 판정 기록으로 남깁니다. 로컬 시뮬레이션·assertion·형식 검증은 실행 명령, 도구 버전, 검사한 조건과 결과를 함께 기록합니다.
- 시뮬레이션 성공, 합성 성공, 타이밍 충족, 보드 동작, 칩 제작 결과를 각각 구분합니다. 한 단계의 통과를 나머지 단계의 통과로 표현하지 않습니다.
- `HDLExercises`·`VerilogExercises`처럼 일반적인 이름만으로는 운영 주체와 이용 조건을 확정하지 않습니다. 정확한 저자 저장소나 공식 도메인을 확인한 자료만 출처로 연결합니다.
