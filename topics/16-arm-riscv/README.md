# Arm · RISC-V · Computer Architecture

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

ISA는 소프트웨어에서 보이는 명령어·레지스터·메모리 동작의 약속이다. 마이크로아키텍처는 그 약속을 실제 회로로 구현하는 방식이다. 같은 ISA를 구현한 프로세서도 파이프라인·캐시·실행 자원에 따라 속도와 전력이 달라진다.

## Arm과 RISC-V

Arm의 Cortex-M은 마이크로컨트롤러, Cortex-A는 운영체제를 사용하는 애플리케이션, Cortex-R은 실시간 처리 응용과 연관된 프로세서 계열이다. RISC-V는 모듈식 확장을 갖는 공개 ISA다. RV32·RV64는 정수 레지스터 폭과 관련된 구분이며, 지원 확장은 구현마다 다르다. x86-64·MIPS·AVR도 서로 다른 명령어 생태계다.

## 명령 실행과 메모리

호출 규약은 함수 인자, 반환값, 레지스터 보존 방식을 정한다. 예외와 인터럽트는 실행 흐름을 처리 루틴으로 옮긴다. 캐시는 자주 쓰는 데이터를 가까이 두고, MMU는 가상 주소 변환과 보호에 관여한다. DMA는 CPU가 매 바이트를 복사하지 않고 주변장치와 메모리 사이의 전송을 진행하도록 한다.

PicoRV32·Ibex·CVA6·Rocket·BOOM은 RISC-V 구현을 읽을 수 있는 프로젝트다. QEMU는 시스템·명령 실행 에뮬레이션, gem5는 컴퓨터 구조 시뮬레이션에 쓰인다. ISA를 이해하는 일과 특정 코어의 성능을 분석하는 일은 서로 이어지지만 분석 대상은 다르다.

## 관련 기술

Arm Cortex-M/A/R, RISC-V RV32/RV64, x86-64, MIPS, AVR, PicoRV32, Ibex, CVA6, Rocket Chip, BOOM, gem5, QEMU

## 참고 자료

- [RISC-V specifications](https://docs.riscv.org/)
- [Arm documentation](https://developer.arm.com/documentation)

## Arm·RISC-V 실행 구조

ISA는 명령어의 표현, 레지스터, 메모리 접근과 예외 처리처럼 프로그램에서 관찰할 수 있는 동작을 정의한다. CPU 코어는 이 규칙을 회로로 구현하며, MCU는 코어에 Flash, SRAM과 주변장치를 결합한다. STM32F767ZI에는 Arm Cortex-M7 코어가 들어 있다. Arm은 아키텍처, Cortex-M7은 코어, STM32F767ZI는 MCU, NUCLEO-F767ZI는 개발보드라는 서로 다른 계층이다. [ST 제품 설명](https://www.st.com/en/microcontrollers-microprocessors/stm32f767zi.html)

같은 C 코드도 대상 ISA에 따라 다른 기계 명령으로 바뀐다. `input_a + input_b`를 Arm과 RISC-V로 각각 빌드하면, 값을 읽는 명령, 더하는 명령, 결과를 저장하는 명령으로 나뉜다. C 한 줄과 CPU 명령 한 개는 같은 단위가 아니다.

```c
volatile uint32_t input_a = 1;
volatile uint32_t input_b = 3;
volatile uint32_t result;
volatile uint32_t trace[2];

result = input_a + input_b;
trace[0] = result;
trace[1] = result + 1;
```

Renode의 Cortex-M7과 Spike의 RV64IMAC에서 명령 단위로 실행했다. 덧셈 직후에는 결과 4가 CPU 레지스터에 있고, 저장 명령 뒤에 `result` 메모리가 4로 바뀐다. 최종 상태는 두 대상 모두 `result=4`, `trace={4,5}`였다. 이 기록은 가상 대상에서 수집한 실행 결과다.

Renode는 MCU와 주변장치 모델을 제공하고, Spike는 RISC-V ISA 시뮬레이터다. 이 실습의 Arm 경로는 Renode의 GDB 서버에 직접 연결하며, RISC-V 경로는 OpenOCD의 `remote_bitbang`으로 Spike의 가상 JTAG에 연결한다. [Renode GDB 문서](https://renode.readthedocs.io/en/latest/debugging/gdb.html), [Spike 프로젝트](https://github.com/riscv-software-src/riscv-isa-sim)
