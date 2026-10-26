# AI·데이터와 제조 IT | AI, data and manufacturing IT

[직무·실무 목차](README.md) · [메모리 제품·양산 직무](03-메모리제품과양산의직무_memory-product-production-roles.md) · [검사결과 판정·기록](11-검사결과의판정과기록_test-decisions-evidence.md) · [출처와 판본](출처와검토범위_SOURCES.md) · [AI·제조 IT의 평가 사례](사례_cases/05-AI와제조IT의평가사례_ai-manufacturing-it.md)

제조 현장의 AI·IT는 모델 하나를 학습시키는 일로 끝나지 않습니다. 장비에서 나온 자료가 올바른 제품·시점·조건과 연결되어야 하고, 분석 결과가 업무 시스템과 실제 설비에서 어떤 조치로 이어지는지도 정해야 합니다.

업무 애플리케이션·데이터 플랫폼·AI·생산관리·물류·설비 제어·시설 모델은 다른 입력과 결과물을 다룹니다. 이 글은 현장에서 얻은 자료가 분석·업무 판단·설비 상태와 연결되는 경로를 설명합니다. 구조와 제품 이름은 공개 기술을 이해하기 위한 예이며 특정 회사의 내부 구축도를 추정한 것이 아닙니다.

## 1. 언어·프레임워크·플랫폼을 구분합니다

| 분류 | 도구·기술의 예 | 실제로 맡을 수 있는 일 |
| --- | --- | --- |
| 프로그램을 표현하는 언어 | C/C++, C#, Java, Python, JavaScript, SQL | 타깃·서버·화면·분석·데이터 질의를 서로 다른 환경에서 구현합니다. |
| 화면 라이브러리 | React | 현황·경보·시험 이력을 사용자가 조작하는 화면을 구성합니다. |
| 서버 애플리케이션 프레임워크 | Spring Boot | 업무 요청·검증·권한·DB 연결 등을 처리하는 서버를 구성합니다. |
| 데이터 저장·접근 도구 | DBMS, Redis | 영속 기록과 빠른 조회·cache 등 역할에 맞게 자료를 다룹니다. |
| AI 개발·연결 도구 | LLM API, LangChain, Hugging Face | 모델 호출·검색·평가·응용을 연결합니다. |
| 시스템 운영 기술 | 컨테이너, Kubernetes, 서버·스토리지·네트워크 | 프로그램을 배포하고 자원·장애·운영 상태를 관리합니다. |
| 공장 자동화·설비 도구 | PLC, 센서·산업 네트워크, AMHS | 실제 설비의 상태를 관측하고 정해진 동작으로 연결합니다. |
| 공간·건설 데이터 도구 | Revit, Navisworks, Dynamo 등 | 건물·설비·배관의 모델과 배치·변경 정보를 다룹니다. |

React·Redis·Kubernetes는 프로그래밍 언어 이름이 아닙니다. 이들을 모두 ‘코딩 가능’이라는 한 항목으로 묶으면 어떤 계층에서 어떤 문제를 풀 수 있는지 설명하기 어렵습니다. 먼저 입력·처리·저장·사용자의 경계를 나눈 뒤 필요한 도구를 고르시면 좋습니다.

IT 문맥의 MSA는 microservices architecture, 즉 업무 기능을 작은 서비스로 나누어 연결하는 구조를 뜻합니다. 계측 분야의 measurement system analysis와 같은 약어이지만 개념은 다릅니다. 작은 서비스로 나누면 독립 배포가 가능해질 수 있지만 API·자료 일관성·장애 전파·관측성도 함께 설계해야 합니다. [Microsoft의 Microservices architecture 정의와 구성](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/microservices)

## 2. 장비 데이터가 판단 근거가 되기까지

다음은 특정 회사 시스템이 아닌 학습용 연결도입니다.

```mermaid
flowchart LR
    A["센서·계측·장비 이벤트"] --> B["수집: 시간·단위·장비 ID"]
    B --> C["원본 보존·형식 검사"]
    C --> D["제품·공정·시험 이력 연결"]
    D --> E["통계·AI·이상 후보"]
    E --> F["업무 판단·조치 승인"]
    F --> G["조치·재검사·변경 기록"]
    G --> D
```

| 단계 | 필요한 개념 | 잘못 연결했을 때 생기는 문제 |
| --- | --- | --- |
| 수집 | event time은 사건이 일어난 때, 수신 시각은 시스템이 받은 때입니다. | 네트워크 지연이 실제 공정의 선후 관계처럼 보일 수 있습니다. |
| 식별 | 장비·chamber·lot·wafer·die·시험 실행의 ID를 구분합니다. | 다른 제품의 계측과 전기 시험을 같은 제품 결과처럼 연결할 수 있습니다. |
| 형식·단위 | 값의 자료형·단위·유효 범위를 맞춥니다. | mA와 A, ms와 s가 같은 열에 섞여 잘못된 경보를 만들 수 있습니다. |
| 품질 | 누락·중복·지연·재전송·센서 교체를 기록합니다. | 센서가 끊긴 값을 정상 상태로 해석하거나 한 사건을 여러 번 집계할 수 있습니다. |
| 이력 연결 | 사용한 recipe·firmware·검사 프로그램·모델 판본을 연결합니다. | 조건 변경의 효과와 제품·판본 차이가 섞일 수 있습니다. |
| 조치 | 관측·판단·승인·실행·결과를 분리합니다. | 경보가 떴다는 사실을 실제 장비 조치가 끝난 것으로 착각할 수 있습니다. |

여기서 pipeline은 원본 자료를 수집·검사·변환·전달하는 처리 경로입니다. governance는 이름·소유자·접근권한·품질 기준·변경 규칙을 관리하는 체계입니다. 마스터 데이터는 제품·장비 등 여러 업무가 공통으로 참조하는 기준 자료입니다. 모델의 높은 점수 이전에 이 자료들이 무엇을 뜻하는지 일치해야 합니다.

## 3. SQL·Python·업무 서버가 나누어 맡는 일

| 도구 | 구체적인 사용 예 | 결과물 |
| --- | --- | --- |
| SQL | wafer ID와 시험 실행 ID를 기준으로 계측·시험 결과를 연결하고 조건별 건수를 집계합니다. | 재현 가능한 조회와 집계 기준입니다. |
| Python | 여러 파일의 단위·누락·시간을 검사하고 분석·모델 평가·그림을 반복 생성합니다. | 검사 로그, 전처리·평가 절차와 분석 자료입니다. |
| Java·C# 등의 서버 코드 | 업무 요청을 받고 권한·상태·트랜잭션을 검사한 뒤 기록합니다. | API 계약·이력·오류 응답입니다. |
| JavaScript·화면 코드 | 원본·처리 상태·경보와 사용자의 승인·수정 입력을 보여 줍니다. | 사용자가 실제 의미를 읽을 수 있는 화면입니다. |
| cache·메시지·저장 계층 | 반복 조회와 비동기 전달·영속 기록을 목적별로 구성합니다. | 조회 속도와 복구·재처리 기준입니다. |

SQL의 `JOIN`은 두 표를 정한 키로 연결하는 연산입니다. 같은 행 번호끼리 연결한다는 뜻이 아닙니다. 제품별 측정이 여러 번 있으면 제품 ID만으로 연결했을 때 중복 행이 늘어날 수 있으므로 시험 실행·시각·판본을 포함한 연결 기준을 정해야 합니다.

PostgreSQL의 primary key·unique·foreign key·not-null 같은 제약은 자료의 일부 규칙을 DB에 표현하는 방법입니다. 다만 ‘모든 센서값의 단위가 올바릅니다’나 ‘이 자료가 실제로 같은 웨이퍼입니다’라는 의미를 자동으로 증명하지는 않습니다. [공식 Constraints 문서의 정의·범위](https://www.postgresql.org/docs/current/ddl-constraints.html)

다음은 설명용 사례입니다. 시험 서버에 같은 완료 이벤트가 두 번 도착했다고 가정합니다. 단순히 두 행을 더하면 생산량·오류 수가 두 배가 될 수 있습니다. 업무 사건을 구분하는 키를 정하고, 재전송은 기존 사건의 재전달인지 새로운 실행인지 판정해야 합니다. 최초 실패와 재시험을 모두 지워 하나의 최신 PASS만 남기는 것 역시 다른 종류의 정보 손실입니다.

이 원리는 [시험 ID·오판율 사례](../설계와검증사례_engineering-cases/시험데이터의식별자와오판율_test-data-identity-metrics.md)와 [시간초과·늦은 쓰기·재시도](../설계와검증사례_engineering-cases/시간초과뒤늦은쓰기와재시도_block-io-timeout-retry.md)에서 구체적으로 이어집니다.

## 4. AMHS는 데이터와 실제 이동을 함께 맞춥니다

AMHS는 automated material handling system, 자동 반송 체계입니다. 원문 11쪽은 OHT·Stocker·Conveyor·AMR와 MCS 최적화를 적습니다. OHT는 머리 위 경로의 반송 차량, stocker는 보관 설비, conveyor는 정한 경로의 운송 장치, AMR은 자율 이동 로봇이라는 서로 다른 이동·보관 수단입니다.

Daifuku의 공식 cleanroom 자료는 반도체용 AMHS의 반송·보관과 시설 이용률을 설명합니다. 반송 장치·보관·호스트 시스템의 연결을 이해하기 위한 공개 예이며, 실제 장비 구성은 공장의 배치·제품·운영 조건에 따라 달라집니다. [공식 Cleanroom·Semiconductor 설명](https://www.daifuku.com/solution/cleanroom/)

| 관점 | 맞춰야 할 대상 | 학습용 오류 예 |
| --- | --- | --- |
| 작업 식별 | 무엇을 어디서 어디로 옮기는 요청인지입니다. | 이전 요청의 완료 응답을 새 요청의 완료로 처리합니다. |
| 물리 상태 | 출발·도착·점유·적재·인계 상태입니다. | DB에서는 도착했지만 실제 장비가 받지 않았습니다. |
| 경로·자원 | 경로·보관 공간·장비 입구를 공유하는 조건입니다. | 한 경로의 효율만 올리다가 다른 병목·대기를 키웁니다. |
| 처리량·이용률 | 일정 시간의 완료량과 자원 사용 정도입니다. | 차량 이용률이 높다는 이유만으로 전체 이동 시간이 짧다고 판단합니다. |
| 장애 복구 | 시간초과·분실 응답·재시작 뒤의 실제 위치입니다. | 통신 재시도를 물리 이동의 무조건 재실행으로 바꿉니다. |

MCS는 이 문맥에서 material control system, 반송 제어 시스템을 가리킵니다. 이동 경로를 계산하는 프로그램, 센서·작동기를 다루는 제어기, 업무 요청을 내는 상위 시스템은 역할이 다릅니다. Python의 시뮬레이션·로그 분석이 유용하더라도 안전 인터록이나 제어기의 시간 요구를 자동으로 대신하는 것은 아닙니다.

제조 장비의 통신에서는 SECS/GEM을 만날 수 있습니다. SEMI의 공식 개요는 E30을 장비 통신·제어의 공통 모델, E5를 SECS-II 메시지 내용의 규격으로 구분합니다. 모델·메시지 규격과 개별 설비의 실제 동작·안전 조건은 다른 층입니다. [SEMI의 SECS/GEM 설명](https://www.semi.org/en/standards-watch-2022-Sept/intro-to-semi-communication-standards)

## 5. AI의 점수와 공정의 원인은 다릅니다

원문 13쪽은 계측·분석·장비·결함 분야의 AI/DT를, 10쪽은 AI 모델·시스템 최적화를 설명합니다. 활용 대상은 영상 분류, 이상 탐지, 수치 예측, 검색 보조 등으로 달라질 수 있습니다.

| 활용 예 | 모델 입력·출력 | 함께 확인할 근거 |
| --- | --- | --- |
| 결함 영상 분류 | 검사 영상에서 결함 종류·위치를 추정합니다. | 실제 라벨·영상 조건·크기별 누락·오검출과 판단하기 어려운 표본입니다. |
| 센서 이상 후보 탐지 | 시계열에서 정상과 다른 양상을 찾습니다. | 센서 고장·공정 변화·제품 변경 중 무엇과 연결되는지입니다. |
| 품질·수율 예측 | 공정·계측 특성에서 후속 결과를 예측합니다. | 예측 시점에 실제로 알 수 있는 입력인지와 다른 lot·시기에서의 성능입니다. |
| 자료 검색·질의 보조 | 문서에서 관련 근거를 찾아 답변을 구성합니다. | 검색한 판본·권한·원문 구간과 답변의 일치입니다. |

데이터 leakage는 실제 예측 시점에 알 수 없는 정보가 학습·평가에 들어가는 문제입니다. 예를 들어 불량 판정 후 작성한 분석 결과를 그 불량의 사전 예측 입력으로 넣으면 실제 운용에서 쓸 수 없는 모델을 만들 수 있습니다. 전처리 평균·특성 선택도 학습 자료에서 정하고 평가 자료는 그 규칙으로 처리해야 합니다. [scikit-learn의 Data leakage·Pipeline 설명](https://scikit-learn.org/stable/common_pitfalls)

같은 웨이퍼·같은 생산 묶음의 비슷한 표본이 학습과 평가에 나뉘면 성능이 좋게 보일 수 있습니다. 목적에 맞게 묶음·시기·제품 경계를 정해야 합니다. 구체적인 모형과 결과는 [생산 묶음 단위 평가](../설계와검증사례_engineering-cases/생산묶음단위분할과평가누출_ai-group-evaluation.md)와 [제조 시계열의 인과 경계](../설계와검증사례_engineering-cases/제조시계열의인과경계_causal-trace-validation.md)를 보시면 좋습니다.

드문 불량에서는 전체 정확도만 높아도 실제 불량을 놓치거나 경보 대부분이 정상일 수 있습니다. 불량을 얼마나 찾는지, 정상 제품을 얼마나 오인하는지, 경보 중 실제 불량 비율이 얼마인지와 표본 수를 함께 봅니다. 계산은 [기저율과 경보 정밀도](../설계와검증사례_engineering-cases/불량비율과경보의정밀도_ai-prevalence-precision.md), 배포 일관성은 [전처리·특성 순서](../설계와검증사례_engineering-cases/AI배포의전처리와특성순서_ai-preprocessing-contract.md)에 연결했습니다.

모델이 어떤 센서를 중요하게 사용했다는 결과는 원인 규명의 출발점이 될 수 있지만 곧바로 그 센서를 조정하면 불량이 줄어든다는 증거는 아닙니다. 조치 전후의 조건을 맞추고 다른 변화와 계측·물리 근거를 함께 확인해야 합니다.

## 6. LLM·RAG를 업무 자료에 연결할 때

RAG는 retrieval-augmented generation, 필요한 외부 자료를 검색하여 답변의 문맥으로 제공하는 구조입니다. 기존 모델에 검색을 연결하는 일과 언어 모델을 처음부터 학습시키는 일은 필요한 자료·연산·평가 범위가 다릅니다. [LangChain의 Retrieval·RAG 공식 설명](https://docs.langchain.com/oss/python/deepagents/retrieval)

| 단계 | 구체적으로 하는 일 | 평가할 오류 |
| --- | --- | --- |
| 자료 준비 | 문서의 본문·쪽·개정·소유자·권한을 저장합니다. | 오래된 판본·표 누락·권한이 다른 자료의 혼합입니다. |
| 검색 | 질문에 필요한 구간을 찾습니다. | 정답 근거가 있는데 못 찾거나 다른 제품의 자료를 찾습니다. |
| 답변 | 찾은 구간을 바탕으로 설명합니다. | 근거에 없는 수치·지원 기능·공정 조건을 덧붙입니다. |
| 업무 연결 | 답변·승인·조치·기록의 경계를 정합니다. | 참고 답변을 승인된 설비 조건·확정 판정으로 오인합니다. |

Python으로 문서 로더·검색·모델 호출·평가를 연결하고 SQL로 문서·판본·권한·로그를 관리할 수 있습니다. 하지만 검색 결과에 출처가 붙었다는 사실만으로 답변 전체가 정확해지는 것은 아닙니다. 검색 성능과 근거를 따르는 답변 능력을 따로 평가해야 합니다. 개념과 예시는 [RAG·도구 실행](../전자컴퓨터공학_ece/46-AI응용에이전트평가_ai-agents-evaluation/해설_notes/RAG와도구실행_retrieval-tools-and-evaluation.md)에서 이어집니다.

## 7. AI 메모리·시스템 연구에서는 병목을 어디서 재나요

원문 10쪽은 데이터센터, xPU/SoC, 메모리 하위 시스템, PIM/PNM/NMP, 이종 메모리, 컴파일러·런타임·플랫폼을 연결합니다. 모델을 실행시키는 SW와 메모리·가속기 구조를 함께 보는 업무입니다.

| 계층 | 확인할 내용 | 잘못된 비교의 예 |
| --- | --- | --- |
| 모델·알고리즘 | 정확도·입력 크기·정밀도·batch·시퀀스 조건입니다. | 문제의 크기나 품질을 바꾼 결과를 같은 과제의 속도 향상으로만 설명합니다. |
| 컴파일러·런타임 | 연산 배치·메모리 할당·전송·실행 순서입니다. | 계산만 재고 자료 전송·초기화 비용을 숨깁니다. |
| 메모리·인터커넥트 | 용량·대역폭·지연·공유·접속 경로입니다. | 이론 대역폭과 실제 응용 처리량을 같은 수치처럼 비교합니다. |
| 여러 장치·서버 | 분산 처리·통신·동기화·운영 자원입니다. | 장치 한 개의 빠른 연산만으로 전체 시스템 확장성을 판단합니다. |

CXL·UCIe·NVLink·Ethernet은 모두 같은 거리·계층·기능을 갖는 인터페이스 이름이 아닙니다. 이 장에서는 이름을 동일한 ‘고속 통신’으로 외우기보다, 어떤 장치를 어떤 범위에서 연결하고 메모리·캐시·프로토콜·운영 SW에 어떤 요구가 생기는지 확인합니다. [SoC 연결 구조](../전자컴퓨터공학_ece/34-SoC연결구조_soc-interconnects/README.md), [고성능·병렬 계산](../전자컴퓨터공학_ece/42-고성능병렬계산_hpc-parallel/README.md), [메모리·저장장치](../전자컴퓨터공학_ece/33-메모리저장장치_memory-storage/README.md)를 함께 읽으시면 좋습니다.

PIM·PNM·NMP 같은 이름도 연산을 메모리 안·근처 등으로 옮기는 접근을 살필 때 등장합니다. 표기만으로 데이터 배치·지원 연산·수치 정밀도·일관성·실제 이동 비용이 확정되지는 않습니다. 비교할 때는 실제 연산·자료 배치·인터페이스와 기준 시스템을 함께 확인합니다.

## 8. 개발 성공과 운영 성공을 구분합니다

Kubernetes는 컨테이너화한 workload와 서비스의 배포·상태·확장 등을 관리하는 체계입니다. 컨테이너는 실행에 필요한 소프트웨어 환경을 묶는 방식입니다. 서비스가 다시 시작된다는 사실만으로 업무 자료의 일관성과 완료 여부까지 복구되지는 않습니다. [Kubernetes 공식 개요](https://kubernetes.io/docs/concepts/overview/)

| 운영에서 볼 항목 | 필요한 기록 |
| --- | --- |
| 잘못된 모델·설정 배포 | 코드·모델·전처리·설정 판본과 배포/복귀 이력입니다. |
| 부분 실패·시간초과 | 요청 ID·실제 작업 상태·재시도·중복 처리 결과입니다. |
| 자료 파이프라인 지연 | 마지막 수신·처리 시각, 누락 범위·재처리 대상입니다. |
| 권한·추적 | 누가 어떤 자료를 보고 어떤 판단·조치를 했는지입니다. |
| 성능·용량 | 부하·응답 분포·오류·자원 사용과 측정 구간입니다. |

원문이 요구하는 개발·운영 경험을 설명하려면 ‘모델을 만들었습니다’나 ‘서비스를 실행했습니다’ 뒤에 입력 자료의 의미, 실패 조건, 판정 기준, 운영 기록을 붙일 수 있어야 합니다. [검사결과의 판정과 기록](11-검사결과의판정과기록_test-decisions-evidence.md)에서 같은 관점을 시험 결과에 적용합니다.

## 출처와 확인 범위

| 자료 | 읽은 범위·사용한 내용 |
| --- | --- |
| [Microsoft Microservices architecture](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/microservices) | What are microservices?·Components의 독립 서비스·API·운영 구성입니다. 특정 회사의 Azure 사용을 주장하지 않았습니다. |
| [PostgreSQL Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html) | 확인 당시 PostgreSQL 18의 not-null·unique·primary key·foreign key 등 자료 제약입니다. |
| [SEMI SECS/GEM 개요](https://www.semi.org/en/standards-watch-2022-Sept/intro-to-semi-communication-standards) | 2022년 공개 설명의 E30/GEM·E5/SECS-II 구분입니다. 유료 규격의 모든 메시지를 검토한 것은 아닙니다. |
| [Daifuku Cleanroom](https://www.daifuku.com/solution/cleanroom/) | 반도체용 AMHS·보관·반송의 공개 범위입니다. 특정 팹의 공급사·배치·운영 조건은 추정하지 않았습니다. |
| [scikit-learn Common pitfalls](https://scikit-learn.org/stable/common_pitfalls) | 확인 당시 1.9.1 문서의 Data leakage·전처리·Pipeline입니다. 모델별 성능 수치는 사용하지 않았습니다. |
| [LangChain Retrieval](https://docs.langchain.com/oss/python/deepagents/retrieval) | retrieval·knowledge base·RAG의 개요입니다. 확인 시점의 Deep Agents 경로로 연결했습니다. |
| [Kubernetes Overview](https://kubernetes.io/docs/concepts/overview/) | 컨테이너화 workload·서비스를 관리하는 플랫폼의 역할입니다. 현장 설비의 안전 제어 대체로 설명하지 않았습니다. |

외부 자료 확인일은 2026-10-26입니다. 처리 흐름·오류 표는 자체 학습 예이며 실제 공장 시스템의 설계도나 운영 측정 결과가 아닙니다.

## English

Manufacturing IT connects equipment events, product identity, data quality, analytics and controlled actions. The chapter separates languages from frameworks, explains SQL/Python roles, and follows material handling, model evaluation, retrieval systems and deployment evidence. The architecture sketches are educational examples rather than a reconstruction of a company's internal systems.
