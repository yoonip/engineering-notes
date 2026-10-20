# 인터페이스와 통신 | Interfaces & Communications

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

인터페이스는 전기적 신호와 연결 구조, 타이밍, 데이터 형식을 정의합니다. 같은 바이트를 주고받아도 전압 레벨이나 클록 조건이 맞지 않으면 통신이 성립하지 않습니다.

## 보드와 장치 사이

UART는 비동기 직렬 통신, SPI는 클록과 데이터 선을 사용하는 동기식 연결, I2C는 주소를 가진 장치들이 공유하는 2선식 버스입니다. I3C는 센서 연결 등을 위한 후속 인터페이스입니다. CAN·CAN FD는 중재와 오류 처리를 포함한 버스이고, USB는 호스트 중심의 장치 연결 체계를 갖습니다.

## 네트워크와 온칩 연결

Ethernet은 유선 네트워크의 링크 계층 기술이고 TCP/IP는 그 위에서 통신을 구성하는 프로토콜 계열입니다. Wi-Fi·BLE·Zigbee·LoRa는 거리·전력·데이터율과 네트워크 구조가 다릅니다. MQTT·Modbus는 장치 데이터를 교환하는 응용 프로토콜입니다.

AXI·AHB·APB는 SoC 내부 구성요소의 연결에 쓰입니다. PCIe는 고속 직렬 링크, DDR은 메모리 인터페이스, MIPI는 디스플레이·카메라 등을 포함한 인터페이스 규격 계열입니다. 대역폭으로 단위 시간의 전송량을, 지연으로 요청에서 결과까지 걸리는 시간을 나타냅니다. 프로토콜 오버헤드와 흐름 제어 때문에 명목 속도와 유효 전송률은 다릅니다.

## CAN 수신 성공과 값의 유효성

CAN 컨트롤러가 프레임을 받았다는 사실만으로 응용 값까지 올바르다고 판단할 수는 없습니다. [SocketCAN 문서](https://docs.kernel.org/networking/can.html#how-to-use-socketcan)는 CAN에 기본 바이트 순서가 정해져 있지 않다고 설명합니다. 송신 측과 수신 측이 ID, 프레임 종류, 길이, 바이트 순서와 단위를 같은 규약으로 해석해야 합니다.

직접 구성한 예로, 두 바이트 `34 12`를 unsigned 16비트 값으로 읽습니다. unsigned는 음수 없이 0부터 값을 표현한다는 뜻입니다. 낮은 자릿수의 바이트가 먼저 오는 little-endian으로는 4,660이고, 높은 자릿수가 먼저 오는 big-endian으로는 13,330입니다. 단위를 0.01로 약속했다면 각각 46.60과 133.30이 됩니다. 둘 다 허용 범위 안에 들어가는 시스템에서는 범위 검사만으로 이 오류를 찾을 수 없습니다.

```python
payload = bytes.fromhex("34 12")  # bytes는 바이트열이며 fromhex는 16진수 문자열을 변환합니다.
little = int.from_bytes(payload, "little")  # int의 메서드로 낮은 자릿수 바이트부터 정수로 읽습니다.
big = int.from_bytes(payload, "big")  # 같은 바이트를 높은 자릿수부터 읽는 대조 경로입니다.
print(little, big)  # 쉼표로 나열한 두 값을 출력하며 결과는 4660 13330입니다.
print(f"{little * 0.01:.2f} {big * 0.01:.2f}")  # f문자열의 :.2f는 소수 둘째 자리까지 표시합니다.
```

| 관측 | 아직 확인할 조건 |
| --- | --- |
| 송신 API가 성공했습니다. | 호스트가 요청을 수락한 것인지 버스 전송까지 끝난 것인지 구분합니다. |
| 컨트롤러가 active로 돌아왔습니다. | 재시작 요청의 반환값과 실제 상태 전이, 이후 응용 데이터 도착을 구분합니다. |
| 같은 ID의 프레임을 받았습니다. | 표준·확장 ID, data·remote·error 구분, 길이와 신호 정의를 확인합니다. |
| 수치가 정상 범위입니다. | 바이트 순서·단위·순번·수신 시각을 확인합니다. 정상 범위의 오래된 값도 있을 수 있습니다. |

자체 시간 예제로 마지막 유효 수신이 1,000 ms, 현재가 1,050 ms, 허용 나이가 20 ms라면 나이는 50 ms여서 사용할 수 없습니다. 이때 잘못된 ID나 길이의 프레임이 도착했다고 마지막 유효 수신 시각을 갱신하면 장애가 숨겨집니다. 시간은 같은 단조 시계 기준으로 비교하며, 장치가 붙인 송신 시각과 호스트 수신 시각을 섞지 않습니다. 이 계산은 프레임 지연을 측정한 결과가 아니라 응용의 신선도 계약을 설명하는 예입니다.

[CAN 복구 정책](../../설계와검증사례_engineering-cases/CAN의ACK와복구정책_can-recovery-policy.md)과 [수신 계약의 오류 재현](../../설계와검증사례_engineering-cases/CAN수신값의형식과신선도_can-payload-contract.md)에서 각 조건이 실패할 때의 상태 변화를 코드와 연결합니다.

## 관련 기술

UART, SPI, I2C, I3C, CAN/CAN-FD, USB, Ethernet, PCIe, MIPI, DDR, AXI/AHB/APB, MQTT, Modbus, BLE, Wi-Fi, Zigbee, LoRa

## 참고 자료

- [Arm documentation](https://developer.arm.com/documentation)
- [Zephyr introduction](https://docs.zephyrproject.org/latest/introduction/index.html)


## 개념·유도·모델·검증

[기초부터 읽기](../../공학기초_foundations/README.md)

- [바이트가 메시지가 되려면: UART, 프레이밍과 CRC](해설_notes/바이트가메시지가되려면_framing-uart-crc.md)

## English

An interface defines electrical signals, topology, timing, and data format. Exchanging the same bytes still requires compatible voltage levels and clock conditions.

### Between boards and devices

UART provides asynchronous serial communication. SPI uses clock and data lines for synchronous transfers. I2C is a shared two-wire bus with addressed devices, and I3C extends the interface for uses such as sensor connections. CAN and CAN FD include arbitration and error handling. USB uses a host-centered device architecture.

### Networks and on-chip links

Ethernet provides wired link-layer communication, with the TCP/IP protocol family building communication above it. Wi-Fi, BLE, Zigbee, and LoRa differ in range, power, data rate, and network structure. MQTT and Modbus are application protocols for exchanging device data.

AXI, AHB, and APB connect components inside an SoC. PCIe is a high-speed serial link, DDR is a memory interface, and MIPI covers a family of interfaces including display and camera links. Bandwidth measures data transferred per unit time; latency measures time from a request to its result. Protocol overhead and flow control make useful throughput different from nominal link speed.


### CAN delivery and application validity

The same bytes `34 12` decode to 4,660 in little-endian and 13,330 in big-endian. A scale of 0.01 yields 46.60 and 133.30, so a range check alone can miss a byte-order error. Application validity also checks frame identity/type, length, units, sequence and age. Only a valid frame refreshes the last-valid-reception timestamp. These are constructed examples rather than CAN hardware measurements.

### Concepts, derivations, models, and verification

[Foundations reading guide](../../공학기초_foundations/README.md#english)

- [UART framing and CRC](해설_notes/바이트가메시지가되려면_framing-uart-crc.md#english)


## 심화 해설 | Advanced article

- [I2C 레지스터 읽기: repeated START와 마지막 NACK](해설_notes/I2C묶음전송_i2c-combined-transactions.md) · [English](해설_notes/I2C묶음전송_i2c-combined-transactions.md#english)
