# 현장 계측과 검증 | Measurement, debugging and validation

보드의 전압을 측정하고, 펌웨어의 간헐적인 오류를 재현하며, 칩의 동작 조건과 통신 실패를 구분하는 기술 자료입니다. 모델명을 정한 장비 설명서, 설정 순서, 계산 예제, 실패 조건과 판정 근거를 함께 읽습니다. 각 글에서 제조사 사양, 직접 구성한 예제, 로컬 실행, 실물 측정을 구분합니다.

## 장비의 선택·연결·설정

| 장비와 본문 | 읽고 판단할 내용 |
| --- | --- |
| [Keysight DSOX1204G 오실로스코프](계측기_instruments/오실로스코프로신호와리플관측_keysight-dsox1204g.md) | 프로브 보정과 부하, 대역폭·샘플링·트리거, 디지털 에지와 전원 리플의 관측 조건 |
| [Keysight 34461A 정밀 멀티미터](계측기_instruments/정밀전압과낮은저항측정_keysight-34461a.md) | 범위와 정확도, 적분 시간·예열, 2선·4선 저항 측정과 오차 계산 |
| [Keithley 2450 SMU](계측기_instruments/전압전류인가와소자특성측정_keithley-2450.md) | 전압·전류 인가와 측정, compliance, local·remote sense, 소자 I–V의 해석 |
| [Saleae Logic Pro 8 로직 분석기](계측기_instruments/디지털타이밍과통신해석_saleae-logic-pro8.md) | 임계값과 디지털 샘플링, UART·I²C 해석, 파형과 디코더의 판단 차이 |
| [Keysight E36312A 전원·Rigol DL3021 전자부하](계측기_instruments/전원과전자부하의전압전류제어_keysight-e36312a-rigol-dl3021.md) | CV·CC·OCP, remote sense, 부하 slew와 전원 과도 응답 |
| [Keysight E4980AL LCR 미터](계측기_instruments/주파수에따른소자특성측정_keysight-e4980al.md) | 시험 주파수·레벨, 직렬·병렬 등가회로, 4TP와 치구 보정 |
| [R&S FPC1500 스펙트럼 분석기](계측기_instruments/스펙트럼의대역폭과입력레벨_rohde-schwarz-fpc1500.md) | RBW·VBW, 입력 감쇠·전치증폭기, 잡음바닥과 내부 고조파 |
| [Keysight E5061B 네트워크 분석기](계측기_instruments/반사와전달의기준면측정_keysight-e5061b.md) | S11·S21, SOLT 교정·기준면, 케이블 손실·위상과 port extension |

## 펌웨어·칩·설비의 오류 분리

| 본문 | 관측에서 원인 후보를 좁히는 방법 |
| --- | --- |
| [Cortex-M7의 DMA 버퍼와 캐시](펌웨어와디버깅_firmware-debugging/DMA버퍼와캐시의경계_cortex-m7-cache-dma.md) | CPU와 DMA가 다른 값을 보는 이유, 캐시 라인 정렬·소유권·clean·invalidate |
| [Cortex-M 예외와 고장 추적](펌웨어와디버깅_firmware-debugging/예외상태와고장원인추적_cortex-m-fault-debugging.md) | fault 상태와 쌓인 레지스터, PC·LR·스택, GDB와 watchpoint로 가설 분리 |
| [PVT·shmoo와 칩 시험](칩과시스템시험_chip-system-testing/조건별오동작과수율의경계_pvt-shmoo-characterization.md) | 온도·전압·주파수 조건, characterization·validation·양산 검사의 차이, 판정 여유와 분모 |
| [CAN·EtherCAT·Modbus의 고장 분리](칩과시스템시험_chip-system-testing/차량과설비통신의고장분리_can-ethercat-modbus.md) | 배선·링크·프로토콜·응용 상태의 구분, 타임아웃·재시도·레지스터 해석 |
| [SCPI·PyVISA와 시험 결과 기록](계측자동화_instrument-automation/명령응답과시험결과기록_scpi-pyvisa-automation.md) | 식별·명령·응답·상태·유효성·판정·정리, 실제 코드의 mock 검사와 합성 전력 계산 |

## 오류를 코드로 재현하기

[실무 검증 코드](../예제_examples/실무검증_practical-validation/README.md)는 잘못된 조건과 해결한 조건을 같은 입력에서 비교합니다. C/C++ 세 프로그램은 실제 호스트 빌드·실행이며 칩·AI 예제는 Python 모형과 합성 자료입니다.

| 재현하는 문제 | 원인과 해결 | 본문 |
| --- | --- | --- |
| 4바이트만 받아도 거대한 프레임을 승인합니다. | 32비트로 좁힌 길이와 실제 공간을 구분하고 곱셈 전에 상한을 검사합니다. | [C 프레임 검사](../설계와검증사례_engineering-cases/이진프레임의길이와바이트순서_c-frame-bounds.md) |
| 큐에 보관한 READY가 ERROR로 바뀝니다. | 빌린 뷰·소유 복사·길이 전달·재할당 핸들을 구분합니다. | [C++ 수신 버퍼](../설계와검증사례_engineering-cases/수신버퍼의소유권과뷰수명_cpp-view-ownership.md) |
| 데이터가 있다고 표시됐는데 옛값을 읽습니다. | 기록 후 공개, 생산자·소비자 소유 필드, release·acquire를 비교합니다. | [링버퍼의 공개 순서](../설계와검증사례_engineering-cases/링버퍼의공개순서와공유카운터_ring-publication.md) |
| 같은 NPU 입력에서 출력이 다릅니다. | 주소식·입력 복사본·누산 폭을 한 조건씩 바꿉니다. | [칩 산술의 계약](../설계와검증사례_engineering-cases/칩산술의레이아웃과누산폭_chip-arithmetic-contract.md) |
| 결과 CSV가 완벽히 일치하지만 제품이 다릅니다. | 행 번호 대신 제품 ID·시험 조건을 검증하고 같은 ID로 연결합니다. | [시험 자료와 오판율](../설계와검증사례_engineering-cases/시험데이터의식별자와오판율_test-data-identity-metrics.md) |
| 모델이 정상 응답하지만 판정이 바뀝니다. | 열 이름·단위·저장 scaler·모델 상태를 같은 계약으로 묶습니다. | [AI 배포 전처리](../설계와검증사례_engineering-cases/AI배포의전처리와특성순서_ai-preprocessing-contract.md) |
| 평가 100%를 새 생산 묶음에서도 기대합니다. | 공유 group을 거절하고 평가 질문에 맞게 분할합니다. | [AI group 분리](../설계와검증사례_engineering-cases/생산묶음단위분할과평가누출_ai-group-evaluation.md) |

## 업무 질문에서 시작하기

반도체·전자·차량·산업 설비의 공통 기술 질문에서 해당 본문과 기존 구현으로 연결합니다.

| 확인하려는 문제 | 먼저 읽을 글 | 이어서 볼 구현·분야 |
| --- | --- | --- |
| 전압 숫자가 기대와 다른 이유를 나누고 싶습니다. | DMM·SMU → 오실로스코프 | [센서·계측](../분야_topics/37-센서계측_sensors-instrumentation/README.md), [PCB 전원·귀환 경로](../분야_topics/12-PCB하드웨어설계_pcb-hardware/README.md) |
| 전송은 끝났는데 데이터가 달라집니다. | DMA·캐시 → 로직 분석기 | [FPGA 프레임 오류 사례](../설계와검증사례_engineering-cases/프레임오류와FPGA검증_fpga-frame-validation.md), [UART 호스트·펌웨어](../프로젝트_projects/embedded-validation-lab/README.md) |
| 최적화를 켜면 고장이 재현되지 않습니다. | Cortex-M 예외 추적 | [C·C++·Python](../분야_topics/04-c-cpp-python/README.md), [펌웨어·RTOS](../분야_topics/17-펌웨어-RTOS_firmware-rtos/README.md), [시스템 디버깅](../분야_topics/19-시스템디버깅_openocd-debugging/README.md) |
| 칩이 특정 조건에서만 틀리거나 시험 결과가 서로 다릅니다. | PVT·shmoo → 계측 자동화 | [DFT·제조 시험](../분야_topics/51-반도체테스트제조_test-manufacturing/README.md), [검증 모델과 결과 집계](../프로젝트_projects/practical-silicon-lab/validation/README.md) |
| 차량·설비의 통신이 간헐적으로 멈춥니다. | CAN·EtherCAT·Modbus → 로직 분석기 | [인터페이스·통신](../분야_topics/20-인터페이스통신_interfaces-communications/README.md), [제어·신호처리](../분야_topics/21-신호처리제어_signals-control/README.md) |
| RTL과 소프트웨어의 정수 결과가 다릅니다. | 프레임 사례의 바이트·채널 해석 | [컴퓨터구조](../분야_topics/16-프로세서구조_arm-riscv/README.md), [Transformer·DRAM-PIM](../프로젝트_projects/transformer-dram-pim/README.md), [부분곱·CNN](../프로젝트_projects/cnn-partial-product-reproduction/README.md) |
| AI의 높은 점수가 입력 누출 때문인지 확인하고 싶습니다. | [제조 시계열의 인과 경계](../설계와검증사례_engineering-cases/제조시계열의인과경계_causal-trace-validation.md) | [제조 이상 탐지 코드](../프로젝트_projects/st-awfd-anomaly-triage/README.md), [AI 평가](../분야_topics/46-AI응용에이전트평가_ai-agents-evaluation/README.md) |
| 서버·자동화 도구가 같은 기록을 덮어씁니다. | [SQLite 갱신 충돌 사례](../설계와검증사례_engineering-cases/동시갱신과SQLite검증_sqlite-concurrency.md) | [Linux](../분야_topics/01-linux-bash/README.md), [DB·데이터공학](../분야_topics/40-데이터베이스데이터공학_databases-data-engineering/README.md) |
| 알고리즘과 언어 구현을 함께 확인하고 싶습니다. | [세 언어의 기초 알고리즘](../프로젝트_projects/coding-practice-basics/README.md) | [C·C++·Python 실행 도구](../프로젝트_projects/coding-practice-toolkit/README.md), [코딩테스트 풀이·줄별 문법](../programmers/README.md) |

전력·열·기계 구동의 배경은 [전력전자·에너지](../분야_topics/31-전력전자에너지_power-energy/README.md), [패키징·열 설계](../분야_topics/36-패키징열설계_packaging-thermal/README.md), [로봇·제어](../분야_topics/22-로봇제어_robotics-boards/README.md)로 이어집니다. 제품의 기술·산업 비교는 [제품 리뷰](../제품리뷰_reviews/README.md)에 따로 있습니다.

## 실행 근거를 읽는 방법

[설계와 검증 사례](../설계와검증사례_engineering-cases/README.md)는 요구사항·대안·선택·오류 주입·관측·남은 검증을 실제 저장소 코드에 연결합니다. 날짜가 붙은 검증 기록에는 환경과 재현 명령이 있습니다. 장비 설명서에서 확인한 사양을 직접 측정한 수치로 표시하지 않으며, mock 통과를 실제 장비 사용 결과로 확대하지 않습니다.

## English

This collection covers nine named instruments in eight notes, Cortex-M firmware debugging, silicon characterization, industrial communications and SCPI automation. Each note connects preparation, configuration, observation, interpretation and record keeping. Reading routes lead to existing C/C++, firmware, architecture, RTL, AI and Python implementations. Manufacturer specifications, constructed examples, local software checks and physical measurements are identified separately.
