# 레벨 2~4 풀이 검증 기록 | Level 2–4 validation

이 문서는 2026-10-19에 확인한 레벨 2~4의 309문제에 대한 검증 기록입니다. 해당 문제의 조건과 예제를 공식 페이지에서 확인했으며, 각 폴더의 검증 코드로 기록된 검사를 다시 실행할 수 있습니다. 이후 추가된 자료의 검증 범위는 각 폴더의 기록을 확인하시면 됩니다.

레벨 0·1과 레벨 5의 줄별 주석본 363개는 [보관 범위](COVERAGE.md)에 있습니다. 파일 해시·주석본·Python 구문 대조는 `python programmers/tests/verify_archive.py`로 실행합니다. 아래 알고리즘 검증 309개와는 확인 범위가 다릅니다.

과거 제출본 86개는 `python programmers/tests/verify_history.py`로 원본과 새 주석본의 실행 구문 AST를 비교하고 공개 예제 197개를 각각 실행했습니다. 394회 검사가 모두 통과했습니다. [과거 제출 검증 기록](HISTORICAL_VALIDATION.json)에 입력별 결과를 남겼습니다. 사이트의 100점은 보존한 원본의 과거 채점 결과이며, 이번에 주석을 붙여 다시 제출한 결과는 아닙니다.

## 확인한 범위

| 항목 | 실행 환경과 결과 |
|---|---|
| 문제별 공개 검증 | Python 3.12.14와 3.13.14에서 각각 309개 스크립트 통과 |
| C++ | Zig 0.17.0의 C++17 컴파일러로 10개 구현 컴파일·공식 예제 26개 통과 |
| C++ 추가 대조 | Level 3 C++ 6개를 작은 생성 입력 180개에서 Python 비교 구현과 대조 |
| SQL | 75문제의 기본·대안 SQL을 SQLite 호환 환경에서 공식 입력과 경계 테이블로 대조 |
| 기존 회귀 검사 | 24개 테스트 통과 |
| 숫자 야구 451808 | 비밀번호 3,024개 전체 전략 트리에서 최대 질문 6회 확인 |
| 원본 보존 | 309개 원본 제출 파일의 SHA-256 일치, 로컬 원본 변경 없음 |

공식 예제 외에 작은 입력의 전수 탐색, 고정 시드 생성 입력, 빈 테이블·NULL·중복·공동 최댓값·날짜 경계 등 문제별 조건을 검사했습니다. 시간 복잡도 설명과 별도로, 일부 문제에는 큰 입력을 생성하는 검증도 있습니다. 각 폴더의 테스트 데이터와 실행 기록에서 실제 확인한 범위를 볼 수 있습니다.

원본의 100점은 로컬에 저장된 당시 채점 기록입니다. 주석과 풀이를 정리한 이번 구현은 로컬에서 검증했으며, 프로그래머스 사이트에 새로 제출한 기록과 구분합니다. 작은 입력에서 두 구현이 일치한다는 사실은 모든 입력의 정답성을 증명하지 않으므로, 해설의 불변식·점화식·교환 논리도 함께 기록했습니다.

SQL은 MySQL 제출 구문을 유지했습니다. 로컬 검증에서는 날짜 함수·문자열 함수 등의 호환 처리를 거쳐 SQLite에서 실행했습니다. 실제 MySQL 서버의 실행계획, 자료형 강제 변환, 정렬 규칙까지 같은 환경으로 검증한 것은 아닙니다. C++의 `bits/stdc++.h`는 필요한 표준 헤더 묶음으로 대체해 컴파일했습니다.

## 다시 실행하기

저장소 최상위에서 실행합니다. 문제별 Python 검증과 SQL 호환 검증에는 Python 표준 라이브러리만 사용합니다.

```bash
python programmers/tests/verify_all.py --report programmers-local-report.json
python -B -m unittest discover -s programmers/Python/tests
```

C++은 컴파일러를 별도로 지정합니다. GCC, Clang 또는 Zig를 사용할 수 있습니다.

```bash
python programmers/tests/test_cpp.py --compiler /path/to/g++
```

각 문제 폴더의 `test_solution.py`, `verify.py`, `test_query.py`, `test_queries.py`를 개별 실행할 수도 있습니다. 큰 입력 검사와 전체 질문 전략 검사는 해당 폴더의 별도 `verify_large.py`·`verify_strategy.py`에 있습니다.

## 지문·제출본에서 확인한 차이

- 284527: 공식 예제의 사원 번호 표기가 입력과 결과에서 다릅니다. 입력의 실제 키를 기준으로 확인했습니다.
- 273709·273710·273711: `RARITY` 자료형 표는 INTEGER이지만 본문과 입력 값은 문자열입니다.
- 164670: 자료형 표의 `NICKANME`와 본문·예제의 `NICKNAME` 철자가 다릅니다.
- 164671: 본문의 파일 ID 내림차순 요구와 예제 결과의 순서가 다릅니다. 본문의 정렬 조건을 따랐습니다.
- 157339: 공식 입력의 대여료를 기간과 할인율로 다시 계산하면 예제 결과표와 다른 값이 나옵니다. 해당 해설에 식과 계산 결과를 적었습니다.
- 131124: 원본 제출본의 `LIMIT 1`은 공동 최다 회원을 누락할 수 있습니다. 현재 두 SQL은 공동 최다를 모두 포함하며 동률 테이블을 추가했습니다.

문제별 공식 출처와 자세한 차이는 해당 README에 있습니다. [전체 실행 기록](VALIDATION.json)과 [파일별 원본 해시](catalog.json)를 함께 확인할 수 있습니다.

## English

Checked on 2026-10-19. Official statements and examples were consulted for all 309 problems, and each folder includes reproducible verification code.

The 363 annotated submissions at Levels 0, 1 and 5 have separate [archive coverage](COVERAGE.md). For the 86 historical entries, `tests/verify_history.py` checked identical executable ASTs and ran both source versions on 197 public examples. All 394 executions passed; [records](HISTORICAL_VALIDATION.json) identify each case. The preserved originals have accepted website results, while the newly annotated copies were tested locally without resubmission.

The 309 per-problem scripts passed under both Python 3.12.14 and 3.13.14. Ten C++ implementations compiled as C++17 with Zig 0.17.0 and passed 26 official examples; six Level 3 implementations were additionally cross-checked against Python comparisons on 180 small generated inputs. All 75 SQL problems were compared using SQLite compatibility fixtures. The 24 existing regression tests also passed. The complete 3,024-secret strategy tree for problem 451808 required at most six queries. SHA-256 checks matched all 309 preserved submissions, and the local originals were unchanged.

Checks include official examples, tiny exhaustive cases, fixed-seed generated cases and relevant boundary conditions: empty tables, NULLs, duplicates, tied maxima and date boundaries. Some folders also provide larger-input checks. Individual data and run records identify the actual coverage. Agreement between implementations is evidence for the tested inputs, not a universal proof; explanations also give invariants, recurrences or exchange arguments.

The saved 100-point grades belong to the original local grading records. The documented implementations were tested locally, without a new website submission. SQL remains in MySQL submission syntax but is locally executed through a SQLite compatibility adapter for functions such as date and string operations. This does not reproduce MySQL query plans, type coercion or collations. The C++ build supplies standard headers in place of the GCC umbrella header `bits/stdc++.h`.

Run `python programmers/tests/verify_all.py` from the repository root for per-problem Python and SQL checks, or run a folder's script separately. The harness uses Python's standard library. Run `python programmers/tests/test_cpp.py --compiler /path/to/g++` with GCC, Clang or Zig for C++ examples. Dedicated large-input and whole-strategy checks are included as `verify_large.py` and `verify_strategy.py` where applicable.

Recorded source discrepancies include the employee ID in 284527, the RARITY type in 273709–273711, NICKANME/NICKNAME in 164670, output ordering in 164671, and independently recalculated rental fees in 157339. Each problem links its official source and explains the discrepancy. For 131124, the documented queries fix the saved submission's single-winner limit to retain all tied leaders; a tie fixture verifies this behavior.

[Execution record](VALIDATION.json) · [Original source hashes](catalog.json) · [Problem index](README.md)
