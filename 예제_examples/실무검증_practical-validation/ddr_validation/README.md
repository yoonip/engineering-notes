# DDR 명령 간격과 메모리 패턴 | DDR command timing and memory patterns

ACT·WR·RD·PRE·REF 명령표를 실제 Icarus Verilog에서 실행하고, Python이 명령 간격과 읽기 자료를 독립적으로 검사합니다. SystemVerilog 파일은 파일 입출력과 배열 메모리를 포함한 비합성 fixture입니다. DDR controller·PHY·실제 DRAM 소자의 구현은 포함하지 않습니다.

| 파일 | 내용 |
| --- | --- |
| [fixtures.json](fixtures.json) | 고정 교육 계약과 정상·의도적 결함·패턴의 검출 한계를 보여 주는 15설정입니다. |
| [ddr_command_fixture.sv](ddr_command_fixture.sv) | 명령표를 클록마다 실행하며 배열의 값과 2cycle 뒤 read 응답을 출력합니다. |
| [run_validation.py](run_validation.py) | 명령표 생성, 실제 compile/sim, 독립 tuple 주소·응답 기대값·시간 검사, 결과·해시 기록입니다. |

## 고정 계약

- 주소 공간은 `2banks × 4rows × 4columns × 16bits = 64bytes`입니다. 배열은 초기화하지 않으며 두 bank는 닫힌 상태에서 시작합니다.
- 추가 지연 AL은 0으로 간주합니다. 명령은 한 cycle에 하나이며 tRCD=3, tRAS=6, tRP=2, tRFC=8, tWR=2, tRTP=2cycle입니다. 명령 간격이 최소값과 같으면 허용합니다.
- REF 명령 발행 간격은 idle을 포함해 최대 40cycle입니다. 실제 규격의 평균 refresh 간격과 postpone/pull-in 정책을 구현한 값이 아닙니다.
- SV 클록은 10ns이며 WR은 배열을 즉시 갱신하고 RD는 명령 시점의 값을 2cycle 뒤 응답합니다. burst·CL/CWL·DQ/DQS·bank group·tCCD/tRRD/tFAW·retention·training·ECC·캐시는 없습니다.
- JSON의 geometry/policy는 이 고정 예제를 설명하는 메타데이터입니다. 임의의 geometry·read latency·DDR 부품으로 바꾸어 사용할 수 있는 범용 설정 인터페이스가 아닙니다.

## 실행

Python 3.10 이상 표준 라이브러리와 Icarus Verilog가 필요합니다. 이번 실행은 Python 3.12.14와 Icarus 12.0 devel을 사용했습니다. 저장소 루트 PowerShell의 예시는 다음과 같습니다.

```powershell
python '예제_examples/실무검증_practical-validation/ddr_validation/run_validation.py' `
  --out 'tmp/ddr-run-1' `
  --iverilog 'C:/iverilog/bin/iverilog.exe' `
  --vvp 'C:/iverilog/bin/vvp.exe' `
  --build-root 'C:/temp/ddr-build'
```

`python`에는 실제 실행 파일 경로를 사용할 수 있습니다. PATH에 Icarus가 있다면 두 도구 옵션을 생략합니다. Linux에서는 `--build-root /tmp/ddr-build`와 같은 경로를 사용합니다. `--out`은 새 폴더여야 하며 기존 폴더는 종료 2로 거절합니다. `python -O`로 실행해도 검사 결과가 같으며 판정을 `assert`에 의존하지 않습니다.

각 설정을 별도 ASCII build 하위 폴더에서 순차 컴파일하고 실행합니다. 자식 `TEMP/TMP`를 build 폴더로 지정합니다. 소스·설정·입력 SHA256과 명령·종료·표준 출력/오류를 `report.json`에 기록합니다. 설정별 `trace.csv`, `program.hex`, `sim.vvp`, `result.json`을 보존합니다. 실행 제한은 자식 명령당 30초입니다.

## 관측한 결과

| 설정 | 기능 판정 | 관측 |
| --- | --- | --- |
| 정상 주소 패턴 | PASS | 256행, WR/RD/응답 각각 32건, REF 8건, 불일치 0입니다. |
| 정상 checkerboard·역패턴 | PASS | 512행, WR/RD/응답 각각 64건, 불일치 0입니다. |
| tRCD/tRAS/tRP/tRFC 위반·REF 누락 | FUNCTIONAL_FAIL | 각각 cycle 10/9/27/7/41에서 첫 오류를 검출했습니다. |
| stuck bit 0·column bit 1 alias, 주소 패턴 | FUNCTIONAL_FAIL | 두 설정 모두 자료 불일치 16건입니다. |
| 같은 결함, 전체 0 패턴 | PASS | 이 입력으로 결함을 구별하지 못한 대조 결과입니다. 무결함 판정이 아닙니다. |
| 쓰기 누락 후 읽기·응답 누락·유효 X | FUNCTIONAL_FAIL | 미초기화·응답 개수·자료 유효성을 각각 확인했습니다. |
| exit 0으로 trace 중단 | INFRA_ERROR | 예정 cycle이 부족하므로 기능 결과를 통과로 계산하지 않습니다. |

회귀 명령의 최종 `PASS`는 15설정이 각자 예상한 판정과 일치하고 7개 오류 trace 대조가 일치했다는 뜻입니다. 정상 완료 4설정에는 의도적인 패턴 검출 한계 2설정이 포함됩니다. 개별 기능 실패를 장치의 성공 결과로 집계하지 않습니다. 예상과 다른 기능 결과는 종료 1, 도구·실행 또는 예상하지 않은 trace 수집 오류는 종료 2입니다. 의도한 중단 설정도 실제 compile/sim이 종료 0이어야 대조가 성립합니다.

## 비교기의 기준

SV의 정수 배열 주소 계산과 별개로 Python은 `(bank, row, column)` tuple을 사전 키로 사용합니다. WR 값과 RD 시점의 기대값을 저장하고, 매 cycle 도착해야 하는 응답의 tag·값·개수를 대조합니다. 응답이 없을 때 값 비교 횟수도 0이라는 이유로 통과시키지 않습니다. 명령표의 echo·행 수·순서·열·control에 X가 있으면 `INFRA_ERROR`, 유효 read 자료의 X/Z나 예정 응답 누락은 `FUNCTIONAL_FAIL`입니다.

이 시험은 디지털 명령·자료 검사이며 실제 보드, JEDEC 적합성, refresh retention, eye margin 또는 모든 주소·결함 유형의 검증 결과가 아닙니다. [사례 본문](../../../설계와검증사례_engineering-cases/DDR명령간격과메모리패턴_ddr-command-pattern-checks.md)과 [검증 기록](../../../설계와검증사례_engineering-cases/검증기록_evidence/DDR명령과패턴검증_20261021.md)을 함께 읽습니다.

## English

An actual Icarus run executes a nonsynthesizable SystemVerilog command/array fixture. Python independently checks a fixed, self-defined timing contract and read transactions using tuple-addressed reference storage. The model has 32 sixteen-bit locations, AL=0, a fixed two-cycle response, and a strict 40-cycle REF issue deadline. JSON geometry/policy fields describe this fixed example rather than a configurable DDR device.

Fifteen settings include correct traffic, controlled timing/data defects, two all-zero pattern blind spots, and an intentionally incomplete trace. The final regression succeeds when those expected outcomes and seven altered-trace controls match. Normal and `-O` runs have identical input and trace hashes. No PHY, burst transfer, cell retention, JEDEC compliance, cache behavior or physical hardware measurement is established.
