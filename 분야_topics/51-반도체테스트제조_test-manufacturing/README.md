# DFT·반도체 테스트·제조 | DFT, Semiconductor Test & Manufacturing

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

DFT는 제조 후 칩 내부의 오류를 관찰하고 제어하기 쉬운 구조를 설계에 넣는 방법입니다. 기능 검증이 RTL의 의도된 동작을 다룬다면 제조 테스트는 제작 과정의 결함을 검출합니다.

## Scan과 pattern

Scan은 내부 register를 shift 가능한 경로로 연결해 상태를 넣고 읽게 합니다. ATPG는 정해진 fault model을 검출하는 입력 pattern을 생성합니다. Stuck-at·transition 같은 모델은 실제 결함을 추상화하며 coverage의 의미는 사용한 모델에 달려 있습니다.

## 내장 테스트와 양산

BIST는 칩 안에서 테스트를 수행하는 구조입니다. MBIST는 메모리, LBIST는 논리 회로의 테스트에 사용됩니다. JTAG·boundary scan은 외부 연결과 테스트 접근에도 쓰입니다. Tessent·TestMAX·Modus는 이런 테스트를 지원하는 상용 도구입니다.

ATE는 테스트 장비이고 wafer·package·system 단계는 관측 조건과 비용이 다릅니다. Yield는 검사 기준을 통과하는 비율이며 공정·설계·테스트 조건과 연결됩니다. Test time·pattern volume·coverage·전력은 양산 테스트의 선택을 좌우합니다. 수명과 환경 스트레스에 대한 신뢰성은 특정 시점의 기능 테스트와 별도로 평가합니다.

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

### Foundation article

- [보이지 않는 내부 상태를 검사하기: scan, ATPG와 fault coverage](해설_notes/보이지않는내부상태를검사하기_scan-atpg-fault-coverage.md#english)


## 심화 해설 | Advanced article

- [다른 출력이 같은 signature가 될 때: aliasing을 계산하기](해설_notes/서명이같아지는오류_signature-aliasing.md) · [English](해설_notes/서명이같아지는오류_signature-aliasing.md#english)
