# DFT·반도체 테스트·제조 | DFT, Semiconductor Test & Manufacturing

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

DFT는 제조 후 칩 내부의 오류를 관찰하고 제어하기 쉬운 구조를 설계에 넣는 방법입니다. 기능 검증이 RTL의 의도된 동작을 다룬다면 제조 테스트는 제작 과정의 결함을 검출합니다.

## Scan과 pattern

Scan은 내부 register를 shift 가능한 경로로 연결해 상태를 넣고 읽게 합니다. ATPG는 정해진 fault model을 검출하는 입력 pattern을 생성합니다. Stuck-at·transition 같은 모델은 실제 결함을 추상화하며 coverage의 의미는 사용한 모델에 달려 있습니다.

## 내장 테스트와 양산

BIST는 칩 안에서 테스트를 수행하는 구조입니다. MBIST는 메모리, LBIST는 논리 회로의 테스트에 사용됩니다. JTAG·boundary scan은 외부 연결과 테스트 접근에도 쓰입니다. Tessent·TestMAX·Modus는 이런 테스트를 지원하는 상용 도구입니다.

ATE는 테스트 장비이고 wafer·package·system 단계는 관측 조건과 비용이 다릅니다. Yield는 검사 기준을 통과하는 비율이며 공정·설계·테스트 조건과 연결됩니다. Test time·pattern volume·coverage·전력은 양산 테스트의 선택을 좌우합니다. 수명과 환경 스트레스에 대한 신뢰성은 특정 시점의 기능 테스트와 별도로 평가합니다.

## 자동 시험 집계의 분모

검증 자동화에서는 시험 대상의 FAIL과 시험이 성립하지 않은 상태를 구분합니다. 프로세스가 종료됐더라도 결과의 입력·코드 버전이 다르거나 예정한 case가 빠지면 유효 결과로 집계할 수 없습니다. 같은 결과 파일을 두 번 읽어 시험 수를 늘리지 않도록 실행 ID와 case ID도 함께 확인합니다.

다음은 직접 구성한 12개 계획 항목의 예입니다. 10개를 시작했고, 그중 1개는 timeout입니다. 종료한 9개 중 1개는 결과 형식이 잘못되어 INVALID이고, 유효한 8개는 PASS 7개와 FAIL 1개입니다. 이 예의 INVALID와 TIMEOUT은 제품 불량이라는 뜻이 아닙니다.

```python
from collections import Counter  # Counter는 각 값이 나타난 횟수를 세는 dict 계열 자료구조입니다.
states = ["PASS"] * 7 + ["FAIL", "INVALID", "TIMEOUT", "NOT_RUN", "NOT_RUN"]  # []는 리스트이며 *는 반복, +는 연결입니다.
counts = Counter(states)  # Counter를 호출해 상태별 개수를 계산합니다.
planned = len(states)  # len 함수로 계획 항목 12개의 개수를 구합니다.
started = planned - counts["NOT_RUN"]  # dict처럼 []로 횟수를 읽고 미시작 2개를 뺍니다.
completed = started - counts["TIMEOUT"]  # 제한 시간 안에 종료한 항목만 셉니다.
valid = counts["PASS"] + counts["FAIL"]  # 제품 판정이 성립한 두 상태의 개수를 더합니다.
print(planned, started, completed, valid, counts["PASS"])  # 12 10 9 8 7을 출력합니다.
print(f"{started/planned:.2%} {valid/planned:.2%} {counts['PASS']/valid:.2%}")  # :.2%는 비율을 백분율로 표시합니다.
```

시작률은 10/12 = 83.33%, 유효 결과 확보율은 8/12 = 66.67%, 유효 결과 안의 통과율은 7/8 = 87.50%입니다. 7/12 = 58.33%는 계획 대비 통과 결과 확보율입니다. 서로 다른 질문의 답이므로 한 수치를 수율이나 coverage라는 이름으로 바꾸지 않습니다. 이 12개는 고장 모델의 검출 대상 fault 수가 아니므로 ATPG fault coverage로 해석할 수 없습니다.

실제 검증 계획은 case뿐 아니라 seed·설정·전압·온도 등의 조합을 포함할 수 있습니다. 어떤 조합을 계획했고 무엇을 제외했는지 먼저 고정해야 누락과 중복을 판별할 수 있습니다. 이 예는 집계의 산술을 보여 주며 특정 공정·칩의 양산 결과를 나타내지 않습니다.

[칩 시험 러너 사례](../../설계와검증사례_engineering-cases/시험러너의종료상태와결과계약_chip-runner-result-contract.md)는 자식프로그램의 종료 코드와 결과 파일의 신뢰 조건을 분리합니다. 정상 종료·PASS 문자열만으로 통과시킨 경우와 입력 해시·실행 ID·예정 case·수치 기대값을 함께 확인한 결과를 비교하실 수 있습니다.

## 관련 기술

DFT, Scan, ATPG, MBIST/LBIST, ATE, JTAG/Boundary Scan, Tessent, TestMAX, Modus

## 참고 자료

- [Siemens Tessent](https://eda.sw.siemens.com/en-US/ic/tessent/)

## 기초 해설

- [보이지 않는 내부 상태를 검사하기: scan, ATPG와 fault coverage](해설_notes/보이지않는내부상태를검사하기_scan-atpg-fault-coverage.md)

## 읽은 값과 오류 기록을 함께 봅니다

메모리를 쓴 뒤 같은 값이 나왔다는 관측은 중요하지만, 그것만으로 모든 오류가 없었다고 판단할 수는 없습니다. 예를 들어 ECC가 내부 오류를 수정한 뒤 올바른 값을 반환할 수 있습니다. Linux [EDAC의 오류 종류](https://docs.kernel.org/driver-api/edac.html#c.hw_event_mc_err_type)는 수정된 오류, 수정할 수 없는 오류, 지연 처리와 치명적 오류 등을 구분합니다. 지원하는 controller·driver와 오류 위치 정보도 함께 확인해야 합니다.

아래는 직접 만든 관측값입니다. 반환 데이터는 같지만 같은 시험 구간에서 corrected-error 수가 10에서 12로 늘었다고 가정합니다. corrected error는 오류를 수정했다는 보고이며, 아무 오류도 발생하지 않았다는 뜻이 아닙니다.

```python
expected, returned = 0xA5, 0xA5  # 0x는 16진수이며 기대값과 반환값을 지정합니다.
before = {"corrected": 10, "uncorrected": 0}  # {}는 이름과 값을 연결하는 사전입니다.
after = {"corrected": 12, "uncorrected": 0}  # 같은 부팅·카운터 구간의 끝 값을 가정합니다.
delta = {name: after[name] - before[name] for name in before}  # 사전 내포로 각 증가량을 계산합니다.
print(returned == expected, delta)  # True와 {'corrected': 2, 'uncorrected': 0}입니다.
```

이 두 건을 실제 장비에서 관측한 결과로 제시하지 않습니다. counter reset·overflow·재부팅·다른 부하가 있으면 단순 차이가 이 시험의 오류 수가 아닐 수 있습니다. 시작과 끝을 같은 구간에 묶고, 발생 주소·채널·시험 입력·온도·전압·주파수 조건을 연결합니다. 수정된 오류를 어느 조건에서 허용할지도 제품의 요구사항으로 정해야 하며, 이 예의 수를 보편적인 합격 한도로 사용하지 않습니다.

## DDR의 명령 간격을 cycle로 바꾸는 예

DDR에서 한 행을 여는 ACT와 그 행에 접근하는 읽기·쓰기 사이에는 필요한 시간 간격이 있습니다. [AMD UG586 v4.2의 설정 표](https://docs.amd.com/r/en-US/ug586_7Series_MIS/Customizing-the-Core)는 tRCD를 ACTIVE에서 READ·WRITE까지의 지연으로 설명합니다. 추가 지연이 없는 단순 명령 계약에서 필요한 시간을 13.75 ns, 명령 클록 주기를 2.5 ns라고 가정하면 5 cycle은 12.5 ns여서 부족하고 최소 6 cycle이 필요합니다. 아래 숫자는 특정 메모리 부품의 정격이 아닌 계산용 입력입니다.

```python
required_ps, cycle_ps = 13750, 2500  # ps는 1 ns의 1/1000이며 정수 단위로 계산합니다.
minimum_cycles = (required_ps + cycle_ps - 1) // cycle_ps  # //는 정수 나눗셈이며 필요한 cycle을 올림합니다.
floor_cycles = required_ps // cycle_ps  # 잘못 내림한 대조는 5 cycle입니다.
print(minimum_cycles, minimum_cycles * cycle_ps)  # 6과 15000 ps입니다.
print(floor_cycles, floor_cycles * cycle_ps)  # 5와 12500 ps로 최소 시간보다 짧습니다.
```

실제 설정에는 시간 단위 제한과 최소 cycle 제한이 함께 있을 수 있습니다. 해당 장치·속도 등급·클록 조건을 확인한 뒤 둘 다 만족해야 합니다. 이 계산은 두 배의 데이터 전송률과 명령 클록을 섞지 않도록 정한 단일 명령 간격 예이며, DDR training·눈 다이어그램·배선 지연이나 실제 데이터 안정성을 측정하지 않습니다.

[DDR 명령 간격과 메모리 패턴 사례](../../설계와검증사례_engineering-cases/DDR명령간격과메모리패턴_ddr-command-pattern-checks.md)는 명시한 cycle 계약의 명령 검사와 데이터 패턴을 연결합니다. 패턴이 검출하는 결함 모델, 제한된 RTL 실행, 실제 소자·보드 검증을 구분하여 읽으실 수 있습니다. 특정 패턴 통과, ECC 관측, timing 조건의 통과는 각각 다른 검사의 근거입니다.

## ECC의 정정 결과와 보장 밖 오류를 구분합니다

[SECDED 실행 예제](../../예제_examples/실무검증_practical-validation/ecc_secded/README.md)는 8비트 자료에 검사 5비트를 붙인 고정 Hamming(13,8) 코드입니다. 자료 위치와 parity 위치를 정의한 뒤 단일 오류 3,328개 조합·이중 오류 19,968개 조합을 실제 Python 함수로 검사했습니다. 전자는 parity 위치까지 원래 자료로 정정하고, 후자는 `uncorrectable`로 판단해 자료를 반환하지 않습니다. 아래는 예제 코드 폴더에서 실행하는 짧은 관측입니다.

```python
from codec import encode, decode  # from/import로 예제 부호화·복호화 함수를 가져옵니다.
word = encode(0xA5)  # 16진수 자료 A5를 13비트 코드워드 0A27로 바꿉니다.
single = decode(word ^ (1 << 12))  # 정수 bit12인 전체 parity 위치13만 반전합니다.
double = decode(word ^ (1 << 2) ^ (1 << 4))  # 자료 위치3·5를 함께 반전합니다.
print(single.status, single.data, single.corrected_position)  # corrected 165 13입니다. 165는 A5의 10진수입니다.
print(double.status, double.data)  # uncorrectable None이며 자료를 정상값처럼 넘기지 않습니다.
```

syndrome이 0이어도 전체 parity가 홀수라면 단일 오류 전제에서 위치 13을 고칩니다. 그러나 자료 0의 위치 1·2·3을 함께 바꾸면 자료 1의 위치 13 단일 오류와 같은 16진수 수신값 0007이 됩니다. 위치 1·2·3·13의 네 비트를 바꾸면 아예 자료 1의 유효 코드워드 1007이 됩니다. [계산과 반례](../../설계와검증사례_engineering-cases/ECC의단일비트정정과이중비트검출_ecc-secded.md)는 오정정·미검출과 단일/이중 보장을 함께 설명합니다.

전체 13비트 입력 8,192개를 대조한 결과도 정한 반경 1 복호 정책과의 일치입니다. 모든 다중 오류의 원본을 알아냈다는 뜻이 아닙니다. 이 코드에는 주소·거래 번호 보호, 실제 메모리 scrubbing·BCH·LDPC·EDAC 장치가 없습니다. [실행 기록](../../설계와검증사례_engineering-cases/검증기록_evidence/ECC오류주입과검출범위_20261021.md)에 기본/최적화와 오류 변이·소스/입력 해시를 연결했습니다. 비교 횟수와 오류 위치 조합을 더해 독립 시험 수나 실제 양산 fault coverage로 해석하지 않습니다.

## English

### DFT, test, and manufacturing

Design for test adds structures that make faults inside a manufactured chip easier to control and observe. Functional verification checks the intended RTL behavior, while manufacturing tests aim to detect fabrication defects.

### Scan and patterns

Scan connects internal registers into shiftable paths so that states can be loaded and observed. ATPG generates input patterns for specified fault models. Models such as stuck-at and transition faults abstract physical defects; coverage must be interpreted in relation to the chosen model.

### Built-in test and production

BIST performs tests within the chip. MBIST targets memories, and LBIST targets logic. JTAG and boundary scan also provide access for interconnect tests and other test operations. Tessent, TestMAX, and Modus provide commercial tools for these tasks.

ATE is automated test equipment. Wafer, package, and system-level tests have different observation conditions and costs. Yield is the proportion of devices that pass the test criteria, and depends on process, design, and test conditions. Test time, pattern volume, coverage, and power affect production-test decisions. Reliability under aging and environmental stress is a separate consideration from passing a functional test at one moment.

### Denominators in automated testing

A constructed twelve-item plan starts ten tests. One times out; one of the nine completed reports is invalid. The eight valid verdicts contain seven passes and one failure. Start rate is 10/12, valid-result availability is 8/12, and pass rate among valid verdicts is 7/8. These are different quantities and do not measure ATPG fault coverage or manufacturing yield. Matching run/case identities and declared input revisions prevents duplicate or stale results entering the denominator.

### Foundation article

- [보이지 않는 내부 상태를 검사하기: scan, ATPG와 fault coverage](해설_notes/보이지않는내부상태를검사하기_scan-atpg-fault-coverage.md#english)


### DDR observations and test criteria

A constructed correct-read example still has two additional corrected-error reports, so returned data and error telemetry answer different questions. Counter deltas require the same observation epoch. In a separate assumed timing calculation, 13.75 ns with a 2.5 ns command clock requires six cycles, while rounding down to five violates the minimum. These are local arithmetic examples; the linked case distinguishes bounded command/pattern checks from physical DDR, ECC, training or board measurements.

### SECDED results and limits

The linked educational Hamming(13,8) example corrects all 3,328 single-error combinations and rejects all 19,968 double-error combinations without exposing payload data. Syndrome zero with odd overall parity identifies position13 under the single-error assumption. Explicit three-bit miscorrection and four-bit undetected examples show why that assumption matters. Checking all 8,192 received words confirms the specified radius-one policy, not knowledge of every multi-bit error's original. Comparison counts and origin/position combinations overlap. This Python codec does not test physical memory ECC, address identity, scrubbing, vendor BCH/LDPC or EDAC hardware.

## 심화 해설 | Advanced article

- [다른 출력이 같은 signature가 될 때: aliasing을 계산하기](해설_notes/서명이같아지는오류_signature-aliasing.md) · [English](해설_notes/서명이같아지는오류_signature-aliasing.md#english)
