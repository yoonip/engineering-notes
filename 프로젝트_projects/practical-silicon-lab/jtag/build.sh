#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
command -v arm-none-eabi-gcc >/dev/null
mkdir -p build
# soft ABI avoids enabling the FPU during this minimal startup.
arm-none-eabi-gcc -mcpu=cortex-m4 -mthumb -mfloat-abi=soft \
  -g3 -O0 -ffreestanding -fno-builtin -fno-stack-protector \
  -ffunction-sections -fdata-sections -nostdlib \
  -Wl,--gc-sections -Wl,--build-id=none -Wl,-T,stm32f401re.ld \
  -Wl,-Map,build/blink.map -Wall -Wextra \
  startup.S blink.c -o build/blink.elf
# Keep the symbolic ELF. The .bin alone has no GDB source/variable metadata.
arm-none-eabi-objcopy -O binary build/blink.elf build/blink.bin
arm-none-eabi-readelf -h -l build/blink.elf > build/elf.txt
arm-none-eabi-objdump -d -S build/blink.elf > build/disasm.txt
arm-none-eabi-objdump -s -j .isr_vector build/blink.elf \
  > build/vector.txt
arm-none-eabi-size build/blink.elf
