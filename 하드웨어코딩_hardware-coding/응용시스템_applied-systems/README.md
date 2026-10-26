# 자율주행·로봇·우주 시스템의 코드와 검증 | Code and checks for autonomous and space systems

센서의 숫자를 어느 좌표와 시각에서 해석할지, 로봇이 지나갈 공간을 어떻게 판단할지, 계산과 메시지의 오류를 무엇과 비교할지 다룹니다. 실내 이동 로봇·고정식 로봇 팔·교육용 위성 원궤도·벤치 계측 메시지를 직접 작성한 코드로 추적합니다.

[하드웨어 코딩](../README.md) · [분야별 구조와 검증](분야별구조와검증_domain-architecture.md) · [공개 프로젝트와 언어](공개프로젝트와언어_sources-and-languages.md) · [실행 기록](확인기록_validation.md)

## 실행 예제

| 예제 | 언어·형식 | 입력부터 결과까지 | 독립적으로 비교하는 대상 |
| --- | --- | --- | --- |
| [이동 로봇의 좌표 변환](01-이동로봇좌표_robot-frames/README.md) | C++17입니다. | 센서의 점 → 차체 좌표 → 지도 좌표 → 역변환입니다. | 별도의 동차행렬 계산·거리 보존·합성 순서입니다. |
| [실내 격자와 로봇 몸체](02-실내격자경로_grid-planning/README.md) | Python입니다. | 점유 지도·반지름·여유 → 충돌 셀 → A* 경로 또는 경로 없음입니다. | BFS 최단거리와 별도의 선분·사각형 기하 검사입니다. |
| [실내 AGV의 측정 융합](03-실내로봇측정융합_robot-estimation/README.md) | Python입니다. | 엔코더 이동량 → 위치 예측 → 비콘의 시각·혁신 검사 → 위치와 분산입니다. | 정밀도 가중식·유리수 손계산·거절 후 상태입니다. |
| [위성의 교육용 원궤도](04-위성교육궤도_satellite-orbit/README.md) | Python입니다. | 정한 원궤도 초기 상태 → RK4 적분 → 해석적 원운동과 오차입니다. | 해석해·에너지·각운동량·시간 간격에 따른 수렴입니다. |
| [2링크 로봇 팔의 구조](05-로봇구조와관절_urdf/README.md) | URDF/XML·Python입니다. | 링크·관절 모델 → 실제 URDF 파서 → 관절각 → 말단 좌표입니다. | 두 링크의 해석식·회전행렬 조건·잘못된 모델의 거절입니다. |
| [벤치 계측 메시지의 유효성](06-벤치텔레메트리_protobuf/README.md) | Protocol Buffers·Python입니다. | 스키마 → 실제 코드 생성 → 직렬화·복원 → 형식·순서·신선도입니다. | 필드 누락·중복·범위·지연과 마지막 정상 표본의 유지입니다. |

각 README에는 짧은 줄별 주석을 단 전체 소스, 입력 계약과 단위, 계산 순서, 실제 실행 명령·출력과 풀이 요약을 담았습니다. 각 `example.json`에는 실행한 소스의 SHA-256과 그때의 결과를 연결합니다. 기존 프로그래머스 풀이와 별도의 학습 예제입니다.

## 학습 순서와 언어 선택

먼저 좌표와 단위를 맞춘 뒤 로봇 몸체가 통과할 공간을 확인합니다. 다음으로 측정 시각과 불확실성을 다루고, 로봇의 구조 파일과 프로그램이 같은 기구를 나타내는지 비교합니다. 우주 계산에서는 단순한 해석해가 있는 조건에서 수치 오차를 확인한 뒤 외부 소프트웨어의 구조를 읽습니다. 메시지 실습에서는 값이 도착했다는 사실과 현재 유효하다는 판단을 나누어 봅니다.

| 배우는 대상 | 언어·도구가 맡는 역할 | 연결할 자료 |
| --- | --- | --- |
| 좌표·추정·경로 계산 | C++은 자료형과 계산 함수를, Python은 작은 수치 실험과 기대값 비교를 표현합니다. | 위 실행 예제와 [차동구동 운동학](../../전자컴퓨터공학_ece/22-로봇제어_robotics-boards/해설_notes/차동구동로봇_differential-drive-kinematics-odometry.md)입니다. |
| 로봇 구조·물리 모형 | URDF와 SDF는 링크·관절·형상을 기록합니다. Modelica는 방정식으로 물리 계통의 관계를 표현합니다. | [URDF 실습](05-로봇구조와관절_urdf/README.md)과 [Gazebo·Modelica 안내](공개프로젝트와언어_sources-and-languages.md)입니다. |
| 모듈 통신·명령·상태 | ROS 2의 메시지, Protocol Buffers의 스키마, F Prime의 FPP 모델은 각각 다른 인터페이스를 표현합니다. | [벤치 메시지 실습](06-벤치텔레메트리_protobuf/README.md)과 [ROS 2·cFS·F Prime 안내](공개프로젝트와언어_sources-and-languages.md)입니다. |
| 계약과 증명 | Ada/SPARK는 자료형·사전조건·사후조건과 증명 도구를 연결합니다. | [Ada/SPARK 안내](공개프로젝트와언어_sources-and-languages.md)입니다. |
| CPU·회로·검증 | RISC-V 어셈블리·Rust·SystemVerilog·cocotb·SPICE·Tcl은 각각 실행 명령·펌웨어·회로·검증·설계 도구를 다룹니다. | 기존 [언어와 도구 확장 실습](../언어확장_language-expansion/README.md)입니다. |

언어 수보다 서로 다른 오류를 드러내는 표현을 고르는 것이 중요합니다. 좌표를 잘못 합성한 문제는 XML의 문법 검사만으로 찾을 수 없고, 오래된 측정값을 받은 문제는 최단경로 알고리즘만으로 판단할 수 없습니다. 입력 계약과 독립 기대값을 함께 적는 이유입니다.

## 분야에 연결하는 범위

자율주행에서는 센서·자기 위치·계획·제어·진단의 관계를, 로봇에서는 좌표·기구·구동 장치의 관계를 읽습니다. 위성·발사체에서는 탑재 컴퓨팅·전원·계측·통신·지상 시험의 역할을 나눕니다. 방산 전자는 공개된 일반 아키텍처와 데이터 검증·고장 감지·신뢰성 시험을 중심으로 정리합니다. 구체적인 분야별 연결은 [구조와 검증 문서](분야별구조와검증_domain-architecture.md)에 있습니다.

여기의 경로 탐색은 정적인 실내 격자, 측정 융합은 한 축의 위치, 궤도 계산은 추력 없는 이상적 원운동으로 한정합니다. 실제 차량·로봇·우주 하드웨어를 작동한 기록은 아닙니다. ROS 2·Gazebo·Autoware·CARLA·cFS·F Prime·SPARK·OpenModelica는 공식 자료를 읽는 경로이며 이 작업에서 그 런타임을 설치·실행한 것으로 표시하지 않습니다.

## 게시 소스와 실행 기록의 대조

저장소 루트에서 다음 명령으로 현재 소스 바이트와 기록의 해시, README의 전체 코드, 로컬 파일 링크를 확인합니다. 이 명령은 예제를 다시 실행하지 않으므로 새로운 수치 실험 결과를 만들지 않습니다. 예제를 실행하려면 각 README의 명령과 의존성 판본을 사용합니다.

```bash
python -B 하드웨어코딩_hardware-coding/응용시스템_applied-systems/check_sources.py --report /path/to/current-source-check.json
```

실행 결과는 [확인 기록](확인기록_validation.md), 읽을 공식 원문은 [출처 안내](공개프로젝트와언어_sources-and-languages.md), 기계 판독용 정보는 [catalog.json](catalog.json)과 [sources.json](sources.json)에 연결합니다.

## English

Original annotated examples cover SE(2) frame transforms, finite-body indoor grid planning, scalar indoor robot estimation, an ideal satellite circular orbit, a two-link URDF model, and Protocol Buffers bench telemetry. The records distinguish actual local execution from reading external ROS, autonomous-driving and flight-software projects. The domain guide connects interfaces, units, time, fault detection and verification without claiming vehicle, flight or hardware validation.
