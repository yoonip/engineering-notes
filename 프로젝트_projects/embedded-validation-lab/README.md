# Embedded validation lab

메모리 패턴 검사와 연산 signature를 C 펌웨어로 구현합니다. QEMU·RTL 시뮬레이션과 UART 호스트 검사를 연결하고, STM32F767ZI·ESP32용 펌웨어를 함께 제공합니다. 실제 보드 시험과 빌드·시뮬레이션의 범위는 아래 실행 기록에 구분했습니다.

## 구성

| 경로 | 내용 |
| --- | --- |
| `common/` | March C− 메모리 검사, 첫 오류 기록, 연산 signature, freestanding runtime |
| `arm/` | Cortex-M7 시작 코드와 QEMU semihosting 실행 |
| `riscv/` | RV32I 펌웨어와 명령어별 directed test |
| `rtl/` | RV32I CPU, SystemVerilog testbench, Python 명령 실행 참조 모델 |
| `stm32/` | STM32F767ZI 클록·GPIO·UART 설정과 명령 처리 |
| `esp32/` | FreeRTOS task·queue·mutex를 이용한 UART 명령 처리 |
| `host/` | sequence 확인, 재시도, timeout, JSON 판정, CSV·JSONL 저장 |
| `mnist/` | CNN 학습·검증·추론과 결과 시각화 |

## 검증 흐름

메모리 검사는 1,024개의 32비트 word를 대상으로 패턴을 쓰고 읽으며 불일치 개수와 첫 오류 위치를 기록합니다. 별도의 정수 연산은 고정된 입력에서 `0x6fda2ac4` signature를 만듭니다. 메모리와 연산 결과를 함께 확인해 서로 다른 실패 원인을 구분합니다.

RV32I testbench는 CPU가 retire한 명령의 PC, 명령어, 목적 레지스터와 값을 Python 참조 모델의 trace와 비교합니다. 메모리 응답에 무작위 지연을 넣고, 잘못된 명령·비정렬 접근·접근 오류·ECALL을 각각 검사합니다. 펌웨어 실행에서는 mailbox에 기록된 메모리 오류 수와 signature도 비교합니다.

UART 호스트는 `RUN,<sequence>`를 전송합니다. 응답의 board·sequence·version·검사 길이·필드 타입·signature를 검증하며, 재시도에는 같은 sequence를 사용합니다. ESP32 worker는 직전 결과를 캐시해 같은 요청의 중복 실행을 피합니다. 장치 응답 원문은 JSONL, 실행별 요약은 CSV로 저장합니다.

## 실행 확인

2026년 10월 19일 이 폴더의 소스로 다시 실행한 결과입니다.

| 검사 | 결과 |
| --- | --- |
| Cortex-M7 펌웨어 | 컴파일·링크, QEMU 메모리·signature 검사 통과 |
| STM32F767ZI 펌웨어 | CMSIS 헤더를 사용한 컴파일·링크 통과 |
| RV32I CPU | 펌웨어와 directed test 각 seed 1·7·42, 예외 8종을 포함한 14회 실행 통과 |
| UART 호스트 | stale 응답, 분할 수신, timeout, 필드 오류 등을 포함한 10개 단위 검사 통과 |

ESP32 펌웨어의 저장된 빌드 기록에서는 컴파일·링크와 이미지 생성을 확인했습니다. 이 결과들은 시뮬레이션·컴파일·호스트 검사에 해당하며, 실제 보드에서 얻은 UART 측정값은 포함하지 않습니다.

## CPU·펌웨어 검사 실행

Python 3, Arm GNU Toolchain, RISC-V GNU Toolchain, QEMU, Icarus Verilog를 사용합니다. `arm-none-eabi-gcc`, `riscv-none-elf-gcc`, `qemu-system-arm`, `iverilog`, `vvp`가 PATH에 있으면 자동으로 찾습니다. 개별 실행 파일은 `ARM_GCC`, `RISCV_GCC`, `QEMU_ARM`, `IVERILOG`, `VVP` 환경변수로 지정할 수 있습니다. `RISCV_OBJCOPY`는 별도로 지정하거나 RISC-V GCC와 같은 디렉터리의 실행 파일을 사용합니다.

STM32 빌드에는 외부 CMSIS 헤더 두 종류가 필요합니다. `CMSIS_CORE_INCLUDE`는 `core_cm7.h`가 있는 디렉터리, `CMSIS_DEVICE_INCLUDE`는 `stm32f767xx.h`가 있는 디렉터리를 가리킵니다.

```bash
python build_all.py
```

실행 로그와 참조 trace, ELF·HEX, 최종 `verification.json`은 `build/`에 생성됩니다. 생성물은 Git 추적에서 제외합니다.

## UART 호스트 검사

```bash
python -m pip install -r host/requirements.txt
python -m unittest discover -s host -p "test_protocol.py" -v
```

장치와 통신할 때는 연결된 포트와 board를 지정합니다.

```bash
python host/run_validation.py --port COM6 --board ESP32 --runs 100
```

ESP32 프로젝트는 `esp32/`에서 `pio run`으로 빌드합니다. PlatformIO 설정은 classic ESP32 Dev Module과 Arduino 프레임워크를 사용합니다.


## 참고 자료

- [RISC-V specifications](https://riscv.org/specifications/)
- [Arm CMSIS Core](https://github.com/ARM-software/CMSIS_6)
- [STM32F7 CMSIS Device](https://github.com/STMicroelectronics/cmsis-device-f7)
- [QEMU Arm system emulation](https://www.qemu.org/docs/master/system/target-arm.html)
- [Arduino core for ESP32](https://docs.espressif.com/projects/arduino-esp32/en/latest/)

## English

This lab implements memory-pattern checks and an arithmetic signature in C, then compares results through CPU simulation and UART automation. Targets include Arm Cortex-M7, a SystemVerilog RV32I CPU, STM32F767ZI and ESP32.

### Components and protocol

| Path | Content |
| --- | --- |
| `common/` | March C− test, first-error capture, arithmetic signature and freestanding runtime |
| `arm/` | Cortex-M7 startup and QEMU semihosting |
| `riscv/` | RV32I firmware and directed instruction tests |
| `rtl/` | RV32I CPU, SystemVerilog testbench and Python instruction reference |
| `stm32/` | STM32F767ZI clock, GPIO, UART and command handling |
| `esp32/` | UART commands with FreeRTOS tasks, queues and mutexes |
| `host/` | Sequence checks, retries, timeout, JSON verdicts and CSV/JSONL export |
| `mnist/` | CNN training, evaluation, inference and plots |

The memory test writes and reads 1,024 32-bit words, recording mismatch count and first failure. A separate fixed-input calculation produces signature `0x6fda2ac4`. Checking both helps distinguish memory faults from computation faults.

The RV32I testbench compares retired PC, instruction, destination register and value against the Python trace. It injects random memory-response delays and checks illegal instructions, misaligned accesses, access faults and ECALL. Firmware mailbox values supply the memory-error count and signature.

The host sends `RUN,<sequence>` and checks board, sequence, version, test length, field types and signature. Retries reuse the same sequence; the ESP32 worker caches its latest response to avoid duplicate execution. Raw responses are saved as JSONL and per-run summaries as CSV.

### Verification

The October 19, 2026 source checks passed Cortex-M7 compilation/linking and QEMU memory/signature execution, STM32F767ZI compilation/linking with CMSIS, fourteen RV32I runs and ten host tests. RV32I coverage includes firmware/directed cases with seeds 1, 7 and 42 and eight exception types. Host cases include stale responses, fragmented reads, timeout and malformed fields. An earlier ESP32 record covers compilation, linking and image generation. These are simulation/build/host checks rather than physical-board UART measurements.

### Running the lab

Use Python 3, Arm/RISC-V GNU toolchains, QEMU and Icarus Verilog. The runner discovers `arm-none-eabi-gcc`, `riscv-none-elf-gcc`, `qemu-system-arm`, `iverilog` and `vvp` on PATH. Override them with `ARM_GCC`, `RISCV_GCC`, `QEMU_ARM`, `IVERILOG` and `VVP`. `RISCV_OBJCOPY` can be set separately or resolved beside RISC-V GCC.

STM32 compilation also needs `CMSIS_CORE_INCLUDE` containing `core_cm7.h` and `CMSIS_DEVICE_INCLUDE` containing `stm32f767xx.h`. `python build_all.py` creates logs, reference traces, ELF/HEX files and `verification.json` under ignored `build/`.

The listed host commands install dependencies and run protocol tests. For hardware communication, specify the actual port and board, as in `--port COM6 --board ESP32 --runs 100`. Build ESP32 from `esp32/` with `pio run`; its PlatformIO target is the classic ESP32 Dev Module with the Arduino framework. Official RISC-V, CMSIS, QEMU and ESP32 references are linked above.
