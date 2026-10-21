# USB의 부분 전송과 중복 없는 복구 / USB bulk results and duplicate-safe recovery

USB 전송 함수가 성공했어도 응용 메시지가 모두 도착하지 않을 수 있습니다. timeout에도 일부 바이트는 이미 이동했을 수 있고, 응답을 못 받았다고 명령을 새로 보내면 같은 동작을 두 번 적용할 수도 있습니다. 이 사례는 실제 장치·libusb·USB host controller를 실행하지 않은 합성 API 결과와 응용 정책 모델입니다.

[코드·입력·실행 안내](../예제_examples/실무검증_practical-validation/usb_pcie/README.md) · [검증 기록](검증기록_evidence/USB와PCIe전송계약검증_20261021.md)

## 1. status와 actual_length는 서로 다른 질문입니다

Bulk는 USB의 전송 종류입니다. endpoint는 장치 안에서 데이터를 주고받는 논리적인 통로이며, IN은 장치에서 호스트로 받는 방향입니다. 여기서는 정해진 순서의 IN 완료 결과만 입력합니다. 버스 packet·data toggle·microframe을 생성하는 USB 시뮬레이터는 아닙니다.

libusb 1.0.30 문서는 COMPLETED가 요청량 전체 전송을 뜻하지 않는다고 설명합니다. timeout과 취소에서도 일부 데이터가 전송될 수 있으므로 callback 뒤의 actual_length를 확인해야 합니다. actual_length는 요청한 buffer 길이가 아니라 실제 전송량입니다. [libusb async status·Cancellation·Timeouts](https://libusb.sourceforge.io/api-1.0/group__libusb__asyncio.html), [transfer 필드](https://libusb.sourceforge.io/api-1.0/structlibusb__transfer.html)

자체 응용 레코드 길이는 6바이트입니다. 아래 결과의 requested는 모두 8바이트지만 실제 데이터는 다릅니다.

| IN 결과 status | actual_length·bytes | 조립 중인 응용 레코드 |
| --- | --- | --- |
| COMPLETED | 3·AABBCC | 3바이트를 보존하며 기다립니다. |
| TIMED_OUT | 2·DDEE | 전송된 prefix를 보존해 5바이트가 됩니다. |
| COMPLETED | 1·FF | AABBCCDDEEFF, 6바이트 레코드가 완성됩니다. |
| COMPLETED | 0·빈 값 | 추가 레코드를 만들지 않습니다. |

COMPLETED에 actual_length가 requested보다 작으면 short completion입니다. USB bulk의 short packet은 요청량 전까지 읽기를 끝낼 수 있지만 응용 메시지의 끝을 뜻하는 보편 규칙은 아닙니다. 이 예제는 API 수준에서 관측한 짧은 결과만 입력하며 실제 packet 크기나 ZLP를 판독하지 않습니다. 응용 레코드 경계는 자체 6바이트 규칙으로 정합니다.

잘못된 경로는 첫 완료의 requested=8을 유효 데이터 길이로 사용합니다. 부족한 부분이 0으로 초기화돼 있다고 만든 오류 대조에서는 첫 레코드가 `AABBCC000000`이 됩니다. 실제 미초기화 메모리가 언제나 0이라는 뜻은 아닙니다. 수정 경로는 actual_length만큼의 유효 bytes만 소비해 `AABBCCDDEEFF`와 비교합니다.

```python
result = bulk_result(**event)  # **는 딕셔너리의 키를 함수의 이름 붙은 인수로 전달합니다.
usable = result['status'] in {'COMPLETED', 'TIMED_OUT'}  # in은 집합에 포함되는지 검사합니다.
if usable:  # if는 이 예제에서 보존하기로 한 부분 데이터인지 확인합니다.
    self.buffer.extend(octets(result['data_hex']))  # extend는 실제 bytes를 bytearray 뒤에 붙입니다.
    while len(self.buffer) >= 6:  # while은 완전한 레코드가 남아 있는 동안 반복합니다.
        frames.append(self.buffer[:6].hex())  # [:6]은 앞 6바이트이며 hex는 표시용 16진수입니다.
        del self.buffer[:6]  # del은 이미 소비한 바이트만 제거합니다.
```

취소·STALL·ERROR 결과의 prefix는 이 조립기에서 응용에 넘기지 않는 정책입니다. 취소 전에 전송된 데이터가 무조건 무효라서가 아닙니다. NO_DEVICE/CANCELLED가 와도 이미 쌓인 partial buffer를 자동 소거하지 않습니다. 이 조립기는 한 연결 세대의 순서가 유지된 입력만 다루며, 재연결 때 호출자가 새 조립기를 만들고 옛 부분 레코드를 폐기해야 합니다. session 상태 모델과 조립기를 자동 결합한 실제 드라이버는 구현하지 않았습니다.

## 2. STALL을 풀어도 이미 적용한 명령이 사라지지 않습니다

STALL은 bulk endpoint가 halt 상태임을 알리는 결과입니다. libusb의 clear_halt는 endpoint의 halt를 해제하며, 먼저 pending 전송을 취소하도록 안내합니다. 취소 요청은 비동기이므로 완료 callback을 받아 buffer 소유권을 회수한 뒤 복구합니다. [libusb clear_halt](https://libusb.sourceforge.io/api-1.0/group__libusb__dev.html)

자체 장치에는 값을 10에서 delta만큼 올리는 명령이 있습니다. command ID 41·delta 7을 적용해 값이 17이 됐지만, 그 뒤 응용 ACK를 읽는 IN 전송이 STALL합니다. 이 일정에서는 명령이 이미 적용됐다는 것을 모델의 장치 쪽 상태로 알고 있으며 호스트가 STALL만 보고 이를 알아내는 것은 아닙니다.

| 복구 방식 | 장치 적용 횟수 | 최종 값 | 원인 |
| --- | ---: | ---: | --- |
| 같은 ID 41·같은 delta 7을 다시 요청합니다. | 1 | 17 | 장치가 저장한 결과를 돌려줍니다. |
| 새 ID 42로 다시 요청합니다. | 2 | 24 | 장치가 별개의 명령으로 적용합니다. |

멱등성은 같은 요청을 다시 실행해도 효과가 더 늘지 않는 성질입니다. 이 예제는 장치가 ID별 인수와 결과를 보관하는 자체 프로토콜로 그 성질을 만듭니다. 같은 ID에 다른 delta를 보내면 COMMAND_ID_CONFLICT입니다. clear_halt나 USB의 link 재전송만으로 이 응용 성질이 자동 제공되지는 않습니다.

실제 제품에는 ID의 유효 기간·장치 재부팅 뒤 저장 여부·중복 응답·응답 상실·인증 규칙이 필요합니다. 이 모델은 같은 장치 객체가 살아 있는 두 요청만 다루며 저장소를 무한히 운영하는 방법이나 전원 상실 뒤 exactly-once를 구현하지 않습니다. 장치가 이런 프로토콜을 제공하지 않으면 호스트만 바꿔 임의의 명령을 안전하게 재실행할 수 없습니다.

## 3. cancel 요청과 buffer 반환을 구분합니다

`UsbEndpoint`는 단일 endpoint와 4개 buffer slot을 가정합니다. token은 `(generation, serial)`이고 callback 전까지 pending에 남습니다. generation은 연결 세대이며 disconnect 사건에서 증가합니다. serial은 제출할 때마다 증가하는 자체 정수입니다.

| 순서 | 관측·판정 |
| --- | --- |
| slot 0과 1을 제출한 뒤 slot 0이 STALL합니다. | slot 1이 pending이므로 clear_halt를 PENDING_ACTIVE로 거부합니다. |
| slot 1에 cancel을 요청합니다. | pending 수는 여전히 1이며 buffer를 반환하지 않습니다. |
| CANCELLED callback이 actual_length=2로 도착합니다. | slot은 반환하되 prefix는 이 응용 정책에서 공개하지 않습니다. |
| callback을 모두 처리하고 clear합니다. | 같은 slot을 다시 제출할 수 있습니다. |

또 다른 일정에서는 세대 0의 slot 0 제출 뒤 disconnect·reconnect합니다. 세대 1의 slot 1을 제출해 둔 채 세대 0의 늦은 callback을 받으면, 옛 slot의 소유권만 반환하고 bytes는 버립니다. 옛 callback이 NO_DEVICE여도 새 세대를 끊지 않습니다. 새 callback의 1122는 정상 공개합니다. 취소 요청 뒤 COMPLETED가 도착하는 경쟁도, 자체 폐기 정책과 실제 수신량을 따로 기록합니다.

실제 USB 주소는 재열거 때 다시 배정될 수 있습니다. 이 generation은 주소 숫자를 읽어 자동 계산한 값이 아닙니다. 실제 프로그램에서는 handle의 생명주기·hotplug·재탐색 결과를 자기 session에 연결해야 합니다. 정수 token을 사용했다고 buffer 해제나 thread 동기화까지 구현되는 것도 아닙니다.

## 4. 계산과 오류 대조

첫 3바이트는 레코드의 `3/6=50%`, timeout 뒤 5바이트는 약 83.3%입니다. 전송 요청 성공률과 레코드 완성률을 같은 지표로 쓰면 첫 단계의 차이를 놓칩니다. 최종 소비량은 `3+2+1=6`이고 실제 전송량 0의 결과는 소비량을 늘리지 않습니다. 값 변화도 `10+7=17`과 `10+7+7=24`로 별도 계산할 수 있습니다. 시간·대역폭의 실측값은 아닙니다.

`usb-drop-timeout` 변이는 timeout의 DDEE를 버려 레코드를 완성하지 못합니다. `usb-new-command-id` 변이는 복구 요청에 새 ID를 부여해 명령을 두 번 적용합니다. 두 경우 리터럴 기대값을 바꾸지 않아 검증기가 종료 1로 실패합니다. USB 속도·케이블·host controller의 원인은 이 결과만으로 진단하지 않습니다.

## 확인 문제

1. COMPLETED인데 3/8바이트이면 응용 레코드가 완성됐나요? 아닙니다. 자체 레코드 6바이트에는 아직 부족합니다.
2. ACK를 못 받았으니 새 ID로 명령을 보내면 되나요? 이미 적용됐을 수 있습니다. 장치의 응용 ACK·ID 중복 처리 계약을 확인해야 합니다.
3. cancel 함수가 반환되면 buffer를 재사용해도 되나요? 이 모델과 libusb의 비동기 취소에서는 callback까지 기다려야 합니다.

## English

Synthetic bulk results separate status, actual length, and a six-byte application record. Timeout prefixes remain usable under the declared policy. A device-side command-ID cache makes an ACK-stall retry duplicate-safe; changing the ID applies the command twice. A separate endpoint lifecycle model retains buffer ownership until callback and drops old-session data. No USB device, libusb API, host controller, or physical transfer was executed.

## 읽은 판본과 범위

2026-10-21에 libusb 공식 문서 화면의 1.0.30을 확인했습니다. Sync I/O의 bulk_transfer, Async I/O의 completion·status·Cancellation·Partial data·Timeouts, transfer의 length·actual_length·callback, Device handling의 clear_halt·reset_device를 읽었습니다. 실제 API를 호출한 기록이 아니라 문서 계약을 참고한 합성 정책입니다.
