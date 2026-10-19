#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
mode="${1:-normal}"
defs=()
case "$mode" in
  normal) ;;
  stuck) defs=(-DREADY_MASK=128u) ;; # TXFE bit7: intentional poll bug.
  wrong-base) defs=(-DUART_BASE=0x09001000UL) ;;
  *) echo "Usage: bash build.sh [normal|stuck|wrong-base]" >&2; exit 2 ;;
esac
command -v aarch64-linux-gnu-gcc >/dev/null
mkdir -p build
# Bare-metal use of a cross compiler: no Linux syscall or runtime is linked.
aarch64-linux-gnu-gcc -g3 -O0 -ffreestanding -fno-builtin \
  -fno-stack-protector -fno-pic -fno-pie -mgeneral-regs-only \
  -nostdlib -static -no-pie -Wl,--build-id=none \
  -Wl,-T,linker.ld -Wl,-Map,build/bringup.map \
  -Wall -Wextra "${defs[@]}" entry.S uart.c -o build/bringup.elf
aarch64-linux-gnu-objdump -d build/bringup.elf > build/disasm.txt
aarch64-linux-gnu-readelf -h -l build/bringup.elf > build/elf.txt
printf '%s\n' "$mode" > build/mode.txt
printf 'Built %s mode. Inspect build/elf.txt and build/disasm.txt.\n' "$mode"
