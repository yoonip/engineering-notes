# TAP 모델과 Cortex-M4 디버깅 참조

`tap_walk.py`는 TMS 입력에 따른 16-state TAP 전이만 계산한다. 프로브를 열거나 IDCODE를 읽지 않는다.

```sh
python -B tap_walk.py --start Shift-DR --tms 1111101100
```

마지막 상태는 `Shift-IR`이다. 모든 상태에서 TMS=1을 5회 적용하면 `Test-Logic-Reset`에 도달한다. 실제 shift register의 데이터·전압·TCK timing은 모델 범위 밖이다.

## 펌웨어 빌드

물리 참조 보드는 **NUCLEO-F401RE / STM32F401RE**, 프로브는 onboard ST-LINK/V2-1이다. 주소와 핀 설정은 이 보드에 한정된다. `arm-none-eabi-gcc`와 binutils, Bash가 있는 호스트에서 다음을 실행한다.

```sh
bash build.sh
cat build/vector.txt
```

`startup.S`는 초기 SP/reset vector, `.data` 복사, `.bss` 초기화를 제공한다. `blink.c`는 PA5/LD2를 구동한다. `stm32f401re.ld`의 flash 512 KiB와 SRAM 96 KiB는 이 MCU의 배치다. 16개 core vector만 정의하며 외부 IRQ는 활성화하지 않는다. Busy loop는 정확한 시간 측정 수단이 아니다.

## 실제 보드 연결 절차

보드의 UM1724와 해당 revision의 전원·CN2 jumper 구성을 먼저 대조한다. 아래 명령은 application flash를 덮어쓰며 실제 보드가 필요한 절차다. 이번 배포 검사에서는 실행하지 않았다.

```sh
# 터미널 A: OpenOCD v0.12.0 설정을 사용한다.
openocd --version
openocd -f nucleo_f401re_openocd012.cfg -l build/openocd.log

# 터미널 B: build/blink.elf를 load하고 main에서 멈춘다.
gdb-multiarch -x debug.gdb
```

OpenOCD 설정은 설치된 공식 `interface/stlink-dap.cfg`와 `target/stm32f4x.cfg`를 참조한다. 이 저장소에 vendor script를 복사하지 않았다. `nucleo_f401re_hla012.cfg`는 같은 0.12.0의 HLA 대안이며, OpenOCD 버전마다 transport 이름을 확인해야 한다. 프로세스는 localhost에만 bind한다.

`main` 진입 전 기대값은 phase=1, magic=`0x13579bdf`, blink_count=0이다. 계속 실행한 뒤 phase=4와 증가하는 counter를 관측한다. RCC `0x40023830`, GPIO MODER `0x40020000`, ODR `0x40020014`, IDR `0x40020010`의 값과 실제 PA5/D13 파형은 서로 다른 관측이다. Register 값만으로 핀 전압이나 LED 연결을 확인한 것으로 보지 않는다.

공식 문서: [ST UM1724](https://www.st.com/resource/en/user_manual/um1724-stm32-nucleo64-boards-mb1136-stmicroelectronics.pdf), [STM32F401 문서](https://www.st.com/en/microcontrollers-microprocessors/stm32f401/documentation.html), [OpenOCD](https://openocd.org/doc-release/html/index.html).
