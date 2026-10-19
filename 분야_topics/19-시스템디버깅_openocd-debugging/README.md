# OpenOCD·GDB와 시스템 디버깅 | OpenOCD, GDB & Instrumentation

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

디버깅에서는 관찰한 증상에서 출발해 원인을 좁혀 갑니다. 소프트웨어 디버거, 디버그 프로브, 칩의 디버그 인터페이스는 서로 다른 구성요소입니다. 회로 문제와 펌웨어 문제는 비슷한 증상을 만들기도 합니다.

## 연결 구조

GDB는 실행 제어와 변수·메모리 조회를 맡습니다. OpenOCD는 지원하는 프로브와 대상 장치를 연결하고 GDB 서버, flash 기록, 실행 제어 등을 제공합니다. JTAG·SWD는 대상 칩과 통신하는 디버그 인터페이스입니다. ST-Link·J-Link는 프로브 제품군이며 pyOCD·probe-rs도 대상별 디버그 도구입니다.

## 관찰 도구의 차이

Breakpoint는 특정 위치에서 실행을 멈추고, watchpoint는 메모리 접근 조건에 반응합니다. 정지 상태의 관찰은 타이밍을 바꿀 수 있습니다. HardFault 분석에는 원인 상태 레지스터, 예외 당시의 스택, PC·LR 같은 실행 정보가 연결됩니다. SWO·ETM은 지원 장치에서 trace와 실행 관찰에 사용됩니다.

오실로스코프는 전압의 시간 파형을, 로직애널라이저는 디지털 상태와 프로토콜을 관찰합니다. Saleae·PulseView·sigrok은 디지털 신호 분석 생태계입니다. 소프트웨어 로그와 실제 핀 파형의 시간이 맞아야 통신 실패나 응답 지연을 해석할 수 있습니다.

## 관련 기술

OpenOCD, GDB, LLDB, J-Link, ST-Link, pyOCD, probe-rs, JTAG, SWD, SWO, ETM, Saleae, PulseView, Sigrok

## 참고 자료

- [About OpenOCD](https://openocd.org/doc/html/About.html)
- [GDB documentation](https://sourceware.org/gdb/documentation/)

## 디버거와 대상 연결

GDB는 ELF의 심볼과 디버그 정보를 읽어 소스, 변수와 CPU 상태를 연결합니다. OpenOCD는 GDB의 요청을 대상의 디버그 기능으로 전달하는 서버입니다. 물리 보드에서는 ST-LINK 같은 프로브와 JTAG 또는 SWD를 통해 칩에 연결합니다. USB, JTAG와 SWD는 연결 위치와 역할이 서로 다릅니다.

```text
GDB → OpenOCD → 디버그 프로브 → JTAG/SWD → 대상 칩
GDB → OpenOCD → remote_bitbang → Spike 가상 JTAG
GDB → Renode의 GDB 서버 → 가상 Cortex-M
```

OpenOCD가 C 코드를 컴파일하거나 CPU를 가상으로 실행하는 것은 아닙니다. GDB의 요청을 전달하고 CPU 정지·재개, 레지스터·메모리 접근 등의 디버그 동작을 제공합니다. [OpenOCD 공식 문서](https://openocd.org/doc/html/GDB-and-OpenOCD.html)

| GDB 명령 | 의미 |
| --- | --- |
| `target extended-remote localhost:3334` | 이 실습의 OpenOCD GDB 서버에 연결 |
| `monitor halt` | 대상 정지 요청을 디버그 서버에 전달 |
| `load` | ELF의 적재 대상 코드·데이터를 메모리에 기록 |
| `break main` | `main` 진입 위치에 중단점 설정 |
| `stepi` | 기계 명령 하나 실행 |
| `info registers` | CPU 레지스터 조회 |
| `x/wx &result` | `result` 주소의 32비트 값 조회 |

`3334`는 이 Spike 실습에 설정한 포트이며, 대상에 따라 다른 값을 사용합니다. STM32의 Flash 기록과 리셋 절차는 대상의 메모리 맵과 OpenOCD 설정을 따릅니다.

## 메모리 검사와 오류 주입

패턴을 기록하고 다시 읽어 기대값과 비교합니다. 결과에는 오류 수, 첫 오류 인덱스, 기대값과 관찰값을 남깁니다. 정상·오류 주입·복원을 같은 절차로 실행해 판정 경로를 확인합니다.

Spike+OpenOCD의 저장된 실행 기록에서는 정상 상태의 오류 수가 0이었고, 인덱스 17의 bit 0을 바꾼 뒤에는 오류 1개가 검출됐으며, 복원 뒤에는 다시 0이었습니다. Renode의 소프트웨어 메모리 회귀검사는 29개 사례를 포함합니다. 모두 가상 대상의 소프트웨어 검사 결과입니다.

## 기초 해설

- [OpenOCD와 GDB: 연결, 정지 상태와 관찰의 의미](해설_notes/OpenOCD와GDB_debug-transport-state-observation.md)

## English

Debugging connects an observed symptom to its cause. A software debugger, a debug probe, and a chip's debug interface occupy different places in that process. Circuit faults and firmware faults can produce similar symptoms.

### Connection layers

GDB controls execution and reads variables and memory. OpenOCD connects supported probes and targets, offering a GDB server, Flash programming, and target control. JTAG and SWD are chip debug interfaces. ST-Link and J-Link are probe families; pyOCD and probe-rs provide other target-dependent debugging tools.

### What each instrument observes

A breakpoint stops execution at a location, while a watchpoint reacts to a memory-access condition. Stopping the target can change timing. HardFault analysis combines fault-status registers, the exception stack frame, and execution information such as PC and LR. SWO and ETM provide trace on supported devices.

An oscilloscope observes voltage over time; a logic analyzer observes digital states and protocols. Saleae, PulseView, and sigrok support digital signal analysis. Aligning software logs with physical pin activity helps explain communication failures and response delays.

### Connecting a debugger to a target

GDB reads symbols and debug information from an ELF to relate source code and variables to CPU state. OpenOCD translates debugger requests into target debug operations. A physical board uses a probe such as ST-LINK and a JTAG or SWD connection to the chip. USB, JTAG, and SWD have different positions and roles in that connection.

The connection diagram above shows three paths: GDB through OpenOCD and a physical probe to a chip; GDB through OpenOCD's `remote_bitbang` to Spike's virtual JTAG; and GDB directly to Renode's GDB server. OpenOCD provides halt/resume and register/memory access; it does not compile C or emulate a CPU. See [GDB and OpenOCD](https://openocd.org/doc/html/GDB-and-OpenOCD.html).

| GDB command | Meaning in this exercise |
| --- | --- |
| `target extended-remote localhost:3334` | Connect to the OpenOCD GDB server |
| `monitor halt` | Ask the debug server to halt the target |
| `load` | Write loadable ELF code and data to target memory |
| `break main` | Set a breakpoint at `main` |
| `stepi` | Execute one machine instruction |
| `info registers` | Inspect CPU registers |
| `x/wx &result` | Read a 32-bit value at the address of `result` |

Port `3334` is configured for this Spike exercise; other targets may use different ports. STM32 Flash programming and reset procedures depend on the target memory map and OpenOCD configuration.

### Memory checks and fault injection

The check writes patterns, reads them back, and compares them with expected values. Results record the error count, first failing index, expected value, and observed value. Normal operation, fault injection, and restoration follow the same procedure to exercise the detection path.

The saved Spike/OpenOCD run reported zero errors initially, one error after flipping bit 0 at index 17, and zero after restoration. The Renode software memory regression includes 29 cases. These results come from software checks on virtual targets.

### Foundation article

- [OpenOCD와 GDB: 연결, 정지 상태와 관찰의 의미](해설_notes/OpenOCD와GDB_debug-transport-state-observation.md#english)


## 심화 해설 | Advanced article

- [Watchpoint: 값이 바뀐 순간과 메모리 접근은 다르다](해설_notes/접근을잡는관찰점_watchpoints-access-values.md) · [English](해설_notes/접근을잡는관찰점_watchpoints-access-values.md#english)
