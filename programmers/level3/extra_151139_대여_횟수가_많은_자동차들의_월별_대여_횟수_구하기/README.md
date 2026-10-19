# 대여 횟수가 많은 자동차들의 월별 대여 횟수 구하기

Level 3 · [151139 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/151139)

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건

2022년 8~10월 시작 대여가 총 5회 이상인 자동차를 골라 해당 기간의 월별 건수를 구합니다. 월 오름차순, 차량 ID 내림차순이며 0건인 월은 제외합니다.

## 풀이를 따라가기

1. 2022년 8~10월 시작 대여가 총 5회 이상인 자동차를 골라 해당 기간의 월별 건수를 구합니다. 월 오름차순, 차량 ID 내림차순이며 0건인 월은 제외합니다.

## 왜 이 방법으로 풀 수 있나

WHERE로 행을 먼저 제한하고, 필요한 키로 묶어 집계하며, 마지막에 출력 열과 정렬을 적용합니다. 조인으로 행이 늘어날 수 있는 곳은 DISTINCT·집계·EXISTS 중 문제에 맞는 방법으로 중복을 제어합니다.

시간·공간: H개 기록에서 단순 IN 조회를 포함한 보수적 상한 O(H²+H log H)

## 다른 방법과 비교

먼저 월별 기록 수를 만든 후 차량별 합을 윈도 함수로 구해 5회 이상만 남깁니다.

| 항목 | 기본 풀이 | 월 집계 후 윈도 합 |
|---|---|---|
| 코드 | [solution.sql](solution.sql) | [alternative.sql](alternative.sql) |
| 비용 | H개 기록에서 단순 IN 조회를 포함한 보수적 상한 O(H²+H log H) | SQL runtime depends on row counts, indexes and join plans |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

테이블 기반 입력과 결과 열은 [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/151139)에서 확인할 수 있습니다.

The official problem provides the input tables and expected result columns.

SQL은 원본 100점 채점 기록을 보존하며 로컬 호환 검증과 MySQL 채점을 구분합니다.

[입력 테이블과 기대 결과](query_fixtures.json) · [실제 제출 원본](submitted_original.sql)

## English

### Task and constraints

For cars with at least five rental starts during August–October 2022, return monthly counts in that period. Order by month ascending and car ID descending; omit zero-count months.

`Table keys, nullability and output ordering follow the official statement.`

### Method and correctness

For cars with at least five rental starts during August–October 2022, return monthly counts in that period. Order by month ascending and car ID descending; omit zero-count months.

### Alternative and trade-offs

Aggregate monthly records, then use a window sum for each car’s period total.

Code: [alternative.sql](alternative.sql). Scope: alternative implementation.

Complexity: SQL runtime depends on row counts, indexes and join plans; sorting R rows costs O(R log R).

### Verification

The original 100-point grading record is retained; local compatibility checks are distinguished from MySQL grading.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 대여 횟수가 많은 자동차들의 월별 대여 횟수 구하기](https://school.programmers.co.kr/learn/courses/30/lessons/151139) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_queries.py
```

[입력 테이블과 기대 결과 / Input tables and expected rows](query_fixtures.json) — 공식 입력·빈 테이블·독립 경계 입력에 두 SQL을 실행한 6회 SQLite 호환 검사를 통과했습니다.

Both SQL implementations passed six SQLite compatibility checks across the official-input, empty-table and independent boundary fixtures.
