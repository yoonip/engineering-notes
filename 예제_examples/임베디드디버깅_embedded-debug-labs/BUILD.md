# 빌드와 디버그 구성

## Arm Cortex-M7

프로젝트 루트에서 실행하는 GNU Arm Embedded Toolchain 명령입니다. ELF에는 실행 코드, 데이터 배치, 심볼과 디버그 정보가 포함됩니다.

```sh
mkdir -p arm/build
arm-none-eabi-gcc -mcpu=cortex-m7 -mthumb -O0 -g3 -ffreestanding -nostdlib -T arm/link.ld arm/start.S arm/main.c -o arm/build/step.elf
arm-none-eabi-objdump -d -S arm/build/step.elf
```

Renode 모니터에서 플랫폼과 ELF를 불러오고 GDB 서버를 엽니다.

```text
include @arm/step.resc
```

다른 터미널의 GDB가 실행과 결과를 확인합니다.

```sh
arm-none-eabi-gdb arm/build/step.elf -x arm/verify.gdb
```

## RISC-V RV64IMAC

```sh
mkdir -p riscv/build
riscv-none-elf-gcc -march=rv64imac -mabi=lp64 -mcmodel=medany -O0 -g3 -ffreestanding -nostdlib -T riscv/link.ld riscv/start.S riscv/main.c -o riscv/build/step.elf
riscv-none-elf-objdump -d -S riscv/build/step.elf
```

Spike의 remote-bitbang 서버와 OpenOCD를 각각 실행합니다. 각 명령은 계속 실행되는 별도 프로세스입니다.

```sh
spike --isa=RV64IMAC --rbb-port=9824 -m0x80000000:0x20000 -H riscv/build/step.elf
openocd -f riscv/spike.cfg
riscv-none-elf-gdb riscv/build/step.elf -x riscv/verify.gdb
```

OpenOCD의 GDB 포트는 `3334`, Spike의 remote-bitbang 포트는 `9824`입니다. 모두 로컬 연결을 사용합니다.

## 명령 단위 관찰

GDB에서 `break main`과 `continue`로 시작 위치에 도달한 뒤 실행할 수 있는 조회 명령입니다.

```gdb
disassemble /m main
info registers
x/wx &result
stepi
info registers
x/wx &result
```

`stepi`는 CPU 명령 한 개를 실행합니다. `step`은 소스 수준으로 실행하며, C 한 줄에 여러 CPU 명령이 대응할 수 있습니다.

## ESP32

`esp32/platformio.ini`에 지정한 환경에서 C++ 코드를 빌드합니다.

```sh
cd esp32
pio run
```

## STM32 GPIO

`stm32-gpio/main.c`는 STM32CubeIDE의 STM32F767ZI 프로젝트에 사용하는 소스입니다. ST의 CMSIS 코어·디바이스 헤더와 시작 코드, 링커 스크립트가 필요합니다. Cortex-M7 컴파일 대상과 보드 핀 배치는 해당 프로젝트 설정을 따릅니다.

## English

Run the Arm and RISC-V commands above from this example's root. ELF files contain executable code, data layout, symbols and debug information.

### Arm Cortex-M7

The GNU Arm commands compile Cortex-M7/Thumb startup and C code using `arm/link.ld`, then disassemble the ELF. In Renode, `include @arm/step.resc` loads the platform/ELF and opens its GDB server. Run `arm-none-eabi-gdb` with `arm/verify.gdb` in a second terminal to inspect execution/results.

### RISC-V RV64IMAC

Compile with `-march=rv64imac -mabi=lp64 -mcmodel=medany`, using the startup and linker files shown above. Spike, OpenOCD and GDB are separate long-running processes. Spike's remote-bitbang port is 9824 and OpenOCD's GDB port is 3334; both are local connections.

### Instruction-level observation

After `break main` and `continue`, use the listed disassembly, register and memory commands around `stepi`. `stepi` executes one CPU instruction; source-level `step` may execute several instructions for one C line.

### MCU builds

Build ESP32 with `pio run` from `esp32/`, using `platformio.ini`. `stm32-gpio/main.c` belongs in a STM32CubeIDE STM32F767ZI project with official ST CMSIS core/device headers, startup and linker files. Use that project's Cortex-M7 target and board pin settings.
