# 인터페이스와 통신 | Interfaces & Communications

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

인터페이스는 전기적 신호와 연결 구조, 타이밍, 데이터 형식을 정의합니다. 같은 바이트를 주고받아도 전압 레벨이나 클록 조건이 맞지 않으면 통신이 성립하지 않습니다.

## 보드와 장치 사이

UART는 비동기 직렬 통신, SPI는 클록과 데이터 선을 사용하는 동기식 연결, I2C는 주소를 가진 장치들이 공유하는 2선식 버스입니다. I3C는 센서 연결 등을 위한 후속 인터페이스입니다. CAN·CAN FD는 중재와 오류 처리를 포함한 버스이고, USB는 호스트 중심의 장치 연결 체계를 갖습니다.

## 네트워크와 온칩 연결

Ethernet의 IEEE 802.3 규격은 데이터 링크 계층의 MAC과 물리 계층의 PHY를 함께 정의합니다. TCP/IP는 Ethernet 등 여러 링크 위에서 사용하는 프로토콜 계열입니다. Wi-Fi·BLE·Zigbee는 거리·전력·데이터율과 연결 방식이 다릅니다. LoRa는 무선 변조 기술이고, LoRaWAN은 이를 사용하는 통신 규약과 네트워크 구조를 정의합니다. MQTT·Modbus는 장치 데이터를 교환하는 응용 프로토콜입니다. [IEEE 802.3-2022의 범위](https://standards.ieee.org/ieee/802.3/10422/)와 [LoRa Alliance의 LoRa·LoRaWAN 구분](https://lora-alliance.org/about-lorawan/)을 참고합니다.

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

## 길이 필드가 가리키는 범위

payload는 해당 계층의 헤더를 뺀 내용입니다. 같은 바이트열도 Ethernet·IP·UDP 중 어느 계층을 보느냐에 따라 payload의 범위가 달라집니다. 캡처 버퍼의 끝까지를 모두 응용 데이터로 읽으면 Ethernet padding까지 결과에 붙을 수 있습니다. padding은 최소 프레임 크기를 맞추는 채움 바이트이며 IP의 Total Length에 포함되지 않습니다. [RFC 894의 Frame Format](https://www.rfc-editor.org/rfc/rfc894)에서 이 범위를 설명합니다.

IPv4 옵션·UDP Options·VLAN·터널이 없고 IP 단편화도 없다고 정한 계산 예입니다. IPv4 헤더를 20바이트, UDP 헤더를 8바이트로 두고 응용 값 4바이트를 보냅니다. IP Total Length는 32, UDP Length는 12입니다. Ethernet 데이터 필드를 최소 46바이트로 맞추면 IP 바깥에 14바이트가 남습니다.

```python
ip_header, udp_header, data = 20, 8, 4  # 쉼표 대입으로 예제의 바이트 수를 저장합니다.
udp_length = udp_header + data  # UDP 길이는 헤더와 응용 데이터를 포함합니다.
ip_total = ip_header + udp_length  # IP 전체 길이는 이 예제에서 32입니다.
padding = max(0, 46 - ip_total)  # max는 큰 값을 고르며 부족한 길이만 채웁니다.
captured = 14 + ip_total + padding  # VLAN 없는 헤더 14바이트를 더하며 FCS는 제외합니다.
wrong_data = captured - 14 - ip_header - udp_header  # 버퍼 끝까지 읽는 오류는 padding도 셉니다.
print(udp_length, ip_total, padding, captured)  # 12 32 14 60입니다.
print(wrong_data, udp_length - udp_header)  # 잘못 계산한 18과 올바른 4를 비교합니다.
print(1500 - ip_header - udp_header)  # IP MTU 1500을 가정하면 응용 공간은 1472입니다.
```

MTU는 이 계산에서 한 번에 담는 IP 패킷의 상한입니다. 1,500바이트가 모두 응용 공간은 아니며, 옵션·터널 등이 있으면 남는 공간이 달라집니다. 위 수치는 프레임 전송률이나 네트워크 지연의 측정값이 아닙니다. 실제 캡처에는 FCS의 포함 여부, VLAN과 드라이버의 처리 방식도 확인해야 합니다.

IPv4의 IHL은 32비트 단위의 헤더 길이이고, UDP Length의 최소값은 헤더 크기인 8입니다. [RFC 791 §3.1](https://www.rfc-editor.org/rfc/rfc791.html#section-3.1)과 [RFC 768 Fields](https://www.rfc-editor.org/rfc/rfc768)를 근거로 계층별 길이를 계산합니다. [RFC 9868 §21](https://www.rfc-editor.org/rfc/rfc9868.html#section-21)은 UDP 끝과 IP 끝 사이 surplus area를 UDP Options에 사용하도록 정의합니다. 따라서 IP payload가 UDP Length보다 길다는 이유만으로 모든 패킷을 잘못된 것으로 단정하지 않습니다. Ethernet padding은 IP 바깥, 이 surplus area는 IP 안쪽이라는 차이도 있습니다.

| 수신 단계 | 분리해서 확인할 조건 |
| --- | --- |
| 원시 Ethernet 캡처 | 캡처된 바이트 수와 각 헤더가 요구하는 길이를 함께 검사합니다. |
| IPv4 해석 | 헤더 길이·Total Length·단편화 상태와 지원 범위를 구분합니다. |
| UDP 해석 | 헤더·길이·checksum 상태를 보고 응용 데이터 범위를 정합니다. |
| socket 수신 | 원시 Ethernet 캡처와 달리 OS가 전달한 응용 데이터의 경계를 읽습니다. |
| 응용 값 사용 | 순번·단위·신선도와 요청의 성공 여부를 별도로 판단합니다. |

[UART 분할 수신 사례](../../설계와검증사례_engineering-cases/UART의분할수신과재동기화_uart-stream-resync.md)와 [Ethernet·UDP 길이 사례](../../설계와검증사례_engineering-cases/이더넷프레임의길이와UDP경계_ethernet-ipv4-udp.md)는 바이트 스트림과 데이터그램의 경계를 비교합니다. 링크가 연결되어 있다는 관측과 응용 메시지를 올바르게 읽었다는 판정은 다른 단계입니다.

## English

An interface defines electrical signals, topology, timing, and data format. Exchanging the same bytes still requires compatible voltage levels and clock conditions.

### Between boards and devices

UART provides asynchronous serial communication. SPI uses clock and data lines for synchronous transfers. I2C is a shared two-wire bus with addressed devices, and I3C extends the interface for uses such as sensor connections. CAN and CAN FD include arbitration and error handling. USB uses a host-centered device architecture.

### Networks and on-chip links

IEEE 802.3 Ethernet defines both the data-link MAC and the physical-layer PHY. TCP/IP operates over Ethernet and other links. Wi-Fi, BLE and Zigbee differ in range, power, data rate and connection design. LoRa is a radio modulation technology; LoRaWAN defines a protocol and network architecture that use it. MQTT and Modbus are application protocols for exchanging device data. See the [IEEE 802.3-2022 scope](https://standards.ieee.org/ieee/802.3/10422/) and the [LoRa Alliance distinction](https://lora-alliance.org/about-lorawan/).

AXI, AHB, and APB connect components inside an SoC. PCIe is a high-speed serial link, DDR is a memory interface, and MIPI covers a family of interfaces including display and camera links. Bandwidth measures data transferred per unit time; latency measures time from a request to its result. Protocol overhead and flow control make useful throughput different from nominal link speed.


### CAN delivery and application validity

The same bytes `34 12` decode to 4,660 in little-endian and 13,330 in big-endian. A scale of 0.01 yields 46.60 and 133.30, so a range check alone can miss a byte-order error. Application validity also checks frame identity/type, length, units, sequence and age. Only a valid frame refreshes the last-valid-reception timestamp. These are constructed examples rather than CAN hardware measurements.

### Concepts, derivations, models, and verification

[Foundations reading guide](../../공학기초_foundations/README.md#english)

- [UART framing and CRC](해설_notes/바이트가메시지가되려면_framing-uart-crc.md#english)


### Lengths at different layers

In a constructed IPv4/UDP example without options or fragmentation, four application bytes give UDP Length 12 and IP Total Length 32. Ethernet padding adds 14 bytes to a minimum 46-byte data field. A raw buffer length of 60, excluding FCS and VLAN, does not make the application payload 18 bytes. The assumed IP MTU of 1500 leaves 1472 bytes with 20-byte IPv4 and eight-byte UDP headers. RFC 9868 additionally defines a UDP Options surplus area inside IP; this differs from Ethernet padding outside IP.

## 심화 해설 | Advanced article

- [I2C 레지스터 읽기: repeated START와 마지막 NACK](해설_notes/I2C묶음전송_i2c-combined-transactions.md) · [English](해설_notes/I2C묶음전송_i2c-combined-transactions.md#english)
