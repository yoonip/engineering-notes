# 하드웨어 언어와 도구의 실행 예제 | Languages across the hardware workflow

CPU가 실행하는 코드, 회로를 검사하는 코드, 아날로그 회로의 연결, 설계 도구를 제어하는 스크립트와 시간 기반 모델을 함께 다룹니다. 기존 Verilog·SystemVerilog·VHDL·Amaranth 실습에서 다른 역할로 이어지는 경로입니다.

[하드웨어 코딩 목차](../README.md) · [선정 이유와 학습 순서](검토와학습순서_language-selection.md) · [실행 기록과 확인 범위](확인기록_validation.md)

## 예제에서 확인할 내용

| 언어·도구 | 직접 작성한 예제 | 확인한 실행과 역할 |
| --- | --- | --- |
| [RISC-V 어셈블리](01-RISC-V비트처리_riscv-assembly/README.md) | 비트필드 갱신·바이트 합·호출 규약 검사 | RV32I로 컴파일한 프로그램을 QEMU CPU에서 실행 |
| [Python·cocotb](02-Python회로검증_cocotb/README.md) | 카운터와 전송 버퍼의 독립 검사 | Icarus와 Python을 연결한 에지 전후·정체·리셋 검사 |
| [SPICE](03-아날로그회로_spice/README.md) | RC 저역통과 회로의 과도·AC 해석 | ngspice 계산값과 독립 해석해의 전압·복소 전달함수 비교 |
| [Rust](04-Rust프레임과비트필드_rust-firmware/README.md) | no_std 비트필드와 입력을 빌리는 프레임 파서 | 라이브러리 컴파일과 호스트에서의 길이·폭·오류 검사 |
| [Tcl·SDC](05-설계자동화_tcl-sdc/README.md) | 합성 작업 제어와 클록·입출력 조건 생성 | Yosys 일반 구조 검사와 제약 파일 생성·명령 대조 |
| [C++·SystemC](06-Cpp이벤트모델_systemc/README.md) | 깊이 1 FIFO의 생산·소비·대기 | SystemC 이벤트 커널의 전달 값과 모형 시간 검사 |

예제마다 의미 있는 코드 줄에 짧은 복습용 주석을 달고, README에는 소스 전체와 입력에서 결과까지의 흐름을 담았습니다. 처음 보는 문법과 그 줄을 쓴 이유, 경계 조건, 실제 장치에 적용할 때 필요한 조건을 함께 설명합니다.

## 같은 언어라도 실행 대상 구분하기

| 표현 | 이 자료에서의 실행 대상 | 혼동하기 쉬운 부분 |
| --- | --- | --- |
| RISC-V 명령·Rust 펌웨어 로직 | CPU의 레지스터·메모리와 프로그램 | CPU 프로그램 자체가 RTL 회로를 생성하는 것은 아닙니다. |
| Python·cocotb | HDL 시뮬레이터의 신호와 시간 | 기존 Amaranth의 회로 구성과 다른 역할입니다. |
| SPICE netlist | 소자 방정식과 시간·주파수 해석 | 디지털 0/1의 진리표와 전압·전류 연속값은 확인 대상이 다릅니다. |
| Tcl과 SDC | 설계 작업 절차와 타이밍 요구 조건 | 제약을 썼다는 사실과 그 제약을 충족했다는 사실을 구분합니다. |
| C++·SystemC | 이벤트와 가정한 시간에 따른 시스템 모형 | 모형의 지연은 실물 회로에서 측정한 지연이 아닙니다. |

SystemC와 cocotb는 각각 C++와 Python에 연결하는 라이브러리·도구입니다. 독립된 새 문법 언어의 수로 세지 않고, 어떤 대상을 만들고 검사하는지를 기준으로 분류합니다.

## 실행과 기록 읽기

각 폴더의 실행 명령으로 필요한 도구를 선택합니다. 실행 환경과 실제 명령·출력·종료 코드·소스 해시는 example.json에 있습니다. 컴파일러·시뮬레이터는 저장소에 포함하지 않으며, 공식 설치 자료와 사용한 판본을 각 README에서 연결합니다.

[check_sources.py](check_sources.py)는 현재 소스의 해시·문서에 실은 코드·연결된 파일을 저장된 실행 기록과 대조합니다. 도구를 다시 실행하는 명령과는 구분합니다.

```bash
python -B 하드웨어코딩_hardware-coding/언어확장_language-expansion/check_sources.py --report /path/to/new-source-check.json
```

이 실습은 로컬 실행 기록입니다. 온라인 문제은행의 채점 통과, 특정 FPGA의 타이밍 충족, MCU나 아날로그 회로의 실물 측정을 확인한 기록은 아닙니다. 의도적 회로 결함의 검출, 잘못된 기대값을 검출한 검사기 대조, 잘못된 설정의 거절도 실행 기록에서 구분합니다.

## English

Original examples across the hardware workflow: RV32I assembly on QEMU, cocotb with an HDL simulator, SPICE transient and AC analysis, a no_std Rust library with host tests, Tcl-driven generic synthesis and SDC generation, and SystemC event-based models. Each example includes annotated source, an execution trace, independent checks, commands and explicit limits. Recorded tool execution and static source/document checks are separate.
