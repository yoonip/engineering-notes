# SPI·I2C 전송 경계 검사 / SPI and I2C transaction-boundary examples

실제 장치 없이 표준 라이브러리 Python으로 논리 파형과 전송 순서를 만듭니다. 정상 경로를 리터럴 기대값과 비교하고, 의도적인 오류와 구현 변이를 검출합니다. SPI controller·I2C adapter·GPIO·Linux driver를 실행하거나 실제 메모리에 쓰지 않습니다.

## 실행

이 폴더에서 매번 새 결과 폴더를 지정합니다. 확인한 환경은 Windows AMD64·Python 3.12.14입니다.

```powershell
python -B run_cases.py --output C:/temp/serial-review-new
python -B -O run_cases.py --output C:/temp/serial-review-optimized-new
```

외부 패키지는 필요하지 않습니다. `-B`는 Python 바이트코드 캐시를 남기지 않으며 `-O`에서도 코드의 `check()` 검사는 사라지지 않습니다. `python`이 Store 별칭으로 연결된 Windows에서는 실제 Python 실행 파일 경로를 사용합니다.

결과 JSON은 원시 합성 SPI 사건·수신값·I2C trace·의도적인 오류·입력 예외와 Python·OS·명령·시각·소스/입력 SHA-256을 기록합니다. 정상 검사가 기대와 같으면 PASS·종료0, 계약 불일치나 예상 밖 예외는 ERROR·1, 기존 출력 폴더 등 CLI 오류는2입니다. 이전 결과를 덮어쓰지 않습니다.

## 모델과 확인 범위

| 대상 | 실행한 내용 | 구현하지 않은 범위 |
| --- | --- | --- |
| SPI | W25Q64JV Rev.C의 Standard SPI 0Bh 일부, mode0, 56/48클록, CS 분리, dummy offset, 자체 표본 지연 | 다른 opcode·Dual/Quad/DTR·용량 끝 순환·보호·BUSY·전원·실물 timing |
| I2C | 24LC256 읽기 일부, 내부 주소2바이트, STOP 사이 pointer 변경, NACK4단계, 마지막 NACK/ACK, 주소 순환 | EEPROM 쓰기·busy·ACK polling·adapter·arbitration·실물 timing |
| Open-drain | release/LOW의4조합과 START 전 SDA/SCL stuck-low | RC 상승·threshold·충돌 전류·GPIO bus-clear·자동 복구 |

[run_cases.py](run_cases.py)가 모델과 검사기이며 [bus_inputs.json](bus_inputs.json)에 직접 정한 메모리·기대 bytes·trace·clock 수를 적었습니다. SPI의 앞5바이트 FF는 유효하지 않은 구간을1로 읽는 자체 가정이며 실제 장치의 보증 응답이 아닙니다. mode0/3의 표본 edge는 같지만 전체 mode3 파형은 생성하지 않습니다.

I2C의 C2는 다른 요청이 STOP 경계에 들어간다는 자체 일정입니다. 두 실제 controller의 동시 실행이 아닙니다. STOP만 있고 C2가 없으면 모형의 pointer와 A55A는 유지됩니다. 기존 내부 주소1바이트 예제의45클록과 새 EEPROM 주소2바이트의54클록을 구분합니다.

## 의도적인 변이

```powershell
python -B run_cases.py --mutation spi-no-dummy --output C:/temp/serial-spi-mutation-new
python -B run_cases.py --mutation i2c-final-ack --output C:/temp/serial-i2c-mutation-new
```

두 명령은 의도적으로 ERROR·1이 나와야 합니다. 첫 변이는 master의 전송 길이가 아니라 장치 모형의 dummy 요구를8에서0으로 바꿉니다. 정상 RX 리터럴과 달라져 검출합니다. 실제 master의 클록 부족은 별도의48클록·8유효표본 대조이고, 수신 위치 오류는 wrong_offset 대조입니다.

둘째 변이는 정상 read 마지막의 controller NACK를 ACK로 바꿉니다. A55A는 같아도 전체 trace가 달라 검출합니다. 변이 결과를 정상 모형의 통과 결과와 혼합하지 않습니다.

## 원인과 검증 기록

- [SPI 선택선·dummy·edge](../../../설계와검증사례_engineering-cases/SPI의선택선과더미클록_spi-cs-dummy-edges.md)
- [I2C 묶음 읽기와 NACK](../../../설계와검증사례_engineering-cases/I2C의묶음읽기와NACK_i2c-combined-read.md)
- [2026-10-21 실행 환경·해시·결과](../../../설계와검증사례_engineering-cases/검증기록_evidence/SPI와I2C전송경계검증_20261021.md)

## English

These deterministic software fixtures model a narrow W25Q64JV Fast Read and 24LC256 read subset. Literal oracles separate CS/dummy/edge faults, pointer interference after STOP, and NACK roles. Normal and optimized execution, two deliberate failing mutations, nine input exceptions, and existing-output refusal are checked. No physical bus, kernel-driver, GPIO, or electrical validation is claimed.
