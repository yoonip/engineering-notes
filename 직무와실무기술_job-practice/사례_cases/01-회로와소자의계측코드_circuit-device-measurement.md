# 회로·소자의 계측 코드와 원인 분석 | Circuit and device measurement code

[사례 목차](README.md) · [직무별 연결](06-직무별사례와담당범위_role-case-map.md) · [제품 회로의 기초](../04-제품회로와시스템검사_product-circuit-system-tests.md) · [코드 출처와 이용 조건](코드출처와이용조건_CODE_SOURCES.md)

회로 검사에서는 측정값이 달라졌다는 사실과 부품이 불량이라는 판단 사이를 조사해야 합니다. 배선·기준 전압·계측기 설정·디지털 통신 때문에 같은 부품도 다른 값으로 보일 수 있습니다. 여기서는 제조사 공개 코드로 그 경계를 읽습니다.

업무 상황과 원인 분리 절차는 회로·소자 평가의 관측 대상을 설명하는 학습 사례입니다. 코드의 실행문은 아래 고정 판본의 원문에서 가져왔으며, 각 줄에 한국어 설명을 붙였습니다. 수치 예제는 별도로 표시한 계산이고, 이번 작성에서 장비를 연결해 얻은 측정값은 없습니다.

## 1. 저항값을 판정하는 제품 회로 검사

### 업무와 장비

모바일·로봇·SSD 보드의 부품 평가나 입고 품질 업무에서, 지정한 조건으로 저항을 측정하고 규격과 비교하는 상황을 생각해 봅니다. 선택한 공개 코드는 Tektronix가 Keithley 2450용으로 제공한 전류 인가·전압 측정·저항 계산 예제입니다. 제품별 규격과 시험 조건을 설정하는 방법을 이해하는 사례입니다.

| 항목 | 이번 사례에서 확인하는 내용 |
| --- | --- |
| DUT | 저항 소자 또는 분리해 측정할 수 있는 저항 경로입니다. DUT는 device under test, 검사 대상입니다. |
| 장비 | Keithley 2450 SMU와 해당 연결 케이블입니다. SMU는 전압·전류를 인가하면서 응답을 측정하는 장비입니다. |
| 인가와 관측 | 원문은 전류 1 µA를 설정하고 전압과 실제 source readback 값을 취득합니다. |
| 원문의 판정값 | `29.5e3 < resistance < 30.5e3`입니다. 이 예제의 조건이며 다른 제품에 그대로 적용할 공통 규격은 아닙니다. |
| 남길 자료 | 시료 ID, 결선, 전류·전압 한계, 측정 범위, 원시 V·I, 저항값과 측정 상태입니다. |

옴의 법칙에서 `R = V/I`입니다. `V`는 전압, `I`는 전류, `R`은 저항입니다. 이상적인 30 kΩ에 1 µA가 실제로 흐르면 전압은 `30,000 × 0.000001 = 0.030 V`입니다. 이는 단위 관계를 설명하는 계산입니다. 실제 저항 판정에는 계측 정확도와 결선·온도 등의 조건도 들어갑니다.

compliance, 제한값은 인가할 수 있는 반대쪽 물리량의 한계입니다. 전류를 1 µA로 요청해도 부하 상태에 따라 설정한 전압 제한에 먼저 도달할 수 있습니다. 원문의 `source.readback`은 요청한 전류만 믿는 대신 실제 source 값을 사용하도록 설정합니다. 값 계산과 별도로 제한 상태·오류 상태도 확인해야 합니다. [2450 공식 사양의 Source Readback·Resistance Measurement Accuracy](https://www.tek.com/en/datasheet/smu-2400-graphical-sourcemeter/model-2450-touchscreen-source-measure-unit-smu-instrument)

### 제조사 Python 원문과 줄별 설명

- 출처: [Tektronix 공식 파일, 고정 commit](https://github.com/tektronix/keithley/blob/96f209329a4c0a995cc4f0a57d9e3d301a640d17/Instrument_Examples/Series_2400_Graphical/2450-SMU/Simple_SourceI_MeasureV_CalcR/source_i_measure_v_compute_r.py#L8-L48), 원본 8–48줄입니다.
- 원문을 소유한 조직: Tektronix, Inc.입니다. [Tektronix Sample Source Code License](licenses/Tektronix-Sample-License.txt)에 따라 Tektronix 제품과 함께 사용하는 범위로 제공됩니다.
- 아래에서는 빈 줄과 영어 설명 주석을 줄이고 한국어 줄 주석을 붙였습니다. 실행문의 순서·설정값·자원 문자열은 원문과 같습니다. 자원 문자열의 USB 식별자는 원문 장비의 예입니다.
- Python은 PC에서 실행되고, 문자열 안의 TSP 명령은 2450이 해석합니다. Python의 `write()`와 장비가 해석하는 `smu.source.func`는 서로 다른 계층입니다.

```python
import pyvisa  # import는 계측 통신 패키지를 불러옵니다.
rm = pyvisa.ResourceManager()  # ResourceManager()로 VISA 자원 관리 객체를 만듭니다.
SMU2450 = rm.open_resource("USB0::0x05E6::0x2450::04509653::INSTR")  # 장비 자원 문자열로 세션을 열며 원문의 USB 식별자를 유지했습니다.
SMU2450.write("reset()")  # write()로 TSP 초기화 명령 문자열을 장비에 보냅니다.
SMU2450.write("smu.source.func = smu.FUNC_DC_CURRENT")  # 장비의 인가 기능을 직류 전류로 설정합니다.
SMU2450.write("smu.source.level = 1e-6")  # 1e-6은 1 µA이며 인가 전류 설정값입니다.
SMU2450.write("smu.source.vlimit.level = 0.1")  # 장비의 전압 제한을 0.1 V로 설정합니다.
SMU2450.write("smu.source.readback = smu.ON")  # 인가값의 실제 readback 사용을 켭니다.
SMU2450.write("smu.measure.func = smu.FUNC_DC_VOLTAGE")  # 장비의 측정 기능을 직류 전압으로 설정합니다.
SMU2450.write("smu.measure.range = 0.2")  # 전압 측정 범위를 0.2 V로 고정합니다.
SMU2450.write("smu.source.output = smu.ON")  # 출력을 켜서 시료에 인가하며 장비 명령입니다.
SMU2450.write("smu.measure.read()")  # 장비에서 한 번 측정해 버퍼에 결과를 넣습니다.
SMU2450.write("smu.source.output = smu.OFF")  # 측정 뒤 출력을 끕니다.
voltage = float(SMU2450.query("printbuffer(1, 1, defbuffer1.readings)"))  # query()의 문자열 응답을 float()로 실수 전압으로 바꿉니다.
current = float(SMU2450.query("printbuffer(1, 1, defbuffer1.sourcevalues)"))  # 버퍼의 실제 source 값을 실수 전류로 읽습니다.
resistance = voltage / current  # 나눗셈 /로 R=V/I를 계산하며 유효 전류가 필요합니다.
print(resistance)  # print()로 계산한 저항을 출력합니다.
if not 29.5e3 < resistance < 30.5e3:  # 연쇄 비교와 not으로 원문의 열린 허용 구간 밖인지 검사합니다.
    SMU2450.write("beeper.beep(0.5, 220)")  # if의 들여쓴 블록으로 비프 명령을 보냅니다.
SMU2450.close()  # 계측기 통신 세션을 닫습니다.
rm.close()  # 자원 관리 객체를 닫습니다.
```

`import`는 다른 모듈의 기능을 사용할 이름을 불러옵니다. `pyvisa`는 계측 통신 자원에 접근하는 Python 패키지입니다. `=`는 값을 변수에 저장하고, `.`은 객체의 기능이나 속성에 접근합니다. `()`는 함수를 호출하며, 따옴표는 전송할 문자열을 나타냅니다. `1e-6`은 `1 × 10⁻⁶`이라는 지수 표기입니다.

원문의 마지막 비교는 열린 구간입니다. 따라서 정확히 29.5 kΩ 또는 30.5 kΩ이면 조건 밖으로 처리되어 비프 명령이 실행됩니다. 제품 규격이 `이상·이하`를 요구한다면 이 예제의 비교 연산자를 그대로 승인 기준으로 가져오면 안 됩니다. 원문은 중간 실패에 대한 `try/finally` 정리 절차를 포함하지 않는 짧은 예제입니다. 장비 출력 종료와 통신 오류 기록은 시험 절차에서 함께 검토할 항목입니다. [Python의 비교 연산](https://docs.python.org/3/reference/expressions.html#comparisons), [오류와 finally](https://docs.python.org/3/tutorial/errors.html#defining-clean-up-actions)

### 값이 벗어났을 때의 해석

| 관측한 상태 | 가능한 설명 | 원인을 나누는 확인 |
| --- | --- | --- |
| V·I가 유효하고 반복해도 R이 규격 밖입니다. | 부품값·회로 경로·온도 조건이 다를 수 있습니다. | 시료 ID·저항 표기·분리 측정 조건을 확인하고 기준 시료와 같은 결선으로 비교합니다. |
| 전류 readback이 요청값과 다르고 전압 제한 상태입니다. | 부하·접촉·개방 때문에 요청 전류를 유지하지 못했을 수 있습니다. | 제한 상태와 실제 V·I, 배선·접촉을 먼저 확인합니다. 단순 R 계산 성공과 유효 측정을 구분합니다. |
| 값이 흔들리거나 케이블을 건드릴 때 급변합니다. | 접촉·잡음·접지·측정 범위가 후보입니다. | 기준 저항으로 재측정하고 결선·케이블·측정 환경을 한 가지씩 바꿉니다. |
| 응답이 없거나 문자열을 숫자로 바꾸지 못합니다. | 자원 주소·명령 모드·통신·장비 오류가 후보입니다. | 장비 식별 응답과 지원 명령을 확인합니다. 이 상태는 부품의 저항 FAIL과 나누어 기록합니다. |

최종 결과에는 최초 측정·재결선·재측정의 이력을 함께 남깁니다. 기준 시료에서도 문제가 재현되면 DUT 교체보다 측정 경로 조사가 먼저입니다. 판정 경계와 불확도는 [검사 결과의 판정과 기록](../11-검사결과의판정과기록_test-decisions-evidence.md)에 연결합니다.

## 2. 커넥터·접속 경로의 작은 저항을 측정하는 검사

### 2선식과 4선식의 차이

작은 저항에서는 측정선의 저항이 DUT의 저항과 비슷해질 수 있습니다. 2선식은 전류를 흘리는 선과 전압을 읽는 선을 공유합니다. 4선식, Kelvin 측정은 전류를 흘리는 Force 선과 DUT 양단 전압을 읽는 Sense 선을 나눕니다. 전압을 읽는 입력에 흐르는 전류가 작아, Force 선의 저항성 전압 강하 영향을 줄일 수 있습니다.

예를 들어 DUT를 1.00 Ω, 왕복 측정선의 저항을 0.20 Ω으로 가정하면 단순 2선식 계산은 1.20 Ω이 됩니다. DUT 대비 20% 차이입니다. 이 수치는 설명용 회로 계산입니다. 실제 케이블·접촉·장비 오차를 측정한 결과는 아닙니다.

| 항목 | 관측·설정할 내용 |
| --- | --- |
| 적용 업무 | 보드 커넥터·케이블·패키지의 접근 가능한 접속 경로를 전기적으로 비교하는 업무입니다. |
| 계측 구성 | 2450 SMU의 Force/Sense 결선과 접촉 치구입니다. 패키지 내부 구조의 공간적 위치는 필요에 따라 X선·단면 분석 등 다른 관측과 연결합니다. |
| 측정량 | 저항, 반복 산포, 상대 시간, 시험 전후 변화입니다. 원문의 `READ, REL`은 읽기값과 상대 시간을 요청합니다. |
| 구분할 원인 | DUT 접속 저항, 치구 접촉 저항, 열기전력, 전류에 따른 자가 발열입니다. |

열기전력은 서로 다른 재료와 온도 차이 때문에 생길 수 있는 작은 전압입니다. DUT에 10 mA를 흘리고 20 µV의 추가 전압을 함께 읽었다고 가정하면 `20 µV / 10 mA = 0.002 Ω`가 저항값에 섞입니다. 원문의 offset compensation은 인가 조건이 다른 두 측정을 이용하여 이런 오프셋 영향을 줄이는 기능입니다. [2450 User's Manual Rev. E, 5장 Measuring low-resistance devices](https://download.tek.com/manual/2450-900-01E_Aug_2019_User.pdf), [공식 저저항 예제의 설명과 설정](https://github.com/tektronix/keithley/blob/96f209329a4c0a995cc4f0a57d9e3d301a640d17/Instrument_Examples/Series_2400_Graphical/2450-SMU/Measuring_Low_Resistance_Devices/Measuring_Low_Resistance_Devices_SCPI.py#L192-L225)

### 제조사 원문의 설정 부분

Copyright Tektronix, Inc. 아래는 같은 공식 저장소의 `Measuring_Low_Resistance_Devices_SCPI.py` 213–225줄입니다. 영어 줄 주석을 한국어 설명으로 바꾼 발췌이며 실행문과 문자열은 유지했습니다. 앞부분의 socket 연결과 `instrument_write()`·`instrument_query()` 정의가 필요한 문맥 발췌입니다. 전체 원본과 [사용 조건](licenses/Tektronix-Sample-License.txt)을 함께 확인하실 수 있습니다.

```python
instrument_write(s, "*RST")  # 보조 함수를 호출해 SMU를 초기화합니다.
instrument_write(s, "TRIG:LOAD \"SimpleLoop\", 100")  # 문자열 안의 이스케이프 따옴표로 100회 SimpleLoop 템플릿을 선택합니다.
instrument_write(s, "SENS:FUNC \"RES\"")  # 장비의 측정 기능을 저항으로 설정합니다.
instrument_write(s, "SENS:RES:RANG:AUTO ON")  # 저항 측정의 자동 범위를 켭니다.
instrument_write(s, "SENS:RES:OCOM ON")  # 열기전력 등 오프셋의 영향을 줄이는 기능을 켭니다.
instrument_write(s, "SENS:RES:RSEN ON")  # remote sense, 4선식 감지를 켭니다.
instrument_write(s, "DISP:SCR SWIPE_GRAPh")  # 장비 화면을 그래프 화면으로 전환합니다.
instrument_write(s, "OUTP ON")  # SMU 출력을 켭니다.
instrument_write(s, "INIT")  # 설정한 trigger model의 측정을 시작합니다.
instrument_write(s, "*WAI")  # 앞선 장비 동작의 완료를 기다리도록 요청합니다.
readings_1 = instrument_query(s, "TRAC:DATA? 1, 50, \"defbuffer1\", READ, REL", (16*100)).rstrip()  # 1–50번째 읽기값·상대 시간 응답에서 뒤쪽 공백을 rstrip()으로 제거합니다.
readings_2 = instrument_query(s, "TRAC:DATA? 51, 100, \"defbuffer1\", READ, REL", (16*100)).rstrip()  # 51–100번째 결과를 별도로 요청하며 16*100은 수신 크기 인수입니다.
instrument_write(s, "OUTP OFF")  # 측정과 읽기 요청을 마친 뒤 SMU 출력을 끕니다.
```

`instrument_write()`는 이 원본 파일이 정의한 보조 함수이고, Python 표준 함수가 아닙니다. SCPI는 계측기가 해석하는 명령 체계입니다. `RSEN ON`은 remote sense, `OCOM ON`은 offset compensation 설정입니다. `*WAI`는 장비 쪽 명령 처리의 대기를 요청하며, PC에서 고정 시간 잠드는 `sleep()`과 역할이 다릅니다.

이 원문은 저항 기능·자동 범위와 trigger template를 설정합니다. 시험 전류를 별도의 `SOUR:CURR` 명령으로 명시하는 발췌는 아닙니다. 시료의 발열과 정격에 맞는 인가 조건은 장비 기능·범위와 함께 확인합니다. 원본의 TCP 보조 함수는 단순 `send()`·`recv()`를 쓰므로, 현장용 수집기의 완전한 메시지 수신·예외 복구까지 포함한 구현으로 해석하지 않습니다. [Python socket의 send·recv 계약](https://docs.python.org/3/library/socket.html#socket.socket.send)

### 불량과 측정 오차를 나누는 절차

1. 기준 저항 또는 정상 기준 경로를 같은 치구에서 측정합니다. DUT를 바꾸기 전에 측정 경로의 반복성을 봅니다.
2. Sense 선이 DUT 양단에 연결됐는지 확인하고 2선식·4선식 차이를 비교합니다. 원격 감지만 켜고 Sense 결선을 빠뜨린 상태와 구분합니다.
3. 측정 전류·인가 시간·온도를 기록합니다. 시간에 따라 저항이 증가하면 접속 변화와 자가 발열을 구분할 대조가 필요합니다.
4. offset compensation 설정 전후와 반복 결과를 비교합니다. 기능을 켰다는 사실만으로 모든 잡음이 제거되는 것은 아닙니다.
5. 전기적 이상이 같은 위치·시료에서 재현되면 X선·초음파·단면 등 해당 구조를 볼 수 있는 분석으로 연결합니다. 전기적 저항값 하나로 접합의 정확한 파괴 위치를 확정하지 않습니다.

조치 후에는 같은 DUT·시험 전류·결선·온도 조건으로 재평가합니다. 치구를 바꾸어 값이 돌아왔다면 치구 영향, 시료를 바꾸었을 때만 돌아왔다면 시료 영향이라는 가설을 더 조사할 수 있습니다. 한 번의 교체만으로 인과관계를 확정하기보다 반복·교차 대조 결과를 남깁니다.

## 3. ADC 보드에서 값이 갱신되지 않는 문제

### 아날로그 값과 디지털 취득을 나눕니다

ADC는 analog-to-digital converter, 전압 같은 연속량을 디지털 수로 바꾸는 소자입니다. AD7124-8은 센서·계측 용도의 ADC이며 제조사가 no-OS C 드라이버를 공개합니다. 소자·회로·설비 제어·펌웨어 업무가 만나는 사례로, 입력 전압은 정상처럼 보이는데 프로그램에서 새 값을 얻지 못하는 상황을 선택합니다. [ADI 제품·평가 보드 설명](https://www.analog.com/en/products/ad7124-8.html)

| 관측 위치 | 사용할 수 있는 장비·자료 | 확인하는 값 |
| --- | --- | --- |
| 아날로그 입력·기준 전압 | 보드 정격에 맞는 기준 전압원·DMM, 회로도 | 실제 AIN 차동 전압·VREF·전원입니다. |
| 디지털 인터페이스 | 오실로스코프·로직 분석기 | CS·SCLK·DIN·DOUT/RDY의 전압·시간·명령·응답입니다. |
| 드라이버 | ADI no-OS 원문과 호출부 로그 | 반환 코드, 레지스터 설정, 채널·필터·동작 모드와 polling 조건입니다. |
| 변환 결과 해석 | 설정 readback과 원시 코드 | 새 데이터인지, 어느 채널인지, unipolar/bipolar와 gain이 일치하는지입니다. |

SPI는 클록과 입출력 선으로 장치와 데이터를 주고받는 직렬 통신입니다. 레지스터는 장치의 설정·상태·데이터를 읽고 쓰는 정해진 위치입니다. RDY 비트는 이 소자에서 새 변환값의 준비 상태를 나타내며 준비되면 0입니다. 비트 이름에 `ready`가 있다고 무조건 1을 기다리면 동작을 거꾸로 해석할 수 있습니다. [AD7124-8 Rev. F, 51쪽 연속 변환·80–81쪽 STATUS register](https://www.analog.com/media/en/technical-documentation/data-sheets/AD7124-8.pdf#page=51)

### 실제 C 드라이버의 준비 상태 대기

출처는 [ADI no-OS, `ad7124_wait_for_conv_ready()`, 337–363줄](https://github.com/analogdevicesinc/no-OS/blob/d173657d7fc186e398cc6292276daad25a63eb22/drivers/adc/ad7124/ad7124.c#L337-L363)입니다. 원본 저작권은 `Copyright 2015-2019, 2023, 2026(c) Analog Devices, Inc.`입니다. BSD 3-Clause 조건과 보증 부인은 [프로젝트의 고지 전문](licenses/ADI-ad7124-BSD-3-Clause.txt)에 보존했습니다. 들여쓰기·설명 주석 외의 C 실행 토큰은 원문과 같습니다.

```c
int32_t ad7124_wait_for_conv_ready(struct ad7124_dev *dev,  // int32_t 반환 함수와 장치 구조체 포인터 인수를 선언합니다.
                   uint32_t timeout)  // uint32_t는 부호 없는 32비트 정수이며 polling 카운터를 받습니다.
{  // 함수 본문을 엽니다.
    struct ad7124_st_reg *regs;  // 장치 레지스터 배열을 가리킬 구조체 포인터를 선언합니다.
    int32_t ret;  // 드라이버 반환 코드를 담을 부호 있는 정수를 선언합니다.
    int8_t ready = 0;  // 아직 준비되지 않았다는 논리 상태를 0으로 초기화합니다.
    if (!dev)  // !dev로 장치 포인터가 비어 있는지 검사합니다.
        return -EINVAL;  // 유효하지 않은 인수의 음수 오류 코드를 반환합니다.
    regs = dev->regs;  // ->로 장치의 레지스터 배열 필드에 접근합니다.
    while (!ready && --timeout) {  // 준비되지 않았고 감소한 카운터가 0이 아닌 동안 반복합니다.
        ret = ad7124_read_register(dev, &regs[AD7124_Status]);  // 배열 원소의 주소 &를 전달해 상태 레지스터를 읽습니다.
        if (ret)  // 0이 아닌 반환 코드인지 확인합니다.
            return ret;  // 읽기 오류를 그대로 호출자에게 반환합니다.
        ready = (regs[AD7124_Status].value &  // 비트 AND &로 RDY 마스크를 선택하는 식을 시작합니다.
             AD7124_STATUS_REG_RDY) == 0;  // RDY 비트가 0일 때 ready가 참이 되도록 비교합니다.
    }  // 반복문 본문을 닫습니다.
    if (!timeout)  // 카운터가 0이 됐는지 논리 부정으로 확인합니다.
        return -ETIMEDOUT;  // 준비 전에 카운터를 소모하면 시간 초과 오류를 반환합니다.
    return 0;  // 준비 상태를 확인한 성공을 0으로 반환합니다.
}  // 함수 본문을 닫습니다.
```

`struct`는 관련 필드를 묶는 구조체, `*dev`는 그 구조체를 가리키는 포인터입니다. `dev->regs`는 포인터가 가리키는 구조체의 필드에 접근합니다. `&regs[...]`는 배열 원소의 주소, `&`의 다른 용법인 `값 & 마스크`는 비트 선택입니다. `!`는 논리 부정, `&&`는 두 조건이 모두 참인지 확인하는 연산입니다. 반환값 0은 이 함수의 성공 규약이며 음수는 오류 코드입니다.

여기서 `timeout`은 밀리초가 아니라 polling 횟수에 관련된 카운터입니다. `--timeout`은 비교 전에 1을 줄입니다. 최초 인수 1이면 본문의 레지스터 읽기를 하지 않고 시간 초과를 반환합니다. 최초 인수 0은 부호 없는 정수에서 감소하며 큰 값으로 돌아가므로 ‘즉시 반환’이라고 해석하면 안 됩니다. 호출부의 양수 인수와 실제 elapsed time을 함께 확인해야 합니다. 이는 원문을 읽어 얻은 경계 분석이며 이번 작성에서 보드로 재현한 오류는 아닙니다.

### 같은 코드의 의미가 달라지는 예

unipolar는 입력 범위를 한쪽 극성으로, bipolar는 차동 입력의 양·음 범위를 표현하는 설정입니다. 이 소자의 bipolar 출력은 offset binary입니다. 0 V 차동 입력의 이상적인 코드가 `0x800000`이므로 이를 2의 보수 signed 정수처럼 읽으면 잘못 해석합니다. [ADI의 출력 코딩 FAQ](https://ez.analog.com/data_converters/precision_adcs/a/documents/do13884/faq-ad7124-data-output-coding), [데이터시트 Rev. F 48쪽 Data Output Coding](https://www.analog.com/media/en/technical-documentation/data-sheets/AD7124-8.pdf#page=48)

| 같은 원시 코드 | 가정한 설정 | 이상적인 해석 |
| --- | --- | --- |
| `0x800000` | unipolar, gain 1, VREF 2.5 V | 양의 중간값 1.25 V입니다. |
| `0x800000` | bipolar, gain 1, VREF 2.5 V | 차동 0 V입니다. |

이것은 데이터시트의 이상적 코딩 관계로 계산한 예입니다. 실제 입력의 허용 전압·공통모드, 교정·오프셋·이득 오차와 노이즈는 별도 조건입니다. bipolar 설정이 단일 전원에서 모든 핀에 음의 절대 전압을 허용한다는 뜻도 아닙니다.

### 증상에서 원인 후보로 이동합니다

| 관측 결과 | 먼저 나눌 원인 | 확인·조치와 재평가 |
| --- | --- | --- |
| SPI 읽기에서 음수 오류가 반환됩니다. | 전원·CS·배선·SPI 설정·CRC·통신 실패입니다. | 실제 파형과 반환 경로를 비교하고 읽기 오류가 사라지는지 먼저 확인합니다. 값을 0으로 대체하면 취득 실패가 정상 전압처럼 보일 수 있습니다. |
| SPI 응답은 있으나 RDY가 내려오지 않습니다. | 채널 비활성·변환 모드·클록·필터 설정·대기 횟수입니다. | 설정 readback과 RDY·시간축을 맞춥니다. 필터 변경 후 필요한 정착 시간이 달라지는지도 봅니다. |
| 데이터는 갱신되지만 값이 절반·배수·중간값에서 어긋납니다. | gain·VREF·코딩·채널 대응입니다. | 동일한 알려진 입력을 넣고 설정과 코드를 함께 저장합니다. 아날로그 입력과 디지털 환산을 분리해 확인합니다. |
| 평균은 맞는데 산포만 커집니다. | 입력·기준 전압 잡음, 결선·공통모드·필터·주변 간섭입니다. | 입력·VREF를 독립 계측하고 조건별 시계열을 비교합니다. 필터를 바꾸면 대역폭·정착·노이즈가 함께 달라집니다. |

필터·출력 속도·정착 시간의 관계는 [데이터시트 66–67쪽 Filter Summary](https://www.analog.com/media/en/technical-documentation/data-sheets/AD7124-8.pdf#page=66)에 있습니다. C의 반환값과 로직 분석기 파형, DMM의 전압을 같은 시료·설정으로 묶는 것이 조사 기록의 핵심입니다. Python을 붙이는 경우 PC에서 계측값과 로그를 모으는 역할을 맡길 수 있지만, 위 C 함수가 Python에 직접 연결된다는 별도 구현은 여기서 새로 만들지 않았습니다.

## 4. 확인한 범위와 출처

| 자료 | 확인한 범위 |
| --- | --- |
| [Tektronix 공식 저장소](https://github.com/tektronix/keithley/tree/96f209329a4c0a995cc4f0a57d9e3d301a640d17) | 위 두 Python 파일 전체와 저장소의 Sample Source Code License를 읽었습니다. 제조사 예제와 해당 장비용 명령이라는 범위를 사용합니다. |
| [2450 공식 사양](https://www.tek.com/en/datasheet/smu-2400-graphical-sourcemeter/model-2450-touchscreen-source-measure-unit-smu-instrument) | 저항 측정·source readback·remote sense·offset compensation의 조건입니다. 모델의 모든 기능을 시험한 결과가 아닙니다. |
| [2450 User's Manual Rev. E](https://download.tek.com/manual/2450-900-01E_Aug_2019_User.pdf) | 공개 검색 본문의 5장 저저항 측정 설명을 원문 코드와 대조했습니다. 전체 PDF는 직접 내려받기 응답 제한으로 확보하지 못했습니다. |
| [ADI 드라이버 고정 판본](https://github.com/analogdevicesinc/no-OS/blob/d173657d7fc186e398cc6292276daad25a63eb22/drivers/adc/ad7124/ad7124.c) | 파일 전체·헤더·준비 상태 대기·데이터 읽기·상위 호출의 양수 polling 인수를 확인했습니다. |
| [AD7124-8 Rev. F](https://www.analog.com/media/en/technical-documentation/data-sheets/AD7124-8.pdf) | 제품 구성과 47–48쪽 입력/코딩, 51쪽 연속 변환, 66–67쪽 필터, 80–81쪽 상태 비트를 확인했습니다. |

Python 원본과 주석 발췌의 실행문을 정적으로 대조하고 단위·경계 계산을 확인했습니다. C 발췌는 원문 실행 토큰을 대조했습니다. 장비 접속·ADC 보드 실행·실물 불량 판정은 수행하지 않았습니다. 확인 기준일은 2026-10-26입니다.

## English

The cases connect Tektronix's published 2450 measurement examples and Analog Devices' AD7124 driver to resistor acceptance, low-resistance connections and ADC acquisition faults. Annotated excerpts retain upstream executable statements and identify their fixed revisions and license terms. Work scenarios and numerical illustrations are authored explanations; no instrument measurements are reported. Error propagation, source readback, Kelvin sensing, ready-bit polarity and input coding guide the separation of DUT faults from measurement and acquisition errors.
