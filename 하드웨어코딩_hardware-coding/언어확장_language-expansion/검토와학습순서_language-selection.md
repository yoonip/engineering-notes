# 하드웨어 언어를 고르는 기준과 학습 순서

[언어 확장 목차](README.md) · [기존 회로 설계 언어 비교](../언어와검증도구_languages-and-verification.md)

## 이번에 선택한 기준

기존 자료에는 Verilog·SystemVerilog·VHDL·Amaranth 회로, C·C++·Python 알고리즘, 임베디드 디버깅과 일부 설계 스크립트가 있습니다. 추가 자료는 그 언어가 하드웨어 작업에서 담당하는 대상과 실제로 검사할 수 있는 결과를 기준으로 골랐습니다. 아래 순서는 이 저장소의 학습 경로에 대한 판단이며, 언어의 보편적인 우열이나 채용 수요 순위가 아닙니다.

| 공부할 대상 | 추천하는 언어·도구 | 추가할 가치 | 먼저 익힐 내용 |
| --- | --- | --- | --- |
| CPU가 명령을 실행하는 과정 | RISC-V 어셈블리 | C 코드와 레지스터·메모리·호출 규약의 관계를 직접 확인합니다. | 정수·비트 연산, 주소와 배열 |
| RTL의 자동 검사 | Python·cocotb | 이미 익숙한 Python으로 클록·리셋·정체를 제어하고 독립 기대값과 비교합니다. | 조합·순차논리와 샘플링 시점 |
| 전압·전류·주파수 응답 | SPICE | 디지털 논리와 연결되는 아날로그 회로를 소자·단위·방정식으로 확인합니다. | 저항·커패시터, 지수함수와 복소수 |
| 경계 조건이 있는 펌웨어 로직 | Rust | 오류를 반환하는 API와 입력을 빌리는 뷰를 통해 길이·수명·소유권 계약을 익힙니다. | C 또는 다른 시스템 언어의 배열·함수 |
| 반복할 수 있는 설계 작업 | Tcl·SDC | 소스·계층·출력·요구 조건을 명시하고 잘못된 설정을 실행 전에 찾습니다. | 파일 경로, 포트·클록의 의미 |
| 시간과 처리량을 가진 시스템 모형 | C++·SystemC | 생산·소비·대기와 이벤트의 관계를 회로 구현 전 모형에서 확인합니다. | C++ 객체와 동시 실행의 개념 |

## RISC-V에서 시작할 때

[RV32I 예제](01-RISC-V비트처리_riscv-assembly/README.md)는 비트필드 갱신과 바이트 합을 짧은 함수로 만들고 C 기준 계산과 비교합니다. ABI는 함수가 인자·반환값을 어느 레지스터에 두고 어떤 레지스터를 보존할지 정하는 약속입니다. 같은 계산이라도 이 약속을 어기면 호출자와 연결했을 때 잘못 동작할 수 있습니다. ISA는 실행할 명령의 의미, ABI는 프로그램 조각을 연결하는 약속으로 나누어 읽습니다. [RISC-V 공식 ISA 문서](https://docs.riscv.org/reference/isa/unpriv/rv32.html), [psABI](https://riscv-non-isa.github.io/riscv-elf-psabi-doc/)

QEMU에서 실행한 프로그램은 실제 RISC-V 명령을 기능적으로 검사합니다. 명령 수행 시간이 실제 칩과 같다는 뜻은 아닙니다. C 드라이버의 일반 메모리 계산과 QEMU 보드의 UART·종료 장치 접근도 구분합니다.

## Python을 회로 검증으로 넓힐 때

[cocotb 예제](02-Python회로검증_cocotb/README.md)는 입력을 바꾼 시점, 클록 에지, 레지스터 갱신 이후의 관측을 나눕니다. 신호를 너무 일찍 읽으면 이전 값을 정답처럼 비교할 수 있으므로 시뮬레이터의 실행 단계와 함께 공부합니다. 전송 버퍼의 기대값은 DUT 내부 상태가 아니라 외부에서 실제 수락·소비한 항목으로 계산합니다. [cocotb 2.0.0 시작 문서](https://docs.cocotb.org/en/v2.0.0/quickstart.html), [타이밍 모델](https://docs.cocotb.org/en/v2.0.0/timing_model.html)

Python에 익숙하고 기존 HDL 회로의 검사를 자동화하려는 경우에 연결하기 좋은 단계입니다. Amaranth는 회로 구조를 구성하고 cocotb는 시뮬레이터의 기존 회로를 구동한다는 차이가 있습니다.

## SPICE로 아날로그 회로를 공부할 때

[RC 예제](03-아날로그회로_spice/README.md)는 소자 값과 단위를 정하고 시간 응답·주파수 응답을 각각 계산합니다. 입력 전압이 순간적으로 바뀌는 계단인지 유한 시간 동안 오르는 램프인지에 따라 초기 응답이 달라집니다. 시뮬레이션 입력과 같은 조건의 해석해를 사용해야 수치 오차와 모델 조건 차이를 구분할 수 있습니다. [ngspice 공식 문서](https://ngspice.sourceforge.io/docs.html)

측정값을 회로 모델과 대조할 때는 소자의 공차·기생 성분·전원·온도도 필요합니다. 이번 이상 RC 모형의 일치는 실물 소자의 허용 오차나 계측 결과를 대신하지 않습니다. SPICE의 소자 정의와 ngspice의 .control 명령도 구분하여 다른 도구로 옮길 때 지원 범위를 확인합니다.

## Rust로 펌웨어 로직을 정리할 때

[Rust 예제](04-Rust프레임과비트필드_rust-firmware/README.md)는 비트필드의 범위를 생성 때 확인하고, 프레임 길이를 확인한 뒤 원본 버퍼의 일부를 빌려 반환합니다. 빌린 데이터의 수명을 입력 버퍼와 연결하면 복사 없이 보되 입력보다 오래 사용하는 코드를 컴파일 단계에서 제한할 수 있습니다. no_std 라이브러리 컴파일과 PC의 std 테스트 환경을 분리해 기록합니다. [Embedded Rust Book의 no_std](https://doc.rust-lang.org/embedded-book/intro/no-std.html), [The Rust Book의 참조와 빌림](https://doc.rust-lang.org/book/ch04-02-references-and-borrowing.html)

실제 MMIO에는 해당 칩의 주소·접근 폭·정렬·부작용과 동시 접근 계약이 추가됩니다. volatile 접근은 그 계약 전체를 보장하지 않으며 스레드 간 원자성을 만들어 주지 않습니다. 이번 예제는 일반 메모리 값과 바이트 프레임을 검사하며 MCU에서 실행하거나 MMIO를 시험한 코드는 아닙니다. [Rust read_volatile의 Safety·동시 접근 설명](https://doc.rust-lang.org/std/ptr/fn.read_volatile.html)

RISC-V 예제와 Rust 예제의 필드 갱신은 오류 정책도 확인하며 비교합니다. 어셈블리 함수는 호출자가 정해진 위치·폭 계약을 지키고 넘치는 새 비트를 자르는 방식이며, Rust API는 잘못된 구성을 Result 오류로 거절합니다. 이런 정책은 언어 이름만으로 정해지는 성질이 아니라 이 예제의 인터페이스 선택입니다.

## Tcl과 SDC로 설계 흐름을 만들 때

[Tcl 예제](05-설계자동화_tcl-sdc/README.md)는 파일과 설정을 명시하고 도구를 실행해 생성물의 포트·상태 폭을 대조합니다. 제약 파일의 명령은 Tcl 문법을 따르지만 get_ports·create_clock 같은 이름은 EDA 도구가 제공하므로 일반 Tcl 인터프리터만으로 회로의 시간을 분석할 수 없습니다. [Yosys Tcl 명령](https://yosyshq.readthedocs.io/projects/yosys/en/0.45/cmd/tcl.html), [OpenSTA 공식 저장소](https://github.com/parallaxsw/OpenSTA)

주기 5ns와 10ns를 SDC에 썼다는 사실과 회로가 그 주기로 동작한다는 사실은 구분합니다. 뒤 단계에서는 셀 라이브러리·매핑된 회로·부하·배선·클록 조건을 함께 주고 타이밍을 확인해야 합니다. 잘못된 설정을 조기에 거절하고 실행별 생성물을 분리하는 것부터 익힙니다.

## SystemC로 시간 모형을 만들 때

[SystemC 예제](06-Cpp이벤트모델_systemc/README.md)는 작은 FIFO를 통해 생산자와 소비자의 대기 시점을 확인합니다. sc_fifo가 가득 차면 쓰기가 기다리고 비어 있으면 읽기가 기다리므로 계산 결과뿐 아니라 항목이 전달되는 시점과 순서도 모델의 결과입니다. 모형 시간의 변화와 같은 시간 안의 delta-cycle도 구분합니다. [Accellera의 SystemC 배포](https://accellera.org/downloads/standards/systemc), [SystemC 개요](https://systemc.org/overview/systemc/)

아키텍처의 지연·처리량·버퍼 요구량을 가정하여 비교할 때 사용할 수 있습니다. 입력한 지연이 실제 하드웨어의 측정값이 되는 것은 아니며, 이 C++ 프로그램을 실행했다는 사실을 RTL 합성이나 핀 수준 검증으로 표시하지 않습니다.

## 다음에 선택할 만한 확장

| 대상 | 다음 자료 | 선택할 조건과 이번 확인 범위 |
| --- | --- | --- |
| 매개변수화한 RTL 생성 | [Chisel 공식 설치](https://www.chisel-lang.org/docs/installation) | Scala의 타입·생성 단계와 하드웨어 값을 함께 익힐 때 적합합니다. 이번에는 공식 경로를 조사했으며 Scala 예제를 실행하지 않았습니다. |
| 레지스터 주소·필드 명세 | [SystemRDL 표준](https://accellera.org/downloads/standards/systemrdl), [SystemRDL Compiler](https://systemrdl-compiler.readthedocs.io/en/stable/) | 문서·RTL·드라이버가 같은 주소와 접근 속성을 공유해야 할 때 검토합니다. 이번에는 컴파일러나 생성기를 실행하지 않았습니다. |
| C·C++ 알고리즘의 하드웨어 구현 | [Vitis HLS UG1399](https://docs.amd.com/r/en-US/ug1399-vitis-hls/Introduction) | 연산·메모리·입출력의 병렬성과 지연을 설계할 때 검토합니다. 일반 C++ 실행 결과만으로 합성·처리율을 판단하지 않으며 이번에는 HLS를 실행하지 않았습니다. |

Chisel은 기존 Amaranth와 같은 RTL 생성 목적을 다른 호스트 언어로 다루므로, 먼저 기존 회로의 클록·비트 폭과 생성 결과를 이해한 뒤 비교하는 순서로 두었습니다. 공식 안내의 Scala CLI 예제와 과거 Bootcamp의 Binder 실행 상태는 구분합니다. [Bootcamp README](https://github.com/freechipsproject/chisel-bootcamp)는 일부 노트북 환경의 노후화와 오류를 알립니다.

SystemRDL은 레지스터 정의를 여러 출력의 공통 원천으로 쓰려는 언어입니다. 해당 명세를 썼다는 사실만으로 주변 장치의 모든 부작용·동시 접근·버스 타이밍까지 맞아지는 것은 아니므로 생성한 뷰와 실제 구현을 대조해야 합니다. 외부 문서와 코드는 공식 링크로 연결하고, 가져오는 파일이 있다면 해당 파일의 이용 조건과 고지를 따로 확인합니다.
