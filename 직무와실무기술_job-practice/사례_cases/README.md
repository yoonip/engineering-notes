# 직무별 업무 사례와 공개 코드 | Role-based cases and public code

[직무·기술 목차](../README.md) · [직무별 사례와 담당 범위](06-직무별사례와담당범위_role-case-map.md) · [코드 출처와 이용 조건](코드출처와이용조건_CODE_SOURCES.md)

검사 대상과 장비, 측정값, 프로그램의 역할, 결과 해석과 원인 분석을 한 흐름으로 읽습니다. 업무 상황은 제공된 직무기술서를 바탕으로 구성했고, 코드 발췌는 제조사·공개 실무 프로젝트·공식 문서의 고정 판본에서 가져왔습니다. 각 글에서 원문 코드·추가 주석·가정한 수치·실제로 실행한 범위를 구분합니다.

## 업무 사례

| 분야 | 선택한 업무 상황 | 공개 코드와 확인할 결과 |
| --- | --- | --- |
| [회로·소자 계측](01-회로와소자의계측코드_circuit-device-measurement.md) | 저항값 판정, 작은 접속 저항 측정, ADC 보드의 데이터 취득 문제 | Tektronix 2450 Python 예제, ADI no-OS C 드라이버로 인가·readback·4선식·RDY·오류 반환을 읽습니다. |
| [펌웨어·통신](02-펌웨어와통신의공개코드_firmware-communication.md) | UART 수신 누락, CAN 통신 분리, 기기 펌웨어의 호스트 시험 | Zephyr의 C·Python 예제로 인터럽트·큐·필터·길이·상태와 시험 판정을 연결합니다. |
| [칩·메모리 검사](03-칩과메모리의공개검사코드_chip-memory-test.md) | RTL 출력 불일치, DRAM 패턴 검사, SSD의 데이터 검증 | cocotb 공식 Python 시험, U-Boot 실제 C 구현, fio 공식 설정으로 기대값·주소·오류·성능 조건을 읽습니다. |
| [공정·설비·패키지](04-공정설비와패키지의검사사례_process-equipment-package.md) | 설비 신호 수집, 공정 집단의 산포 비교, 패키지 분석의 인계 | PyEpics·SciPy 공개 코드를 신호의 유효성·분산 검정·시료 추적과 연결합니다. |
| [AI·제조 IT](05-AI와제조IT의평가사례_ai-manufacturing-it.md) | 전처리 누락·평가 누출, 제조 기록의 중복 수신 | scikit-learn·PostgreSQL 공식 예제로 학습/평가 분리·파이프라인·식별자·재처리를 읽습니다. |

## 읽는 순서

1. [직무별 연결표](06-직무별사례와담당범위_role-case-map.md)에서 담당 대상과 업무 상황을 선택합니다.
2. 장비와 측정 항목을 읽고, 어떤 물리량이나 동작을 관찰하는지 확인합니다.
3. 코드의 실행 위치를 구분합니다. MCU·부트로더의 C, 호스트 PC의 Python, RTL 시뮬레이터와 시험 환경은 서로 다른 일을 맡습니다.
4. 정상·이상·취득 실패를 나누고, 같은 증상을 만들 수 있는 원인을 비교합니다.
5. 원인을 나누는 대조, 조치 후 재검사 조건과 남길 결과물을 확인합니다.

코드는 함수나 설정의 일부를 읽기 위해 발췌한 경우가 있습니다. 원본 전체의 초기화·호출부·장비 설정·의존성을 함께 연결했으며, 발췌를 그대로 복사하면 독립 실행된다고 표시하지 않았습니다. 실제 장비를 연결해 측정한 결과와 문헌·코드 검토, 공식 예제의 로컬 실행은 각 글의 마지막에 따로 적었습니다.

## 기본 개념을 이어서 읽습니다

- [C·C++·Python의 사용 위치](../10-C와Python이쓰이는위치_languages-in-the-workflow.md): 제품 안의 코드와 호스트의 계측·분석을 나눕니다.
- [검사 판정과 기록](../11-검사결과의판정과기록_test-decisions-evidence.md): 규격·불확도·유효하지 않은 측정·재검사 이력을 읽습니다.
- [기반 지식과 학습 경로](../12-기반지식과학습경로_foundations-learning-path.md): 회로·수학·컴퓨터 구조·반도체·데이터 기초로 돌아갑니다.

## English

These cases connect role-specific work to instruments, observables, public C/Python code, result interpretation and fault isolation. Published excerpts identify fixed upstream revisions, original locations, license terms and changes. Work scenarios and assumed calculations remain distinct from instrument measurements and from locally executed official software examples.
