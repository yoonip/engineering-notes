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
