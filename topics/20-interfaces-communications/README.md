# Interfaces & Communications

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

인터페이스는 전기적 신호, 연결 구조, 타이밍, 데이터 형식의 약속을 묶는다. 같은 바이트를 주고받아도 전압 레벨이나 클록 조건이 맞지 않으면 통신이 성립하지 않는다.

## 보드와 장치 사이

UART는 비동기 직렬 통신, SPI는 클록과 데이터 선을 사용하는 동기식 연결, I2C는 주소를 가진 장치들이 공유하는 2선식 버스다. I3C는 센서 연결 등을 위한 후속 인터페이스다. CAN·CAN FD는 중재와 오류 처리를 포함한 버스이고, USB는 호스트 중심의 장치 연결 체계를 갖는다.

## 네트워크와 온칩 연결

Ethernet은 유선 네트워크의 링크 계층 기술이고 TCP/IP는 그 위에서 통신을 구성하는 프로토콜 계열이다. Wi-Fi·BLE·Zigbee·LoRa는 거리·전력·데이터율과 네트워크 구조가 다르다. MQTT·Modbus는 장치 데이터를 교환하는 응용 프로토콜이다.

AXI·AHB·APB는 SoC 내부 구성요소의 연결에 쓰인다. PCIe는 고속 직렬 링크, DDR은 메모리 인터페이스, MIPI는 디스플레이·카메라 등을 포함한 인터페이스 규격 계열이다. 대역폭은 단위 시간의 전송량이고, 지연은 요청에서 결과까지 걸리는 시간이다. 프로토콜 오버헤드와 흐름 제어 때문에 명목 속도와 유효 전송률은 다르다.

## 관련 기술

UART, SPI, I2C, I3C, CAN/CAN-FD, USB, Ethernet, PCIe, MIPI, DDR, AXI/AHB/APB, MQTT, Modbus, BLE, Wi-Fi, Zigbee, LoRa

## 참고 자료

- [Arm documentation](https://developer.arm.com/documentation)
- [Zephyr introduction](https://docs.zephyrproject.org/latest/introduction/index.html)
