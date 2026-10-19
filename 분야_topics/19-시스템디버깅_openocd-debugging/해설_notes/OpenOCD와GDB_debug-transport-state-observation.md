# OpenOCD와 GDB: 연결, 정지 상태와 관찰의 의미

[OpenOCD & Debugging](../README.md) · [상태 모형](../../../예제_examples/확장기초_extended/systems/extended_models.py) · [검증 코드](../../../예제_examples/확장기초_extended/systems/test_extended_models.py)

## 한국어

### 디버깅에는 서로 다른 연결 단계가 있습니다

GDB는 심볼과 실행 상태를 이용해 코드를 살펴보는 debugger입니다. OpenOCD는 디버그 어댑터와 target을 제어하고 GDB가 접속할 서버를 제공할 수 있습니다. JTAG·SWD는 그 아래의 전송 방식입니다. PC에서 OpenOCD 프로세스가 떴다는 사실, 어댑터를 열었다는 사실, target을 인식했다는 사실, GDB가 심볼을 올바르게 연결했다는 사실은 각각 다릅니다. [OpenOCD GDB 연결](https://openocd.org/doc/html/GDB-and-OpenOCD.html)

어댑터 종류·USB 권한, 전송 방식, target 설정, reset 연결을 실제 보드에 맞춰야 합니다. JTAG와 SWD 지원은 어댑터·칩·설정에 달려 있습니다. system reset과 JTAG TAP reset도 같은 동작으로 가정하지 않습니다. [OpenOCD 어댑터 설정](https://openocd.org/doc/html/Debug-Adapter-Configuration.html)

### 실행 중인 시스템을 멈추면 무엇이 바뀔까요

CPU 레지스터 접근에는 보통 halted 상태가 필요합니다. `halt`는 정지를 요청하고, `resume`은 실행을 계속합니다. `reset halt`는 reset 이후 정지를 요청하지만 구체 효과와 지원 여부는 reset 설정·target에 달려 있습니다. CPU 정지가 timer·DMA·외부 장치의 정지까지 뜻하지는 않으므로, 정지 중 본 값을 자연 실행 중의 동시 snapshot이라고 곧바로 해석하지 않습니다. [OpenOCD General Commands](https://openocd.org/doc/html/General-Commands.html)

소프트웨어 breakpoint는 코드에 trap 등을 넣을 수 있고, 하드웨어 breakpoint·watchpoint는 장치 자원과 조건의 제약을 받습니다. flash 영역, 읽기 전용 코드와 최적화 여부에 따라 가능한 방식이 달라집니다. MMIO 값을 읽는 동작 자체가 상태를 바꿀 수 있는 레지스터도 있으므로 일반 RAM 관찰과 구분합니다.

### 소스 한 줄과 명령 한 개는 다릅니다

GDB의 `step`은 소스 수준으로 진행하며 함수 안으로 들어갈 수 있고, `next`는 현재 프레임의 다음 줄을 목표로 합니다. `stepi`는 기계 명령 수준으로 진행합니다. 최적화·inlining·디버그 정보의 유무 때문에 소스 줄과 실제 명령이 일대일로 대응하지 않을 수 있습니다. 한 줄이 여러 번 보이거나 변수가 최적화되어 사라져도 곧바로 compiler 오류라고 판단하지 않습니다. [GDB Continuing and Stepping](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Continuing-and-Stepping.html)

다음은 올바른 target 설정으로 OpenOCD를 시작했고, 대응되는 architecture의 GDB와 ELF 심볼이 준비되었다는 조건의 관찰 절차입니다. 3333은 일반적인 GDB 서버 포트이며 설정이 다르면 변경해야 합니다.

```gdb
file firmware.elf
target extended-remote localhost:3333
monitor halt
info registers pc
x/4i $pc
stepi
info registers pc
```

여기서 `file`은 호스트의 심볼 파일을 선택하는 것이고, 이 명령 묶음이 firmware를 flash에 기록하는 절차는 아닙니다. 실제 보드와 ELF가 같은 빌드인지 확인하고, PC와 disassembly를 먼저 연결합니다. `stepi` 뒤 PC가 항상 일정한 바이트 수만큼 증가하지는 않습니다. 분기·예외·명령 길이가 영향을 줍니다.

### 구현과 검증

`DebugTarget`은 실행·정지의 전제만 분리한 모형입니다. 정지 전 PC 읽기를 거부하고, 정지 상태에서만 지정한 길이의 단순 전이를 허용합니다. `step_model`은 분기 없는 가상 명령의 전이이며 Arm이나 RISC-V 명령을 실행하지 않습니다. 테스트는 전제 위반과 resume 이후 접근을 점검합니다.

실제 디버깅 기록에는 target·어댑터·전송 방식·clock·reset 설정, OpenOCD/GDB 버전, ELF digest와 관찰 시점을 연결합니다. 같은 문제가 debugger를 붙였을 때만 사라진다면 timing과 정지로 바뀐 주변장치 상태를 다시 살핍니다. 이 묶음에서 실장치 접속·flash 기록·단일 명령 실행을 검증했다고 주장하지 않습니다.

## English

### Debugging has several connection layers

GDB uses symbols and execution state. OpenOCD controls an adapter and target and can serve GDB. JTAG and SWD are underlying transports. Starting OpenOCD, opening an adapter, identifying a target, and matching correct ELF symbols are distinct milestones. [GDB and OpenOCD](https://openocd.org/doc/html/GDB-and-OpenOCD.html)

Adapter permissions, transport, target, and reset wiring must match the board. Transport support is device- and adapter-specific; system reset and JTAG TAP reset are not interchangeable. [Adapter configuration](https://openocd.org/doc/html/Debug-Adapter-Configuration.html)

### Halting changes the experiment

Core-register access generally requires a halted target. Halt requests a stop; resume continues execution. Reset-halt behavior depends on target/reset support. A stopped CPU does not necessarily stop timers, DMA, or external devices, so observations need not be a simultaneous snapshot of naturally running hardware. [General commands](https://openocd.org/doc/html/General-Commands.html)

Software breakpoints may alter code with traps; hardware breakpoints and watchpoints have resource and condition limits. Flash, read-only code, and optimization affect available methods. Some MMIO reads have side effects and therefore differ from reading ordinary RAM.

### A source line differs from one instruction

`step` advances at source level and can enter functions; `next` aims at the next line in the current frame; `stepi` operates at instruction level. Optimization, inlining, and debug information prevent a universal one-to-one mapping between lines and instructions. Missing optimized variables or surprising line movement alone do not establish a compiler fault. [GDB stepping](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Continuing-and-Stepping.html)

The command sequence assumes a configured OpenOCD target, matching architecture GDB, and correct ELF. Port 3333 is common but configurable. `file` selects host symbols; these commands do not describe flashing. Relate PC to disassembly and the actual loaded build. PC need not advance by a fixed byte count after `stepi` because branches, exceptions, and instruction sizes matter.

### Model and verification

`DebugTarget` only models running/halted preconditions. It rejects premature PC access and permits a specified straight-line transition while halted. It emulates neither Arm nor RISC-V instructions. Tests cover invalid state access and resumption.

Real records connect target, adapter, transport, clocks/reset, tool versions, ELF digest, and observation time. Debugger-dependent disappearance of a fault calls for examination of changed timing and peripheral state. The portable tests do not claim a hardware connection, flash programming, or real single stepping.

## 출처 / Sources

OpenOCD의 연결·target 규칙을 GDB의 소스/명령 진행 규칙과 대조했습니다. / OpenOCD target contracts were cross-checked with GDB stepping semantics. 확인 / checked: 2026-10-19.
