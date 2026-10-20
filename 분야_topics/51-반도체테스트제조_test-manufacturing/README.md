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


## 심화 해설 | Advanced article

- [다른 출력이 같은 signature가 될 때: aliasing을 계산하기](해설_notes/서명이같아지는오류_signature-aliasing.md) · [English](해설_notes/서명이같아지는오류_signature-aliasing.md#english)
