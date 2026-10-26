# 로봇 제어·Arduino·Raspberry Pi | Robotics, Arduino & Raspberry Pi

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

로봇은 센서로 상태를 관측하고 제어기의 판단에 따라 액추에이터를 움직입니다. 기구·전원·회로·펌웨어·추정·계획 알고리즘이 함께 동작합니다.

## 보드의 역할

Arduino는 보드와 개발 환경의 생태계이며 제품마다 MCU와 실행 환경이 다릅니다. Raspberry Pi의 대표적인 SBC 제품은 Linux 애플리케이션과 네트워크·카메라 처리에 쓰이고, Pico 계열은 MCU 보드입니다. STM32 Nucleo·ESP32·BeagleBone·Jetson도 각각 MCU 제어·연결·Linux·AI 연산에 활용됩니다.

## 운동과 관측

기구학은 관절 값과 위치·자세의 관계, 동역학은 힘·토크와 운동의 관계를 다룹니다. 엔코더는 회전·위치 정보를, IMU는 가속도와 각속도 등을 제공합니다. PWM 명령과 실제 토크의 관계에는 모터 드라이버·전원·기구 부하가 개입합니다. SLAM은 지도 작성과 자기 위치 추정을 함께 다룹니다.

## 소프트웨어와 시뮬레이션

ROS 2는 노드와 메시지를 통해 로봇 기능을 연결합니다. Topic은 연속 데이터 전달, service는 요청·응답, action은 진행 상태가 있는 작업에 사용됩니다. MoveIt은 조작·경로 계획, Nav2는 이동 로봇 내비게이션 생태계입니다. Gazebo·MuJoCo·Isaac Sim은 모델과 물리 시뮬레이션을 제공하며, 모델 오차와 센서·구동기의 차이가 실제 로봇으로 옮길 때 영향을 줍니다.

## 관련 기술

Arduino, Raspberry Pi, STM32 Nucleo, ESP32, BeagleBone, Jetson, ROS 2, MoveIt, Nav2, Gazebo, MuJoCo, Isaac Sim, SLAM

## 참고 자료

- [ROS 2 documentation](https://docs.ros.org/)
- [Raspberry Pi documentation](https://www.raspberrypi.com/documentation/)

## STM32·ESP32·Arduino·Raspberry Pi

MCU와 보드 개발은 회로의 전원·클록·리셋, 핀 연결, 펌웨어와 호스트 프로그램을 함께 다룹니다. GPIO는 디지털 입출력, ADC는 아날로그 신호의 수치 변환, 타이머는 주기·펄스 생성과 시간 측정에 쓰입니다. UART·SPI·I²C는 외부 장치와 데이터를 주고받는 인터페이스입니다.

| 대상 | 하드웨어와 개발 환경 |
| --- | --- |
| STM32 | Arm Cortex-M 기반 MCU 제품군. CubeIDE, GCC와 CMSIS를 이용한 펌웨어·레지스터 제어 |
| ESP32 | 제품군에 따라 Xtensa 또는 RISC-V 코어를 포함하는 SoC. ESP-IDF 또는 Arduino 프레임워크를 이용한 개발 |
| Arduino | 개발보드와 소프트웨어를 포함하는 플랫폼. 스케치는 일반적으로 C++로 컴파일되며 `setup()`·`loop()`와 장치 API를 사용 |
| Raspberry Pi SBC | Linux 환경에서 프로세스·드라이버와 GPIO·SPI 등 장치 인터페이스를 연결하는 보드 개발. [Pico 계열](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html)은 별도의 MCU 보드 제품군 |

ESP32는 실행 대상 칩이고, Arduino 코어는 선택할 수 있는 소프트웨어 프레임워크입니다. VS Code에서는 ESP-IDF와 Arduino 등 여러 개발 환경을 사용할 수 있습니다. 편집기와 펌웨어 프레임워크는 역할이 다릅니다. [ESP32 Arduino 코어](https://docs.espressif.com/projects/arduino-esp32/en/latest/)

## STM32 GPIO 레지스터 제어

STM32F767ZI 예제는 `RCC->AHB1ENR`로 GPIOB의 클록을 활성화하고, `GPIOB->MODER`로 PB0을 출력으로 설정합니다. `GPIOB->ODR`의 bit 0을 반전하면 해당 핀의 출력 상태가 바뀝니다. 제조사 헤더는 레지스터의 주소, 구조체와 비트 마스크를 C 이름으로 제공합니다. `->`, `|=`, `&= ~`는 일반 C 문법입니다. [ST CMSIS Device F7](https://github.com/STMicroelectronics/cmsis-device-f7)

CPU 범용 레지스터는 계산값과 주소를 보관하고, 주변장치 레지스터는 GPIO 같은 회로의 설정과 상태를 나타냅니다. 보드의 LED 동작은 핀의 출력값뿐 아니라 실제 회로의 연결과 활성 극성에 따라 정해집니다.

## 좌표·경로·측정·로봇 구조의 실행 예제

[응용 시스템 실습](../../하드웨어코딩_hardware-coding/응용시스템_applied-systems/README.md)에서 센서→차체→지도 좌표 변환, 원형 몸체의 실내 격자 경로, 엔코더·비콘의 한 축 위치 추정, 2링크 URDF의 정기구학을 코드와 실행 흐름으로 확인합니다. [ROS 2·Gazebo 등 공개 프로젝트 안내](../../하드웨어코딩_hardware-coding/응용시스템_applied-systems/공개프로젝트와언어_sources-and-languages.md)는 독립 수치 예제 다음에 읽을 통신·모델·통합 자료를 연결합니다. 해당 예제의 호스트 검사와 실제 ROS 통합·보드 구동을 구분합니다.

## 기초 해설

- [차동구동 로봇: 바퀴 회전에서 위치 추정까지](해설_notes/차동구동로봇_differential-drive-kinematics-odometry.md)

## English

A robot observes its state through sensors, makes control decisions, and drives actuators. Mechanical structures, power supplies, circuits, firmware, estimation, and planning algorithms operate together.

### Board roles

Arduino is an ecosystem of boards and development tools; MCU and execution environment vary by product. Raspberry Pi's main SBC products support Linux applications, networking, and cameras, while the Pico family consists of MCU boards. STM32 Nucleo, ESP32, BeagleBone, and Jetson support different combinations of MCU control, connectivity, Linux, and AI computation.

### Motion and observation

Kinematics relates joint values to position and orientation. Dynamics relates forces and torques to motion. Encoders report position or rotation, and IMUs measure quantities such as acceleration and angular velocity. The relationship between a PWM command and actual torque also depends on the driver, supply, and mechanical load. SLAM combines mapping with localization.

### Software and simulation

ROS 2 connects robot functions through nodes and messages. Topics carry ongoing data, services handle requests and responses, and actions support longer-running work with progress and results. MoveIt supports manipulation and motion planning, and Nav2 supports mobile-robot navigation. Gazebo, MuJoCo, and Isaac Sim provide models and physics simulation. Model error and differences in sensing and actuation affect transfer to a physical robot.

### STM32, ESP32, Arduino, and Raspberry Pi

Board development connects power, clocks, reset, pin wiring, firmware, and host software. GPIO provides digital I/O, ADC converts analog signals to numbers, and timers generate periods and pulses or measure time. UART, SPI, and I²C exchange data with peripherals.

| Target | Hardware and development environment |
| --- | --- |
| STM32 | Arm Cortex-M MCU family; firmware and register control with CubeIDE, GCC, and CMSIS |
| ESP32 | SoC family using Xtensa or RISC-V cores, depending on the device; development with ESP-IDF or Arduino |
| Arduino | Boards and software platform; sketches generally compile as C++ and use `setup()`, `loop()`, and device APIs |
| Raspberry Pi SBC | Linux processes and drivers connected to interfaces such as GPIO and SPI; the [Pico family](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html) is a separate MCU-board family |

ESP32 is the target chip family, while the Arduino core is one available software framework. VS Code is an editor and development tool; using it does not determine the framework. See the [ESP32 Arduino core](https://docs.espressif.com/projects/arduino-esp32/en/latest/).

### STM32 GPIO register control

The STM32F767ZI example enables the GPIOB clock through `RCC->AHB1ENR` and configures PB0 as an output through `GPIOB->MODER`. Toggling bit 0 of `GPIOB->ODR` changes the pin output. Vendor headers expose register addresses, structures, and bit masks as C names. `->`, `|=`, and `&= ~` are ordinary C syntax. See [ST CMSIS Device F7](https://github.com/STMicroelectronics/cmsis-device-f7).

CPU general-purpose registers hold values and addresses. Peripheral registers hold configuration and state for hardware blocks such as GPIO. Whether an LED lights depends on the pin value, board wiring, and active polarity.

### Foundation article

- [차동구동 로봇: 바퀴 회전에서 위치 추정까지](해설_notes/차동구동로봇_differential-drive-kinematics-odometry.md#english)


## 심화 해설 | Advanced article

- [바퀴 속도 PI 제어: 포화된 모터에 적분을 계속 더하면](해설_notes/속도PI와포화_speed-pi-anti-windup.md) · [English](해설_notes/속도PI와포화_speed-pi-anti-windup.md#english)
