# MCU 펌웨어와 디버깅 실습

C 코드가 CPU 명령으로 바뀌고, 실행 결과가 레지스터와 메모리에 반영되는 과정을 다룬다. Arm Cortex-M7과 RISC-V RV64IMAC에 같은 계산 코드를 사용하고, GDB로 명령 실행 전후의 상태를 비교한다.

| 경로 | 대상 | 내용 |
| --- | --- | --- |
| `arm/` | Renode의 STM32F767ZI 모델 | Cortex-M7 시작 코드, 메모리 배치, GDB 실행 확인 |
| `riscv/` | Spike + OpenOCD | RV64IMAC 시작 코드, 가상 JTAG, GDB 연결 |
| `stm32-gpio/` | STM32F767ZI | CMSIS 레지스터 정의를 이용한 GPIO 제어 |
| `esp32/` | ESP32 + Arduino 프레임워크 | FreeRTOS task·queue·mutex를 이용한 명령 처리 |
| `common/` | 공통 C 코드 | 메모리 패턴 검사와 연산 signature |

## C 코드와 CPU 상태

`main.c`는 `input_a=1`, `input_b=3`을 읽고 `result=4`, `trace={4,5}`를 저장한다. 덧셈이 끝나는 시점과 메모리에 값을 쓰는 시점은 서로 다르다. Arm에서는 `add`, RISC-V에서는 `addw`와 그 뒤의 저장 명령을 기준으로 이 차이를 관찰한다.

저장된 가상 실행 기록에서 두 대상 모두 최종값이 `result=4`, `trace={4,5}`로 확인됐다. STM32 GPIO와 ESP32 코드는 MCU용 예제이며, 함께 제공된 새 펌웨어의 확인 범위는 빌드·링크까지다.

## 실행 구성

Arm 경로는 `GDB → Renode GDB server → Cortex-M7 모델`이다. RISC-V 경로는 `GDB → OpenOCD → remote_bitbang → Spike`이며, 이 경로에서는 OpenOCD의 JTAG 디버그 접근을 사용한다. Renode의 직접 GDB 연결과 OpenOCD 연결은 별도의 구성이다.

빌드와 디버그 명령은 [BUILD.md](BUILD.md)에 정리했다.

## STM32 GPIO

`RCC->AHB1ENR`로 GPIOB의 클록을 활성화하고, `GPIOB->MODER`로 PB0을 출력 모드로 설정한다. 메인 루프에서는 `GPIOB->ODR`의 bit 0을 반전한다. `stm32f767xx.h`와 CMSIS는 STMicroelectronics의 공식 배포본을 사용한다.

## ESP32 명령 처리

호스트가 UART로 `RUN,<sequence>`를 보내면 수신 루프가 명령을 파싱해 queue에 넣는다. worker task는 내부 RAM에서 메모리 패턴 검사와 연산 signature 계산을 수행하고 JSON 결과를 반환한다. mutex는 여러 실행 흐름의 출력이 섞이는 것을 방지한다. 같은 sequence의 재요청에는 저장한 결과를 반환한다.

PlatformIO 설정은 classic ESP32 Dev Module과 Arduino 프레임워크를 지정한다. ESP32는 실행 대상 SoC이고, Arduino는 이 예제에서 사용하는 소프트웨어 프레임워크다.

## 참고 자료

- [STMicroelectronics STM32F767ZI](https://www.st.com/en/microcontrollers-microprocessors/stm32f767zi.html)
- [STMicroelectronics CMSIS Device F7](https://github.com/STMicroelectronics/cmsis-device-f7)
- [Renode GDB debugging](https://renode.readthedocs.io/en/latest/debugging/gdb.html)
- [OpenOCD GDB connection](https://openocd.org/doc/html/GDB-and-OpenOCD.html)
- [Spike RISC-V ISA simulator](https://github.com/riscv-software-src/riscv-isa-sim)
- [Arduino core for ESP32](https://docs.espressif.com/projects/arduino-esp32/en/latest/)
