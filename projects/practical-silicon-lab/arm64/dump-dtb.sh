#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
machine="${QEMU_MACHINE:-virt}"
mkdir -p build
qemu-system-aarch64 -M "$machine",dumpdtb=build/virt.dtb \
  -cpu cortex-a53 -m 128M -smp 1 -nographic
dtc -I dtb -O dts build/virt.dtb -o build/virt.dts
printf '%s\n' "Read PL011 reg and memory nodes in build/virt.dts."
grep -A12 -E 'pl011@|memory@' build/virt.dts || true
