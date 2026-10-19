# Robotics · Arduino · Raspberry Pi

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

로봇은 센서로 상태를 관측하고 제어기로 결정을 내려 액추에이터를 움직이는 시스템이다. 기구·전원·회로·펌웨어·추정·계획 알고리즘이 함께 동작한다.

## 보드의 역할

Arduino는 보드와 개발 환경의 생태계이며 제품마다 MCU와 실행 환경이 다르다. Raspberry Pi의 대표적인 SBC 제품은 Linux 애플리케이션과 네트워크·카메라 처리에 쓰이고, Pico 계열은 MCU 보드다. STM32 Nucleo·ESP32·BeagleBone·Jetson도 각각 MCU 제어·연결·Linux·AI 연산에 활용된다.

## 운동과 관측

기구학은 관절 값과 위치·자세의 관계, 동역학은 힘·토크와 운동의 관계를 다룬다. 엔코더는 회전·위치 정보를, IMU는 가속도와 각속도 등을 제공한다. PWM 명령과 실제 토크의 관계에는 모터 드라이버·전원·기구 부하가 개입한다. SLAM은 지도 작성과 자기 위치 추정을 함께 다룬다.

## 소프트웨어와 시뮬레이션

ROS 2는 노드와 메시지를 통해 로봇 기능을 연결한다. Topic은 연속 데이터 전달, service는 요청·응답, action은 진행 상태가 있는 작업에 사용된다. MoveIt은 조작·경로 계획, Nav2는 이동 로봇 내비게이션 생태계다. Gazebo·MuJoCo·Isaac Sim은 모델과 물리 시뮬레이션을 제공하며, 모델 오차와 센서·구동기의 차이가 실제 로봇으로 옮길 때 영향을 준다.

## 관련 기술

Arduino, Raspberry Pi, STM32 Nucleo, ESP32, BeagleBone, Jetson, ROS 2, MoveIt, Nav2, Gazebo, MuJoCo, Isaac Sim, SLAM

## 참고 자료

- [ROS 2 documentation](https://docs.ros.org/)
- [Raspberry Pi documentation](https://www.raspberrypi.com/documentation/)
