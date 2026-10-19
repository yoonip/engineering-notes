# MCU 펌웨어와 디버깅 실습

C 코드가 CPU 명령으로 바뀌고, 실행 결과가 레지스터와 메모리에 반영되는 과정을 다룹니다. Arm Cortex-M7과 RISC-V RV64IMAC에 같은 계산 코드를 사용하고, GDB로 명령 실행 전후의 상태를 비교합니다.

| 경로 | 대상 | 내용 |
| --- | --- | --- |
| `arm/` | Renode의 STM32F767ZI 모델 | Cortex-M7 시작 코드, 메모리 배치, GDB 실행 확인 |
| `riscv/` | Spike + OpenOCD | RV64IMAC 시작 코드, 가상 JTAG, GDB 연결 |
| `stm32-gpio/` | STM32F767ZI | CMSIS 레지스터 정의를 이용한 GPIO 제어 |
| `esp32/` | ESP32 + Arduino 프레임워크 | FreeRTOS task·queue·mutex를 이용한 명령 처리 |
| `common/` | 공통 C 코드 | 메모리 패턴 검사와 연산 signature |

## C 코드와 CPU 상태

`main.c`는 `input_a=1`, `input_b=3`을 읽고 `result=4`, `trace={4,5}`를 저장합니다. 덧셈이 끝나는 시점과 메모리에 값을 쓰는 시점은 서로 다릅니다. Arm에서는 `add`, RISC-V에서는 `addw`와 그 뒤의 저장 명령을 기준으로 이 차이를 관찰합니다.

저장된 가상 실행 기록에서 두 대상 모두 최종값이 `result=4`, `trace={4,5}`로 확인됐습니다. STM32 GPIO와 ESP32 코드는 MCU용 예제이며, 함께 제공된 새 펌웨어의 확인 범위는 빌드·링크까지입니다.

## 실행 구성

Arm 경로는 `GDB → Renode GDB server → Cortex-M7 모델`입니다. RISC-V 경로는 `GDB → OpenOCD → remote_bitbang → Spike`이며, 이 경로에서는 OpenOCD의 JTAG 디버그 접근을 사용합니다. Renode의 직접 GDB 연결과 OpenOCD 연결은 별도의 구성입니다.

빌드와 디버그 명령은 [BUILD.md](BUILD.md)에 정리했습니다.

## STM32 GPIO

`RCC->AHB1ENR`로 GPIOB의 클록을 활성화하고, `GPIOB->MODER`로 PB0을 출력 모드로 설정합니다. 메인 루프에서는 `GPIOB->ODR`의 bit 0을 반전합니다. `stm32f767xx.h`와 CMSIS는 STMicroelectronics의 공식 배포본을 사용합니다.

## ESP32 명령 처리

호스트가 UART로 `RUN,<sequence>`를 보내면 수신 루프가 명령을 파싱해 queue에 넣습니다. worker task는 내부 RAM에서 메모리 패턴 검사와 연산 signature 계산을 수행하고 JSON 결과를 반환합니다. mutex는 여러 실행 흐름의 출력이 섞이는 것을 방지합니다. 같은 sequence의 재요청에는 저장한 결과를 반환합니다.

PlatformIO 설정은 classic ESP32 Dev Module과 Arduino 프레임워크를 지정합니다. ESP32는 실행 대상 SoC이고, Arduino는 이 예제에서 사용하는 소프트웨어 프레임워크입니다.

## 참고 자료

- [STMicroelectronics STM32F767ZI](https://www.st.com/en/microcontrollers-microprocessors/stm32f767zi.html)
- [STMicroelectronics CMSIS Device F7](https://github.com/STMicroelectronics/cmsis-device-f7)
- [Renode GDB debugging](https://renode.readthedocs.io/en/latest/debugging/gdb.html)
- [OpenOCD GDB connection](https://openocd.org/doc/html/GDB-and-OpenOCD.html)
- [Spike RISC-V ISA simulator](https://github.com/riscv-software-src/riscv-isa-sim)
- [Arduino core for ESP32](https://docs.espressif.com/projects/arduino-esp32/en/latest/)

## English

These exercises follow C code into CPU instructions and observe register/memory changes. Arm Cortex-M7 and RISC-V RV64IMAC run the same calculation, with GDB comparing the states before and after instructions.

| Directory | Target | Content |
| --- | --- | --- |
| `arm/` | Renode STM32F767ZI | Cortex-M7 startup, memory layout and GDB verification |
| `riscv/` | Spike/OpenOCD | RV64IMAC startup, virtual JTAG and GDB |
| `stm32-gpio/` | STM32F767ZI | CMSIS-register GPIO control |
| `esp32/` | ESP32/Arduino | FreeRTOS task/queue/mutex command handling |
| `common/` | Shared C | Memory-pattern checks and arithmetic signature |

### CPU state and debug paths

`main.c` reads `input_a=1` and `input_b=3`, then stores `result=4` and `trace={4,5}`. Arithmetic completion and memory stores happen at different instructions: Arm `add` and RISC-V `addw` precede their stores. Recorded virtual runs ended with the expected values on both targets. MCU GPIO/ESP32 examples have build/link records rather than physical-board validation.

Arm uses GDB → Renode GDB server → Cortex-M7 model. RISC-V uses GDB → OpenOCD → remote_bitbang → Spike, exercising JTAG debug access. Direct Renode GDB and OpenOCD are separate configurations. Commands are in [BUILD.md](BUILD.md).

### MCU examples

STM32 enables GPIOB through `RCC->AHB1ENR`, sets PB0 output mode through `GPIOB->MODER` and toggles bit 0 of `GPIOB->ODR`. `stm32f767xx.h` and CMSIS come from STMicroelectronics.

For ESP32, the host sends `RUN,<sequence>` over UART. The receive loop parses/enqueues it; a worker runs internal-RAM pattern checks and an arithmetic signature, then returns JSON. A mutex prevents interleaved output, and repeated sequences receive the cached result. PlatformIO selects the classic ESP32 Dev Module and Arduino software framework. Official ST, Renode, OpenOCD, Spike and ESP32 references are linked above.
