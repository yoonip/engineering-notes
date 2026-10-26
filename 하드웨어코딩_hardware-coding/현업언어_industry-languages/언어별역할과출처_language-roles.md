# 프로그램·회로·모델·자동화 언어의 실무 역할 | Roles of programming, modeling and automation languages

[실행 예제 목차](README.md) · [실행·미실행 범위](확인기록_validation.md)

확인일은 2026-10-26입니다. 언어가 실제 표준·제품·공개 설계에 쓰이는 근거를 연결합니다. 공급사의 소개와 교육 자료는 사용 대상과 기능의 근거이며, 시장 전체의 사용률·성능 우위를 입증하는 통계로 사용하지 않습니다. 출처별 확인 위치는 [sources.json](sources.json)에 있습니다.

## C·C++·Python과 함께 사용하는 것

| 분야와 작업 | 사용하는 언어·형식 | C·C++·Python과의 관계 | 근거와 학습 경로 |
| --- | --- | --- | --- |
| 디지털 RTL 설계 | Verilog·SystemVerilog·VHDL | 레지스터·조합논리·클록의 회로 모델입니다. CPU의 명령 순서와 구분합니다. | [AMD UG901, 2022.1의 합성 언어 안내](https://www.amd.com/content/dam/xilinx/support/documents/sw_manuals/xilinx2022_1/ug901-vivado-synthesis.pdf)와 기존 [VHDL 예제](../예제_examples/04-카운터와범위_vhdl-counter/README.md)입니다. |
| 레지스터 명세 | SystemRDL | 주소·비트·접근 속성에서 문서·헤더·RTL 등의 뷰를 만드는 공통 원천입니다. | [Accellera SystemRDL 2.0](https://www.accellera.org/downloads/standards/systemrdl)과 [실제 컴파일 예제](01-레지스터명세_systemrdl/README.md)입니다. |
| 제어·신호·수치 계산 | MATLAB, GNU Octave의 `.m` 코드 | 행렬·수치 함수를 사용하는 작성 언어이며 Python 라이브러리와 일대일 대응하지 않습니다. | [MathWorks의 분야별 모델 예제](https://www.mathworks.com/help/simulink/applications.html)와 [Octave 실행 예제](02-수치계산_matlab-octave/README.md)입니다. |
| 동적 계통·상태 모델 | Simulink·Stateflow | 블록·신호·상태 전이 모델을 작성합니다. 지원 도구·설정으로 코드를 생성할 수 있습니다. | [Simulink 공식 기능](https://www.mathworks.com/products/simulink.html)과 [FCA/Stellantis의 모델 기반 개발 사례](https://de.mathworks.com/company/user_stories/case-studies/fca-develops-autosar-compliant-engine-control-system-with-model-based-design.html)입니다. |
| PLC·산업 자동화 | Structured Text(ST), Ladder Diagram(LD), Function Block Diagram(FBD), SFC 구조 요소 | PLC의 프로그램·블록·상태와 태스크를 표현합니다. ST가 C로 번역되어도 작성 언어는 ST입니다. | [IEC 61131-3:2025 공개 개요](https://webstore.iec.ch/en/publication/68533), [PLCnext Engineer](https://engineer.plcnext.help/latest/iecprogramming.htm), [ST 실행 예제](04-PLC스캔_structured-text/README.md)입니다. |
| 범위·계약이 중요한 소프트웨어 | Ada·SPARK | Ada는 별도 언어이며 SPARK는 분석·증명을 위한 언어 규칙과 도구를 연결합니다. | [AdaCore의 산업 적용 설명](https://learn.adacore.com/booklets/adacore-technologies-for-airborne-software/chapters/tools.html)과 [Ada 실행 예제](03-계약과범위_ada-spark/README.md)입니다. |
| 임베디드 메모리·오류 처리 | Rust | 소유권·빌림·자료형을 컴파일 단계에 연결하는 별도 시스템 언어입니다. | 기존 [Rust의 범위·프레임 예제](../언어확장_language-expansion/04-Rust프레임과비트필드_rust-firmware/README.md)와 그 공식 출처입니다. |
| 설계 자동화·제약 | Tcl, SDC·XDC | Tcl은 도구를 제어하고, SDC·XDC 명령은 지원 EDA 도구가 해석하는 설계 조건을 표현합니다. | 기존 [Tcl·SDC 예제](../언어확장_language-expansion/05-설계자동화_tcl-sdc/README.md)입니다. |
| 아날로그·혼합신호 모델 | SPICE, Verilog-A·Verilog-AMS | 전압·전류·연속 시간·이벤트 모델을 표현합니다. 일반적인 디지털 RTL 합성과 구분합니다. | 기존 [SPICE 실행](../언어확장_language-expansion/03-아날로그회로_spice/README.md)과 [Accellera의 Verilog-AMS 2023 승인 안내](https://www.accellera.org/news/press-releases/393-accellera-approves-verilog-ams-2023-standard-for-release)입니다. |

MATLAB·Simulink·Stateflow는 같은 제품군에서 연결되지만 같은 언어 이름은 아닙니다. Simulink의 블록 연결, Stateflow의 상태·전이, MATLAB의 수치 코드가 맡는 역할을 각각 봅니다. 공급사의 FCA 사례는 실제 개발 팀이 모델·자료 사전·코드 생성을 함께 사용했다고 설명하는 발표 요약입니다. 사례의 결과를 자체 측정한 생산성이나 모든 프로젝트의 효과로 확대하지 않습니다.

이 저장소의 `.m` 예제는 GNU Octave에서 실행했습니다. MATLAB의 모든 문법·툴박스·Simulink 모델이 Octave와 호환되는 것은 아닙니다. 수치 코드의 통과, 모델 시뮬레이션, C 코드 생성, ECU 실행, HIL 확인을 따로 기록해야 합니다.

IEC 61131-3:2025는 ST·LD·FBD와 SFC 구조 요소를 설명합니다. 오래된 자료에서 IL(Instruction List)을 포함한 언어 목록을 보더라도 최신 표준과 제품의 이전 버전 호환 기능을 구분합니다. 이 문서는 표준의 공개 개요와 공급사 설명을 사용하며 유료 표준 전문을 읽은 것으로 표시하지 않습니다.

## 현장에서 특정 도구와 연결하는 언어

아래 언어·환경도 실제 제품의 공식 문서와 학습 자료가 있습니다. 이 표는 읽을 경로이며, 이 작업에서 상용 런타임을 설치하거나 코드를 실행한 기록은 아닙니다.

| 작업 | 언어·환경 | 먼저 읽을 내용과 실제 확인 대상 |
| --- | --- | --- |
| 차량 통신의 분석·시뮬레이션·시험 | Vector CAPL·CANoe | [공식 CAPL Basics V1.6](https://elearning.vector.com/course/view.php?id=158&section=1)는 C의 영향을 받은 문법과 CANoe 구성에서의 연습을 안내합니다. 일반 C 컴파일만으로 CANoe의 실행 문맥을 확인할 수는 없습니다. |
| IC 설계 데이터와 반복 작업 | Cadence SKILL·Virtuoso | [Cadence의 SKILL 소개](https://community.cadence.com/cadence_blogs_8/b/cic/posts/the-cadence-skill-language-where-coding-blends-with-chip-design)는 설계 데이터 조회·도형·PCell·도구 자동화를 설명합니다. 일반 Lisp·Scheme에서 식이 계산된다는 것과 Virtuoso 데이터베이스 API가 동작한다는 것은 다릅니다. |
| 계측·시험 장치·화면의 데이터 흐름 | NI LabVIEW의 G | [NI의 그래픽 프로그래밍 설명](https://www.ni.com/en/shop/labview/benefits-of-programming-graphically-in-ni-labview.html)은 G와 컴파일·디버깅 환경을 구분합니다. [공식 입문](https://learn.ni.com/learn/article/labview-tutorial?client=national-instruments)에서 블록·와이어·데이터 의존성과 입출력을 읽습니다. |
| 동기식 임베디드 모델 | SCADE Suite의 Scade, Scade One의 Swan | [Ansys의 Swan 설명](https://innovationspace.ansys.com/knowledge/forums/topic/scade-one-bridging-the-gap-between-model-based-design-and-traditional-programming/)은 논리 시간·데이터 흐름·상태와 텍스트·그림 표기를 설명합니다. Lustre의 연구 계보, SCADE Suite의 Scade 6, Scade One의 Swan을 동일한 문법으로 취급하지 않습니다. |
| 전기·기계·열의 방정식 모델 | Modelica | [공식 OpenModelica 학습 경로와 판본·이용 조건](../응용시스템_applied-systems/공개프로젝트와언어_sources-and-languages.md)을 연결합니다. 물리 계통의 방정식 모델과 펌웨어를 구분합니다. |
| 매개변수화한 디지털 회로 생성 | Scala·Chisel | [Chisel 공식 소개](https://www.chisel-lang.org/)는 Scala로 회로를 구성하고 Verilog로 변환하는 흐름을 설명합니다. Scala의 실행과 생성된 회로의 시뮬레이션·합성은 서로 다른 검사입니다. |
| 우주 소프트웨어의 컴포넌트 구조 | F Prime의 FPP | [F Prime 공식 자료 안내](../응용시스템_applied-systems/공개프로젝트와언어_sources-and-languages.md)에서 컴포넌트·포트·토폴로지 모델과 C++ 구현·Python 개발 도구를 나누어 읽습니다. |

CAPL 공식 입문은 CANoe 구성에서 연습하고 생성된 토큰으로 웹의 답을 확인하는 절차를 제공합니다. 온라인 자료라는 이유만으로 브라우저에서 언어 런타임까지 제공하는 문제 사이트로 생각하면 안 됩니다. 여기서는 CANoe 측정·토큰 발급·온라인 채점을 수행하지 않았습니다.

SKILL은 설계 데이터와 도구 API를 다루므로 도형·레이어·좌표 단위·cellview·변경 저장 범위가 코드의 입력 계약입니다. 계측 환경에서는 채널·자료형·표본 시각·장치 오류·작업 종료가 계약입니다. 언어를 고를 때 문법의 익숙함과 함께 해당 도구가 제공하는 객체와 실행 문맥을 봐야 하는 이유입니다.

SCADE 계열의 논리적 동기 시간은 실행을 해석하는 규칙이며, 실제 대상 하드웨어의 마감 시간 충족을 자동으로 측정한 결과가 아닙니다. 공급사의 코드 생성·검증 기능 설명을 자체 모델의 증명이나 제품 인증 결과로 옮기지 않습니다.

## 언어와 라이브러리·파일 형식을 나눕니다

| 이름 | 어떤 종류인지 | 혼동하기 쉬운 지점 |
| --- | --- | --- |
| C++·SystemC | C++ 언어와 시스템 모델링 라이브러리입니다. | SystemC의 시간 모형을 실행했다고 RTL 합성을 마친 것은 아닙니다. |
| Python·cocotb | Python 언어와 HDL 시뮬레이터를 구동하는 검증 도구입니다. | 테스트벤치가 Python이라고 회로 자체도 CPU Python 프로그램이 되는 것은 아닙니다. |
| SystemVerilog·UVM | 언어와 검증 방법론·라이브러리입니다. | UVM은 독립 언어 이름이 아니며 테스트벤치 코드와 합성할 RTL을 구분합니다. |
| ROS 2·Autoware | 통신·로봇 기능을 연결하는 소프트웨어 생태계입니다. | 제품 이름만으로 구현 언어를 한 가지로 정할 수 없습니다. |
| URDF·SDF·Protocol Buffers | 구조·모델·메시지를 기술하는 형식·명세입니다. | 범용 알고리즘 언어와 역할이 다릅니다. |
| MATLAB·Simulink | 수치 언어·환경과 블록 모델 환경입니다. | `.m` 코드 실행을 Simulink 실행으로 표시하지 않습니다. |

SystemC·cocotb·ROS 2의 정의와 기존 실행 범위는 각각 [언어 확장 자료](../언어확장_language-expansion/README.md)와 [응용 시스템 자료](../응용시스템_applied-systems/README.md)에 있습니다. UVM은 [Accellera 표준 목록](https://www.accellera.org/downloads/standards)에서 클래스 참조·방법론 안내·IEEE 1800.2 구현으로 연결합니다. 모든 도구를 같은 종류의 새 프로그래밍 언어로 세지 않습니다.

## 먼저 익힐 순서

디지털 RTL을 공부한다면 Verilog·SystemVerilog·VHDL 중 사용하는 도구와 프로젝트에 맞는 언어에서 클록·리셋·비트 폭을 먼저 확인합니다. 다음으로 Tcl·제약·검증과 레지스터 명세를 연결합니다. 제어·로봇 수치 계산은 `.m` 코드와 행렬·단위·표본 시각에서 시작하고, 모델과 생성 코드의 실행 차이를 비교합니다. 산업 자동화는 ST의 블록 상태·주기·I/O에서, 고신뢰 소프트웨어는 Ada의 자료형·계약과 테스트·증명의 차이에서 시작합니다.

검사 대상으로 삼을 수 없는 도구 이름을 목록에 늘리기보다 작성할 산출물과 비교할 기대값을 정하는 것이 좋습니다. 실제 실행한 예제는 [실행 기록](확인기록_validation.md)에, 아직 읽기 단계인 상용·외부 도구는 위 표에 구분합니다.
