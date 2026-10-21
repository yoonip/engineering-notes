# SPI의 선택선과 더미 클록 / SPI chip select, dummy clocks, and sampling edges

SPI에서 읽은 값이 한 바이트 밀리거나 모두 FF라면 바이트 순서부터 바꾸기 전에 명령·주소·대기·유효 데이터의 경계를 살펴야 합니다. 이 사례는 W25Q64JV의 Standard SPI Fast Read 0Bh 일부를 합성해, 잘못된 수신 위치·부족한 클록·CS 분리·표본 시점의 차이를 실행합니다. 실제 Flash·보드·Linux 드라이버의 통신 결과가 아니라 직접 만든 논리 파형입니다.

[실행 코드](../예제_examples/실무검증_practical-validation/serial_buses/run_cases.py), [리터럴 입력·기대값](../예제_examples/실무검증_practical-validation/serial_buses/bus_inputs.json), [실행 안내](../예제_examples/실무검증_practical-validation/serial_buses/README.md), [실행 기록](검증기록_evidence/SPI와I2C전송경계검증_20261021.md)을 함께 봅니다.

## 1. 읽기 한 번에 무엇을 보내는지 나눕니다

Winbond W25Q64JV Revision C의 0Bh는 명령 8비트, 주소 24비트, dummy 8클록 뒤에 데이터를 내보냅니다. dummy는 내부 준비를 기다리며 클록을 제공하는 구간이고 그때의 DO 값은 유효 데이터가 아닙니다. 03h Read Data와 0Bh Fast Read의 차이도 구분합니다. 이 글은 Dual·Quad·DTR·QPI나 다른 개정의 가변 dummy 설정을 모델링하지 않습니다. [공식 데이터시트, Read Data·Fast Read, 인쇄 27~28쪽](https://www.winbond.com/resource-files/w25q64jv%20spi%20%20%20revc%2006032016%20kms.pdf)

자체 메모리에서 주소 0x000012=18에 A5, 다음 주소에 5A를 넣습니다. 이 값은 실제 Flash에서 읽거나 써 넣은 내용이 아닙니다. 2바이트를 읽기 위해 전송하는 바이트열은 다음과 같습니다.

```text
TX: 0B | 00 00 12 | 00 | 00 00
    명령   주소      dummy  데이터 수신용 클록
RX: FF | FF FF FF | FF | A5 5A
    유효 데이터가 아닌 앞 5바이트 | 유효 데이터
CS: └─────────────────────────┘ 한 번의 LOW 구간
```

앞의 FF는 모델이 유효하지 않은 입력을 pull-up으로 1로 읽게 정한 결과입니다. 데이터시트가 dummy의 반환값을 FF로 보장한다는 뜻이 아닙니다. 실제 high-Z, bus 연결, pull-up, 드라이버가 어떤 값을 읽는지에 따라 달라질 수 있습니다. FF만으로 장치 부재나 배선 불량을 확정하지 않습니다.

## 2. dummy를 건너뛰는 것과 클록을 제공하는 것은 다릅니다

SPI는 읽을 때도 클록이 필요합니다. 전체 수신 버퍼에는 명령·주소 전송 중에 들어온 비트도 포함될 수 있습니다. 올바른 데이터 시작은 1+3+1=5바이트 뒤입니다. dummy 한 바이트를 생략한 위치 4에서 2바이트를 고르면 FF A5가 되어, 길이 자체는 2바이트인데 내용이 틀립니다.

```python
payload = normal['rx_hex'][10:14]  # hex는 바이트당 두 글자이므로 5바이트 뒤를 고릅니다.
bad_offset = normal['rx_hex'][8:12]  # 잘못된 경로는 dummy를 데이터 앞부분으로 읽습니다.
```

소프트웨어 슬라이스만 바꾸는 일과 전송 클록을 줄이는 일은 또 다릅니다. 7바이트 대신 `0B 00 00 12 00 00`의 6바이트만 보내면 총 48클록입니다. 장치는 처음 32클록을 명령·주소, 다음 8클록을 dummy로 사용하므로 데이터는 8클록, 즉 A5 하나만 나옵니다. “마지막 2바이트”를 취해도 부족한 두 번째 데이터의 클록이 생기지는 않습니다.

정상은 8+24+8+16=56클록입니다. 1 MHz라는 자체 가정에서는 클록 구간이 56 µs입니다. 16개의 유효 데이터 비트만 나누면 2/7≈28.57%가 payload 비트입니다. CS setup/hold·전송 간 지연·호스트 처리까지 포함한 실제 처리율은 이 계산과 다릅니다.

## 3. CS를 올리면 다음 바이트의 의미가 바뀝니다

CS는 여러 바이트가 같은 명령에 속한다는 경계입니다. 모델에서 명령·주소 4바이트 뒤에 CS를 HIGH로 올렸다 다시 내리면 장치의 명령 해석을 초기화합니다. 뒤의 `00 00 00`은 앞 명령의 dummy·수신 클록이 아니라 새 명령의 시작으로 보입니다. 이 부분 모형은 새 opcode 00을 지원하지 않으므로 유효 데이터 표본은 0이고 읽힌 두 바이트는 FF FF입니다.

Linux SPI 문서는 message를 여러 transfer로 구성할 수 있으며 CS의 유지·변경을 설명합니다. 두 개의 독립 API 호출이 하드웨어에서 하나의 CS 구간이라는 가정을 해서는 안 됩니다. 반대로 함수 호출을 하나로 합쳤다고 모든 controller가 요청한 타이밍을 지원한다고 단정하지 않습니다. [Linux 6.14 SPI, spi_message·spi_transfer·spi_sync](https://docs.kernel.org/6.14/driver-api/spi.html)

이 예제의 해결은 명령·주소·dummy·데이터를 같은 CS LOW 구간에 두고, 장치의 규약에 맞는 전체 클록을 제공하는 것입니다. 실제 구현에서는 controller의 CS 제어·DMA 분할·전송 간 지연·device 설정을 캡처와 함께 대조합니다.

## 4. 어느 edge에서 안정된 값을 읽는지 확인합니다

CPOL은 클록의 유휴 레벨, CPHA는 첫 번째·두 번째 전이 중 어느 쪽에서 표본을 얻는지 정합니다. 일반적인 mode 번호에서 0·3은 rising 표본, 1·2는 falling 표본입니다. 같은 rising 표본이어도 유휴 레벨과 첫 전이의 관계는 다릅니다. W25Q64JV 문서의 mode 0·3과 입력 rising·출력 falling 관계를 확인했습니다. 파형 생성기는 그중 mode 0만 구현하고 mode 3 전체 파형은 실행하지 않았습니다.

```python
return 'rising' if cpol == cpha else 'falling'  # 조건 표현식으로 이 조합의 표본 edge를 구합니다.
```

모형의 clock 주기는 1,000 ns입니다. MOSI는 rising 400 ns 전부터 고정하고, target의 DO는 falling 뒤 5 ns에 다음 비트로 바뀐다고 직접 정했습니다. 정상 수신은 rising에서 안정된 값을 읽습니다. 잘못된 대조 경로는 falling 뒤 10 ns에 읽어 이미 다음 비트로 바뀐 값을 취합니다. A5 5A의 비트열을 한 칸 앞당겨 읽은 결과는 4A B5입니다. 마지막 비트에는 다음 주소의 FF 첫 비트가 들어갑니다.

이것은 “CPHA가 틀리면 모든 실제 장비에서 항상 4A B5가 나온다”는 예측이 아닙니다. 실제 같은 edge의 출력 변화와 입력 표본에는 지연·setup/hold·전압·온도·배선이 개입합니다. 잘못된 edge에서도 우연히 같은 값이 보일 수 있습니다. 5 ns·10 ns는 데이터시트의 보증 한계가 아닌, 표본 시점이 달라지는 조건을 드러내기 위한 자체 가정입니다.

## 5. 실행 결과와 변이 검사

| 경로 | 실제 로컬 모형 결과 | 드러난 원인 |
| --- | --- | --- |
| 정상 56클록·CS 유지 | 유효 표본 16개, A5 5A | 명령·주소·대기를 지난 데이터입니다. |
| 수신 시작을 한 바이트 앞당김 | FF A5 | dummy를 데이터로 해석했습니다. |
| 전송을 48클록으로 줄임 | 유효 표본 8개 | 두 번째 데이터를 내보낼 클록이 부족합니다. |
| 주소 뒤 CS 분리 | 유효 표본 0개, FF FF | 명령의 연결이 끊겼습니다. |
| 자체 falling+10 ns 표본 | 4A B5 | 다음 비트를 읽는 시점으로 바뀌었습니다. |

입력 JSON에 바이트열·클록 수·edge 목록·payload를 리터럴로 적고 결과와 비교합니다. 기대 payload를 모델 함수를 다시 호출해 생성하지 않습니다. `--mutation spi-no-dummy`는 장치 모형에서 dummy를 없애는 의도적인 변이입니다. 이 잘못된 모형은 고정 RX 기대값을 만족하지 못해 ERROR·AssertionError·종료 1이 됩니다. 이 변이는 검증기가 잘못된 장치 모형을 거부하는지 확인합니다. 호스트의 클록 부족과 수신 위치 오류는 앞의 별도 대조로 확인합니다.

```powershell
python -B run_cases.py --output C:/temp/serial-review-new
python -B run_cases.py --mutation spi-no-dummy --output C:/temp/serial-spi-mutation-new
```

정상 결과와 의도적인 실패는 서로 다른 새 폴더의 JSON에 남깁니다. 실제 장비에 command를 보내거나 Flash의 쓰기·삭제를 수행하지 않습니다.

## 6. 현장에서 남길 자료

수신 숫자 외에 CS 전체 구간, 명령·주소 바이트, MOSI/MISO, SCK 유휴 레벨·표본 edge, dummy 수, 실제 클록 수, bus 폭, 펌웨어·controller 설정을 함께 남깁니다. CPU의 바이트 순서는 이 wire 상의 MSB-first 규칙·수신 버퍼 위치와 별개의 질문입니다.

부분 모형은 sparse map, 즉 일부 주소의 값만 지정한 사전을 사용합니다. 전원·BUSY·HOLD·WP·보호 상태·다른 opcode·용량 끝의 주소 순환·전기적 정격·신호 무결성·controller 지연을 구현하거나 검증하지 않습니다. 데이터에 맞춰 offset을 임의로 바꾸기보다 데이터시트의 명령 프레임을 기준으로 먼저 원시 파형의 구간을 표시합니다.

## 확인 문제

1. 명령 1·주소 3·dummy 1바이트 뒤의 2바이트를 수신하려면 몇 클록이 필요할까요?
2. 버퍼 위치를 바꾸면 부족한 수신 클록을 해결할 수 있을까요?
3. wrong-edge 예의 4A B5를 모든 실제 보드의 공통 결과로 예측해도 될까요?

답: 1. (1+3+1+2)×8=56클록입니다. 2. 안 됩니다. 장치가 유효 비트를 내보내도록 클록을 추가해야 합니다. 3. 안 됩니다. 여기서 정한 출력·표본 지연에서 얻은 결정적 결과입니다.

## English

A read-only Standard SPI subset of W25Q64JV Fast Read separates command/address/dummy/data clocks and CS continuity. Literal checks distinguish A55A from FFA5, a 48-clock short transfer, a split-CS transaction, and a constructed late-falling sample. Mode-0 waveforms use explicitly invented delays; no universal wrong-mode byte pattern or physical timing validation is claimed.

## 출처와 읽은 범위

2026-10-21에 W25Q64JV Revision C, 2016-06-03의 §4.1·§6.1·Read Data·Fast Read와 그림 14·16을 공식 PDF에서 읽었습니다. 현재 다른 개정·패키지·모드의 전체 사양으로 확장하지 않았습니다. Linux 6.14 SPI의 message·transfer·CS 관련 설명도 읽었습니다. 원도표를 전재하지 않고 자체 연결 구간과 논리 파형을 구성했습니다.
