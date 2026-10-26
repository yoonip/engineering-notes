# UART의 분할 수신과 재동기화 / UART stream parsing and resynchronization

수신 함수의 반환 경계를 메시지 경계로 사용하면, 같은 데이터도 읽는 시점에 따라 사라지거나 합쳐집니다. 이 사례는 수신 조각을 이어 받는 파서와 매번 상태를 버리는 파서를 같은 바이트열로 비교합니다. UART 장치·COM 포트·baud 오차·FIFO overrun은 실행하지 않은 Python 호스트 모델입니다.

[코드·입력·실행 안내](../예제_examples/실무검증_practical-validation/uart_ethernet/README.md) · [실행 기록](검증기록_evidence/UART와UDP수신경계검증_20261021.md) · [기존 escape·CRC 프레임](../전자컴퓨터공학_ece/20-인터페이스통신_interfaces-communications/해설_notes/바이트가메시지가되려면_framing-uart-crc.md)

## 1. 읽은 바이트 수가 달라지는 이유

프레이밍은 연속 바이트에서 메시지의 시작과 끝을 결정하는 규칙입니다. `read(7)`을 호출했다는 사실은 장치가 한 메시지를 7바이트로 보냈다는 뜻이 아닙니다. pySerial 3.5의 `Serial.read(size)`는 timeout이 설정되어 있으면 요청한 수보다 적은 바이트를 반환할 수 있습니다. 여기서는 실제 pySerial 대신 그 상황을 입력 조각으로 재현합니다. [pySerial API: timeout·read](https://pyserial.readthedocs.io/en/latest/pyserial_api.html#serial.Serial.read)

자체 형식은 `A5 5A LEN SEQ DATA SUM8`입니다. `LEN`은 payload 길이 0~8이고, `SEQ`는 태그입니다. 중복·유실·순서·신선도 정책은 구현하지 않습니다. `SUM8=(LEN+SEQ+DATA의 각 바이트 합) mod256`이며 CRC가 아닙니다. 기존 글의 `7E` escape·CRC-16 형식은 그대로 별도 예제로 유지합니다.

| 필드 | 바이트 수 | 이 모델의 역할 |
| --- | --- | --- |
| A5 5A | 2 | 프레임 시작 후보를 찾습니다. |
| LEN | 1 | 기다릴 payload 길이를 정합니다. |
| SEQ | 1 | 출력 프레임을 구별합니다. |
| DATA | LEN | 응용 바이트입니다. |
| SUM8 | 1 | 단순 합을 비교합니다. |

첫 프레임은 `A5 5A 02 01 11 22 36`입니다. `2+1+17+34=54=0x36`을 직접 계산할 수 있습니다. 두 번째 `A5 5A 02 02 A5 5A 03`은 payload 안에도 시작 표식이 있습니다. 길이를 먼저 확인하므로 이 표식에서 정상 프레임을 잘라 버리지 않습니다. 세 번째 `A5 5A 00 03 03`은 빈 payload입니다.

## 2. 같은 19바이트가 읽기 경계에 따라 사라지는 오류

첫 7바이트·둘째 7바이트·셋째 5바이트를 연결하면 19바이트입니다. 오작동 경로 `faulty_each_read_is_one_frame()`는 매 수신 호출에서 새 `StreamParser`를 만들고 완성 결과의 첫 항목만 사용합니다.

| 입력 조각 | 잘못된 경로 | 상태를 유지한 경로 |
| --- | --- | --- |
| 첫 프레임의 앞 2바이트, 나머지 5바이트 | 두 조각을 연결하지 못해 0프레임입니다. | sequence 1·payload 1122입니다. |
| 19바이트를 한 번에 입력합니다. | 첫 프레임만 남습니다. | sequence 1·2·3의 3프레임입니다. |
| 한 바이트씩 19번 입력합니다. | 호출 경계를 메시지 경계로 삼을 수 없습니다. | 같은 3프레임입니다. |

정상 검사에는 한 묶음·바이트별 분할·두 조각으로 자르는 18위치의 총 20가지 분할을 사용합니다. 출력 기대값은 fixture에 적은 `1122`, `a55a`, 빈 바이트열이며 파서의 출력을 다시 정답으로 만들지 않습니다. 가능한 모든 분할을 검사했다는 뜻은 아닙니다.

## 3. 수정: 상태 유지, 길이 제한, 한 바이트 이동

`StreamParser` 객체를 연결 단위로 유지합니다. 완성 프레임을 찾은 뒤에도 버퍼에 남은 바이트를 계속 처리해야 여러 프레임을 한 번에 받을 수 있습니다. 아래는 구현의 핵심 순서를 줄별로 읽기 위한 발췌이며 완전한 실행 코드는 연결한 `models.py`에 있습니다.

```python
def feed(self, chunk):  # def는 함수 정의이며 self는 이 파서 객체입니다.
    if not isinstance(chunk, bytes):  # not은 부정이며 bytes 입력인지 확인합니다.
        raise InputError('UART chunk must be bytes')  # raise는 잘못된 입력을 예외로 알립니다.
    frames = []  # []는 완성 프레임을 담는 리스트입니다.
    for byte in chunk:  # for는 이번 수신 조각의 바이트를 하나씩 순회합니다.
        self.buffer.append(byte)  # bytearray의 끝에 바이트를 추가합니다.
        self.peak = max(self.peak, len(self.buffer))  # len은 길이, max는 최고 저장량을 구합니다.
        frames.extend(self._drain())  # extend는 완성된 여러 프레임을 목록에 합칩니다.
    return frames  # return은 이번 호출에서 완성한 목록을 반환합니다.
```

`_drain()`은 표식 전의 잡음을 제거하고, `LEN>8`이면 후보의 첫 바이트를 버린 뒤 다시 찾습니다. 필요한 `5+LEN`바이트가 부족하면 다음 입력을 기다립니다. 합이 틀린 후보도 첫 바이트만 버려 안쪽의 다음 표식을 살핍니다. 정상 후보에서는 정확히 그 프레임 길이만 소비합니다. `buffer[:needed]`의 `:`는 앞에서 `needed` 직전까지 자르는 슬라이스입니다. `sum(candidate[2:-1]) & 0xFF`는 LEN부터 payload까지 더하고 하위 8비트를 남깁니다. `-1`은 마지막 체크섬 위치입니다.

입력을 한 바이트씩 처리하므로 이 형식의 내부 staging buffer는 최대 13바이트입니다. 잡음 100,000바이트 뒤 최대 길이 프레임을 넣었을 때도 관측 최고값은 13이었습니다. 반환 프레임의 리스트와 호출자가 축적한 결과까지 13바이트라는 뜻은 아닙니다. 실제 서비스에는 결과 큐의 용량·소비 속도도 필요합니다.

## 4. 오류 검출과 복구는 각각 확인합니다

| 대조 입력 | 기대·관측 결과 | 확인하는 원인 |
| --- | --- | --- |
| 첫 프레임 checksum 36을 37로 바꾼 뒤 둘째를 붙입니다. | 첫 후보를 거부하고 둘째a55a만 복구합니다. checksum 오류 1회입니다. | 손상 수락과 후속 복구를 함께 검사합니다. |
| `A5 5A FF 00` 뒤 첫 프레임을 붙입니다. | 길이 오류 1회 뒤 1122를 복구합니다. | 잘못된 LEN을 무제한 기다리지 않습니다. |
| `A5 5A 08` 뒤 첫 프레임을 붙입니다. |10바이트이므로 13바이트 후보를 기다립니다. 명시적인 만료 사건 후 1122를 복구합니다. | 허용 길이의 가짜 후보가 후속 정상 데이터를 가릴 수 있습니다. |
| `A5 5A 02 01 12 21 36` | 다른 payload 1221도 수락합니다. | 단순 합의 충돌을 보여 줍니다. |

마지막 대조는 `0x11+0x22=0x12+0x21=0x33`이므로 같은 SUM8이 나옵니다. 체크섬 통과가 데이터의 진실성·인증을 보장하지 않습니다. 실제 프로토콜의 CRC·인증·순번 정책은 별도로 선택해야 합니다.

`expire_partial()`은 호출자가 선언하는 정책 사건입니다. 실제 시계나 UART timeout을 측정하지 않습니다. 후보의 첫 바이트를 버리고 남은 버퍼를 재검사합니다. 실제 적용에서는 최대 프레임 전송 시간과 드라이버·스케줄러 지연을 함께 고려해야 합니다. 읽기 함수가 한 번 반환됐다는 이유로 만료시키면 정상 분할 프레임도 잃습니다. 표식과 단순 합이 우연히 일치하는 입력에서는 오인식도 가능하므로 모든 손상을 완벽히 재동기화한다는 보장은 없습니다.

## 5. 계산으로 먼저 확인하는 시간 예산

8N1·115200 bit/s·idle 없음이라는 자체 조건에서 7바이트는 `7×10/115200=0.000607639초`, 약 0.608ms입니다. 최대 13바이트는 약 1.128ms이고, 최대 길이의 payload 비율은 `8/13≈61.5%`입니다. 헤더와 체크섬을 포함한 선로 바이트 수와 payload 수를 구분한 계산입니다. USB buffering·운영체제 지연·실제 오류율의 측정값은 아닙니다.

현장에서는 raw bytes와 수신 길이·시각을 먼저 보존한 뒤 동일 바이트열을 오프라인 파서에 넣습니다. 파서에서 재현되면 경계·길이·체크섬·만료 정책을 확인합니다. raw bytes 자체가 유실됐다면 UART status의 overrun·framing·parity 오류, 드라이버 buffer와 처리 지연을 별도 조사합니다. 이 소프트웨어 결과로 baud나 배선 원인을 확정하지 않습니다.

## 6. 검증기가 틀린 구현을 잡는지 확인합니다

정상 실행과 `python -B -O` 실행의 의미상 결과를 비교합니다. `require()`는 일반 `assert` 대신 명시적인 예외를 발생시키므로 최적화 옵션으로 사라지지 않습니다. `--mutation uart-ignore-checksum`은 손상 후보의 합 검사를 건너뛰어 오류 프레임까지 수락하게 만듭니다. 이 실행은 `UART checksum rejection/recovery literal failed`·종료 1이어야 합니다. 정상 모델의 실패와 의도한 변이 검출은 [검증 기록](검증기록_evidence/UART와UDP수신경계검증_20261021.md)에서 구분합니다.

## 확인 문제

1. 시작 표식 두 바이트만 읽었는데 다음 `read()`까지 기다리면 안 되나요? 기다려야 합니다. 같은 파서의 버퍼에 보존합니다.
2. payload에A55A가 있으면 새 프레임인가요? 유효한 후보의 길이 안에서는 payload입니다. 길이·체크섬이 실패했을 때 재탐색합니다.
3. checksum이 맞은 1221을 왜 오류로 표시하지 않나요? 이 합만으로 1122와 구별할 수 없습니다. 검출 능력의 한계를 드러내는 대조입니다.

## English

An invented length-prefixed frame demonstrates partial reads, merged frames, bounded staging storage, and explicit partial-candidate expiry. A persistent parser yields the same three literal frames under 20 selected chunkings. A stateless per-read path loses partial or merged messages. A deliberate additive-checksum collision remains accepted; this checksum is neither CRC nor authentication. UART hardware, clocks, drivers, and FIFO overruns were not exercised.

## 읽은 자료와 범위

- pySerial 3.5 API의 timeout·`Serial.read(size)`·bytes 반환 설명을 2026-10-21에 확인했습니다. pySerial을 설치하거나 실제 serial port를 열지는 않았습니다. [공식 문서](https://pyserial.readthedocs.io/en/latest/pyserial_api.html)
- 형식·19바이트 입력·20가지 분할·만료·합 충돌·시간 계산은 직접 만든 예제입니다. 기존 CRC-16 구현의 결과와 섞지 않습니다.
