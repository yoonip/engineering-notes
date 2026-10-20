# 차량·설비 통신의 고장 분리 / Diagnosing CAN, EtherCAT and Modbus TCP

기준일은 2026-10-21입니다. 케이블·설정·메시지·응용 프로그램의 고장을 구별하도록 공식 문서와 자체 오프라인 trace를 비교합니다. 예의 주소·값은 교육용이며 실제 차량·설비의 수집·제어 기록이 아닙니다.

## 어느 단계의 성공인지 표시합니다

다음 구분은 진단을 위한 묶음이며 세 프로토콜을 동일한 OSI 계층 구조로 정의한 표가 아닙니다.

| 단계 | 확인할 증거 | 그것만으로 확정하지 못하는 것 |
|---|---|---|
| 물리선·전기 | 연결 구성, 차동 파형, 종단·접촉·공통 기준, 해당 PHY 상태입니다. | 프레임의 내용과 응용의 수신입니다. |
| 링크·전송 | CAN 오류·ACK, Ethernet link·frame 오류, TCP 연결·재전송입니다. | 응용의 명령 처리와 최신 데이터입니다. |
| 프로토콜 | ID·형식·길이, EtherCAT datagram·WKC, Modbus transaction·function·exception입니다. | 센서 단위·제어 상태·처리 부작용입니다. |
| 애플리케이션 | register map·단위·byte/word 순서, 값의 시각·유효성, 요청 처리 상태입니다. | 실제 기계 동작이나 센서 자체의 정확도입니다. |

Link LED가 켜져도 응용 값은 오래된 cache일 수 있습니다. CAN ACK·TCP ACK와 작업 완료 응답을 구별합니다.

## CAN과 CAN FD: 형식·bit timing·물리선을 나눕니다

CAN의 식별자는 일반적인 점대점 수신 주소와 다르며 여러 노드가 메시지를 관찰할 수 있습니다. Classical CAN의 데이터는 최대 8byte, CAN FD는 최대 64byte입니다. FD는 프레임의 데이터 구간에서 다른 bit rate를 사용할 수 있습니다. FD라고 항상 더 빠르게 전송되는 것은 아닙니다. [Bosch CAN Protocols](https://www.bosch-semiconductors.com/products/ip-modules/can-protocols/)

Nominal/data bit rate, bit rate switch, sample point 등 decoder·controller 설정을 남깁니다. Nominal rate만 맞아도 FD 구간 설정이 다르면 해석이 실패할 수 있습니다. 초기 non-ISO FD와 ISO FD도 구분합니다. Bosch M_CAN은 ISO 11898-1:2015 지원과 별도 transceiver 필요를 명시합니다.

고속 차동 CAN의 기준 구성은 선로 양 끝을 특성 임피던스에 맞게 종단합니다. [TI SLOA101B](https://www.ti.com/lit/an/sloa101b/sloa101b.pdf) §5는 120Ω 두 개의 예를 제시합니다. 자체 모형에서 다른 경로 없이 병렬인 두 120Ω은 `120||120=60Ω`입니다. 실제 측정에는 다른 회로·접점도 들어가므로 60Ω만으로 모든 배선을 합격 판정하지 않습니다.

ACK error는 송신자가 확인을 받지 못했다는 단서입니다. 상대 부재·설정 불일치·신호 문제를 나누며 배선 불량으로 단정하지 않습니다. Arbitration에서 우선권을 내준 것과 프레임 오류도 다릅니다. ACK가 있어도 특정 ECU의 응용이 값을 채택했다는 확인은 아닙니다.

## 오류 counter는 시각과 상태를 함께 봅니다

TEC·REC는 송신·수신 오류 counter입니다. 증가 양상·오류 종류·error passive·bus-off 상태를 같은 시점에 연결합니다. 재시작 뒤 0이라는 기록이 이전 오류를 지우지는 않으며 counter만으로 물리적 원인을 지목할 수는 없습니다.

[Bosch M_CAN User's Manual Rev. 3.3.1](https://www.bosch-semiconductors.com/media/ip_modules/pdf_2/m_can/mcan_users_manual_v331.pdf)의 §2.3.13~14는 counter와 protocol status를 나눕니다. 이 구현의 REC 값과 passive 표시는 별도 필드입니다. 일부 오류 누적 필드는 읽는 접근으로 지워지는 특성이 있으므로 진단 자료에도 읽은 순서와 도구를 남겨야 합니다. 한 controller의 register 배치를 모든 CAN 칩에 그대로 적용하지 않습니다.

ACK error의 반복과 bus-off는 별도로 관측합니다. 오류마다 TEC에 일정 값을 더해 만든 간단한 계산을 controller의 전체 error confinement 동작으로 제시하지 않습니다. Payload의 byte 순서보다 controller·decoder 설정, 상대 상태와 원시 파형을 먼저 대조할 상황도 있으며, counter나 오류 이름 하나로 특정 선의 단선을 확정하지 않습니다.

## CAN 재시작은 요청·활성 확인·응용 회복을 나눕니다

[실행 가능한 정책 예제](../../예제_examples/실무검증_practical-validation/can/README.md)는 25개 합성 controller 관측을 읽습니다. 실제 controller 레지스터·CAN bit stream을 재현하지 않으며, bus-off가 관측된 다음 호스트가 무엇을 허용할지 검사하는 모형입니다. READY 초기 상태, 100 ms 대기, 직전 1,000 ms에 최대 요청 2개라는 조건을 직접 정했습니다.

40 ms에 bus-off, 50 ms에 정책 확인, 140 ms에 재시작 요청, 150 ms에 활성 확인이 있다고 가정합니다. 잘못된 경로는 첫 확인인 50 ms에 즉시 재시작을 요청하고 READY로 간주해 141 ms의 송신을 허용합니다. 수정 경로는 40+100=140 ms 전까지 기다리고, 요청 후에는 WAIT_ACTIVE로 남아 141 ms를 차단합니다. 150 ms의 활성 관측 후에야 송신을 허용합니다. 요청 중 bus-off 상태가 다시 보이는 것은 같은 미복구 회차로 취급합니다.

Linux 6.14의 [SocketCAN 재시작 설명](https://docs.kernel.org/6.14/networking/can.html#starting-and-stopping-the-can-network-device)은 `restart-ms`와 응용 주도 재시작을 구분합니다. 위 모형의 횟수 제한과 확인 정책이 Linux 기능의 내부 구현이라는 뜻은 아닙니다. 실제 bus-off 복구에는 controller와 드라이버의 조건도 있으므로 호스트 timer만으로 물리 복구를 완료했다고 판단하지 않습니다.

합성 요청 시각이 140·300 ms이면 500 ms에는 두 요청이 모두 창 안에 있어 새 요청을 보류합니다. 1,140 ms에는 첫 요청의 나이가 정확히 1,000 ms여서 창에서 빠지고 다음 요청을 낼 수 있습니다. 경계에서 `<1000`인지 `<=1000`인지도 기록해야 재현할 수 있습니다. [ACK와 복구 사례](../../설계와검증사례_engineering-cases/CAN의ACK와복구정책_can-recovery-policy.md)는 이 중간 상태와 기대 action을 비교합니다.

## 프레임이 와도 값의 계약은 따로 검사합니다

[수신 계약 사례](../../설계와검증사례_engineering-cases/CAN수신값의형식과신선도_can-payload-contract.md)는 표준 ID 0x321·Classical data·8바이트라는 자체 형식을 사용합니다. ID 숫자뿐 아니라 확장 여부·remote·FD·오류 사건, 길이, 형식 버전, little-endian mV, 순번과 나이를 확인합니다. `34 12`의 알려진 패턴은 4,660 mV이고 반대 순서는 13,330 mV입니다. 범위 안에 들어가는 잘못된 값도 있을 수 있어 알려진 패턴 검사와 범위 검사를 나눕니다.

핵심은 거부할 입력으로 마지막 유효 상태를 바꾸지 않는 것입니다. 마지막 순번 254 뒤에 오래된 255가 오면 거부하고 254를 유지해야, 뒤의 정상 255를 채택할 수 있습니다. 먼저 순번을 저장한 잘못된 경로는 앞을 STALE로 거부하면서도 뒤를 DUPLICATE로 거부합니다.

시간 예제는 샘플·수집·사용 시각이 동일한 32비트 ms 시계라는 가정입니다. 생성 240·수집 250·사용 341 ms이면 수신 시점 나이 10 ms와 사용 시점 나이 101 ms가 다릅니다. 생성 105·수집 100·사용 110 ms는 나이가 짧아도 시간 순서가 잘못돼 거부합니다. 시계가 다른 장치의 송신 시각과 호스트 수신 시각을 그냥 빼지 않습니다. 동기화가 없다면 수신 측의 마지막 유효 수신 timeout 등 다른 계약을 정합니다.

로컬 실행은 응용 레코드 24개에서 채택 6·거부 18을 확인했고, 잘못된 형식 입력 12개는 별도 `InputError`였습니다. 이 수는 실제 통신 성공률이 아닙니다. 엄격한 연속 순번이므로 실제 유실 뒤 자동 재동기화는 제공하지 않습니다. [검증 기록](../../설계와검증사례_engineering-cases/검증기록_evidence/CAN정책과수신계약검증_20261021.md)은 실행 환경·입력·소스 해시·의도적인 결함·남은 범위를 연결합니다.

현장의 진단은 다음 순서로 기록할 수 있습니다. 먼저 시각·관측 노드·bit timing·원시 오류와 controller 상태를 보존합니다. 다음으로 반복 송신 실패와 bus-off·복구 요청·활성 관측을 나눕니다. 정상 데이터가 도착하면 ID·형식·길이·map을 대조하고, 마지막으로 값·순번·신선도와 응용 처리 확인을 봅니다. 어느 단계에서 막혔는지 적어야 물리 문제를 응용 파서 수정으로 덮거나, 바이트 순서 문제를 전원 재시작으로 숨기지 않습니다.

## EtherCAT: 연결·datagram 처리·데이터 유효성을 나눕니다

EtherCAT의 순환 프레임은 일반적인 TCP 요청·응답과 구별합니다. Ethernet 프레임 안의 Working Counter인 WKC는 datagram 처리의 단서입니다. 기대값은 command·주소·접근 조건에 따라 정하며 연결 장치 수와 항상 같지는 않습니다.

[EtherCAT Technology Group의 §1.6](https://www.ethercat.org/en/technology.html)은 WKC와 노드별 오류·link 상태를 함께 봅니다. 자체 trace B에서 link는 유지되지만 기대 WKC 6에 관측 4라면 그 주기의 정상 갱신 근거가 부족합니다. ‘차이가 2이니 두 노드 고장’은 기여 규칙을 생략한 결론입니다.

[Beckhoff의 Additional Diagnostic information](https://infosys.beckhoff.com/content/1033/tcsystemmanager/1089009035.html)은 하나의 command가 여러 장치를 다루면 관련 장치의 WcState가 함께 invalid로 표시될 수 있음을 설명합니다. 표시된 장치 전부가 물리적으로 고장 났다는 뜻은 아닙니다. 실제·설정 topology, 장치 상태와 status code, node별 오류, 해당 datagram을 함께 비교합니다.

Distributed Clocks는 장치의 시간 기준을 맞춥니다. Link·WKC가 정상이어도 동기·샘플 시각·값의 최신성·센서 교정은 따로 확인합니다.

## Modbus TCP: 연결 성공과 예외 응답을 구별합니다

[Modbus Application Protocol V1.1b3](https://www.modbus.org/file/secure/modbusprotocolspecification.pdf)는 function·데이터 모델을, [TCP 가이드 V1.0b](https://www.modbus.org/file/secure/messagingimplementationguide.pdf)는 MBAP·transaction·timeout을 설명합니다. Transaction Identifier는 같은 TCP 연결의 요청·응답을 짝짓습니다. Protocol Identifier·Length·Unit Identifier·function도 대조합니다. TCP stream의 packet 하나가 항상 Modbus 메시지 하나는 아닙니다.

자체 trace C의 읽기 요청은 TID=0x002A·function=0x03입니다. 같은 TID의 응답 PDU `83 02`는 정상 register 값이 아닌 예외 응답이며 code 02는 Illegal Data Address입니다. 서버까지 요청·응답 경로가 있었다는 증거이므로 function·시작 주소·개수·map 버전을 대조합니다. 무응답과 같은 사건이 아닙니다.

문서의 register 번호와 PDU의 0부터 시작하는 주소가 어떻게 대응하는지 확인합니다. Register 한 개는 16bit이고 높은 byte부터 전송합니다. 32bit의 word 순서·signed 여부·float 해석·scale은 장치의 map이 필요합니다.

자체 register `0x1234`, `0x5678`을 첫 word가 상위라고 합치면 `0x12345678=305419896`, 반대는 `0x56781234=1450709556`입니다. 전송 오류가 없어도 응용 값은 달라집니다. 알려진 시험값·map·도구의 해석을 비교하며 그럴듯한 값 하나로 순서를 확정하지 않습니다.

## Timeout과 재시도에는 처리 상태가 남습니다

Modbus TCP 가이드 §4.4.1.4는 공통 필수 응답 시간을 정하지 않습니다. 자체 예의 100ms timeout은 사용자가 정한 조건입니다. 처리 시간·대기열·지연·수집 손실·응답 짝짓기를 구별합니다. 늦은 응답을 새 요청과 잘못 연결하면 값의 순서도 바뀝니다.

Timeout은 작업이 실행되지 않았다는 증명이 아닙니다. TCP 내부의 재전송과 응용이 새 요청을 보내는 재시도는 다릅니다. 읽기에도 읽으면 지워지는 register가 있을 수 있고, 쓰기는 같은 값을 다시 넣어도 장치가 이벤트로 해석할 수 있습니다. 요청의 반복 가능성·중복 검출·응용 처리 확인 정책을 map과 장치 문서로 정해야 합니다. 연결을 다시 맺었다는 사실이 이전 작업을 취소하지는 않습니다.

## 오프라인 판정 기록을 남깁니다

분석 자료에는 raw capture와 decoder 버전·설정, 시각 단위·clock 기준, 관측 위치·방향, 필터·누락 통계, firmware·map 버전을 함께 둡니다. CAN은 ID 형식·FD/BRS·counter·오류 상태, EtherCAT은 cycle·datagram·기대/관측 WKC·장치 상태, Modbus는 TCP 연결·TID·function·주소·응답을 연결합니다.

결론은 ‘현상→가능한 원인→남은 대안→필요한 증거’로 적습니다. A의 ACK error, B의 WKC 불일치, C의 주소 예외를 통신 불량 하나로 집계하면 서로 다른 진단 단계가 사라집니다.

## 확인 문제

1. CAN ACK나 TCP ACK가 있으면 응용의 작업 완료까지 확인됩니까?
2. 기대 WKC 6에 관측 4이면 두 장치의 물리 고장이라고 확정할 수 있습니까?
3. Modbus 읽기 응답 `83 02`와 timeout은 같은 증거입니까?

<details>
<summary>답과 이유</summary>

1. 아닙니다. 링크·전송 확인과 응용의 처리·데이터 채택은 별도입니다.
2. 확정할 수 없습니다. Command의 기여 규칙·상태·주소를 확인해야 하고 여러 장치에 invalid가 함께 표시될 수도 있습니다.
3. 아닙니다. 앞은 주소 관련 예외 응답을 받은 것이고 뒤는 정한 시간 안에 응답을 확인하지 못한 것입니다. Timeout만으로 미실행을 단정할 수 없습니다.

</details>

## English summary

Separate physical signals, transport, protocol processing and application meaning. CAN acknowledgments, EtherCAT working counters and Modbus replies prove different things. The linked software fixtures check 25 controller observations and 24 application records without modeling physical CAN or error confinement. Recovery requests, observed active state, and application completion remain separate. Preserve raw traces and settings, and treat timeouts as uncertain completion rather than automatic permission to repeat a command.

## 원자료와 읽은 범위

2026-10-21에 Bosch CAN Protocols·M_CAN 제품 본문, M_CAN Rev. 3.3.1(문서 표기 11.03.2023) §2.3.13~14, TI SLOA101B Rev. B(2016-05) §5를 확인했습니다. CAN FD 형식과 bit timing은 Bosch Florian Hartwich의 [Bit Time Requirements for CAN FD](https://www.bosch-semiconductors.com/media/ip_modules/pdf_2/papers/icc14_2013_paper_hartwich_1.pdf), iCC 2013의 관련 설명도 대조했습니다. 초기 논문의 수치를 최신 모든 controller의 사양으로 옮기지 않습니다.

추가한 CAN 실행 사례는 Linux 6.14 SocketCAN의 frame 구조·byte order·filter·오류 보고·상태·재시작 설명과 M_CAN의 ECR·PSR 절을 같은 날 다시 읽고 대조했습니다. Linux API나 실제 CAN 장비를 실행한 결과로 쓰지 않았습니다. 코드·입력·판정은 링크한 자체 소프트웨어 자료입니다.

Modbus는 V1.1b3(2012-04-26) §4.2~4.4·§6.3·§7, TCP 가이드 V1.0b(2006-10-24) §3.1.3·§4.4.1을 읽었습니다. ETG §1.5~1.6은 검색 도구가 반환한 본문을 사용했고 원페이지 직접 접근은 제한됐습니다. Beckhoff 진단 본문은 직접 열람했습니다. 예의 trace·저항망·word 계산은 자체 자료이며 실차·현장망의 실측은 아닙니다.

[함께 읽기: 조건별 오동작과 수율](조건별오동작과수율의경계_pvt-shmoo-characterization.md)
