# 펌웨어와 소프트웨어 검증 | Firmware and software validation

[직무 목차](README.md) · [DX 직무표](01-삼성DX의직무와요구역량_samsung-dx-role-map.md) · [제품 회로 검사](04-제품회로와시스템검사_product-circuit-system-tests.md)

로봇의 센서값이 PC 화면에 나타나는 과정에는 센서·통신 장치, 드라이버, OS, 미들웨어와 응용이 있습니다. 어느 층에서 값과 시간을 책임지는지 나누어야 필요한 언어와 검증 방법도 보입니다. 장치 안의 C/C++와 PC의 Python, 서버의 Java가 같은 일을 반복하는 것이 아닙니다.

삼성 DX JD의 직접 연결 위치는 미래로봇추진단 시스템 SW(PDF 7쪽), 네트워크 미들웨어·서버·애플리케이션(PDF 10–12쪽), MX·Samsung Research AI(PDF 8–9쪽), Global CS센터 품질(PDF 14쪽)입니다. 이 글의 구조·시험·실패 예시는 공개 기술을 설명하도록 구성한 것으로, 특정 조직의 내부 구현이나 필수 언어를 추가로 단정하지 않습니다.

## 1. 프로그램이 실행되는 층을 먼저 정합니다

| 층 | 담당하는 일 | 사용하는 지식과 코드의 예 | 여기서 확인할 결과 |
| --- | --- | --- | --- |
| 부팅·보드 지원, BSP | 보드에서 코드가 시작하고 메모리·클록·장치가 준비되게 합니다. | 시작 코드·메모리 배치·보드 설정·부트 상태입니다. | reset 종류·초기 상태·실패 시 복구 경로입니다. |
| 장치 드라이버 | 레지스터·인터럽트·DMA를 OS/응용에서 쓸 수 있는 입출력으로 연결합니다. | C 등으로 장치 자원·주소·버퍼 수명을 다룹니다. | 데이터·길이·순서·오류·중단 후 자원 상태입니다. |
| HAL | 장치별 차이를 정해진 인터페이스 뒤로 감춥니다. | 함수·자료형·상태·오류 계약을 정의합니다. | 장치가 바뀌어도 유지할 의미와 달라질 기능입니다. |
| OS·실시간 실행 | task·메모리·동시성·장치 실행의 자원을 관리합니다. | 우선순위·스케줄링·동기화·시간·메모리입니다. | 주기·지연·기한·교착·자원 고갈입니다. |
| 미들웨어 | 응용 간 통신·공통 라이브러리·자원 접근을 제공합니다. | 직렬화·큐·RPC·이중화·공유 자원입니다. | 메시지 완전성·호환성·타임아웃·재시도 부작용입니다. |
| 응용·서버·AI | 제어·서비스·모델 실행과 사용자 기능을 구현합니다. | C/C++·Java·Python 등으로 각 기능과 운영 경로를 구성합니다. | 기능·부하·권한·정확도·응답 시간·실패 복구입니다. |
| 시험 실행·분석 | 조건을 준비하고 여러 층의 결과를 모아 비교합니다. | Python·SQL·시험 프레임워크·로그 분석 등입니다. | 어떤 입력·판본·환경에서 어떤 판단을 했는지의 기록입니다. |

실제 제품에서는 여러 층이 합쳐지거나 별도 프로세스·칩·서버로 나뉩니다. 예를 들어 Python 시험기가 장치에 명령을 보내더라도, 그 명령을 받아 실제 모터·센서를 제어하는 코드와 시간 책임은 별도입니다.

## 2. C/C++가 필요한 이유를 데이터와 자원의 수명으로 봅니다

C는 고정 폭 정수·배열·포인터 등을 사용하여 하드웨어가 주고받는 바이트와 메모리 구조를 표현할 수 있습니다. C++는 이러한 경계 위에서 자료형·객체·자원 수명·라이브러리 등의 구조를 만들 수 있습니다. 언어 이름만으로 실행 시간이나 메모리 안전성이 자동 보장되지는 않습니다.

| 구체적 작업 | 알아야 할 문법·개념 | 잘못 구현했을 때 생기는 문제 | 시험의 예 |
| --- | --- | --- | --- |
| 수신 프레임에서 길이·값 읽기 | 고정 폭 정수, 비트 연산, endian·정렬·범위 검사입니다. | 짧은 입력을 정상으로 읽거나 부호·순서를 잘못 해석합니다. | 모든 분할 위치·최소/최대 길이·잘못된 길이를 비교합니다. |
| 인터럽트와 task의 자료 전달 | 공유 상태·원자성·임계 구역·큐입니다. | 갱신 유실, 부분 상태 관측, 처리 순서 변경입니다. | 가능한 실행 순서를 나누고 값·개수·순서를 확인합니다. |
| DMA 수신 버퍼 사용 | CPU/장치 주소, 매핑, 소유권, cache 일관성입니다. | 장치가 쓰는 동안 CPU가 읽거나 오래된 데이터를 읽습니다. | 완료·중단·재사용·크기 경계와 CPU/장치 관측을 나눕니다. |
| C++ 객체가 비동기 작업을 소유 | 생성/소멸, 참조 수명, 이동·해제 순서입니다. | callback이 끝난 객체를 사용하거나 자원을 두 번 해제합니다. | 완료 전 취소·종료·오류·재시작을 시험합니다. |
| 통신 라이브러리의 큰 입력 처리 | 버퍼·큐 크기, backpressure, 계산 복잡도입니다. | 입력이 쌓여 메모리·지연이 계속 늘어납니다. | 정상·과부하·느린 소비자와 복구 후 상태를 확인합니다. |

Linux의 DMA 주소는 CPU 가상 주소와 같은 숫자라고 가정할 수 없습니다. 장치가 사용할 수 있는 주소 범위와 플랫폼의 매핑·동기화 API를 따라야 합니다. [Linux Dynamic DMA mapping Guide의 CPU and DMA addresses·Types of DMA mappings](https://docs.kernel.org/core-api/dma-api-howto.html)는 CPU 주소·bus 주소와 coherent/streaming 매핑을 구분합니다. bare-metal MCU의 cache 조작을 Linux 드라이버에 그대로 복사하는 대신 해당 계층의 API를 사용해야 합니다.

`volatile`은 공유 자료를 안전하게 교환하는 lock이나 일반 메모리 barrier를 대신하지 않습니다. [GCC의 Volatiles 설명](https://gcc.gnu.org/onlinedocs/gcc/Volatiles.html)은 volatile 접근과 일반 메모리 쓰기의 순서가 자동으로 묶이지 않는 예를 설명합니다. 원자성·메모리 순서·CPU와 장치 사이의 동기화는 각각 맞는 수단으로 다룹니다.

자세한 오류 경계는 [인터럽트·DMA·MMIO](../분야_topics/17-펌웨어-RTOS_firmware-rtos/해설_notes/CPU와장치가같은데이터를다룰때_mmio-interrupt-dma.md), [Cortex-M7 DMA·캐시](../현장계측과검증_measurement-validation/펌웨어와디버깅_firmware-debugging/DMA버퍼와캐시의경계_cortex-m7-cache-dma.md), [UART 분할 수신](../설계와검증사례_engineering-cases/UART의분할수신과재동기화_uart-stream-resync.md)에서 이어집니다.

## 3. 실시간은 빠른 평균보다 기한의 문제입니다

제어 주기, period는 작업을 반복하는 간격이고 deadline은 결과가 유효해야 하는 마지막 시점입니다. latency는 입력·사건에서 반응까지의 지연이며 jitter는 반복 시점이나 지연의 흔들림입니다. 실행 시간이 짧아도 큐 대기·인터럽트·잠금·메모리·장치 통신 때문에 기한을 넘을 수 있습니다.

예를 들어 1 ms 주기의 제어기를 가정하고, 입력 수집에서 출력 반영까지 800 µs 이내라는 별도 기한을 정할 수 있습니다. 계산 자체가 200 µs여도 큐에서 700 µs 기다리면 합계 900 µs가 되어 이 가정의 기한을 넘습니다. 이 숫자는 교육용이며 실제 로봇의 주기나 사양이 아닙니다.

| 기록할 시간 | 알아내려는 것 |
| --- | --- |
| 센서의 실제 취득 시각 | 값이 언제의 물리 상태를 나타내는지입니다. |
| 장치 수신·callback 시각 | 전송·인터럽트·드라이버 지연입니다. |
| 제어 task 시작·종료 | 대기와 계산 시간을 분리합니다. |
| 출력 전달·장치 적용 시각 | 통신과 실제 반영까지 포함한 종단 지연입니다. |
| 기한 초과·값 폐기·누락 수 | 늦은 정상값과 유효한 제어값을 구분합니다. |

Linux PREEMPT_RT는 선점·잠금·인터럽트 실행 방식 등을 다루는 커널 구성이며, 하드웨어·메모리·버스·펌웨어의 조건도 관련됩니다. [Linux Real-time preemption 문서의 Scheduling·Priority inheritance·Considering hardware](https://docs.kernel.org/core-api/real-time/index.html)를 출발점으로 읽을 수 있습니다. 설정 이름만 확인하기보다 목표 보드·부하에서 지연 분포와 기한 초과를 측정해야 합니다.

ROS2 같은 통신·실행 환경을 활용해도 메시지가 최신인지, 어느 시간에 취득했는지, 큐가 밀렸을 때 무엇을 버릴지는 설계해야 합니다. JD의 ROS2 경험은 이런 로봇 시스템의 연결을 이해하는 데 이어집니다. 분산된 장치의 시각을 비교할 때에는 시계 기준과 동기화 오차도 남깁니다.

## 4. 미들웨어 검증: 메시지와 작업 완료를 구분합니다

직렬화는 구조화된 값을 전송·저장할 바이트 표현으로 바꾸는 일입니다. Protobuf 같은 메시지 정의, gRPC 같은 원격 호출, 큐·라이브러리·서비스 이중화가 연결될 수 있습니다. 중요한 것은 ‘받았다’가 정확히 무엇을 뜻하는지 정하는 것입니다.

| 경계 | 잘못 가정하기 쉬운 내용 | 확인할 시험 |
| --- | --- | --- |
| 입력→파서 | 한 번 읽은 바이트가 항상 메시지 하나입니다. | 분할·합쳐진 수신, 잘못된 길이, 지원하지 않는 판본입니다. |
| 메시지→작업 | 수신 성공이면 작업도 끝났습니다. | 접수·실행 시작·완료·실패를 별도 상태로 관측합니다. |
| 응답→재시도 | 응답이 없으면 서버도 아무 일도 하지 않았습니다. | 서버 적용 후 응답 유실, 재시도와 중복 부작용을 확인합니다. |
| 서버 전환 | 다른 서버가 같은 상태를 즉시 가지고 있습니다. | 진행 중 요청·저장 상태·중복 처리·순서의 전환 결과입니다. |
| 느린 소비자 | 큐를 계속 늘리면 처리량 문제가 해결됩니다. | 큐 길이·메모리·지연·입력 제한과 정상 복구입니다. |

gRPC deadline은 클라이언트가 어느 시점까지 응답을 기다릴지를 정합니다. 기본적으로 deadline이 없을 수 있으므로 목표 지연·부하를 바탕으로 설정하고 검증합니다. 클라이언트의 기한 초과를 이미 실행된 부작용의 롤백과 동일하게 취급하지 않습니다. [gRPC Deadlines의 Client·Server·Cancellation 설명](https://grpc.io/docs/guides/deadlines/), [Retry 설명](https://grpc.io/docs/guides/retry/)에서 대기·취소·재시도의 역할을 읽을 수 있습니다.

### 교육용 사례: 명령은 적용됐지만 응답이 사라집니다

설정값을 한 번 올리는 요청이 서버에서 적용된 직후 응답만 유실되었다고 가정합니다. 클라이언트가 같은 의미의 요청을 새 작업으로 다시 보내면 값이 두 번 바뀔 수 있습니다. 반대로 현재 상태를 특정 값으로 설정하는 연산이라도 부가 알림·이력 등 다른 부작용이 있다면 그 의미까지 정의해야 합니다.

검증에서는 요청 ID·입력·적용 상태·응답을 함께 기록하고, 중복 요청·늦은 응답·재시작 뒤 같은 요청이 들어오는 조건을 비교합니다. 해결 방향은 요청의 멱등성, 중복 식별·보관 기간, 상태 저장과 결과 재전달의 계약을 정하는 것입니다. 이는 회사의 실제 서버 장애 기록이 아닌 일반적인 분산 처리 예입니다. [시간초과 뒤 늦은 쓰기](../설계와검증사례_engineering-cases/시간초과뒤늦은쓰기와재시도_block-io-timeout-retry.md), [HTTP API 계약](../분야_topics/52-Web-API응용_web-api-applications/해설_notes/HTTPAPI의계약_http-idempotency-pagination-validation.md)에서 더 구체적인 경계를 봅니다.

## 5. 서버·컨테이너 검증: 프로세스가 떠 있다고 서비스가 준비된 것은 아닙니다

컨테이너는 응용과 실행 의존성을 묶어 배포하는 단위이며, Kubernetes는 Pod 등 자원의 배치·상태·재시작·서비스 연결을 관리합니다. JD의 Cloud Native·Kubernetes 경험은 배포 도구 조작뿐 아니라 이 과정의 실패와 복구를 이해하는 일로 이어집니다.

| 검사 신호 | 확인하는 목적 | 잘못 결합했을 때의 문제 |
| --- | --- | --- |
| startup probe | 초기 준비가 끝날 때까지 시간을 줍니다. | 초기화가 느린 정상 프로세스를 반복 종료할 수 있습니다. |
| liveness probe | 재시작이 필요한 실행 불능 상태를 찾습니다. | 단순한 외부 의존성 지연에 반응해 불필요한 재시작이 늘 수 있습니다. |
| readiness probe | 지금 서비스 요청을 받을 준비가 되었는지 봅니다. | 실행만 된 인스턴스로 요청이 가서 실패할 수 있습니다. |

[Kubernetes의 공식 probe 설명](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)에서 startup·liveness·readiness의 역할을 구분합니다. readiness 실패는 서비스 트래픽 대상에서 빠지는 판단이며, 그 신호 자체가 컨테이너 재시작을 뜻하지 않습니다.

서버 시험에서는 정상 부하뿐 아니라 DB 지연, 연결 끊김, 의존 서비스 오류, 재배포·종료 중 요청, 비정상 큰 입력을 정합니다. 결과로 처리량·상위 지연·오류율·메모리·큐 길이와 데이터 일관성을 함께 남깁니다. 평균 응답 시간이 낮아도 일부 요청이 매우 늦거나 상태가 중복 적용되면 다른 문제입니다.

## 6. 단위 시험에서 실기기 시험까지 근거가 달라집니다

| 시험 수준 | 구체적 대상 | 좋은 실패 입력의 예 | 그 수준에서 확인하지 못하는 부분 |
| --- | --- | --- | --- |
| 정적 분석·컴파일 진단 | 실행 전 코드의 규칙·경로·자료형 문제입니다. | 범위·수명·변환·해제의 의심 경로입니다. | 실제 입력과 장치의 모든 동작은 실행하지 않습니다. |
| 단위 시험 | 파서·상태 전이·계산 등 작은 경계입니다. | 최소 길이·범위 끝·중복·잘못된 순서입니다. | 실제 장치·네트워크·타이밍은 대신하지 않습니다. |
| host 실행·sanitizer | 실행 중 메모리·정의되지 않은 연산의 일부를 찾습니다. | 해제 후 사용·범위 밖 접근·잘못된 shift 등입니다. | 실행하지 않은 경로와 실기기 동시성·전기 상태는 남습니다. |
| 통합·모의 장치 | 드라이버·통신·서비스 사이의 계약입니다. | 지연·부분 완료·취소·오류 응답입니다. | 모델에서 생략한 장치 동작·물리 제약이 남습니다. |
| 실기기·HIL | 실제 보드/제어기를 다른 실제 또는 모의 환경과 연결합니다. | 정의한 환경·부하·결함 조건입니다. | 수행하지 않은 조건 전체를 보증하지 않습니다. |
| 시스템·회귀 | 제품 기능·성능·호환성과 변경 영향을 봅니다. | 이전 실패 입력과 의존 기능 조합입니다. | 시험 범위 밖의 동작은 별도 근거가 필요합니다. |

ASan은 범위 밖 접근·해제 후 사용 등 메모리 오류를 실행 중 찾고, UBSan은 잘못된 shift·signed overflow·정렬 등 정의되지 않은 연산의 일부를 찾습니다. [Clang AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html), [UndefinedBehaviorSanitizer](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html)의 검출 범위와 실행 옵션을 따릅니다. 경고가 없다는 사실만으로 모든 코드 경로나 하드웨어 타이밍이 정상이라는 결론은 나오지 않습니다.

Android 품질 검증에서도 host와 DUT, device under test의 역할이 다릅니다. [AOSP VTS 문서](https://source.android.com/docs/core/tests/vts)는 호스트의 Trade Federation이 실행을 관리하고 C++ GTest와 kernel 시험은 기기에서 실행되는 구성을 설명합니다. Java JUnit 계열에는 호스트에서 기기 shell 명령을 실행하는 시험도 있습니다. 이는 ‘C++와 Java로 어떤 검사를 만드나요’에 대한 공개된 구체적 예이며 삼성 내부에서 특정 시험을 그대로 사용한다는 단정은 아닙니다.

## 7. AI 기능은 모델 출력과 제품 행동을 함께 검증합니다

MX AI JD는 단말·서버·Agent·RAG·sLLM 등을, Samsung Research JD는 생성형·멀티모달·VLM/VLA·경량화 등을 다룹니다. VLM은 시각과 언어를 함께 다루는 모델, VLA는 시각·언어와 행동 출력을 연결하는 접근입니다. 제품에 넣으려면 출력 정확도뿐 아니라 실행 위치·시간·메모리·권한·실패 대응을 평가해야 합니다.

| 검증 대상 | 고정할 입력·조건 | 확인할 결과 |
| --- | --- | --- |
| 모델 기본 기능 | 데이터·정답 기준·전처리·모델 판본입니다. | 과제별 성능과 실패 유형·집단별 분포입니다. |
| RAG 검색·응답 | 문서 판본·접근 권한·검색 설정입니다. | 올바른 근거를 찾았는지, 응답이 근거와 맞는지입니다. |
| Agent 도구 실행 | 허용 도구·인자·상태·중단 조건입니다. | 의도한 작업·부작용·중복·복구와 권한 경계입니다. |
| 단말 최적화 | 하드웨어·연산 정밀도·입력 크기·warm-up·동시 부하입니다. | 지연·메모리·전력과 최적화 전후 기능 차이입니다. |
| 사용자 기능 통합 | 네트워크·입력 오류·취소·백그라운드 전환입니다. | 오류 표시·fallback·응답 시간과 제품 상태입니다. |

위 표는 JD의 키워드를 평가 항목으로 연결한 학습용 정리입니다. 회사 모델의 구조·데이터·성능은 추정하지 않습니다. 상세한 평가 원리는 [AI 응용·에이전트 평가](../분야_topics/46-AI응용에이전트평가_ai-agents-evaluation/README.md), [RAG와 도구 실행](../분야_topics/46-AI응용에이전트평가_ai-agents-evaluation/해설_notes/RAG와도구실행_retrieval-tools-and-evaluation.md), [데이터 분할·재현성](../분야_topics/03-python-jupyter/해설_notes/데이터와분할재현성_data-split-reproducibility.md)에서 이어집니다.

## 8. 언어 경험을 설명할 때 필요한 구체성

‘C++ 사용’보다 ‘비동기 수신 객체가 취소된 뒤 callback이 참조하는 수명을 정의하고 중단·재시작 입력을 시험했습니다’가 다루는 문제를 드러냅니다. ‘Python 자동화’도 어느 장치·API를 제어했고 응답 누락·잘못된 단위·재시도·정리 상태를 어떻게 처리했는지 설명해야 합니다. 실제 수행한 범위와 모의 환경에서만 확인한 범위를 구분합니다.

| 언어·도구 경험 | 함께 제시할 수 있는 산출물 |
| --- | --- |
| C 드라이버·펌웨어 | 인터페이스 계약·장치 상태·버퍼 수명·시험 입력·관측 로그입니다. |
| C++ 통신·시스템 | 자료형·객체 소유권·동시성 설계와 실패 입력입니다. |
| Java 서버 | API·트랜잭션·동시 요청·오류 복구와 부하 결과입니다. |
| Python 시험·분석 | 실행 설정·원시 결과·오류 처리·판정·분석 재현 방법입니다. |
| SQL 데이터 분석 | 스키마·join 키·기간·중복/누락 처리와 지표의 분모입니다. |
| CI/CD | 어떤 변경에 어떤 검사를 실행하고 실패를 어떻게 보존·차단했는지입니다. |

CI/CD는 검사·빌드·배포 경로를 자동으로 연결하는 방식입니다. 검사 개수를 늘리는 것보다 요구사항·오류 경계·변경 영향에 맞는 근거를 남기는 일이 중요합니다. 실제 저장소 예시는 [실무 검증 코드](../예제_examples/실무검증_practical-validation/README.md), [임베디드 검증 프로젝트](../프로젝트_projects/embedded-validation-lab/README.md), [소프트웨어 설계·품질](../분야_topics/48-소프트웨어설계품질_software-quality/README.md)에서 읽으실 수 있습니다.

## 출처와 확인 범위

| 근거 | 읽은 범위 |
| --- | --- |
| 삼성 DX 2026년 상반기 JD | PDF 7–12·14쪽의 담당 업무·요건·우대입니다. 8–9쪽은 특정 언어보다 AI 기술·프레임워크를 명시합니다. |
| [Linux DMA mapping Guide](https://docs.kernel.org/core-api/dma-api-howto.html) | CPU/DMA 주소, coherent·streaming 구분과 동기화·소유권의 역할입니다. |
| [GCC Volatiles](https://gcc.gnu.org/onlinedocs/gcc/Volatiles.html) | volatile과 일반 메모리 순서의 차이입니다. 예시 barrier를 모든 플랫폼의 장치 동기화 해법으로 전용하지 않았습니다. |
| [Linux Real-time preemption](https://docs.kernel.org/core-api/real-time/index.html) | scheduling·priority inheritance·threaded interrupt·하드웨어 고려 사항의 공식 문서 구조를 확인했습니다. 특정 보드의 지연 보장을 제시하지 않았습니다. |
| [gRPC Deadlines](https://grpc.io/docs/guides/deadlines/) · [Retry](https://grpc.io/docs/guides/retry/) | 기한·취소·재시도 정책의 역할입니다. 자체 중복 적용 예는 이 문서의 실제 장애 보고가 아닙니다. |
| [Kubernetes probe 설명](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/) | startup·liveness·readiness의 목적과 서비스 트래픽·재시작 구분입니다. |
| [Clang ASan](https://clang.llvm.org/docs/AddressSanitizer.html) · [UBSan](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html) | Introduction·검출 범위·옵션을 확인했습니다. 이 글에서 실제 대상 펌웨어에 sanitizer를 실행한 결과는 아닙니다. |
| [AOSP VTS](https://source.android.com/docs/core/tests/vts) | host/DUT 구분과 GTest·kernel·JUnit 계열 시험 설명입니다. |

확인일은 2026-10-26입니다. 시간 계산과 실패 시나리오는 직접 구성한 교육용 예입니다. 공개 구현의 실제 실행 기록은 연결한 프로젝트의 해당 기록에서 구분해 확인하실 수 있습니다.

## English

The note follows board support, drivers, HALs, real-time execution, middleware and application services. It explains why C/C++ memory and resource ownership matter, why Python test orchestration is separate, and how Java services, RPCs, container probes and AI features require their own contracts. Concrete test inputs distinguish parsing, cancellation, retries, deadlines, readiness and staged hardware validation. Educational examples are not reports of internal company implementations or measured device results.
