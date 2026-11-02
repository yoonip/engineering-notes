# 즐겨찾기가 가장 많은 식당 정보 출력하기

Level 3 · [131123 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/131123)

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건

음식 종류별 즐겨찾기가 가장 많은 식당의 종류·ID·이름·즐겨찾기 수를 구하고 음식 종류 내림차순으로 정렬합니다.

## 풀이와 정답이 되는 이유

각 식당의 즐겨찾기 수를 같은 음식 종류에서 구한 MAX와 비교합니다. MAX는 NULL을 제외하므로 숫자 값이 없는 분류는 출력하지 않으며, 숫자 최댓값과 같은 행은 모두 남습니다. 음식 종류의 <=> 비교는 양쪽이 NULL일 때도 같은 분류로 취급합니다.

실행 비용: R개 식당에서 상관 MAX를 매번 스캔하면 O(R²+R log R)

## 다른 방법과 비교

DENSE_RANK에서 NULL만 있는 분류도 1위를 받으므로 FAVORITES IS NOT NULL을 함께 검사합니다. NULL은 최댓값 후보에서 제외하며, 숫자 값이 전혀 없는 분류는 출력하지 않습니다.

음식 종류마다 즐겨찾기 내림차순 순위를 매기고 공동 1위까지 남깁니다.

| 항목 | 기본 풀이 | DENSE_RANK |
|---|---|---|
| 코드 | [solution.sql](solution.sql) | [alternative.sql](alternative.sql) |
| 비용 | R개 식당에서 상관 MAX를 매번 스캔하면 O(R²+R log R) | 행 수·인덱스·조인 계획에 따라 달라집니다 |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

테이블 기반 입력과 결과 열은 [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/131123)에서 확인할 수 있습니다.

The official problem provides the input tables and expected result columns.

SQL은 원본 100점 채점 기록을 보존하며 로컬 호환 검증과 MySQL 채점을 구분합니다.

[입력 테이블과 기대 결과](query_fixtures.json) · [실제 제출 원본](submitted_original.sql)

## English

### Task and constraints

Return food type, ID, name and favorites for each type’s maximum-favorite restaurant, ordered by food type descending.

`Table keys, nullability and output ordering follow the official statement.`

### Method and correctness

Compare each restaurant with the MAX of its food type. MAX ignores NULL, so a type with no numeric favorite count is omitted; every row equal to a numeric maximum is retained. The null-safe <=> comparison treats two NULL food types as one group.

### Alternative and trade-offs

DENSE_RANK also assigns rank one to an all-NULL group, so FAVORITES IS NOT NULL is required. NULL is not a candidate maximum; omit a type with no numeric value.

Rank favorites within each food type and retain all tied first-place rows.

Code: [alternative.sql](alternative.sql). Scope: alternative implementation.

Complexity: SQL runtime depends on row counts, indexes and join plans; sorting R rows costs O(R log R).

### Verification

The original 100-point grading record is retained; local compatibility checks are distinguished from MySQL grading.

[query_fixtures.json](query_fixtures.json) contains input tables and expected rows. The saved original submission received 100 points; running the current queries in SQLite is a separate compatibility check, not a new MySQL submission.

## 출처 / Sources

- [MySQL 8.4 집계 함수](https://dev.mysql.com/doc/refman/8.4/en/aggregate-functions.html) — MAX의 NULL 제외 규칙 / NULL handling in MAX. 확인 / checked: 2026-11-02.
- [프로그래머스 공식 문제: 즐겨찾기가 가장 많은 식당 정보 출력하기](https://school.programmers.co.kr/learn/courses/30/lessons/131123) — 문제 조건·입력 테이블·예제 / task rules, input tables and examples. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_queries.py
```

[입력 테이블과 기대 결과 / Input tables and expected rows](query_fixtures.json) — 공식 입력·빈 테이블·독립 경계 입력에 두 SQL을 실행한 8회 SQLite 호환 검사를 통과했습니다. NULL만 있는 분류와 숫자·NULL 혼합 분류를 별도 경계 입력으로 포함합니다.

Both SQL implementations passed eight SQLite compatibility checks, including an additional fixture with an all-NULL group and a mixed numeric/NULL group.
