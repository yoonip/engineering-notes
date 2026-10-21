# 펌웨어·RTOS | Firmware & RTOS

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

Firmware는 장치의 부팅과 주변장치 제어, 통신, 동작 상태를 담당하는 소프트웨어입니다. Bare-metal 프로그램은 운영체제 없이 동작하고, RTOS는 태스크 스케줄링과 동기화 같은 실행 기반을 제공합니다.

## 리셋에서 main까지

시작 코드는 스택과 메모리 영역을 준비하고 초기화된 데이터 복사와 BSS 초기화 등을 수행합니다. 링커 스크립트는 코드·상수·데이터를 flash·RAM의 어느 영역에 둘지 정합니다. 부트로더는 다음 프로그램을 검증하거나 선택해 실행하는 역할을 할 수 있습니다.

## 주변장치와 시간

GPIO는 디지털 입출력, timer는 시간과 이벤트 계수, ADC는 아날로그 입력 변환, PWM은 주기와 듀티비로 출력 파형을 만듭니다. 인터럽트는 이벤트에 반응하고 DMA는 데이터 전송의 CPU 부담을 줄입니다. 드라이버는 레지스터 제어를 상위 코드에서 쓸 수 있는 인터페이스로 묶습니다.

## RTOS의 동시성

FreeRTOS·Zephyr·ThreadX·RT-Thread는 임베디드 실행 환경에서 쓰입니다. 태스크·큐·세마포어·뮤텍스는 실행과 데이터 전달을 구성합니다. 실시간 시스템에서는 평균 속도와 함께 마감시간 충족 여부와 최악 지연을 살펴봅니다. 우선순위 역전은 낮은 우선순위 태스크가 가진 자원을 높은 우선순위 태스크가 기다리며 발생할 수 있습니다.

STM32·ESP32·Nordic nRF·NXP·TI·Microchip·Renesas·RP2040/RP2350은 MCU를 접하는 여러 생태계입니다. 코어 종류가 같아도 주변장치와 메모리 맵은 제조사·제품별로 다릅니다.

## 관련 기술

STM32, ESP32/ESP-IDF, Nordic nRF, NXP, TI, Microchip AVR/PIC/SAM, Renesas, RP2040/RP2350, FreeRTOS, Zephyr, ThreadX, RT-Thread

## 참고 자료

- [Zephyr introduction](https://docs.zephyrproject.org/latest/introduction/index.html)

## 시작 코드와 메모리 배치

펌웨어는 CPU가 실행하는 소프트웨어이며, 주변장치와 보드의 동작을 제어합니다. 컴파일러와 어셈블러가 만든 목적 파일을 링커가 연결하면 ELF가 생성됩니다. ELF에는 실행 코드와 데이터의 배치 정보, 심볼과 디버그 정보가 포함될 수 있습니다.

일반적인 Cortex-M 시작 코드에서는 벡터 테이블의 초기 스택 포인터와 Reset Handler 주소를 이용합니다. Reset Handler는 `.data`의 초기값을 RAM으로 복사하고 `.bss`를 0으로 채운 뒤 `main()`을 호출합니다. 링커 스크립트는 Flash와 RAM의 주소·크기, 각 섹션의 배치를 지정합니다.

| 영역 | 내용 |
| --- | --- |
| `.text` | 실행 코드 |
| `.rodata` | 읽기 전용 상수 |
| `.data` | 초기값이 있는 전역·정적 변수 |
| `.bss` | 0으로 초기화하는 전역·정적 변수 |

## 인터럽트·DMA·FreeRTOS

인터럽트는 이벤트에 따라 CPU의 실행 흐름을 처리 함수로 넘깁니다. DMA는 설정한 규칙에 따라 주변장치와 메모리 사이의 데이터를 전송합니다. CPU와 인터럽트·DMA가 데이터를 공유하면 버퍼 소유권, 갱신 시점과 캐시 상태도 함께 다룹니다.

RTOS는 작업을 task로 나누고 우선순위에 따라 실행을 관리합니다. queue는 작업 사이의 데이터를 전달하고, mutex는 공유 자원에 대한 동시 접근을 조정합니다. ESP32 예제에서는 UART 수신 루프가 명령을 파싱해 queue에 넣고, worker task가 메모리 검사와 연산 signature를 계산해 결과를 반환합니다. 같은 sequence의 재요청에는 저장한 결과를 반환하며, 출력은 mutex로 보호합니다. [Espressif FreeRTOS 문서](https://docs.espressif.com/projects/esp-idf/en/v5.1/esp32/api-guides/freertos-smp.html)

`volatile`은 외부에서 값이 바뀔 수 있는 대상에 대한 접근이 최적화로 제거되거나 이전 값으로 대체되는 것을 제한합니다. 원자성, 실행 흐름 사이의 동기화와 DMA·캐시 일관성은 별도로 다룹니다.


## 개념·유도·모델·검증

[기초부터 읽기](../../공학기초_foundations/README.md)

- [CPU와 장치가 같은 데이터를 다룰 때: MMIO, 인터럽트, DMA](해설_notes/CPU와장치가같은데이터를다룰때_mmio-interrupt-dma.md)

## 시간 카운터가 한 바퀴 돌아갈 때

tick은 시간을 세는 정수 카운터입니다. 크기가 정해진 카운터는 최댓값 다음에 0으로 돌아갑니다. 설명을 위해 8비트 카운터와 tick당 1 ms를 가정합니다. 마지막 진행 시각이 250이고 현재가 3이면, 실제로 9 ms가 지났어도 일반 정수 뺄셈은 -247입니다. 아래 Python은 하위 8비트만 남겨 카운터의 순환을 계산합니다.

```python
last = 250  # =는 마지막으로 작업이 진행된 tick을 저장합니다.
now = 3  # 순환 뒤 현재 tick이며, 여기서는 9 tick 뒤라고 가정합니다.
mask = (1 << 8) - 1  # <<는 비트 이동이며 8비트 마스크 255를 만듭니다.
elapsed = (now - last) & mask  # &는 비트 AND이며 하위 8비트로 차이를 계산합니다.
timeout = 8  # 이 예제는 경과 시간이 8 이상이면 만료로 정합니다.
print(now - last, elapsed, elapsed >= timeout)  # -247 9 True를 출력합니다.
print([(tick, (tick - last) & mask) for tick in range(4)])  # 목록 내포로 (0,6)~(3,9)를 계산합니다.
```

이는 두 관측 사이 실제 경과가 256 tick 미만이라는 전제의 예입니다. 256 tick이 지나면 같은 카운터 값이 되어 이 차이만으로는 0과 256을 구분할 수 없습니다. timeout이 8이라는 사실만으로 장기간 검사를 못 하는 상황까지 해결되지는 않습니다. 검사 주기와 최악 실행 지연을 제한하거나 순환 횟수를 함께 관리해야 합니다. Python의 `int` 자체에는 8비트 순환이 없으므로 마스크를 명시했습니다.

FreeRTOS Kernel [V11.2.0의 timeout 처리](https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/V11.2.0/tasks.c#L5059-L5146)는 tick과 overflow 횟수를 함께 보존하고, 임계 구역에서 읽은 tick으로 남은 대기 시간을 계산합니다. 위 식을 FreeRTOS API의 전체 구현으로 취급하지 않습니다. 임계 구역은 공유 상태를 읽고 바꾸는 동안 간섭을 제한하는 구간입니다. 커널의 대기·취소·무기한 대기 규칙은 사용하는 API와 설정을 따릅니다.

## 실행 중이라는 표시와 작업 완료의 차이

워치독은 일정 조건 안에 갱신되지 않으면 리셋 등을 발생시키는 감시 장치입니다. 감시 task가 실행된다는 사실은 센서 수집·제어·통신 task가 모두 진행한다는 뜻이 아닙니다. 예를 들어 제어 결과의 순번이 41에서 멈췄는데 감시 task가 매번 갱신하면 제어 중단을 숨길 수 있습니다. 반대로 유효한 대기 상태를 진행 실패로 잘못 판정하면 정상 동작 중 리셋을 일으킵니다.

| 구분할 상태 | 확인할 내용 |
| --- | --- |
| task가 스케줄됐습니다. | 이번 작업의 완료 순번이 실제로 바뀌었는지 확인합니다. |
| 예전에 완료한 적이 있습니다. | 이전 감시 구간의 완료 표시가 이번 구간에 재사용되지 않는지 확인합니다. |
| 새 결과가 있습니다. | 같은 tick 기준의 나이와 예상 주기·허용 지연을 함께 확인합니다. |
| 리셋 뒤 tick이 다시 0입니다. | 이전 부팅의 시각을 현재 부팅의 시각과 직접 빼지 않습니다. |

[워치독과 리셋 기록 사례](../../설계와검증사례_engineering-cases/작업진행을확인하는워치독과리셋기록_watchdog-health-reset.md)는 작업 진행을 확인하는 정책과 원인 플래그 보존을 실행 코드로 비교합니다. 감시 기준은 task마다 정한 실제 진행 조건이며, 모든 제품에 같은 timeout을 적용하는 규칙이 아닙니다. 위 카운터 예제는 Python 정수 계산이고 MCU 타이머나 RTOS를 실행한 결과와 구분합니다.

## English

Firmware controls device startup, peripherals, communication, and operating state. Bare-metal code runs without an operating system. An RTOS provides execution services such as task scheduling and synchronization.

### After reset

Startup code prepares the stack and memory, copies initialized data, and clears BSS. A linker script assigns code, constants, and data to Flash and RAM regions. A bootloader may validate or select the next program before transferring control to it.

### Peripherals and timing

GPIO handles digital I/O, timers measure time and count events, ADCs convert analog inputs, and PWM produces waveforms with a chosen period and duty cycle. Interrupts respond to events, while DMA reduces CPU involvement in data transfers. Drivers expose register-level operations through interfaces used by higher-level code.

### RTOS concurrency

FreeRTOS, Zephyr, ThreadX, and RT-Thread provide embedded execution environments. Tasks, queues, semaphores, and mutexes organize execution and data exchange. Real-time behavior concerns deadlines and worst-case latency more than average speed. Priority inversion can occur when a higher-priority task waits for a resource held by a lower-priority task.

STM32, ESP32, Nordic nRF, NXP, TI, Microchip, Renesas, and RP2040/RP2350 represent several MCU ecosystems. Even devices using the same core can have different peripheral blocks and memory maps.

### Startup code and memory layout

A compiler and assembler produce object files, and the linker combines them into an ELF file. An ELF may contain executable code, data placement, symbols, and debug information.

A typical Cortex-M startup sequence reads the initial stack pointer and Reset Handler address from the vector table. The handler copies `.data` initial values into RAM, clears `.bss`, and calls `main()`. The linker script defines Flash and RAM addresses, sizes, and section placement. `.text` holds executable code, `.rodata` read-only constants, `.data` initialized global and static variables, and `.bss` zero-initialized global and static variables.

### Interrupts, DMA, and FreeRTOS

An interrupt diverts CPU execution to a handler. DMA moves data between peripherals and memory according to its configuration. Shared data between CPU code, interrupts, and DMA requires attention to buffer ownership, update timing, and cache state.

In the ESP32 example, a UART receive loop parses commands and sends them to a queue. A worker task performs memory checks and computes an arithmetic signature before returning the result. Repeated requests with the same sequence number use a cached response, and a mutex protects output. The [Espressif FreeRTOS documentation](https://docs.espressif.com/projects/esp-idf/en/v5.1/esp32/api-guides/freertos-smp.html) describes its execution environment.

`volatile` constrains optimizations that could remove accesses or reuse an earlier value for an object that can change externally. Atomicity, synchronization, and DMA/cache coherence require separate mechanisms.


### Concepts, derivations, models, and verification

[Foundations reading guide](../../공학기초_foundations/README.md#english)

- [MMIO, interrupts, DMA and cache ownership](해설_notes/CPU와장치가같은데이터를다룰때_mmio-interrupt-dma.md#english)


### Wrapping ticks and task progress

An eight-bit example gives `(3 - 250) & 255 = 9`. This elapsed-time calculation assumes fewer than 256 ticks between observations; it cannot distinguish zero elapsed time from a full turn. FreeRTOS V11.2.0 retains overflow state in its timeout implementation. Watchdog policy also distinguishes scheduling from fresh task progress and separates boot epochs. The linked case supplies executable host models; the chapter's arithmetic does not run an RTOS.

## 심화 해설 | Advanced article

- [RTOS의 우선순위 역전: 누가 mutex를 놓을 수 있을까](해설_notes/우선순위역전_priority-inheritance.md) · [English](해설_notes/우선순위역전_priority-inheritance.md#english)
