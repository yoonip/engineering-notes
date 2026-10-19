#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
machine="${QEMU_MACHINE:-virt}"
mode="${1:-run}"
extra=()
case "$mode" in
  run) ;;
  debug) extra=(-S -gdb tcp:127.0.0.1:1234) ;; # Stop before first opcode.
  *) echo "Usage: bash run.sh [run|debug]" >&2; exit 2 ;;
esac
[[ -s build/bringup.elf ]] || { echo "Run bash build.sh first" >&2; exit 2; }
# -kernel accepts this ELF; QEMU loads its segments and starts at its entry.
exec qemu-system-aarch64 -M "$machine" -cpu cortex-a53 \
  -m 128M -smp 1 -nographic -no-reboot \
  -kernel build/bringup.elf "${extra[@]}"
