# 대여 횟수가 많은 자동차들의 월별 대여 횟수 구하기

Level 3 · [151139 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/151139)

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건

2022년 8~10월 시작 대여가 총 5회 이상인 자동차를 골라 해당 기간의 월별 건수를 구합니다. 월 오름차순, 차량 ID 내림차순이며 0건인 월은 제외합니다.

## 풀이와 정답이 되는 이유

8월부터 10월까지의 시작일 조건을 자격 판단과 월별 집계에 똑같이 적용합니다. 전체 기간에 5회 이상 대여한 자동차만 고른 뒤 월·자동차별로 세므로, 월마다 5회 이상이어야 한다는 잘못된 조건을 추가하지 않습니다.

실행 비용: H개 기록에서 단순 IN 조회를 포함한 보수적 상한 O(H²+H log H)

## 다른 방법과 비교

먼저 월별 기록 수를 만든 후 차량별 합을 윈도 함수로 구해 5회 이상만 남깁니다.

| 항목 | 기본 풀이 | 월 집계 후 윈도 합 |
|---|---|---|
| 코드 | [solution.sql](solution.sql) | [alternative.sql](alternative.sql) |
| 비용 | H개 기록에서 단순 IN 조회를 포함한 보수적 상한 O(H²+H log H) | 행 수·인덱스·조인 계획에 따라 달라집니다 |
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

Use the same August-through-October start-date range for eligibility and monthly counts. Select cars rented at least five times over the full period, then count by month and car; five rentals are not required in each month.

### Alternative and trade-offs

Aggregate monthly records, then use a window sum for each car’s period total.

Code: [alternative.sql](alternative.sql). Scope: alternative implementation.

Complexity: SQL runtime depends on row counts, indexes and join plans; sorting R rows costs O(R log R).

### Verification

The original 100-point grading record is retained; local compatibility checks are distinguished from MySQL grading.

[query_fixtures.json](query_fixtures.json) contains input tables and expected rows. The saved original submission received 100 points; running the current queries in SQLite is a separate compatibility check, not a new MySQL submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 대여 횟수가 많은 자동차들의 월별 대여 횟수 구하기](https://school.programmers.co.kr/learn/courses/30/lessons/151139) — 문제 조건·입력 테이블·예제 / task rules, input tables and examples. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_queries.py
```

[입력 테이블과 기대 결과 / Input tables and expected rows](query_fixtures.json) — 공식 입력·빈 테이블·독립 경계 입력에 두 SQL을 실행한 6회 SQLite 호환 검사를 통과했습니다.

Both SQL implementations passed six SQLite compatibility checks across the official-input, empty-table and independent boundary fixtures.
