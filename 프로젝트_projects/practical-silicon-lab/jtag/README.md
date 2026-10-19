# TAP 모델과 Cortex-M4 디버깅 참조

`tap_walk.py`는 TMS 입력에 따른 16-state TAP 전이만 계산합니다. 프로브를 열거나 IDCODE를 읽지 않습니다.

```sh
python -B tap_walk.py --start Shift-DR --tms 1111101100
```

마지막 상태는 `Shift-IR`입니다. 모든 상태에서 TMS=1을 5회 적용하면 `Test-Logic-Reset`에 도달합니다. 실제 shift register의 데이터·전압·TCK timing은 모델 범위 밖입니다.

## 펌웨어 빌드

물리 참조 보드는 NUCLEO-F401RE / STM32F401RE, 프로브는 onboard ST-LINK/V2-1입니다. 주소와 핀 설정은 이 보드에 한정됩니다. `arm-none-eabi-gcc`와 binutils, Bash가 있는 호스트에서 다음을 실행합니다.

```sh
bash build.sh
cat build/vector.txt
```

`startup.S`는 초기 SP/reset vector, `.data` 복사, `.bss` 초기화를 제공합니다. `blink.c`는 PA5/LD2를 구동합니다. `stm32f401re.ld`의 flash 512 KiB와 SRAM 96 KiB는 이 MCU의 배치입니다. 16개 core vector만 정의하며 외부 IRQ는 활성화하지 않습니다. Busy loop는 정확한 시간 측정 수단이 아닙니다.

## 실제 보드 연결 절차

보드의 UM1724와 해당 revision의 전원·CN2 jumper 구성을 먼저 대조합니다. 아래 명령은 application flash를 덮어쓰며 실제 보드가 필요한 절차입니다. 2026-10-19 검사에서는 실행하지 않았습니다.

```sh
# 터미널 A: OpenOCD v0.12.0 설정을 사용한다.
openocd --version
openocd -f nucleo_f401re_openocd012.cfg -l build/openocd.log

# 터미널 B: build/blink.elf를 load하고 main에서 멈춘다.
gdb-multiarch -x debug.gdb
```

OpenOCD 설정은 설치된 공식 `interface/stlink-dap.cfg`와 `target/stm32f4x.cfg`를 참조합니다. 이 저장소에 vendor script를 복사하지 않았습니다. `nucleo_f401re_hla012.cfg`는 같은 0.12.0의 HLA 대안이며, OpenOCD 버전마다 transport 이름을 확인해야 합니다. 프로세스는 localhost에만 bind합니다.

`main` 진입 전 기대값은 phase=1, magic=`0x13579bdf`, blink_count=0입니다. 계속 실행한 뒤 phase=4와 증가하는 counter를 관측합니다. RCC `0x40023830`, GPIO MODER `0x40020000`, ODR `0x40020014`, IDR `0x40020010`의 값과 실제 PA5/D13 파형은 서로 다른 관측입니다. Register 값만으로 핀 전압이나 LED 연결을 확인한 것으로 보지 않습니다.

공식 문서: [ST UM1724](https://www.st.com/resource/en/user_manual/um1724-stm32-nucleo64-boards-mb1136-stmicroelectronics.pdf), [STM32F401 문서](https://www.st.com/en/microcontrollers-microprocessors/stm32f401/documentation.html), [OpenOCD](https://openocd.org/doc-release/html/index.html).

## English

`tap_walk.py` computes only the sixteen TAP states driven by TMS. It does not open a probe or read IDCODE. The example sequence ends in `Shift-IR`; five TMS=1 clocks reach `Test-Logic-Reset` from every state. Shift-register data, voltage and TCK timing are outside the model.

### Firmware and physical reference

The reference is NUCLEO-F401RE/STM32F401RE with onboard ST-LINK/V2-1. Addresses and pins apply to this board. Use `arm-none-eabi-gcc`, binutils and Bash to run the build commands above.

`startup.S` defines the initial SP/reset vector, copies `.data` and clears `.bss`; `blink.c` drives PA5/LD2. The linker uses this MCU's 512 KiB flash and 96 KiB SRAM. Only sixteen core vectors are defined, with no external IRQs enabled. The busy loop is not a precise timer.

Check UM1724 and the board revision's power/CN2 jumpers before the physical-board procedure. The listed OpenOCD/GDB commands overwrite application flash and require the real target; they were not run in the October 19 check.

OpenOCD configuration references installed official `interface/stlink-dap.cfg` and `target/stm32f4x.cfg`; vendor scripts are not copied here. `nucleo_f401re_hla012.cfg` is an HLA alternative for version 0.12.0. Transport names depend on OpenOCD version. Processes bind only to localhost.

Expected values before entering `main` are phase=1, magic=`0x13579bdf` and blink_count=0. After continuing, inspect phase=4 and an increasing counter. RCC `0x40023830`, GPIO MODER `0x40020000`, ODR `0x40020014` and IDR `0x40020010` are register observations; PA5/D13 voltage and LED wiring need separate physical observation. Official ST/OpenOCD references are linked above.
