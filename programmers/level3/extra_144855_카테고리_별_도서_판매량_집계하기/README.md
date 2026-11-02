# 카테고리 별 도서 판매량 집계하기

Level 3 · [144855 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/144855)

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건

2022년 1월 판매량을 도서 카테고리별로 합산하고 카테고리 오름차순으로 정렬합니다.

## 풀이와 정답이 되는 이유

도서 ID로 판매 기록에 카테고리를 연결하고 2022년 1월 판매만 남깁니다. 카테고리별 SUM은 그 카테고리에 속한 모든 도서의 해당 기간 판매량을 합칩니다.

실행 비용: B권 도서·S개 판매에서 중첩 조인 상한 O(BS+S log S)

## 다른 방법과 비교

기간 내 판매량을 도서별로 먼저 합친 뒤 카테고리별로 다시 합칩니다.

| 항목 | 기본 풀이 | 도서별 판매량 선집계 |
|---|---|---|
| 코드 | [solution.sql](solution.sql) | [alternative.sql](alternative.sql) |
| 비용 | B권 도서·S개 판매에서 중첩 조인 상한 O(BS+S log S) | 행 수·인덱스·조인 계획에 따라 달라집니다 |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

테이블 기반 입력과 결과 열은 [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/144855)에서 확인할 수 있습니다.

The official problem provides the input tables and expected result columns.

SQL은 원본 100점 채점 기록을 보존하며 로컬 호환 검증과 MySQL 채점을 구분합니다.

[입력 테이블과 기대 결과](query_fixtures.json) · [실제 제출 원본](submitted_original.sql)

## English

### Task and constraints

Sum January 2022 book sales per category and order by category ascending.

`Table keys, nullability and output ordering follow the official statement.`

### Method and correctness

Join sales to books by book ID and retain January 2022 sales. SUM by category combines the period sales of every book in that category.

### Alternative and trade-offs

Preaggregate sales by book within the requested period, then sum by category.

Code: [alternative.sql](alternative.sql). Scope: alternative implementation.

Complexity: SQL runtime depends on row counts, indexes and join plans; sorting R rows costs O(R log R).

### Verification

The original 100-point grading record is retained; local compatibility checks are distinguished from MySQL grading.

[query_fixtures.json](query_fixtures.json) contains input tables and expected rows. The saved original submission received 100 points; running the current queries in SQLite is a separate compatibility check, not a new MySQL submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 카테고리 별 도서 판매량 집계하기](https://school.programmers.co.kr/learn/courses/30/lessons/144855) — 문제 조건·입력 테이블·예제 / task rules, input tables and examples. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_queries.py
```

[입력 테이블과 기대 결과 / Input tables and expected rows](query_fixtures.json) — 공식 입력·빈 테이블·독립 경계 입력에 두 SQL을 실행한 6회 SQLite 호환 검사를 통과했습니다.

Both SQL implementations passed six SQLite compatibility checks across the official-input, empty-table and independent boundary fixtures.
