# CAN의 ACK와 복구 정책 / CAN acknowledgment evidence and restart policy

송신 함수를 호출한 직후 완료 건수를 올리거나, 재시작 요청이 반환됐다는 이유로 송신을 다시 허용하면 실제 상태와 응용 기록이 어긋날 수 있습니다. 이 사례는 합성 controller 관측을 순서대로 읽으며 요청·전송·응용 완료와 bus-off 복구 정책을 구분합니다. 실제 ECU의 장애나 CAN 물리층 시험이 아니라, 의도적인 오류를 넣은 결정적 소프트웨어 예제입니다.

[실행 코드](../예제_examples/실무검증_practical-validation/can/run_cases.py), [합성 controller trace](../예제_examples/실무검증_practical-validation/can/controller_trace.json), [실행 안내](../예제_examples/실무검증_practical-validation/can/README.md), [검증 기록](검증기록_evidence/CAN정책과수신계약검증_20261021.md)을 연결합니다.

## 1. 관측을 같은 성공으로 합치지 않습니다

| 사건 | 예제에서 확인한 범위 | 확인하지 못한 내용 |
| --- | --- | --- |
| `tx_queued` | 송신 요청을 대기열에 넣은 관측입니다. | 버스 전송, ACK, 응용 처리 완료입니다. |
| `ack_error` | 송신 측이 확인을 받지 못했다는 관측입니다. | 특정 선의 단선, 상대 응용의 처리 상태입니다. |
| `tx_complete` | controller의 링크 전송 완료 관측입니다. | 특정 수신 응용이 값을 채택하고 작업을 끝낸 사실입니다. |
| `bus_off` | controller가 bus-off라는 관측입니다. | 물리적 원인과 복구 완료 시점입니다. |
| `controller_active` | 모델에 입력한 활성 상태 관측입니다. | 이후 모든 응용 통신의 정상 동작입니다. |

ACK error는 배선 문제의 단서일 수 있지만 상대 노드 부재, 설정 불일치 등 대안이 있습니다. ACK가 있더라도 특정 응용의 처리 완료까지 입증하지 않습니다. 실제 송신 API의 반환 의미·송신 완료 이벤트·local echo도 사용한 드라이버 문서에 맞춰 구분해야 합니다. 이 코드의 사건 이름은 SocketCAN API를 직접 실행해 받은 구조체가 아닙니다.

Bosch M_CAN Rev.3.3.1의 PSR.LEC는 AckError와 Bus_Off 상태를 별도로 설명합니다. 이 사례는 그 의미를 참고하지만 레지스터를 읽거나 TEC·REC를 계산하지 않습니다. ACK 오류마다 TEC에 8을 더해 bus-off까지 가는 단순 모형은 error confinement 전체와 같지 않으므로 구현하지 않았습니다. [M_CAN 매뉴얼, §2.3.13~14](https://www.bosch-semiconductors.com/media/ip_modules/pdf_2/m_can/mcan_users_manual_v331.pdf)

## 2. 의도적으로 잘못 만든 경로

`faulty_recovery`는 bus-off 후 첫 `tick`에서 바로 재시작을 요청하고 정책 상태를 READY로 바꿉니다. 여기서 `tick`은 호스트가 정책을 다시 살펴보는 합성 시점입니다. 실제 인터럽트나 실시간 스케줄러를 실행하지 않습니다.

```python
elif event['kind'] == 'tick' and phase == 'BUS_OFF':  # elif는 앞 조건이 거짓일 때의 추가 분기입니다.
    phase = 'READY'  # 잘못된 경로: 요청만 한 상태를 활성 확인으로 취급합니다.
    rows.append({'time_ms': event['time_ms'], 'action': 'REQUEST_RESTART'})  # 사전을 목록 끝에 추가합니다.
```

합성 trace의 bus-off는 40 ms입니다. 잘못된 경로는 50 ms에 재시작을 요청하고, 활성 확인은 150 ms인데 141 ms의 송신을 허용합니다. 50 ms와 141 ms는 오류가 드러나는 독립적인 관측점입니다. 단순히 마지막 상태가 READY인지 확인하는 테스트로는 이 중간 위반을 놓칩니다.

또 다른 대조값은 `tx_queued`를 완료로 세는 방식입니다. 입력에는 요청 1개, ACK error 2개, 링크 전송 완료 1개가 있지만 응용 완료 응답은 없습니다. 따라서 응용 완료 확인 건수는 0입니다. 요청을 세는 잘못된 방식에서는 1이 됩니다. “실패한 전송이 두 번이니 응용이 두 번 실패했다”로 옮기지도 않습니다.

## 3. 재시작 요청과 활성 확인을 분리합니다

자체 호스트 정책은 READY → BUS_OFF → WAIT_ACTIVE → READY의 상태를 사용합니다. 정책은 bus-off 관측 후 송신을 차단하고, 최소 100 ms를 기다린 뒤 재시작을 요청합니다. 요청을 낸 뒤에도 활성 관측 전까지 송신을 막습니다. 100 ms는 제품 요구사항에서 가져온 값이 아니라 예제를 위해 정한 호스트 대기시간입니다.

```python
elif self.phase == 'WAIT_ACTIVE':  # self는 현재 정책 객체의 상태를 가리킵니다.
    action = 'WAIT_ACTIVE'  # 요청 뒤 확인이 없으면 계속 기다립니다.
elif when - self.bus_off_at < self.cooldown:  # 두 정수의 차이를 대기시간과 비교합니다.
    action = 'WAIT_COOLDOWN'  # 기다려야 할 때 재시작 요청을 만들지 않습니다.
```

Linux SocketCAN은 `restart-ms` 자동 재시작과 응용 주도 재시작을 설명합니다. 예제의 자체 횟수 제한·WAIT_ACTIVE 상태는 Linux의 `restart-ms` 구현을 복제한 것이 아닙니다. 실제 구현에서는 드라이버·controller의 상태 전이와 버스 복구 조건을 대조해야 합니다. [Linux 6.14, Starting and Stopping the CAN Network Device](https://docs.kernel.org/6.14/networking/can.html#starting-and-stopping-the-can-network-device)

특히 M_CAN의 bus-off 복구에는 controller가 관측해야 할 버스 상태가 있습니다. 호스트에서 잠깐 기다렸거나 초기화 비트를 바꿨다는 사실로 그 조건을 건너뛰었다고 주장할 수 없습니다. 이 프로그램에는 CAN bit stream·recessive 구간·자동 재전송·arbitration·물리 파형이 없습니다.

## 4. 반복 재시작을 제한합니다

근본 원인이 남아 있으면 재시작을 무한 반복해도 통신이 정상화되지 않을 수 있습니다. 자체 정책은 직전 1,000 ms 안의 요청을 최대 2개로 제한합니다. “직전”의 구간은 `0 ≤ 현재-요청시각 < 1000`으로 정했습니다. 정확히 1,000 ms가 지난 요청은 창에서 빠집니다.

```python
self.request_times = [t for t in self.request_times if when - t < self.window]  # 목록 내포로 창 안의 요청만 남깁니다.
if len(self.request_times) >= self.maximum:  # len은 목록 원소 수를 반환합니다.
    action = 'HOLD_RATE_LIMIT'  # 요청 한도에 이르면 송신 차단을 유지합니다.
```

첫 요청 140 ms와 다음 요청 300 ms가 창에 남은 500 ms에는 세 번째 요청을 보류합니다. 1,139 ms에도 140 ms 요청의 나이가 999 ms이므로 보류합니다. 1,140 ms에는 나이가 1,000 ms여서 창에서 빠지고 새 요청을 낼 수 있습니다. 마지막 상태만 검사하지 않고 창의 바로 전·경계를 분리해 확인합니다.

이 정책은 실패를 숨기기 위한 자동 재시도와 다릅니다. 실제 시스템이라면 요청·controller 상태·정비 판단을 남기고 응용의 재전송 가능성을 따로 결정해야 합니다. 차량·설비 제어의 특정 시간 제한이나 안전 기능을 만족한다고 주장하지 않습니다.

## 5. 25개 관측의 로컬 실행 결과

2026-10-21 Windows AMD64·Python 3.12.14에서 표준 라이브러리만으로 실행했습니다. JSON의 각 관측에는 사람이 정한 기대 action이 있으며 코드 반환값과 비교합니다. 별도로 재시작 요청 시각 목록 `[140, 300, 1140]`을 직접 비교합니다.

| 시각 ms | 입력과 조건 | 수정 경로 | 잘못된 경로의 차이 |
| --- | --- | --- | --- |
| 40 | bus-off 관측 | 송신 차단 | bus-off 자체는 관측합니다. |
| 50 | 대기 10 ms | 대기 유지 | 너무 일찍 재시작을 요청합니다. |
| 139 / 140 | 대기 99 / 100 ms | 대기 / 요청 | 경계 검사가 없습니다. |
| 141 / 150 | 송신 요청 / 활성 관측 | 차단 / 송신 재개 | 확인 전 송신을 허용합니다. |
| 500 / 1139 | 창 안에 요청 2개 | 횟수 제한 유지 | 반복 요청 제한이 없습니다. |
| 1140 | 오래된 요청이 창에서 빠짐 | 다음 재시작 요청 | 창의 계약이 없습니다. |

같은 bus-off 알림이 45 ms에 반복돼도 최초 40 ms 대기 기준을 계속 미루지 않습니다. 요청 뒤 142 ms의 bus-off 재관측도 같은 미복구 회차로 취급해 WAIT_ACTIVE를 유지합니다. 새 회차는 활성 확인 뒤 다시 bus-off가 관측됐을 때 시작합니다. 이 계약 없이 반복 상태 표본을 모두 새 고장으로 세면 대기시간·재시작 횟수가 달라질 수 있습니다. 모델의 사건 시각은 증가 순서로 받고, 음수·bool 시각·알 수 없는 사건·역행 시각 등 잘못된 입력은 `InputError`로 구분합니다. 의도한 오류 검출과 실행기 자체의 예외를 JSON에서 분리합니다.

```powershell
python -B run_cases.py --output C:/temp/can-review-new
```

명령은 예제의 can 폴더에서 실행합니다. 기존 결과 폴더를 주면 종료 코드 2로 거부하며 이전 결과를 덮어쓰지 않습니다. 계약 위반을 잡지 못하거나 예기치 않은 오류가 생기면 실행 결과는 ERROR와 종료 코드 1입니다. 의도적으로 잘못 만든 경로가 기대대로 드러나고 수정 경로가 조건을 만족하면 PASS·0입니다.

## 6. 현장에서 추가로 모아야 할 증거

ACK 오류의 원인은 오프라인 정책 코드로 결정할 수 없습니다. 실제 조사에서는 관측 노드·드라이버·controller·transceiver·bit timing·상대 상태·파형을 연결합니다. 오류 보고를 요청하지 않은 socket의 정상 데이터 목록만 보고 “오류가 없다”고 판단하면 수집 단계부터 불충분할 수 있습니다. 또한 전송 요청이 남은 상태에서 재시작할 때 미전송·재전송·중복 처리 정책을 확인해야 합니다.

현재 코드는 재시작 요청 뒤 활성 확인이 영원히 오지 않으면 차단을 유지합니다. 실제 제품의 확인 timeout·경보·상위 상태 전이, 전원 재인가, 중복 없는 응용 명령, 드라이버 이벤트 유실 대처는 구현하지 않았습니다. 이러한 한계를 소프트웨어 모형의 PASS와 함께 남깁니다.

## 확인 문제

1. 40 ms의 bus-off 뒤 100 ms를 기다리는 정책이라면 139 ms와 140 ms는 어떻게 다릅니까?
2. 재시작 요청이 성공 반환됐다는 이유로 WAIT_ACTIVE를 생략해도 될까요?
3. `tx_complete` 하나를 관측하면 특정 ECU의 작업 완료도 하나로 셀 수 있을까요?

답: 1. 경과 시간이 99 ms와 100 ms이므로 앞은 대기, 뒤는 다른 조건을 만족하면 요청입니다. 2. 아닙니다. 실제 활성 상태를 확인해야 하며 버스 복구 조건도 별도입니다. 3. 아닙니다. 이 사례에는 응용 완료 응답이 없습니다.

## English

Synthetic controller observations expose two deliberately faulty assumptions: queue acceptance equals application completion, and a restart request immediately makes transmission ready. The corrected host policy blocks transmission after bus-off, separates cooldown/request/active confirmation, and limits requests in a defined rolling window. It checks 25 literal expected observations. Repeated bus-off observations while awaiting confirmation stay in the same unresolved episode. It does not simulate CAN error confinement, physical bus recovery, or SocketCAN I/O.

## 출처와 읽은 범위

- [Bosch M_CAN User's Manual Rev.3.3.1, 11.03.2023](https://www.bosch-semiconductors.com/media/ip_modules/pdf_2/m_can/mcan_users_manual_v331.pdf): §2.3.13~14의 ECR·PSR, AckError·Bus_Off·읽기 부작용·복구 설명을 읽었습니다. controller의 의미를 참고했으며 레지스터 접근은 수행하지 않았습니다.
- [Linux 6.14 SocketCAN](https://docs.kernel.org/6.14/networking/can.html): Network Problem Notifications, RAW_ERR_FILTER, Local Loopback, CAN Network Device Driver Interface의 상태·재시작 설명을 읽었습니다. 예제는 Windows에서 실행한 순수 Python이며 Linux API 시험 결과와 구분합니다.
