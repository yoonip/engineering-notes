# 시험 러너의 종료 상태와 결과 계약 / Process exits and chip-job result contracts

자동화한 시험이 종료 코드 0을 반환하고 화면에 PASS를 적어도 시험 대상이 통과했다는 뜻은 아닐 수 있습니다. 실패를 JSON에만 기록하거나, 예전 결과를 다시 읽거나, 일부 항목을 실행하지 않은 상태에서도 프로그램은 정상 종료할 수 있습니다. 이 사례는 실제 자식 Python 프로세스 16개를 실행하여 단순 집계와 결과 계약 검사를 비교합니다. 합성 정수 산술 작업이며 RTL·실칩·ATE·계측기를 실행하지 않습니다.

## 세 가지 질문을 나눕니다

첫째는 프로세스가 정상적으로 끝났는지, 둘째는 이번 입력의 완전한 결과인지, 셋째는 그 결과가 기대 동작과 맞는지입니다. 종료 코드·JSON 형식·DUT 판정은 각각 다른 질문의 근거입니다. DUT는 시험 대상 장치라는 뜻이며 여기서는 작은 소프트웨어 모형입니다.

자식 [`fixture_child.py`](../예제_examples/실무검증_practical-validation/chip_automation/fixture_child.py)는 네 정수의 곱을 더하는 세 항목을 실행합니다. 부모 [`run_validation_jobs.py`](../예제_examples/실무검증_practical-validation/chip_automation/run_validation_jobs.py)는 자식의 계산 함수를 불러오지 않고 손으로 계산한 기대값 185, 65,536, 0을 보유합니다. 자식이 스스로 적은 expected 값을 믿고 비교하는 구조를 피했습니다.

```text
signed_dot: 20×7 + (-3)×(-2) + 5×3 + 6×4 = 185
edge_dot:   (-128)×(-128)를 네 번 더함 = 65,536
zero_dot:   0×127 + 1×3 + (-1)×3 + 5×0 = 0
```

입력은 signed int8 범위이고 이 네 항의 합은 int32 범위 안입니다. Python의 임의 정밀도 정수로 계산하므로 실제 int32 회로나 명령어의 overflow 검증은 아닙니다. 더 일반적인 가속기 검증은 [레이아웃·누산 폭 사례](칩산술의레이아웃과누산폭_chip-arithmetic-contract.md)와 연결합니다.

## 잘못된 러너는 무엇을 받아들이는지 확인합니다

다음 두 조건을 잘못된 대조로 기록합니다. 출력 문자열 검색은 로그를 이해하는 방법이 아니라 단어가 존재하는지 보는 방법입니다.

```python
accepted = completed.returncode == 0  # 프로세스 성공을 DUT 통과로 대신한 잘못된 대조입니다.
accepted = accepted and 'PASS' in completed.stdout  # PASS라는 부분 문자열이 있어도 근거는 부족합니다.
```

`dut_fail` 자식은 첫 결과를 185에서 184로 바꾸고 항목과 전체 상태를 FAIL로 기록하지만 종료 코드는 0입니다. 정상적으로 보고서를 완성한 기능 실패를 표현한 것입니다. `lying_pass`는 같은 184를 적으면서 PASS라고 주장합니다. `stdout_only`는 PASS라는 글자만 출력하고 결과 파일을 만들지 않습니다. 세 프로세스 모두 위 두 조건으로는 통과합니다.

수정한 러너는 순서대로 실행 상태, 결과 파일, 형식, 시도 ID, 입력 hash, 계획 항목과 실제 항목의 집합, 각 값과 판정의 일관성을 확인합니다. FAIL을 보고한 정상 보고서와 거짓 PASS를 구별합니다. 앞의 세 경우는 각각 `DUT_FAIL`, `FALSE_VERDICT`, `MISSING_RESULT`입니다. 유효한 기능 실패를 통신·실행 기반 오류와 같은 불량 수로 합치지 않습니다.

## 이번 실행의 결과인지 연결합니다

각 작업 폴더에는 새 `run_id`와 입력 JSON을 만들고 실제 입력 바이트의 SHA-256을 계산합니다. 자식은 읽은 입력의 hash와 run ID를 결과에 적습니다. 부모는 자신이 만든 값과 비교합니다. 파일이 있다는 조건이나 파일 수정 시각만으로 이번 결과라고 판단하지 않습니다.

`stale_result` 대조에는 새 작업 폴더 안에 오래된 결과를 흉내 낸 파일을 의도적으로 심습니다. 세 수치와 PASS 상태는 맞지만 `run_id=OLD-ATTEMPT`입니다. 자식은 이를 갱신하지 않고 정상 종료합니다. 부모는 `RUN_ID`로 거부하며 대조 파일이 갱신되지 않았다는 hash도 보존합니다. 실제 과거 프로젝트의 결과를 가져다 바꾸는 작업은 하지 않았습니다.

`wrong_hash`는 현재 run ID를 쓰지만 입력 hash를 64개의 0으로 기록합니다. 이 경우는 `INPUT_HASH`로 거부합니다. run ID와 hash는 추적의 근거이지 서명이나 악의적인 실행 파일에 대한 인증은 아닙니다. 이 예제는 통제한 자식 프로그램의 실수·오류를 재현하는 작업 러너입니다.

## 빠진 항목과 중복은 합계 전에 검사합니다

부모가 계획한 ID 집합은 `signed_dot`, `edge_dot`, `zero_dot`입니다. 세 항목이 전부 같은 의미로 한 번씩 있어야 전체 판정이 가능합니다. 집합만 만들면 중복이 사라지므로 ID를 사전에 넣기 전에 중복 여부를 검사합니다. 항목 하나가 빠졌거나 알 수 없는 항목이 추가되면 `CASE_SET`, ID가 두 번 나오면 `DUPLICATE_CASE`입니다.

```python
if row['id'] in found:                  # dict의 key에 같은 ID가 이미 있는지 확인합니다.
    raise InvalidReport('DUPLICATE_CASE', 'duplicate case')  # 덮어쓰기 전에 거부합니다.
if set(found) != set(ORACLE):            # 보고한 ID와 사전에 계획한 ID 집합을 비교합니다.
    raise InvalidReport('CASE_SET', 'different case IDs')
```

실행하지 않은 항목을 없애고 남은 항목만 100%라고 보고하지 않습니다. 반대로 일부 항목의 유효 FAIL을 무조건 프로세스 오류로 바꾸지도 않습니다. 계획·완료·유효 결과·기능 통과의 분모를 각각 남겨야 자동화 상태와 제품 상태를 다시 판단할 수 있습니다.

## JSON을 읽었다고 스키마가 맞는 것은 아닙니다

스키마는 필드 이름·자료형·허용값의 약속입니다. 이 형식은 버전 1의 정확한 필드 집합, 세 항목 ID와 정수 actual, PASS·FAIL 상태를 요구합니다. Python에서 `True == 1`, `False == 0`이므로 값 비교만 하면 version=True나 actual=False가 들어올 수 있습니다. 실행기는 `type(value) is int`로 순수 정수인지 확인합니다.

기본 `json.loads()`는 중복 key의 마지막 값을 사용하고 NaN도 받아들일 수 있습니다. 그래서 `object_pairs_hook`에서 중복 key를 거부하고 `parse_constant`에서 NaN 등의 확장 상수를 거부합니다. `schema_version`에 999와 1을 두 번 적은 보고서는 단순 parser에서 마지막 1만 남지만 수정한 parser에서는 `INVALID_JSON`입니다. 파싱한 결과의 버전이 bool이면 `SCHEMA`, actual이 bool이면 `FIELD_TYPE`으로 분류합니다.

이 작은 형식은 파일 크기를 64KiB 이하로 제한합니다. 모든 비신뢰 입력·무제한 표준출력·악의적인 코드에 대한 보안 샌드박스를 구현한 것은 아닙니다. 생산 러너에는 시험 도구와 결과의 버전, 자원 상한, 실행 권한과 장비 정리 정책을 별도로 정해야 합니다.

## 종료와 timeout도 결과에 남깁니다

실행 명령은 문자열로 조합하여 셸에 넘기지 않고 인자 목록과 `shell=False`를 사용합니다. 표준출력·표준오류는 서로 다른 파일에 저장합니다. 정상 대조의 제한 시간은 5초, timeout 대조는 0.25초입니다. timeout 자식은 출력 후 5초를 기다리므로 부모가 실제 자식 프로세스를 제한 시간에 종료하는 경로를 실행합니다.

`subprocess.run()`의 timeout은 프로세스를 종료하고 기다린 뒤 `TimeoutExpired`를 발생시킵니다. 부모는 이를 `TIMEOUT`으로 기록합니다. 이 API 경로에서는 `CompletedProcess.returncode`를 받지 못했으므로 returncode를 0이나 임의의 음수로 만들지 않고 `null`로 둡니다. 프로세스 생성 지연까지 포함한 엄격한 실시간 마감 보장은 아닙니다. 자식이 다시 다른 프로세스를 만드는 트리의 정리도 이번 범위에 포함하지 않습니다.

## 관측 결과

| 의도한 자식 조건 | 수정한 러너의 분류 |
|---|---|
| 정상 세 항목 | ACCEPT |
| 실제 값 184, FAIL 보고, 종료 0 | DUT_FAIL |
| 실제 값 184, 거짓 PASS | FALSE_VERDICT |
| stdout에만 PASS | MISSING_RESULT |
| 이전 시도의 결과 | RUN_ID |
| 다른 입력 hash | INPUT_HASH |
| 항목 누락·미계획 항목 | CASE_SET |
| 중복 항목 ID | DUPLICATE_CASE |
| bool 버전·bool 실제값 | SCHEMA / FIELD_TYPE |
| 끊긴 JSON·중복 key·NaN | INVALID_JSON |
| PASS 보고서가 있으나 종료 7 | EXIT_CODE |
| 제한 시간 초과 | TIMEOUT |

2026-10-21, CPython 3.12.14·Windows AMD64에서 두 번 새 폴더로 실행했습니다. 각 실행은 16개 오류 대조 조건을 예상대로 분류했습니다. 자식 프로세스는 15개가 완료했고 하나는 timeout이었습니다. 종료 0만 보거나 PASS 문자열을 덧붙여 보는 기준은 모두 14개를 수용했습니다. 엄격한 정상 수용은 한 개, 유효 DUT FAIL 보고도 한 개입니다. 이 숫자는 의도적으로 섞은 오류 fixture의 결과이며 생산 수율·결함 검출 확률을 추정하는 표본이 아닙니다.

## 직접 실행합니다

저장소 루트에서 아직 없는 출력 폴더를 지정합니다. 외부 패키지는 필요하지 않습니다.

```shell
python -B 예제_examples/실무검증_practical-validation/chip_automation/run_validation_jobs.py --out /new/path/chip-jobs
```

작업별 `input.json`, `result.json`이 존재하는 경우의 원문, `stdout.txt`, `stderr.txt`, `job.json`과 전체 `summary.json`이 저장됩니다. 결과가 없는 조건에는 없는 상태 자체를 남깁니다. 같은 출력 경로를 다시 지정하면 종료 2로 거부합니다. 전체 러너의 PASS는 오류 대조 16개가 예상과 같다는 뜻이며, 16개 DUT가 통과했다는 뜻이 아닙니다. [실행 기록](검증기록_evidence/칩시험러너오류재현_20261021.md)에서 명령·해시·보존 범위를 확인할 수 있습니다.

## 확인 문제

1. 종료 0과 PASS 글자가 있으면 결과 파일 없이 통과시켜도 됩니까?
2. 3개 계획 항목 중 2개만 PASS라면 전체 PASS입니까?
3. timeout 경로의 returncode가 `null`이면 기능 FAIL과 같습니까?

<details>
<summary>답과 이유</summary>

1. 안 됩니다. 프로세스 성공과 결과의 존재·현재성·의미는 별도로 확인합니다.
2. 아닙니다. 계획 항목의 누락으로 전체 결과가 불완전합니다.
3. 아닙니다. 유효한 기능 결과를 얻지 못한 실행 상태입니다. DUT의 기능 실패와 같은 분모로 합치지 않습니다.

</details>

## English summary

Sixteen controlled child processes separate process completion, report validity and DUT correctness. Exit-zero and stdout substring checks each accept fourteen fixtures, while strict validation accepts one normal job and preserves one valid DUT failure. Fixed hand-calculated values are independent of the child's accumulator. Attempt IDs, input hashes, case sets, JSON types and timeout records prevent the demonstrated false accepts. No physical chip or RTL simulator is exercised.

## 원자료와 읽은 범위

2026-10-21에 Python 3.12 공식 [subprocess.run·TimeoutExpired](https://docs.python.org/3.12/library/subprocess.html), [JSON의 object_pairs_hook·parse_constant와 표준 준수 설명](https://docs.python.org/3.12/library/json.html#standard-compliance-and-interoperability), [Path.mkdir](https://docs.python.org/3.12/library/pathlib.html#pathlib.Path.mkdir)을 읽었습니다. 열람 시 문서는 3.12.15, 실행 환경은 3.12.14입니다. 위 수치·오류 분류는 자체 재현 결과이며 Python 문서가 칩 시험 절차를 보증하는 것은 아닙니다.
