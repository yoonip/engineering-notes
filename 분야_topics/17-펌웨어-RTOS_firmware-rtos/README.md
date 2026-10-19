# 펌웨어·RTOS | Firmware & RTOS

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

Firmware는 장치의 부팅과 주변장치 제어, 통신, 동작 상태를 담당하는 소프트웨어다. Bare-metal 프로그램은 운영체제 없이 동작하고, RTOS는 태스크 스케줄링과 동기화 같은 실행 기반을 제공한다.

## 리셋에서 main까지

시작 코드는 스택과 메모리 영역을 준비하고 초기화된 데이터 복사와 BSS 초기화 등을 수행한다. 링커 스크립트는 코드·상수·데이터를 flash·RAM의 어느 영역에 둘지 정한다. 부트로더는 다음 프로그램을 검증하거나 선택해 실행하는 역할을 할 수 있다.

## 주변장치와 시간

GPIO는 디지털 입출력, timer는 시간과 이벤트 계수, ADC는 아날로그 입력 변환, PWM은 주기와 듀티비로 출력 파형을 만든다. 인터럽트는 이벤트에 반응하고 DMA는 데이터 전송의 CPU 부담을 줄인다. 드라이버는 레지스터 제어를 상위 코드에서 쓸 수 있는 인터페이스로 묶는다.

## RTOS의 동시성

FreeRTOS·Zephyr·ThreadX·RT-Thread는 임베디드 실행 환경에서 쓰인다. 태스크·큐·세마포어·뮤텍스는 실행과 데이터 전달을 구성한다. 실시간 시스템에서는 평균 속도와 함께 마감시간 충족 여부와 최악 지연을 살펴본다. 우선순위 역전은 낮은 우선순위 태스크가 가진 자원을 높은 우선순위 태스크가 기다리며 발생할 수 있다.

STM32·ESP32·Nordic nRF·NXP·TI·Microchip·Renesas·RP2040/RP2350은 MCU를 접하는 여러 생태계다. 코어 종류가 같아도 주변장치와 메모리 맵은 제조사·제품별로 다르다.

## 관련 기술

STM32, ESP32/ESP-IDF, Nordic nRF, NXP, TI, Microchip AVR/PIC/SAM, Renesas, RP2040/RP2350, FreeRTOS, Zephyr, ThreadX, RT-Thread

## 참고 자료

- [Zephyr introduction](https://docs.zephyrproject.org/latest/introduction/index.html)

## 시작 코드와 메모리 배치

펌웨어는 CPU가 실행하는 소프트웨어이며, 주변장치와 보드의 동작을 제어한다. 컴파일러와 어셈블러가 만든 목적 파일을 링커가 연결하면 ELF가 생성된다. ELF에는 실행 코드와 데이터의 배치 정보, 심볼과 디버그 정보가 포함될 수 있다.

일반적인 Cortex-M 시작 코드에서는 벡터 테이블의 초기 스택 포인터와 Reset Handler 주소를 이용한다. Reset Handler는 `.data`의 초기값을 RAM으로 복사하고 `.bss`를 0으로 채운 뒤 `main()`을 호출한다. 링커 스크립트는 Flash와 RAM의 주소·크기, 각 섹션의 배치를 지정한다.

| 영역 | 내용 |
| --- | --- |
| `.text` | 실행 코드 |
| `.rodata` | 읽기 전용 상수 |
| `.data` | 초기값이 있는 전역·정적 변수 |
| `.bss` | 0으로 초기화하는 전역·정적 변수 |

## 인터럽트·DMA·FreeRTOS

인터럽트는 이벤트에 따라 CPU의 실행 흐름을 처리 함수로 넘긴다. DMA는 설정한 규칙에 따라 주변장치와 메모리 사이의 데이터를 전송한다. CPU와 인터럽트·DMA가 데이터를 공유하면 버퍼 소유권, 갱신 시점과 캐시 상태도 함께 다룬다.

RTOS는 작업을 task로 나누고 우선순위에 따라 실행을 관리한다. queue는 작업 사이의 데이터를 전달하고, mutex는 공유 자원에 대한 동시 접근을 조정한다. ESP32 예제에서는 UART 수신 루프가 명령을 파싱해 queue에 넣고, worker task가 메모리 검사와 연산 signature를 계산해 결과를 반환한다. 같은 sequence의 재요청에는 저장한 결과를 반환하며, 출력은 mutex로 보호한다. [Espressif FreeRTOS 문서](https://docs.espressif.com/projects/esp-idf/en/v5.1/esp32/api-guides/freertos-smp.html)

`volatile`은 외부에서 값이 바뀔 수 있는 대상에 대한 접근이 최적화로 제거되거나 이전 값으로 대체되는 것을 제한한다. 원자성, 실행 흐름 사이의 동기화와 DMA·캐시 일관성은 별도로 다룬다.


## 개념·유도·모델·검증

[기초부터 읽기](../../문서_docs/공학기초_FOUNDATIONS.md)

- [CPU와 장치가 같은 데이터를 다룰 때: MMIO, 인터럽트, DMA](해설_notes/CPU와장치가같은데이터를다룰때_mmio-interrupt-dma.md)

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

[Foundations reading guide](../../문서_docs/공학기초_FOUNDATIONS.md#english)

- [MMIO, interrupts, DMA and cache ownership](해설_notes/CPU와장치가같은데이터를다룰때_mmio-interrupt-dma.md#english)
