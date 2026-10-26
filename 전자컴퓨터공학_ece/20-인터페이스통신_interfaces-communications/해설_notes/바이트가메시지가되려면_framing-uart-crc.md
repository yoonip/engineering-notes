# 바이트가 메시지가 되려면: UART, 프레이밍과 CRC

[상위 주제](../README.md) · [프레임 구현](../../../예제_examples/공학기초_foundations/systems/systems_models.py) · [검증 코드](../../../예제_examples/공학기초_foundations/systems/test_systems_models.py)

## 한국어

### UART가 보내는 바이트와 프로그램의 메시지는 다릅니다

UART로 `온도=25`라는 데이터를 보냈다고 해도 수신 함수가 이를 한 번에 돌려준다는 보장은 없습니다. 일부 바이트씩 나뉘거나 여러 메시지가 함께 도착할 수 있습니다. UART는 비트의 시작과 끝을 정하고, 애플리케이션 프레임은 메시지의 시작과 끝을 정합니다. 전기적 신호와 상위 데이터의 경계를 나눠 생각해야 합니다.

8N1은 시작 비트 1개, 데이터 8비트, parity 없음, 정지 비트 1개입니다. 비트 시간을 $`1/B`$초라 하면 한 바이트의 전송 시간은 $`10/B`$초입니다. 쉬는 구간이 없다는 가정에서 $`115200`$ bit/s의 UART는 최대 $`11520`$ data byte/s를 전송합니다. 메시지 헤더와 CRC, escape 바이트를 빼면 실제 데이터 처리율은 더 낮아집니다. baud와 bit/s가 일반적으로 같은 뜻인 것은 아니지만, 여기서는 한 심벌에 한 비트를 보내는 UART를 다룹니다. [TI UART configuration](https://software-dl.ti.com/C2000/docs/C2000_driverlib_api_guide/f28p65x/build/html/modules/uart.html)

### 경계 표시가 데이터 안에도 나오면?

이 예제는 `0x7E`를 경계로 사용합니다. 데이터나 CRC 안의 `0x7E`와 `0x7D`는 `0x7D` 뒤에 원래 바이트 XOR `0x20`을 보내는 방식으로 바꿉니다. 수신기는 escape 상태를 기억해 원래 바이트를 복원합니다. 한 바이트씩 들어와도 이 상태를 유지하므로 분할 수신을 처리할 수 있습니다. 이 방식은 RFC1662의 octet stuffing과 FCS 계산을 참고한 작은 애플리케이션 프레임이며, 주소·제어·프로토콜 필드나 ACCM 협상 등을 갖춘 완전한 PPP 구현은 아닙니다. [RFC1662 §4·Appendix C](https://www.rfc-editor.org/rfc/rfc1662.html)

![바이트가 메시지가 되려면: UART, 프레이밍과 CRC — 개념도 / Concept diagram](../../../그림자료_assets/도식_diagrams/framing-uart-crc.png)

[SVG](../../../그림자료_assets/도식_diagrams/framing-uart-crc.svg) · [그림 원본 / Diagram source](../../../그림자료_assets/도식_diagrams/framing-uart-crc.mmd)

| 번호 / No. | 출발 / From | 도착 / To | 조건·동작 / Condition and action |
| --- | --- | --- | --- |
| 1 | 시작 / Start | WAIT | 초기화 / Initialize |
| 2 | WAIT | COLLECT | 0x7E |
| 3 | COLLECT | ESCAPE | 0x7D |
| 4 | ESCAPE | COLLECT | XOR 0x20 후 저장 / Decode and append |
| 5 | COLLECT | COLLECT | 일반 바이트 저장 / Append byte |
| 6 | COLLECT | DROP | 길이 상한 초과 / Capacity exceeded |
| 7 | DROP | COLLECT | 0x7E |
| 8 | COLLECT | COLLECT | 0x7E에서 검사·초기화 / Validate and restart |
| 9 | ESCAPE | COLLECT | 0x7E에서 폐기·초기화 / Abort and restart |

직접 작성한 상태도입니다. `DROP` 상태는 경계가 나올 때까지 모든 내용을 버립니다. 입력이 잘못되어도 저장 공간을 끝없이 늘리지 않습니다. 경계 직전이 escape이면 미완성 프레임으로 버립니다. 전송 중단 후의 timeout은 이 바이트 모델 밖에서 시간 기준을 정해 추가할 수 있습니다.

### CRC를 다항식으로 보기

CRC는 비트열을 $`GF(2)`$ 위의 다항식으로 보고, 정한 생성 다항식으로 나눈 나머지를 이용합니다. 계수는 0 또는 1이고 덧셈·뺄셈은 XOR입니다. 여기서는

$$G(x)=x^{16}+x^{12}+x^5+1$$

을 사용합니다. 다항식만 같다고 CRC가 같은 것은 아닙니다. 입력 비트 순서, 초기값, 최종 XOR와 전송 순서까지 맞아야 합니다.

| 항목 | 이 예제의 CRC-16/X-25, CRC-16/IBM-SDLC 설정 |
| --- | --- |
| width / poly | 16 / `0x1021` (최상위 항 제외) |
| init / xorout | `0xFFFF` / `0xFFFF` |
| refin / refout | true / true |
| reflected 루프 상수 | `0x8408` |
| FCS 전송 순서 | 낮은 바이트 먼저 |
| `123456789`의 결과 | `0x906E` |
| payload+FCS의 raw residue | 최종 XOR 전 `0xF0B8` |

구현의 오른쪽 시프트는 다항식 나눗셈을 비트 순서에 맞춰 수행합니다. 매 바이트에 8번 반복하므로 길이 $`N`$에서 $`O(N)`$ 시간, CRC 상태는 $`O(1)`$ 공간입니다. 처리율이 부족하면 같은 규칙으로 만든 lookup table이나 하드웨어 CRC를 사용할 수 있지만, 장치의 reflection과 초기·최종 처리 설정까지 비교해야 합니다.

### 검출과 보안의 경계

CRC는 잡음이나 전송 오류의 검출 수단입니다. 공격자는 데이터를 바꾸고 CRC도 다시 계산할 수 있으므로 인증 수단이 아닙니다. 검출되지 않는 오류도 존재합니다. 예를 들어 코드 다항식에 $`G(x)`$의 배수인 오류를 XOR하면 나머지가 변하지 않습니다. 따라서 “CRC가 맞으니 내용이 반드시 정확하다”는 결론은 성립하지 않습니다. [보안과 신뢰성의 경계](../../38-보안암호하드웨어신뢰_security-cryptography/해설_notes/오류를찾는것과공격을막는것_security-and-reliability-boundaries.md)

### 구현과 검증

프레임의 최대 payload를 $`M`$으로 제한하면 수신 내부 버퍼는 CRC를 포함해 $`M+2`$ 바이트입니다. 최악의 escape 확장까지 포함한 송신 크기는 $`2(M+2)+2`$ 바이트 이하이며, 8N1 전송 시간은 그 바이트 수에 $`10/B`$를 곱한 값입니다. `FrameParser.feed()`는 결과를 순차적으로 내보내는 generator여서 반환 프레임을 내부에 누적하지 않습니다. 호출자가 결과를 무제한 모으면 그 공간은 별도로 늘어납니다.

테스트는 `123456789` 벡터와 RFC1662 residue를 확인합니다. CRC를 정방향 `binascii.crc_hqx()`와 비트 반전으로 독립 계산해 비교하고, 모든 256종 바이트, 빈 메시지, 다양한 chunk 크기를 검사합니다. 80개 단일 비트 오류, 10,000바이트 초과 프레임의 저장 상한, 다음 정상 경계에서 복구, escape 중단도 확인합니다. 테스트는 특정 UART의 baud 오차·배선·FIFO overrun을 측정하지 않습니다. [실행 안내](../../../예제_examples/공학기초_foundations/systems/README.md)

### 분할 수신과 오류 뒤의 복구를 따로 재현하기

[UART 분할 수신 사례](../../../설계와검증사례_engineering-cases/UART의분할수신과재동기화_uart-stream-resync.md)는 위 escape·CRC 형식과 구별되는 `A5 5A LEN SEQ DATA SUM8` 자체 형식을 사용합니다. SUM8은 단순 합이고 CRC가 아닙니다. 수신 함수의 반환 경계를 프레임 경계로 오해했을 때의 오류를 작은 리터럴로 확인합니다. pySerial의 timeout이 설정된 `read(size)`는 요청 수보다 적은 바이트를 반환할 수 있으므로 같은 객체의 상태를 다음 읽기까지 유지해야 합니다. [pySerial 3.5 read](https://pyserial.readthedocs.io/en/latest/pyserial_api.html#serial.Serial.read)

첫 프레임 `A5 5A 02 01 11 22 36`은 `2+1+17+34=54=0x36`입니다. 7바이트를 2바이트·5바이트로 나눠 읽을 때 매번 새 파서를 만들면 복원하지 못합니다. 반대로 19바이트의 3프레임을 한 번에 읽고 첫 결과만 사용하면 나머지 2개를 잃습니다. [실행 코드](../../../예제_examples/실무검증_practical-validation/uart_ethernet/README.md)는 선택한 20가지 분할에서 동일한 3프레임을 확인합니다. payload에 A5 5A가 있어도 유효한 길이 안에서는 데이터로 유지합니다.

| 구분 | 새 사례의 결과 | 해석 |
| --- | --- | --- |
| checksum 36을 37로 바꾼 프레임 뒤 정상 프레임 |checksum 오류 1회, 후속 정상 payload를 복구합니다. |오류 검출과 재동기화를 함께 봅니다. |
| LEN을 FF로 바꾼 후보 뒤 정상 프레임 |길이 오류 1회, 다음 프레임을 복구합니다. |상한 밖의 길이를 계속 기다리지 않습니다. |
| LEN 8 후보 뒤 정상 7바이트, 총 10바이트 |필요한 13바이트를 기다리다가 명시적 만료 후 복구합니다. |허용 길이의 미완성 후보는 별도 만료 정책이 필요합니다. |
| payload 1122를 1221로 변경합니다. |같은 SUM8=36으로 수락합니다. |단순 합은 이 두 데이터를 구별하지 못합니다. |

`expire_partial()`은 호출자가 선언하는 만료 사건이며 실제 시계·UART timer를 실행하지 않습니다. 읽기 호출의 종료를 만료로 삼으면 정상 분할 데이터도 버릴 수 있습니다. 최대 프레임 전송 시간·드라이버 지연·응용 deadline을 구분해야 합니다. 8N1·115200 bit/s·idle 없음의 계산에서 7바이트는 약 0.608 ms, 최대 13바이트는 약 1.128 ms입니다. 장치·USB·스케줄러 지연의 실측값은 아닙니다.

잡음 100,000바이트 뒤 정상 최대 프레임을 넣었을 때 내부 staging buffer 최고값은 13바이트였습니다. 반환 목록과 외부 큐 용량까지 제한한 것은 아닙니다. UART의 overrun·baud·배선·parity·framing 오류는 이 호스트 모델에서 측정하지 않으며, 실제 raw bytes가 사라지는 상황은 하드웨어 상태와 드라이버 기록으로 별도 확인합니다. 정상/-O·의도적 변이와 관측 범위는 [검증 기록](../../../설계와검증사례_engineering-cases/검증기록_evidence/UART와UDP수신경계검증_20261021.md)에 연결합니다.



## English

### A byte stream is not a message stream

Sending `temperature=25` over UART does not guarantee one receive call returns the entire message. Data may arrive in fragments or several messages together. UART defines bit-level character boundaries; application framing defines message boundaries. Separate electrical signaling from higher-level data structure.

8N1 uses one start bit, eight data bits, no parity, and one stop bit. At $`B`$ bit/s, each character takes $`10/B`$ seconds. With no idle gaps, $`115200`$ bit/s allows at most $`11520`$ data bytes/s before application overhead. Headers, CRC, and escaping reduce useful throughput. Baud is not universally synonymous with bit/s; this UART model sends one bit per symbol. [TI UART configuration](https://software-dl.ti.com/C2000/docs/C2000_driverlib_api_guide/f28p65x/build/html/modules/uart.html)

### What if a boundary byte appears inside the data?

The example uses `0x7E` as a delimiter. A payload or CRC byte equal to `0x7E` or `0x7D` is encoded as `0x7D` followed by the original byte XOR `0x20`. A receiver retains escape state across chunks and reconstructs the byte. This compact application format follows RFC1662 octet stuffing and FCS computation; it is not complete PPP with its address, control, protocol fields, and ACCM negotiation. [RFC1662 §4, Appendix C](https://www.rfc-editor.org/rfc/rfc1662.html)

The original state diagram above includes waiting, collecting, escaping, and dropping. Capacity overflow discards data until the next delimiter instead of growing memory without limit. An escape immediately followed by a delimiter aborts the incomplete frame. A wall-clock timeout for interrupted transmission is outside this byte-only model.

### CRC as polynomial arithmetic

A CRC treats bits as coefficients of a polynomial over $`GF(2)`$ and uses a remainder under a chosen generator. Coefficients are 0 or 1; addition and subtraction are XOR. Here

$$G(x)=x^{16}+x^{12}+x^5+1.$$

The polynomial alone does not identify a CRC variant. Input bit order, initial value, final XOR, and transmission order must agree too.

| Parameter | CRC-16/X-25, also CRC-16/IBM-SDLC, used here |
| --- | --- |
| Width / polynomial | 16 / `0x1021`, omitting the leading term |
| Initial value / final XOR | `0xFFFF` / `0xFFFF` |
| Input / output reflection | true / true |
| Reflected loop constant | `0x8408` |
| FCS wire order | Low byte first |
| Check for `123456789` | `0x906E` |
| Raw payload+FCS residue | `0xF0B8` before final XOR |

The right-shift implementation performs polynomial reduction in the reflected bit order. Eight iterations per byte give $`O(N)`$ time for $`N`$ bytes and $`O(1)`$ CRC state. A lookup table or hardware unit can improve throughput, but reflection, initialization, and finalization must still match.

### Detection is different from authentication

A CRC detects communication errors; an adversary can modify a message and recompute its CRC. Undetected error patterns also exist: XORing an error polynomial divisible by $`G(x)`$ preserves the remainder. A matching CRC therefore does not prove the content is correct or authentic. [Security and reliability boundaries](../../38-보안암호하드웨어신뢰_security-cryptography/해설_notes/오류를찾는것과공격을막는것_security-and-reliability-boundaries.md)

### Implementation and verification

For a maximum payload $`M`$, the parser's internal decoded buffer is bounded by $`M+2`$ bytes including CRC. Worst-case encoded size is at most $`2(M+2)+2`$ bytes. Multiply the actual wire length by $`10/B`$ for ideal 8N1 time. `FrameParser.feed()` yields frames incrementally instead of accumulating output internally; a caller collecting unlimited results creates its own unbounded storage.

Tests check the `123456789` value and RFC1662 residue, and independently compare CRC results using forward `binascii.crc_hqx()` plus bit reflection. They cover all 256 byte values, empty payloads, chunk boundaries, 80 single-bit errors, a 10,000-byte oversized input, recovery at the next delimiter, and aborted escapes. They do not measure UART baud tolerance, wiring quality, or FIFO overrun. [Execution guide](../../../예제_examples/공학기초_foundations/systems/README.md)

### A separate chunking and recovery example

The [UART case](../../../설계와검증사례_engineering-cases/UART의분할수신과재동기화_uart-stream-resync.md) uses an invented length-prefixed additive-checksum format, distinct from the escape/CRC format above. Twenty selected chunkings produce the same three literal frames. Bad lengths and sums recover at later markers; explicit partial-candidate expiry handles one stalled candidate. A collision remains accepted, exposing the simple sum's limitation. The 13-byte staging bound excludes returned frames and caller queues. The model does not execute a UART driver, hardware timer, or electrical link.



## 출처와 교차 확인 / Sources and cross-check

- TI UART API: 데이터 폭·parity·정지 비트 구성 / data width, parity, and stop-bit configuration.
- RFC 1662 (July 1994), §§3.1·4.2–4.3 and Appendix C: escape 방식·생성 다항식·FCS 잔여값 / escaping, generator, and FCS residue.
- 식의 처리율·최대 길이는 프레임 정의에서 직접 계산했으며 CRC는 별도 구현과 비교했습니다. / Throughput and maximum size follow from the defined format; CRC is compared against an independent implementation.
- pySerial 3.5 API의 timeout·`read(size)` 반환 설명을 2026-10-21에 확인했습니다. 새 SUM8 예제의 분할·복구·시간 계산은 자체 구성입니다. / pySerial's documented partial-read contract motivates the separate host example.
