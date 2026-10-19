# 자동차 대여 기록에서 대여중 / 대여 가능 여부 구분하기

Level 3 · [157340 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/157340)

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건

2022-10-16이 대여 시작일과 종료일 사이에 포함되면 대여중, 아니면 대여 가능으로 표시합니다. 자동차별 한 행, ID 내림차순입니다.

## 풀이를 따라가기

1. 2022-10-16이 대여 시작일과 종료일 사이에 포함되면 대여중, 아니면 대여 가능으로 표시합니다. 자동차별 한 행, ID 내림차순입니다.

## 왜 이 방법으로 풀 수 있나

WHERE로 행을 먼저 제한하고, 필요한 키로 묶어 집계하며, 마지막에 출력 열과 정렬을 적용합니다. 조인으로 행이 늘어날 수 있는 곳은 DISTINCT·집계·EXISTS 중 문제에 맞는 방법으로 중복을 제어합니다.

시간·공간: H개 기록을 정렬 집계하면 O(H log H), 차량별 상태 O(차량 수)

## 다른 방법과 비교

차량 목록마다 기준일이 포함되는 대여 구간의 존재를 검사합니다. 양 끝 날짜를 모두 포함합니다.

| 항목 | 기본 풀이 | 상관 EXISTS |
|---|---|---|
| 코드 | [solution.sql](solution.sql) | [alternative.sql](alternative.sql) |
| 비용 | H개 기록을 정렬 집계하면 O(H log H), 차량별 상태 O(차량 수) | SQL runtime depends on row counts, indexes and join plans |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

테이블 기반 입력과 결과 열은 [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/157340)에서 확인할 수 있습니다.

The official problem provides the input tables and expected result columns.

SQL은 원본 100점 채점 기록을 보존하며 로컬 호환 검증과 MySQL 채점을 구분합니다.

[입력 테이블과 기대 결과](query_fixtures.json) · [실제 제출 원본](submitted_original.sql)

## English

### Task and constraints

Return one availability row per car as of 2022-10-16, including both rental endpoints, ordered by car ID descending.

`Table keys, nullability and output ordering follow the official statement.`

### Method and correctness

Return one availability row per car as of 2022-10-16, including both rental endpoints, ordered by car ID descending.

### Alternative and trade-offs

For each car, test whether any closed rental interval contains the reference date.

Code: [alternative.sql](alternative.sql). Scope: alternative implementation.

Complexity: SQL runtime depends on row counts, indexes and join plans; sorting R rows costs O(R log R).

### Verification

The original 100-point grading record is retained; local compatibility checks are distinguished from MySQL grading.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 자동차 대여 기록에서 대여중 / 대여 가능 여부 구분하기](https://school.programmers.co.kr/learn/courses/30/lessons/157340) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_queries.py
```

[입력 테이블과 기대 결과 / Input tables and expected rows](query_fixtures.json) — 공식 입력·빈 테이블·독립 경계 입력에 두 SQL을 실행한 6회 SQLite 호환 검사를 통과했습니다.

Both SQL implementations passed six SQLite compatibility checks across the official-input, empty-table and independent boundary fixtures.
