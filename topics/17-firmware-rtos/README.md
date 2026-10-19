# Firmware & RTOS

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

Firmware는 장치의 부팅과 주변장치 제어, 통신, 동작 상태를 담당하는 소프트웨어다. Bare-metal 프로그램은 운영체제 없이 동작하고, RTOS는 태스크 스케줄링과 동기화 같은 실행 기반을 제공한다.

## 리셋 이후의 실행

시작 코드는 스택과 메모리 영역을 준비하고 초기화된 데이터 복사와 BSS 초기화 등을 수행한다. 링커 스크립트는 코드·상수·데이터를 flash·RAM의 어느 영역에 둘지 정한다. 부트로더는 다음 프로그램을 검증하거나 선택해 실행하는 역할을 할 수 있다.

## 주변장치와 시간

GPIO는 디지털 입출력, timer는 시간과 이벤트 계수, ADC는 아날로그 입력 변환, PWM은 주기와 듀티비로 출력 파형을 만든다. 인터럽트는 이벤트에 반응하고 DMA는 데이터 전송의 CPU 부담을 줄인다. 드라이버는 레지스터 제어를 상위 코드에서 쓸 수 있는 인터페이스로 묶는다.

## RTOS의 동시성

FreeRTOS·Zephyr·ThreadX·RT-Thread는 임베디드 실행 환경에서 쓰인다. 태스크·큐·세마포어·뮤텍스는 실행과 데이터 전달을 구성한다. 실시간성은 평균 속도보다 마감시간 충족과 최악 지연에 가깝다. 우선순위 역전은 낮은 우선순위 태스크가 가진 자원을 높은 우선순위 태스크가 기다리며 발생할 수 있다.

STM32·ESP32·Nordic nRF·NXP·TI·Microchip·Renesas·RP2040/RP2350은 MCU를 접하는 여러 생태계다. 코어 종류가 같아도 주변장치와 메모리 맵은 제조사·제품별로 다르다.

## 관련 기술

STM32, ESP32/ESP-IDF, Nordic nRF, NXP, TI, Microchip AVR/PIC/SAM, Renesas, RP2040/RP2350, FreeRTOS, Zephyr, ThreadX, RT-Thread

## 참고 자료

- [Zephyr introduction](https://docs.zephyrproject.org/latest/introduction/index.html)
