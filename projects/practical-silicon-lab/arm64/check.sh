#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
bash build.sh normal
set +e
timeout 4s bash run.sh run > build/serial.log 2>&1
rc=$?
set -e
if [[ "$rc" != 124 && "$rc" != 0 ]]; then
  cat build/serial.log
  printf 'QEMU failed with exit code %s\n' "$rc" >&2
  exit 1
fi
grep -q 'B0: C entry; UART alive' build/serial.log
grep -q 'B1: RAM smoke PASS' build/serial.log
grep -q 'B2: idle' build/serial.log
printf '%s\n' "PASS: observed B0, B1, B2. Timeout is expected at idle."
cat build/serial.log
