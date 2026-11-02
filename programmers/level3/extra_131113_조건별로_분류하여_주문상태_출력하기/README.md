# 조건별로 분류하여 주문상태 출력하기

Level 3 · [131113 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/131113)

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건

출고일이 2022-05-01 이하이면 출고완료, 이후이면 출고대기, NULL이면 출고미정입니다. 날짜는 YYYY-MM-DD, 주문 ID 오름차순입니다.

## 풀이와 정답이 되는 이유

CASE는 출고일이 NULL인지 먼저 확인한 뒤 기준일 이하와 이후를 구분합니다. 세 경우가 모든 주문을 포함하므로 행을 제거하거나 집계하지 않고 각 주문의 상태를 결정합니다.

실행 비용: F개 주문의 행별 분류 O(F), 정렬 포함 O(F log F)

## 다른 방법과 비교

출고일 NULL을 먼저 분기하고 기준일 이하·초과를 나눕니다. CASE와 IF의 표현 차이를 비교합니다.

| 항목 | 기본 풀이 | NULL 우선 IF |
|---|---|---|
| 코드 | [solution.sql](solution.sql) | [alternative.sql](alternative.sql) |
| 비용 | F개 주문의 행별 분류 O(F), 정렬 포함 O(F log F) | 행 수·인덱스·조인 계획에 따라 달라집니다 |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

테이블 기반 입력과 결과 열은 [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/131113)에서 확인할 수 있습니다.

The official problem provides the input tables and expected result columns.

SQL은 원본 100점 채점 기록을 보존하며 로컬 호환 검증과 MySQL 채점을 구분합니다.

[입력 테이블과 기대 결과](query_fixtures.json) · [실제 제출 원본](submitted_original.sql)

## English

### Task and constraints

Classify shipping dates as completed on or before 2022-05-01, pending afterwards, or unknown for NULL. Format dates YYYY-MM-DD and order by order ID ascending.

`Table keys, nullability and output ordering follow the official statement.`

### Method and correctness

CASE first handles a NULL shipping date, then separates dates on or before the deadline from later dates. These cases cover every order; no row filtering or aggregation is needed.

### Alternative and trade-offs

Handle a NULL ship date first, then split at the inclusive deadline. This compares CASE with nested IF.

Code: [alternative.sql](alternative.sql). Scope: alternative implementation.

Complexity: SQL runtime depends on row counts, indexes and join plans; sorting R rows costs O(R log R).

### Verification

The original 100-point grading record is retained; local compatibility checks are distinguished from MySQL grading.

[query_fixtures.json](query_fixtures.json) contains input tables and expected rows. The saved original submission received 100 points; running the current queries in SQLite is a separate compatibility check, not a new MySQL submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 조건별로 분류하여 주문상태 출력하기](https://school.programmers.co.kr/learn/courses/30/lessons/131113) — 문제 조건·입력 테이블·예제 / task rules, input tables and examples. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_queries.py
```

[입력 테이블과 기대 결과 / Input tables and expected rows](query_fixtures.json) — 공식 입력·빈 테이블·독립 경계 입력에 두 SQL을 실행한 6회 SQLite 호환 검사를 통과했습니다.

Both SQL implementations passed six SQLite compatibility checks across the official-input, empty-table and independent boundary fixtures.
