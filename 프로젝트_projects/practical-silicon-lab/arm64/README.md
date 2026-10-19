# ARM64 가상 타깃

호스트는 Linux이고, 실행 타깃은 QEMU `virt`의 Cortex-A53 한 코어입니다. 게스트 Linux 없이 `entry.S`가 stack과 BSS를 준비하고 `uart.c`로 진입합니다. `linker.ld`는 RAM 안의 ELF 배치를 정합니다.

필요한 도구는 `aarch64-linux-gnu-gcc`와 binutils, `qemu-system-aarch64`, Bash, GNU timeout입니다. DTB를 읽으려면 `dtc`, 대화형 디버깅에는 `gdb-multiarch`가 필요합니다. 도구는 별도로 설치된 환경을 전제로 합니다.

```sh
cd arm64
bash dump-dtb.sh
bash check.sh
```

`check.sh`는 정상 이미지를 빌드하고 4초 안에 B0(C 진입), B1(RAM smoke), B2(idle)를 관측합니다. 펌웨어는 끝에서 계속 대기하므로 timeout 종료 124를 허용합니다. 검사는 UART 문자열 기반이며 전기적 타이밍을 측정하지 않습니다.

```sh
bash build.sh stuck
timeout 4s bash run.sh run
```

`stuck`은 UART FIFO flag를 잘못 해석하는 오류입니다. 정상 상태의 phase=4에 도달하지 못하고 polling 경로에 머무르는 것이 기대 결과입니다. `wrong-base`는 잘못된 UART 주소를 넣는 별도 이미지이며, exception handler가 없는 이 최소 예제에서의 결과를 실물의 동작으로 일반화하지 않습니다.

대화형 GDB를 사용할 때는 첫 터미널에서 `bash build.sh normal` 후 `bash run.sh debug`, 두 번째 터미널에서 `gdb-multiarch -x debug.gdb`를 실행합니다. debug 모드는 localhost 1234에 GDB endpoint를 열고 첫 명령 전에 멈춥니다. QEMU terminal 종료 키는 Ctrl+A를 누르고 놓은 뒤 X입니다. 2026-10-19 검사에서는 이 debug endpoint를 열지 않았습니다.

RAM base는 `0x40000000`, ELF entry는 `0x40080000`으로 설정되어 있습니다. PL011 base `0x09000000`은 이 machine 구성의 값입니다. `build/virt.dts`의 `reg`와 실제 QEMU 버전을 대조합니다. 이 firmware는 DTB를 직접 파싱하지 않습니다. QEMU의 ELF loader가 RAM을 준비한 시작 조건이므로 실물 Boot ROM·DDR training·전원 시퀀스는 포함하지 않습니다.

공식 문서: [QEMU Arm virt](https://www.qemu.org/docs/master/system/arm/virt.html), [QEMU GDB](https://www.qemu.org/docs/master/system/gdb.html).

## English

The build host is Linux and the execution target is one Cortex-A53 core in QEMU `virt`. Without a guest Linux kernel, `entry.S` prepares the stack/BSS and enters `uart.c`; `linker.ld` places the ELF in RAM.

Use `aarch64-linux-gnu-gcc`/binutils, `qemu-system-aarch64`, Bash and GNU timeout. Reading the DTB needs `dtc`; interactive debugging needs `gdb-multiarch`. The tools are installed separately. Run `dump-dtb.sh` and `check.sh` from `arm64/` as shown above.

`check.sh` builds the normal image and observes B0 (C entry), B1 (RAM smoke) and B2 (idle) within four seconds. Firmware remains idle, so timeout exit 124 is accepted. The check observes UART text, not electrical timing.

The `stuck` image intentionally misinterprets a UART FIFO flag. It should remain in polling rather than reach normal phase 4. `wrong-base` uses an incorrect UART address. This minimal example has no exception handler; its behavior does not describe every physical target.

For GDB, run `bash build.sh normal` followed by `bash run.sh debug` in one terminal and `gdb-multiarch -x debug.gdb` in another. Debug mode binds localhost port 1234 and stops before the first instruction; QEMU exits with Ctrl+A, release, then X. The October 19 check did not open that debug endpoint.

RAM starts at `0x40000000`; ELF entry is `0x40080000`. PL011 base `0x09000000` belongs to this machine configuration. Compare `reg` in `build/virt.dts` with the actual QEMU version; firmware does not parse the DTB. QEMU's ELF loader prepares RAM, so physical Boot ROM, DDR training and power sequencing are outside this example. Official QEMU machine/GDB documentation is linked above.
