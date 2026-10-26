# I2C의 묶음 읽기와 NACK / I2C combined reads, NACK roles, and bus release

I2C에서 NACK를 모두 실패로 처리하면 정상적인 마지막 읽기를 실패로 기록할 수 있습니다. 반대로 주소 단계의 NACK 뒤에 예전 수신 버퍼를 반환하면 장치와 통신하지 못했는데도 그럴듯한 값이 남습니다. 이 사례는 24LC256의 random/sequential read 일부와 직접 정한 메모리를 사용해, 전송의 묶음·NACK 주체·전기적 release의 의미를 구분합니다. 실제 EEPROM·I2C adapter·Linux API를 실행한 기록은 아닙니다.

[코드](../예제_examples/실무검증_practical-validation/serial_buses/run_cases.py), [리터럴 기대 trace](../예제_examples/실무검증_practical-validation/serial_buses/bus_inputs.json), [실행 안내](../예제_examples/실무검증_practical-validation/serial_buses/README.md), [검증 기록](검증기록_evidence/SPI와I2C전송경계검증_20261021.md)을 연결합니다.

## 1. bus 주소와 메모리 내부 주소를 구분합니다

예제의 7비트 target 주소는 0x50입니다. wire 주소 바이트는 write 0xA0, read 0xA1입니다. CPU가 사용하는 API에 이미 이동한 0xA0을 7비트 주소로 넣는 경우는 입력 오류로 거부합니다. 이 값은 신호를 전달할 I2C target을 고르는 주소이고, EEPROM 내부 0x0012와 다릅니다.

24LC256은 내부 위치를 지정하는 주소 바이트 두 개를 사용합니다. random read에서 그 주소를 알려 준 뒤 repeated START로 방향을 바꾸고, sequential read로 다음 위치를 이어 읽을 수 있습니다. 마지막 데이터 뒤에는 controller-receiver가 NACK를 보내 종료합니다. [Microchip DS21203Q, §8.1~8.3·그림 8-1~8-3](https://ww1.microchip.com/downloads/en/DeviceDoc/21203Q.pdf)

자체 메모리 0x0012=A5·0x0013=5A를 읽는 기대 trace는 다음과 같습니다. C1은 요청자, TARGET은 응답자입니다. 응답 데이터는 실제 EEPROM에서 읽은 값이 아닙니다.

```text
C1: START → TX A0 → TARGET ACK
          → TX 00 → TARGET ACK → TX 12 → TARGET ACK
          → repeated START → TX A1 → TARGET ACK
TARGET:   TX A5 → C1 ACK → TX 5A → C1 NACK → C1 STOP
```

위 순서를 리터럴 목록으로 입력 JSON에 저장하고 생성 trace 전체와 비교합니다. 데이터 A5 5A만 비교하는 검사와 전송 경계·응답 주체까지 비교하는 검사를 나눕니다.

## 2. STOP 두 번과 repeated START는 같은 묶음이 아닙니다

의도적으로 분리한 경로는 내부 주소를 보낸 뒤 STOP으로 bus를 놓고 다음 START에서 읽습니다. 이 모형에서 STOP 자체가 내부 pointer를 0으로 지우지는 않습니다. 다른 요청이 없다면 A5 5A가 그대로 나옵니다. “STOP을 넣으면 모든 I2C 장치가 무조건 오독한다”는 설명은 하지 않습니다.

차이는 중간에 다른 요청이 들어갈 수 있는 경계입니다. 자체 일정에서 C1이 bus를 놓은 사이 C2가 같은 target의 pointer를 0x0020으로 지정합니다. 그 위치의 값은 C3·3C입니다. C1이 이어 읽으면 주소 0x0012를 원했는데 C3 3C를 받습니다. 이를 그대로 정상 값으로 쓰는 것이 재현한 오류입니다.

```python
trace.append('C1:STOP')  # 분리 경로는 bus를 놓는 경계를 만듭니다.
current = interloper_pointer  # 그 사이 들어온 자체 C2 요청이 내부 pointer를 바꿉니다.
trace.append('C1:START')  # C1의 다음 read는 바뀐 pointer를 사용합니다.
```

수정 경로는 주소 설정과 읽기를 repeated START로 묶어 이 중간 STOP을 만들지 않습니다. 프로그램은 두 실제 controller의 arbitration이나 동시 thread를 실행하지 않습니다. “STOP 경계에서만 C2를 넣는다”는 직접 정한 직렬 일정으로 값의 차이를 보여 줍니다. 단일 controller의 여러 소프트웨어 요청에도 장치 상태를 공유한다는 비슷한 질문이 생기지만, 실제 bus lock·driver 지원은 별도로 확인해야 합니다. [Linux 6.14 I2C Protocol, Combined transactions](https://www.kernel.org/doc/html/v6.14/i2c/i2c-protocol.html)

## 3. NACK의 주체와 위치를 기록합니다

NACK는 ACK 비트 시간에 선이 HIGH로 남는 응답입니다. 누가 직전 바이트의 receiver였는지를 함께 봐야 합니다. 주소·내부 주소를 보낸 C1에 대해 target이 NACK하는 것과, 마지막 데이터를 받은 C1이 NACK하는 것은 다른 사건입니다. [NXP UM10204 Rev.7.0, §3.1.6](https://cache.nxp.com/docs/en/user-guide/UM10204.pdf)

모형은 target NACK를 네 위치에 각각 주입하고 그 뒤 RX 데이터를 만들지 않습니다. 이는 실제 장치가 왜 NACK했는지를 설명하는 물리 모형이 아니라 호출자가 중단 경계를 지키는지 보는 검사입니다.

| target NACK 위치 | 그때까지의 clock | 수정 경로의 결과 |
| --- | --- | --- |
| write 주소 A0 | 9 | 주소 단계 실패를 기록하고 STOP합니다. |
| 내부 주소 상위 00 | 18 | data/address 단계 실패를 기록하고 STOP합니다. |
| 내부 주소 하위 12 | 27 | 불완전한 주소 지정 뒤 읽지 않습니다. |
| read 주소 A1 | 36 | 데이터 없음과 실패 위치를 돌려줍니다. |

잘못된 `faulty_cache_fallback`은 read 주소 NACK 뒤에 저장된 A5 5A를 돌려줍니다. 출력 bytes가 정상처럼 보여도 이번 요청으로 확인한 데이터가 아닙니다. 수정 경로는 상태·오류 위치와 빈 데이터를 함께 반환합니다. 실패한 요청의 값을 쓰지 않는다는 규칙을 데이터 해석 이전에 적용합니다.

다른 잘못된 경로는 trace에 NACK라는 단어가 하나라도 있으면 실패로 처리합니다. 정상 읽기도 끝에 `C1:NACK`가 있으므로 이 판정은 정상 결과를 실패로 바꿉니다. 반대로 마지막 byte에 ACK를 보내는 대조 경로는 A5 5A를 그대로 내지만 전체 trace는 기대값과 달라집니다. 이 경우 payload만 확인하면 종료 신호의 오류를 놓칩니다.

## 4. release는 HIGH를 강제로 출력한다는 뜻이 아닙니다

일반적인 양방향 I2C의 open-drain 연결에서는 장치가 LOW를 당기거나 선을 놓습니다. HIGH는 pull-up 경로에 의해 형성됩니다. 이 예제는 두 장치와 강제 stuck-low 조건의 논리 결과만 계산합니다. 특수한 단일 controller SCL 구성 등 모든 I2C 변형을 같은 전기 회로로 모델링하지 않습니다. [UM10204 §3.1.1·§3.1.16](https://cache.nxp.com/docs/en/user-guide/UM10204.pdf)

```python
return int(controller_release and target_release and not stuck_low)  # 모두 놓아야 이 이상 모형에서1입니다.
```

| controller | target | 이상적인 관측값 |
| --- | --- | --- |
| release | release | 1 |
| release | LOW | 0 |
| LOW | release | 0 |
| LOW | LOW | 0 |

controller가 release를 요청해도 target이나 다른 원인이 LOW를 유지하면 선은 LOW입니다. 코드의 SDA_STUCK·SCL_STUCK 입력은 START 전에 그 상태를 확인하고 clock 0·데이터 없음으로 반환합니다. 실제 원인은 장치의 상태, 손상·접촉, 핀 설정, 전원 경계 등으로 나누어 봐야 합니다. 이 모형만으로 원인을 지목하거나 자동 복구를 보장하지 않습니다.

UM10204의 bus clear는 상태에 따른 별도 절차입니다. 여기서는 자동 9펄스 복구·전원 제어·GPIO 조작을 실행하지 않습니다. 선이 HIGH로 돌아온 시간, RC 상승시간·threshold·clock stretching·충돌 전류도 계산하지 않습니다.

## 5. 시간 계산과 주소 경계

정상 read는 write 주소, 내부 주소 두 바이트, read 주소, 데이터 두 바이트로 6개의 clocked byte입니다. 각 9클록이므로 54클록이고 400 kHz에서는 clock 구간만 135 µs입니다. 중간 C2의 pointer 설정 3바이트를 포함한 분리 경로는 81클록·202.5 µs입니다. START/STOP timing, stretch, bus free, 소프트웨어 지연은 별도입니다.

기존 [I2C 묶음 전송 글](../전자컴퓨터공학_ece/20-인터페이스통신_interfaces-communications/해설_notes/I2C묶음전송_i2c-combined-transactions.md)의 내부 주소 1바이트 예제는 45클록입니다. 어느 쪽이 맞는지의 문제가 아니라 장치의 내부 주소 폭이 다릅니다.

24LC256의 sequential read는 마지막 0x7FFF 뒤에 0x0000으로 돌아가는 경계가 있습니다. 자체 메모리에 0x7FFF=66, 0x0000=99를 넣고 2바이트 결과 66 99와 비교합니다. 전체 EEPROM 내용·쓰기 수명·page write·busy 시간·ACK polling은 구현하지 않았습니다.

## 6. 검증기가 잘못된 구현도 거부하는지 봅니다

정상 경로는 독립적인 trace·bytes·clock 수와 비교하고, NACK 4개 위치·마지막 ACK 대조·open-drain 4조합·SDA/SCL stuck·pointer 순환을 별도로 확인했습니다. 잘못된 입력 검사는 7비트 범위를 넘는 주소, 음수 pointer, 알 수 없는 NACK 위치 등을 `InputError`로 구분합니다.

`--mutation i2c-final-ack`는 정상 경로의 마지막 NACK를 ACK로 바꾸는 변이입니다. A5 5A 자체는 같지만 고정 trace 기대값이 달라져 ERROR·AssertionError·종료 1입니다. 값을 맞춰 반환했다고 전송 경계까지 확인됐다는 결론을 피하기 위한 검사입니다.

```powershell
python -B run_cases.py --mutation i2c-final-ack --output C:/temp/serial-i2c-mutation-new
```

오류를 재현한 결과와 실패를 검출한 실행기를 구분하고, 정상·변이 결과 JSON을 새 폴더에 보존합니다. 회로·kernel adapter가 없더라도 재현할 수 있지만 실제 장치의 timing·driver 오류를 확인한 것은 아닙니다.

## 확인 문제

1. STOP 뒤 다른 요청이 없으면 이 모델의 pointer도 반드시 사라질까요?
2. read 주소 NACK와 마지막 데이터 뒤 controller NACK는 같은 실패일까요?
3. controller가 선을 release하면 물리 선이 반드시 즉시 HIGH일까요?

답: 1. 아닙니다. 이 사례는 중간에 pointer를 바꾼 다른 요청의 영향을 분리합니다. 2. 아닙니다. 앞은 읽기 주소의 거부이고 뒤는 정상적인 읽기 종료입니다. 3. 아닙니다. 다른 장치가 LOW를 유지할 수 있고 실제 상승에는 전기적 조건도 작용합니다.

## English

An invented schedule around a 24LC256 read subset exposes pointer interference after STOP, while preserving the pointer when no other request intervenes. Target NACKs abort without data; the controller's final NACK ends a normal read. A full-trace oracle catches a wrong final ACK even when payload bytes match. Open-drain truth checks and stuck-low inputs do not establish physical recovery or electrical timing.

## 출처와 읽은 범위

2026-10-21에 NXP UM10204 Rev.7.0(2021-10-01) §3.1.1·§3.1.4~6·§3.1.16, Microchip DS21203Q(©2010) §8.1~8.3·그림 8-1~8-3, Linux 6.14 I2C Protocol의 Combined·Modified transactions를 읽었습니다. 실제 데이터 값·C2 일정·의도적인 결함은 자체 구성입니다. 보존한 구판의 동작 설명을 최신 제품 전체의 전기 사양으로 옮기지 않았습니다.
