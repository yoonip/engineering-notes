# 대여 기록이 존재하는 자동차 리스트 구하기

Level 3 · [157341 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/157341)

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건

세단 중 10월에 대여 시작 기록이 있는 자동차 ID를 중복 없이 구하고 내림차순 정렬합니다.

## 풀이와 정답이 되는 이유

자동차와 대여 기록을 연결해 세단이면서 10월에 대여를 시작한 기록만 남깁니다. 같은 차의 조건에 맞는 기록이 여러 개라도 DISTINCT로 자동차 ID를 한 번만 출력합니다.

실행 비용: C대 차량·H개 기록에서 중첩 조인 상한 O(CH+H log H)

## 다른 방법과 비교

각 세단에 대해 10월에 시작한 대여 기록의 존재만 확인합니다. 중복 대여가 있어도 차량이 중복되지 않습니다.

| 항목 | 기본 풀이 | EXISTS 세미 조인 |
|---|---|---|
| 코드 | [solution.sql](solution.sql) | [alternative.sql](alternative.sql) |
| 비용 | C대 차량·H개 기록에서 중첩 조인 상한 O(CH+H log H) | 행 수·인덱스·조인 계획에 따라 달라집니다 |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

테이블 기반 입력과 결과 열은 [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/157341)에서 확인할 수 있습니다.

The official problem provides the input tables and expected result columns.

SQL은 원본 100점 채점 기록을 보존하며 로컬 호환 검증과 MySQL 채점을 구분합니다.

[입력 테이블과 기대 결과](query_fixtures.json) · [실제 제출 원본](submitted_original.sql)

## English

### Task and constraints

Return distinct sedan IDs having a rental beginning in October, ordered descending.

`Table keys, nullability and output ordering follow the official statement.`

### Method and correctness

Join cars to rentals and retain sedan rentals beginning in October. DISTINCT emits each car ID once even when several matching rental records exist.

### Alternative and trade-offs

Use EXISTS to test for an October rental start. Multiple qualifying rentals never duplicate a car.

Code: [alternative.sql](alternative.sql). Scope: alternative implementation.

Complexity: SQL runtime depends on row counts, indexes and join plans; sorting R rows costs O(R log R).

### Verification

The original 100-point grading record is retained; local compatibility checks are distinguished from MySQL grading.

[query_fixtures.json](query_fixtures.json) contains input tables and expected rows. The saved original submission received 100 points; running the current queries in SQLite is a separate compatibility check, not a new MySQL submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 대여 기록이 존재하는 자동차 리스트 구하기](https://school.programmers.co.kr/learn/courses/30/lessons/157341) — 문제 조건·입력 테이블·예제 / task rules, input tables and examples. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_queries.py
```

[입력 테이블과 기대 결과 / Input tables and expected rows](query_fixtures.json) — 공식 입력·빈 테이블·독립 경계 입력에 두 SQL을 실행한 6회 SQLite 호환 검사를 통과했습니다.

Both SQL implementations passed six SQLite compatibility checks across the official-input, empty-table and independent boundary fixtures.
