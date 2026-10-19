# I2C 레지스터 읽기: repeated START와 마지막 NACK

[분야 안내](../README.md) · [실행 예제](../../../예제_examples/심화_advanced/systems/advanced_models.py) · [독립 테스트](../../../예제_examples/심화_advanced/systems/test_advanced_models.py) · [실행 안내](../../../예제_examples/심화_advanced/systems/README.md)

## 한국어

### 주소를 쓴 뒤 읽는 이유

센서의 “온도 레지스터 0x12를 읽는다”는 동작은 CPU 메모리의 주소 0x12를 읽는 것과 다릅니다. I2C target에 먼저 내부 레지스터 번호를 알려 주고, 이어서 데이터 방향을 바꿔 bytes를 받아야 하는 장치가 많습니다. 이 내부 번호와 실제 bus 주소는 별개입니다. 레지스터 번호 크기와 auto-increment 여부도 장치의 데이터시트가 정합니다.

NXP UM10204는 START·STOP, ACK/NACK와 combined format을 정의합니다. repeated START는 STOP으로 bus를 놓지 않고 다음 주소·방향 단계로 이어 갑니다. Linux `i2c_transfer()`의 combined transaction도 메시지 사이 STOP 대신 START가 오는 구조를 표현합니다. 모든 adapter가 모든 조합을 지원하는 것은 아니므로 driver가 기능을 확인해야 합니다. [NXP UM10204 §3.1](https://www.nxp.com/docs/en/user-guide/UM10204.pdf), [Linux I2C protocol](https://docs.kernel.org/i2c/i2c-protocol.html)

### 7비트 주소와 전송 byte를 구분합니다

이 글은 7비트 target 주소 $`A`$만 다룹니다. 첫 address byte는 $`(A\ll1)\mathbin{\mathrm{OR}}R`$이고 R=0은 write, R=1은 read입니다. 예제 주소 0x50에서는 write byte 0xA0과 read byte 0xA1이 됩니다. API가 7비트 주소를 요구하는데 이미 이동한 0xA0을 넣으면 다른 주소를 지정합니다. reserved 주소와 10비트 addressing은 별도 규약입니다.

레지스터 0x12에서 두 byte를 읽는 논리 trace는 아래와 같습니다. 표의 ACK는 직전에 보낸 byte를 받은 쪽의 응답입니다.

| 순서 | controller의 동작 | 응답 주체 |
| --- | --- | --- |
| START, 0xA0 | target에 write 방향 요청 | target ACK |
| 0x12 | 내부 register pointer 지정 | target ACK |
| repeated START, 0xA1 | 같은 target을 read 방향으로 지정 | target ACK |
| 첫 데이터 수신 | 한 byte 더 필요함을 ACK로 알림 | controller ACK |
| 마지막 데이터 수신, STOP | 더 읽지 않음을 NACK로 알림 | controller NACK |

마지막 NACK는 실패로만 해석하면 안 됩니다. controller-receiver가 이 read를 끝내기 위해 보내는 정상 신호입니다. 반대로 주소를 보낸 뒤 target이 NACK하면 존재하지 않는 주소, 준비되지 않은 장치 등 다른 원인을 조사합니다. ACK 하나가 장치 내부 연산 완료까지 증명하는 것도 아닙니다.

### 전송 시간의 하한을 계산합니다

address write, register byte, address read, 데이터 N바이트에는 각각 8 data bit와 1 ACK/NACK clock이 필요합니다. 따라서 이 형식의 clocked bit 수는 $`9(N+3)`$입니다. N=2이면 45 clock이고 400 kHz에서 clock 구간만 112.5 μs입니다. START·STOP setup/hold, bus free 시간, clock stretching, 재시도와 소프트웨어 지연은 이 값에 포함하지 않습니다. 측정 시간이 이 하한보다 길다고 곧바로 오류인 것은 아닙니다.

repeated START가 사이 STOP을 없애더라도 장치 register가 항상 자동으로 증가하는 것은 아닙니다. 두 byte를 연달아 읽는 의미도 그 장치의 register map에서 확인해야 합니다. I2C의 open-drain 전기적 특성, pull-up과 rise time은 논리 trace만으로 검증할 수 없습니다.

### 실행과 검증 범위

`i2c_register_read()`는 임의로 고른 응답 bytes를 받아 위 이벤트 trace를 만듭니다. 실제 bus에서 읽은 값이 아니라 transaction 순서를 검증하는 모델입니다. 테스트는 전송 address bytes 0xA0·0x12·0xA1, 두 RX byte, 마지막 NACK와 STOP을 독립적인 기대 trace와 비교하고 clock 수 45를 확인합니다. 한 byte read도 바로 마지막 NACK를 사용하는지 검사합니다.

생성 시간과 trace 저장은 읽는 길이에 비례합니다. 실제 controller에서는 NACK 발생 위치, arbitration loss, timeout, bus stuck 복구와 adapter의 repeated START 지원을 함께 확인합니다. 이 예제는 software retry나 전기적 파형을 실행하지 않았으므로 oscilloscope나 logic analyzer 측정 결과로 표현하지 않습니다.

저장소 루트에서 실행합니다. 첫 명령은 입력과 계산 결과를 출력하고, 두 번째 명령은 이 디렉터리의 전체 테스트를 실행합니다.

```sh
python "예제_examples/심화_advanced/systems/demo.py" i2c
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## English

### Why a register read starts by writing

Reading a sensor's register 0x12 is not reading CPU memory address 0x12. Many I2C targets first receive an internal register pointer, then send bytes after a direction change. That internal pointer differs from the bus address. Pointer width and auto-increment are device-specific.

NXP UM10204 defines START/STOP, ACK/NACK, and combined formats. A repeated START continues the transaction without releasing the bus through STOP. Linux `i2c_transfer()` represents combined messages with START rather than STOP between them. Adapter support must be checked; not every adapter supports every combination. [NXP UM10204 §3.1](https://www.nxp.com/docs/en/user-guide/UM10204.pdf), [Linux I2C protocol](https://docs.kernel.org/i2c/i2c-protocol.html)

### Separate seven-bit addresses from transmitted bytes

This example uses seven-bit address $`A`$. The transmitted address byte is $`(A\ll1)\mathbin{\mathrm{OR}}R`$, with R=0 for write and R=1 for read. Address 0x50 therefore produces 0xA0 and 0xA1. Supplying an already shifted 0xA0 to an API expecting seven-bit addresses is incorrect. Reserved addresses and ten-bit addressing have separate rules.

For a two-byte read from register 0x12:

| Step | Controller operation | Response source |
| --- | --- | --- |
| START, 0xA0 | Address target for writing | Target ACK |
| 0x12 | Select internal register pointer | Target ACK |
| Repeated START, 0xA1 | Address same target for reading | Target ACK |
| Receive first byte | Request another byte with ACK | Controller ACK |
| Receive final byte, STOP | End reception with NACK | Controller NACK |

The final NACK is normal termination by the controller-receiver, not necessarily failure. A target NACK after addressing has different causes such as absence or temporary unavailability. ACK alone also does not establish completion of an internal device operation.

### Derive a timing lower bound

Write address, register pointer, read address, and N received bytes each require eight data clocks plus one ACK/NACK clock. This format therefore uses $`9(N+3)`$ clocked bits. Two data bytes require 45 clocks, or 112.5 μs at 400 kHz. START/STOP timing, bus-free intervals, stretching, retries, and software delay are additional costs.

Repeated START does not itself guarantee register auto-increment. The meaning of consecutive bytes comes from the target register map. Open-drain electrical behavior, pull-ups, and rise times cannot be verified from a logical trace.

### Execution and scope

`i2c_register_read()` accepts constructed response bytes and emits the event sequence. It validates ordering rather than reading a real bus. Tests independently expect address bytes 0xA0, 0x12, and 0xA1, two RX bytes, final NACK/STOP, and 45 clocks. A one-byte read must immediately terminate with NACK.

Generation time and trace storage scale with read length. Hardware validation additionally needs NACK position, arbitration loss, timeout, stuck-bus recovery, and repeated-START support. No retry implementation or electrical waveform is executed here, so these outputs are not oscilloscope or logic-analyzer measurements.

Run the following commands from the repository root. The first prints the input and computed observations; the second runs the complete test suite in this example directory.

```sh
python "예제_examples/심화_advanced/systems/demo.py" i2c
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## 출처 / Sources

- [NXP UM10204 Rev.7](https://www.nxp.com/docs/en/user-guide/UM10204.pdf): START·combined format·ACK/NACK / START, combined format, ACK/NACK
- [Linux: The I2C Protocol](https://docs.kernel.org/i2c/i2c-protocol.html): i2c_transfer와 combined transaction / combined transactions
