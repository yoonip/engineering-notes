# 응용 시스템의 공개 프로젝트와 언어 | Projects and languages for applied systems

로봇·자율주행·우주 탑재 소프트웨어를 공부할 때에는 언어, 메시지 프레임워크, 물리 시뮬레이터와 검증 도구의 역할을 나누어 봅니다. 이 문서는 공식 입문 예제와 이용 조건을 연결합니다. 확인일은 2026년 10월 26일이며, 상세 확인 위치와 미확인 항목은 [sources.json](sources.json)에 있습니다.

[분야별 구조와 검증](분야별구조와검증_domain-architecture.md) · [하드웨어 언어의 역할](../언어와검증도구_languages-and-verification.md)

## 독립 예제와 외부 런타임의 구분

이 폴더의 직접 예제는 실내 좌표 계산, 실내 격자 A*, AGV의 1차원 측정 융합, 교육용 지구 위성 원궤도 계산, 민간 2링크 URDF 모형과 Protobuf 벤치 센서 메시지를 다룹니다. 확인한 계산·파서와 조건은 개별 예제의 실행 기록에 적습니다. 교육용 원궤도 계산을 비행 소프트웨어나 발사체 모델로, XML 파싱을 Gazebo 물리 시뮬레이션으로 표현하지 않습니다.

아래 ROS 2·Gazebo·Autoware·CARLA·cFS·F Prime·GNATprove·OpenModelica의 공식 자료는 읽어 확인했으며, 이 응용 시스템 예제의 실행 기록에는 해당 외부 런타임을 설치·구동하거나 실제 장치와 연결한 결과가 없습니다. 로컬 C++·Python·파서 검사가 통과했다는 사실만으로 외부 프레임워크의 통합 시험이 통과한 것은 아닙니다.

## 무엇을 더 배우는지

| 대상 | 주된 언어·입력 | 새로 익힐 대상 | 공식 입문 경로 | 현재 실행 범위 |
| --- | --- | --- | --- | --- |
| ROS 2 | C++·Python, 메시지 정의 | 노드·토픽·요청 응답·작업과 통신 계약 | [Python publisher/subscriber](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html) | 공식 자료 확인이며 ROS 노드 실행은 하지 않았습니다. |
| Gazebo | SDF·URDF, 플러그인과 메시지 | 로봇의 기구·접촉·센서와 물리 시간 | [두 바퀴 로봇 만들기](https://gazebosim.org/docs/jetty/building_robot/) → [움직이기](https://gazebosim.org/docs/jetty/moving_robot/) | 독립 URDF 파싱과 Gazebo 구동을 구분합니다. |
| Autoware | C++·ROS 2·설정 파일 | 자율주행 모듈 사이의 데이터와 계획·제어 통합 | [Open AD Kit planning simulation](https://autowarefoundation.github.io/openadkit/deployments/planning-simulation/) | Autoware·RViz·컨테이너는 실행하지 않았습니다. |
| CARLA | C++ 서버·Python 클라이언트 | 가상 도로·센서·환경·서버와 클라이언트 동기 | [UE5 quick start](https://carla-ue5.readthedocs.io/en/latest/start_quickstart/) | CARLA 서버·센서 시뮬레이션은 실행하지 않았습니다. |
| NASA cFS | C, 앱·플랫폼 설정 | 소프트웨어 버스·앱·운영체제·플랫폼의 경계 | [Demo Bundle의 Build and Run Quick Start](https://github.com/nasa/cFS#build-and-run-quick-start) | cFS 앱·지상 도구는 실행하지 않았습니다. |
| F Prime | C++·FPP·Python 도구 | 컴포넌트·포트·토폴로지와 명령·이벤트·텔레메트리 | [Hello World](https://fprime.jpl.nasa.gov/latest/tutorials-hello-world/docs/hello-world/) → [MathComponent](https://fprime.jpl.nasa.gov/latest/docs/tutorials/) | FPP 생성·F Prime·GDS는 실행하지 않았습니다. |
| Ada/SPARK | Ada와 계약·주석 | 값의 범위·의존성·사전후조건과 정적 증명 | [Getting Started with SPARK](https://docs.adacore.com/spark2014-docs/html/ug/en/getting_started.html) | Ada 컴파일·GNATprove 증명은 하지 않았습니다. |
| Modelica/OpenModelica | Modelica 방정식·모델 연결 | 전기·기계·열 등 여러 물리 영역의 연립방정식 | [OpenModelica 공식 사용자 문서](https://openmodelica.org/useresresources/userdocumentation/) | Modelica 컴파일·방정식 해석은 실행하지 않았습니다. |

## ROS 2와 Gazebo: 통신과 물리 모델의 역할

ROS 2는 로봇의 기능을 노드로 나누고 메시지를 전달하는 소프트웨어 생태계입니다. [공식 Python 입문 예제](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html)는 한 노드가 토픽에 문자열을 발행하고 다른 노드가 구독하는 작은 흐름입니다. 이 예제부터 메시지 이름·자료형·수신 시점·종료 처리를 확인한 뒤 로봇 기능을 연결하는 순서가 좋습니다. 단순한 Python 큐에서 데이터가 전달됐다고 해서 실제 미들웨어 통신이나 ROS의 전달 정책인 QoS를 시험한 것은 아닙니다.

ROS 배포판은 버전이 맞는 패키지 집합입니다. 공식 [배포판 목록 원문](https://github.com/ros2/ros2_documentation/blob/rolling/source/Releases.rst)에는 Lyrical Luth의 공개일을 2026년 5월 22일, 지원 종료 예정일을 2031년 5월로 표시하며, Jazzy Jalisco는 2029년 5월까지로 표시합니다. 개발 중인 Rolling과 배포판을 고정한 실습을 구분합니다. HTML 문서가 접근 차단 화면을 반환하면 동일 공식 저장소의 [Jazzy 입문 원문](https://github.com/ros2/ros2_documentation/blob/jazzy/source/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.rst)에서 설명과 코드를 확인할 수 있습니다.

Gazebo는 물리 세계와 로봇 모델을 실행하는 별도 프로젝트입니다. [공식 설치 조합](https://gazebosim.org/docs/jetty/ros_installation/)은 Lyrical–Jetty, Jazzy–Harmonic, Kilted–Ionic을 연결합니다. 가장 새 이름을 각각 골라 섞기보다, 선택한 ROS 배포판이 지원하는 Gazebo와 브리지 판본을 맞춥니다. 공식 두 바퀴 로봇 예제에서는 SDF의 링크·관절·기하·물성·플러그인을 배웁니다. URDF 문서가 파싱된다는 사실과 물성·충돌·센서가 실제 시뮬레이터에서 의도대로 작동한다는 사실은 다릅니다.

[ros2/examples의 Jazzy LICENSE](https://github.com/ros2/examples/blob/jazzy/LICENSE)와 [gz-sim10 LICENSE](https://github.com/gazebosim/gz-sim/blob/gz-sim10/LICENSE)는 Apache-2.0입니다. 이 조건을 모든 ROS 패키지·웹 문서·Gazebo Fuel 자산에 일괄 적용하지 않습니다. 실제로 가져오는 패키지와 모델의 고지를 확인합니다.

## Autoware와 CARLA: 가상 환경의 통합은 별도 실험입니다

Autoware는 자율주행 기능을 연결하는 소프트웨어이며 CARLA는 가상 도로·행위자·센서 환경을 제공하는 시뮬레이터입니다. 둘을 같은 종류의 언어나 한 개의 설치 도구로 취급하지 않습니다. [Open AD Kit planning simulation](https://autowarefoundation.github.io/openadkit/deployments/planning-simulation/)은 데모 지도와 계획·제어 스택, 브라우저에서 표시하는 RViz 작업을 연결합니다. [시작 안내](https://autowarefoundation.github.io/openadkit/getting-started/)의 호스트·컨테이너·지도 조건을 해당 배포물과 함께 확인합니다. 계획 모형만으로 센서·인지·충돌의 정확도를 확인했다고 표현하지 않습니다.

CARLA의 [UE5 설치 문서](https://carla-ue5.readthedocs.io/en/latest/start_quickstart/)는 Windows 11 또는 Ubuntu 22.04·24.04, 그래픽 장치·드라이버·디스크와 Python 조건을 설명합니다. 서버와 동봉 Python wheel의 판본·플랫폼·Python minor 버전을 맞춰야 합니다. 이 문서는 PyPI의 `carla` 패키지가 UE4 클라이언트이므로 UE5 서버와 섞지 말라고 안내합니다. 확인 시점의 `latest` 문서에는 1.0.0 패키지·컨테이너 링크를 확정하지 않은 TODO도 있으므로, 문서의 명령에 번호가 있다는 이유만으로 그 배포물이 정식 공개됐다고 간주하지 않습니다.

[Autoware workspace LICENSE](https://github.com/autowarefoundation/autoware/blob/main/LICENSE)는 Apache-2.0입니다. 구성 패키지와 지도는 개별 조건을 확인합니다. [CARLA 공식 저장소의 Licenses](https://github.com/carla-simulator/carla#licenses)는 CARLA 전용 코드의 MIT, 전용 자산의 CC-BY, Unreal Engine의 별도 조건을 구분합니다. 자산별 정확한 조건과 의존성도 따로 확인하며, 시뮬레이터에서 만든 장면을 이 저장소가 직접 주행 시험한 기록으로 사용하지 않습니다.

## cFS와 F Prime: 벤치의 명령·상태·텔레메트리부터 봅니다

cFS의 [공식 README](https://github.com/nasa/cFS)는 cFE·OSAL·PSP와 앱으로 구성되는 프레임워크 및 공개 Demo Bundle을 설명합니다. 앱의 기능, 운영체제 추상화, 플랫폼 지원과 메시지 경로를 나누어 읽을 수 있습니다. 현재 README의 빠른 실행 경로는 Make·CMake·GCC·Git과 서브모듈, `pc-linux` 구성을 사용합니다. 시험 대상의 판본·플랫폼·앱 집합을 고정한 뒤 벤치에서 no-op과 명령 카운터·텔레메트리를 확인하는 경로입니다.

같은 README는 공개 번들이 flight distribution이 아니며 그대로 비행시켜서는 안 되고, 운영 시스템으로 완전히 검증된 배포물이 아니라고 명시합니다. 특정 우주 임무가 프레임워크를 사용했다는 사실은 이 Demo Bundle이나 자체 예제의 임무 적합성을 보증하지 않습니다. 이 폴더의 Protobuf 센서 메시지는 자체 벤치 형식이며 cFS 패킷·소프트웨어 버스·지상국을 구현한 결과가 아닙니다.

F Prime의 [공식 입문](https://fprime.jpl.nasa.gov/latest/docs/getting-started/)은 C++ 컴포넌트, 포트·토폴로지와 코드 생성 도구를 설명합니다. [Hello World](https://fprime.jpl.nasa.gov/latest/tutorials-hello-world/docs/hello-world/) 뒤에 MathComponent의 사용자 포트·자료형·단위 검사를 읽으면 명령, 이벤트와 텔레메트리가 어떤 경계에서 생기는지 살펴볼 수 있습니다. FPP는 구조를 기술하는 모델 언어, C++은 컴포넌트 구현으로 구분합니다. Python 개발 도구와 지상 데이터 도구인 GDS는 생성·실행·관측을 돕습니다. [설치 안내](https://fprime.jpl.nasa.gov/latest/docs/getting-started/installing-fprime/)는 프로젝트별 가상 환경과 도구 의존성을 설명하며 WSL 1은 지원하지 않는다고 표시합니다.

[cFS LICENSE](https://github.com/nasa/cFS/blob/main/LICENSE)와 [F Prime LICENSE.txt](https://github.com/nasa/fprime/blob/devel/LICENSE.txt)는 Apache-2.0입니다. 서브모듈·별도 앱·튜토리얼 저장소의 조건은 각각 확인합니다. 두 프레임워크의 이름만 보고 동일한 큐·스레드·메시지 형식으로 구현됐다고 가정하지 않습니다.

## Ada/SPARK와 Modelica: 다른 종류의 오류를 찾는 언어

Ada/SPARK에서는 데이터 범위와 계약을 코드와 함께 표현하고 GNATprove로 분석합니다. [공식 시작 예제](https://docs.adacore.com/spark2014-docs/html/ug/en/getting_started.html)는 `Diff`의 의존 계약과 잘못된 계산을 이용해 도구의 역할을 설명합니다. [Introduction to SPARK](https://learn.adacore.com/courses/intro-to-spark/index.html)로 언어를 익힌 뒤 작은 벤치 자료형의 범위·사전조건·후조건부터 읽는 경로를 권합니다. Ada 컴파일 성공, 예제 입력의 테스트 통과와 GNATprove가 명시한 가정 아래 성질을 증명했다는 결과는 각각 기록해야 합니다.

확인한 온라인 User’s Guide는 개발판 28.0w이며, [Alire의 GNATprove](https://alire.ada.dev/crates/gnatprove)는 16.1.0으로 표시됩니다. Alire 설명은 해당 빌드가 특정 SPARK Pro 정식 판본과 같지 않을 수 있다고 밝힙니다. 배포 도구에 동봉한 문서와 온라인 최신 문서를 구분합니다. 도구 소스의 [LICENSE](https://github.com/AdaCore/spark2014/blob/master/LICENSE)는 GPL v3 텍스트이며 Alire 패키지는 GPL-3.0-or-later로 표시합니다. 이것을 별도 예제·문서·프로그램 전체에 대한 일괄 이용 조건으로 확대하지 않습니다.

Modelica는 부품·연결·방정식으로 여러 물리 영역의 모델을 기술하는 언어입니다. OpenModelica는 이를 처리하는 도구 중 하나입니다. [공식 사용자 문서](https://openmodelica.org/useresresources/userdocumentation/)는 OMEdit·명령행·OMNotebook·OMWebbook 등의 학습 경로를 연결합니다. 전기·기계·열을 함께 읽을 때 유용하지만, Python의 별도 미분방정식 계산을 실행했다고 Modelica 모델을 번역·해석한 것은 아닙니다. 실제 예제에서는 모델, 라이브러리 판본, 초기조건·해석기·출력 시간을 함께 기록해야 합니다.

[Windows 배포 안내](https://openmodelica.org/download/download-windows/)는 확인 시점 공식 판본을 1.27.1로 표시합니다. [Modelica Standard Library](https://github.com/modelica/ModelicaStandardLibrary)의 현재 안내는 4.1.0이며 [LICENSE](https://github.com/modelica/ModelicaStandardLibrary/blob/master/LICENSE)는 BSD-3-Clause입니다. OpenModelica 컴파일러의 [OSMC-License.txt](https://github.com/OpenModelica/OpenModelica/blob/master/OSMC-License.txt)는 AGPL v3 또는 OSMC-PL 1.8 조건을 설명하고, [런타임 조건](https://github.com/OpenModelica/OpenModelica/blob/master/OSMC-Runtime-License.txt)은 BSD New 선택도 별도로 설명합니다. 언어·표준 라이브러리·컴파일러·생성물에 연결되는 런타임을 하나의 라이선스로 합치지 않습니다.

## 자료와 실행 기록을 읽는 기준

- 외부 코드·도표·문제 원문을 통째로 옮기는 대신 공식 링크와 직접 작성한 설명·예제를 사용합니다. 실제 외부 파일을 재사용하면 판본·경로·해시·라이선스 고지를 개별 기록합니다.
- 공식 튜토리얼의 존재, 문서의 설치 명령, 이 환경에서 실제로 실행한 결과를 나누어 적습니다. 웹에서 읽는 문서는 온라인 자동 채점 서비스와도 구분합니다.
- 같은 시각·좌표·단위·자료형의 조건이 맞아야 모듈을 연결할 수 있습니다. 라이브러리가 빌드됐다는 사실과 센서·네트워크·시간·물리 모형이 함께 맞는다는 사실은 다릅니다.
- 교육용 로봇과 벤치 메시지에서 익힌 오류 격리·기록·재현 원칙을 시스템의 공통 기반으로 연결합니다. 이 자료는 운용 차량·기체·무기 시스템의 승인이나 인증을 제시하지 않습니다.
