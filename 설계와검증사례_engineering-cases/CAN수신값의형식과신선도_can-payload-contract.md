# CAN 수신값의 형식과 신선도 / Frame identity, byte order, sequence, and freshness

CAN 프레임이 도착했고 숫자도 정상 범위라고 응용 값까지 맞는 것은 아닙니다. 같은 바이트를 반대로 읽거나 오래된 값을 다시 채택하면 전송 오류와 다른 종류의 장애가 생깁니다. 이 사례는 직접 정한 작은 응용 형식에 잘못된 ID·프레임 종류·길이·순번·시각을 넣고, 채택 여부와 상태 변경을 확인합니다. 실제 차량 프로토콜이나 현장 CAN 캡처가 아닌 결정적 소프트웨어 예제입니다.

[실행 코드](../예제_examples/실무검증_practical-validation/can/run_cases.py), [24개 입력 레코드](../예제_examples/실무검증_practical-validation/can/application_frames.json), [실행 안내](../예제_examples/실무검증_practical-validation/can/README.md), [검증 기록](검증기록_evidence/CAN정책과수신계약검증_20261021.md)을 함께 봅니다.

## 1. 링크 형식과 응용 형식을 나눕니다

예제의 필터는 표준 11비트 ID `0x321`의 Classical CAN data만 허용합니다. 같은 숫자의 확장 ID, remote·FD·driver error 레코드는 이 계약에 맞지 않습니다. 실제 SocketCAN의 `can_id`에는 ID와 형식 플래그가 함께 들어가며, payload의 기본 바이트 순서는 CAN 자체가 정하지 않습니다. [Linux 6.14, CAN frame structure·Filter Usage](https://docs.kernel.org/6.14/networking/can.html#how-to-use-socketcan)

JSON은 학습을 위해 ID와 각 형식 플래그를 분리했습니다. `is_error`는 driver가 보고하는 오류 사건을 응용 데이터와 혼동하지 않기 위한 필드입니다. 실제 CAN 데이터 프레임에 이런 Boolean 필드가 실리는 것은 아닙니다. “9바이트 Classical payload” 레코드도 실제 유효 wire frame을 만들었다는 뜻이 아니라, 캡처·어댑터 계층의 잘못된 레코드를 파서가 거부하는 검사입니다.

| 위치 | 자체 규칙 | 알려진 첫 입력 |
| --- | --- | --- |
| 0 | 형식 버전 1 | `01` |
| 1 | 8비트 순번 | `FE` = 254 |
| 2~3 | little-endian unsigned 16비트 전압, 1 mV 단위 | `34 12` = 4,660 mV |
| 4~7 | little-endian unsigned 32비트 샘플 시각, ms | `64 00 00 00` = 100 ms |

이 값은 특정 자동차 신호 정의나 DBC에서 가져오지 않았습니다. 정상 범위 0~5,000 mV, 허용 샘플 나이 100 ms, 엄격한 연속 순번도 자체 정책입니다. ID가 맞아도 발신자를 인증한 것은 아니며, CAN CRC의 계산·검사는 이 코드의 범위가 아닙니다.

## 2. 바이트 순서는 알려진 패턴으로 검사합니다

```python
millivolts = int.from_bytes(data[2:4], 'little')  # 슬라이스 [2:4]의 두 바이트를 작은 자리부터 읽습니다.
wrong = int.from_bytes(data[2:4], 'big')  # 같은 바이트를 반대로 읽는 의도적 대조 경로입니다.
```

첫 입력에서 수정 경로는 4,660, 반대 순서는 13,330입니다. `34 12`는 직접 정한 0x1234 패턴이므로 기대값을 파서와 다른 계산으로도 확인할 수 있습니다. 0x12×256+0x34=4,660이며, 0x34×256+0x12=13,330입니다. 두 함수가 같은 값을 내는지만 비교하면 둘 다 잘못됐을 때 놓칠 수 있습니다.

이 예제의 상한 5,000 mV는 반대 순서를 거부하는 데 도움이 되지만 언제나 그렇지는 않습니다. 바이트 `01 02`는 두 순서에서 513과 258로 모두 이 범위 안입니다. 따라서 범위 검사와 알려진 패턴 검사는 목적이 다릅니다. 특정 환경에서 이상해 보이지 않는 값 하나를 받아 바이트 순서를 확정하지 않습니다.

## 3. 잘못된 입력을 거부한 뒤에도 상태가 남을 수 있습니다

의도적인 `faulty_advance_before_age`는 순번을 먼저 저장하고 나이를 검사합니다. 마지막 채택 순번 254에서 오래된 순번 255가 오면 STALE을 반환하지만 저장 순번은 이미 255가 됩니다. 이후 정상적인 순번 255가 도착하면 DUPLICATE로 잘못 거부합니다.

```python
state[key] = sequence  # 잘못된 경로: 유효성을 확인하기 전에 채택 상태를 바꿉니다.
age = age32(frame['now_ms'], sample)  # 공통 시계에서 샘플 나이를 계산합니다.
return 'STALE' if age is None or age > 100 else 'ACCEPT'  # 조건 표현식으로 판정을 반환합니다.
```

수정 경로는 ID·형식·길이·버전·값·시각·순번을 전부 확인한 뒤 `state[session]`을 바꿉니다. 실행기는 거부 전의 상태 사본과 거부 후 상태를 비교합니다. 반환값이 STALE인지만 보는 검사에 더해 “거부가 마지막 유효 순번을 오염시키지 않는다”는 조건을 확인합니다.

표준 순번의 마지막 255 뒤에는 0을 허용합니다. 구현의 `(sequence - previous) & 0xFF`는 8비트 순환 차이를 구합니다. 예제는 차이가 정확히 1인 경우만 허용합니다. 중간 프레임 하나를 실제로 잃으면 이후 프레임도 계속 거부될 수 있으므로, 이는 진단을 위해 멈추는 엄격한 계약입니다. 자동 gap 허용·송신기 재부팅·세션 재동기화는 구현하지 않았습니다. 실제 제품에서는 상태 재설정의 근거와 누락 허용 범위를 별도로 정해야 합니다.

## 4. 수신 시각과 사용할 시각을 나눕니다

JSON의 `sample_ms`, `rx_ms`, `now_ms`는 모두 같은 32비트 단조 ms 시계라는 합성 가정입니다. `sample_ms`는 payload 안의 생성 시각, `rx_ms`는 수집 시각, `now_ms`는 검증·사용 시각입니다. 서로 동기화하지 않은 ECU와 호스트의 숫자를 그대로 빼는 방법이 아닙니다.

샘플 생성 240 ms, 수신 250 ms, 사용 341 ms이면 수신 당시에는 10 ms 된 값이지만 사용 시점에는 101 ms입니다. 수신 시점에만 검사하면 대기열에서 오래된 값을 채택할 수 있습니다. 이 입력은 STALE로 거부합니다. 반대로 100 ms 경계는 허용하고 101 ms는 거부하는 레코드를 따로 둡니다.

시계가 순환할 때 차이는 다음처럼 계산합니다.

```python
age = (now - then) & MASK32  # &는 32비트 안에서 순환 차이를 얻는 비트 AND입니다.
return None if age >= HALF32 else age  # 반주기 이상 차이는 미래·역행 등으로 구분합니다.
```

샘플 `0xFFFFFFFD`, 사용 시각 3은 이 가정에서 6 ms 차이입니다. 실제 시간 차이가 2³¹ ms보다 작아 순서를 구분할 수 있다는 전제가 필요합니다. 임의로 오래된 시각을 받아도 이 식이 과거와 미래를 모두 알아내는 것은 아닙니다.

공통 시계에서는 샘플 생성이 수신보다 뒤일 수도 없습니다. `rx=100`, `now=110`, `sample=105`이면 샘플 나이 5 ms가 대기열 나이 10 ms보다 작아 순서가 어긋납니다. 수정 경로는 이를 SAMPLE_AFTER_CAPTURE로 거부합니다. 코드 검토에서 이 조건의 누락을 찾아 추가했으며, 현재 24번째 레코드가 그 회귀 검사입니다.

동기화가 없는 실제 통신에서는 수신 측의 마지막 유효 수신 시각으로 timeout을 정할 수 있습니다. 다만 이 방식은 송신기의 측정 시점부터 수신까지의 지연을 직접 알지는 못합니다. 목적에 맞는 시간 계약을 먼저 선택합니다.

## 5. 24개 입력의 결과와 입력 예외

2026-10-21 Windows AMD64·Python 3.12.14에서 실행했습니다. 수정 경로는 6개를 채택하고 18개를 응용 계약상 거부했습니다. 모든 레코드를 정상 데이터라고 취급하는 잘못된 경로는 24개를 채택하게 됩니다. 이 차이는 통신 장치의 손실률이나 실제 차량의 불량률이 아닙니다.

| 판정 | 개수 | 대표 입력 |
| --- | --- | --- |
| ACCEPT | 6 | 알려진 값, 255→0, 정확히 100 ms, 시계 순환 |
| ID / ID_FORMAT | 1 / 1 | 다른 ID, 같은 숫자의 확장 ID |
| FRAME_TYPE / LENGTH / VERSION | 3 / 2 / 1 | remote·FD·오류 사건, 7·9바이트, 다른 형식 버전 |
| SAMPLE_CLOCK / CAPTURE_CLOCK / SAMPLE_AFTER_CAPTURE | 1 / 1 / 1 | 미래·역행 등으로 해석되는 시각, 생성/수집 순서 불일치 |
| STALE | 3 | 나이 101 ms와 대기열에서 오래된 값 |
| DUPLICATE / SEQUENCE | 1 / 2 | 중복·역순·간격이 있는 순번 |
| VALUE_RANGE | 1 | 65,000 mV라는 자체 상한 밖의 값 |

다른 12개 입력 검사는 음수·bool 시각, 알 수 없는 사건, 잘못된 hex, 숫자로 전달한 flag, ID 표현 범위 초과 등을 `InputError`로 거부하는지 확인합니다. 이는 위 24개 응용 레코드 수에 합산하지 않습니다. JSON의 `expected`는 사람이 지정한 리터럴 판정이며, 기대 mV도 파서 호출로 생성하지 않았습니다.

## 6. 실무 진단으로 옮길 때

먼저 원시 바이트·ID 형식·길이·수집 방향·필터·누락 통계와 신호 map 버전을 보존합니다. 그런 다음 알려진 시험값으로 바이트 순서·부호·단위를 대조하고, 순번·시각·상태 갱신의 순서를 봅니다. 데이터가 도착했다는 로그와 마지막으로 채택한 값을 따로 기록하면 무효 프레임이 계속 도착하는 상황을 구분하기 쉽습니다.

값에 범위를 적용해도 신호의 의미까지 검증한 것은 아닙니다. 3,300 mV가 정상 범위여도 잘못된 센서 채널, 보정 계수, 전원 기준일 수 있습니다. CRC가 맞아도 이러한 응용 해석은 남습니다. 현재 코드는 연결·차동 파형·bit timing·정합·버스 부하·실시간 응답·드라이버 FIFO 유실을 시험하지 않습니다.

## 확인 문제

1. 오래된 순번 255를 거부하면서 마지막 유효 순번을 255로 바꾸면 무엇이 달라질까요?
2. 240 ms 생성·250 ms 수신·341 ms 사용을 수신 시점에서만 판단하면 무엇을 놓칠까요?
3. 송신 시각과 수신 시각이 다른 clock에 속하면 이 코드의 나이 계산을 그대로 쓸 수 있을까요?

답: 1. 뒤의 유효한 255가 중복으로 거부될 수 있습니다. 2. 대기열 지연으로 사용 시점의 나이가 101 ms가 된 점을 놓칩니다. 3. 안 됩니다. 동기화와 오차 경계 또는 수신 측 timeout 등 다른 계약이 필요합니다.

## English

An invented eight-byte Classical CAN contract checks frame identity/type, exact length, version, little-endian millivolts, shared-clock freshness, timestamp ordering, and strict sequence continuity. Twenty-four records yield six accepts and eighteen rejects. A deliberately premature sequence update poisons later acceptance. Clock wrap is checked under a half-range assumption. No physical CAN, SocketCAN, CRC, authentication, or automatic resynchronization is tested.

## 출처와 읽은 범위

[Linux 6.14 SocketCAN](https://docs.kernel.org/6.14/networking/can.html)의 How to use SocketCAN, Network Problem Notifications, RAW_CAN_FILTER·Filter Usage Optimisation, CAN FD Driver Support를 2026-10-21 읽었습니다. ID 플래그·payload 길이·byte order와 오류 사건 구분의 근거로 사용했습니다. 표의 자체 형식·시간·순번 정책·결함 입력·실행 결과는 공식 프로토콜의 일부로 제시하지 않습니다.
