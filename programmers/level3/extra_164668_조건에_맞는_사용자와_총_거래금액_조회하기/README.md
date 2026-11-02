# 조건에 맞는 사용자와 총 거래금액 조회하기

Level 3 · [164668 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/164668)

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건

거래 완료(DONE) 금액 합이 700,000원 이상인 사용자의 ID·닉네임·총액을 구하고 총액 오름차순으로 정렬합니다.

## 풀이와 정답이 되는 이유

완료된 거래만 사용자에게 연결한 뒤 사용자별 가격을 더합니다. HAVING은 개별 거래 가격이 아니라 완료 거래의 합계가 70만 원 이상인지 검사합니다.

실행 비용: U명 사용자·B개 게시글에서 중첩 조인·정렬 집계 상한 O(UB+B log B+U log U)

## 다른 방법과 비교

완료된 거래만 사용자별로 먼저 합산해 조인 중간 행을 줄입니다.

| 항목 | 기본 풀이 | 완료 거래 선집계 |
|---|---|---|
| 코드 | [solution.sql](solution.sql) | [alternative.sql](alternative.sql) |
| 비용 | U명 사용자·B개 게시글에서 중첩 조인·정렬 집계 상한 O(UB+B log B+U log U) | 행 수·인덱스·조인 계획에 따라 달라집니다 |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

테이블 기반 입력과 결과 열은 [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/164668)에서 확인할 수 있습니다.

The official problem provides the input tables and expected result columns.

SQL은 원본 100점 채점 기록을 보존하며 로컬 호환 검증과 MySQL 채점을 구분합니다.

[입력 테이블과 기대 결과](query_fixtures.json) · [실제 제출 원본](submitted_original.sql)

## English

### Task and constraints

Return user ID, nickname and completed-sale total of at least 700,000, ordered by the total ascending.

`Table keys, nullability and output ordering follow the official statement.`

### Method and correctness

Join only completed transactions to users and sum their prices per user. HAVING tests whether the completed-sales total, rather than any individual transaction, reaches 700,000.

### Alternative and trade-offs

Preaggregate completed sales per writer before joining users.

Code: [alternative.sql](alternative.sql). Scope: alternative implementation.

Complexity: SQL runtime depends on row counts, indexes and join plans; sorting R rows costs O(R log R).

### Verification

The original 100-point grading record is retained; local compatibility checks are distinguished from MySQL grading.

[query_fixtures.json](query_fixtures.json) contains input tables and expected rows. The saved original submission received 100 points; running the current queries in SQLite is a separate compatibility check, not a new MySQL submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 조건에 맞는 사용자와 총 거래금액 조회하기](https://school.programmers.co.kr/learn/courses/30/lessons/164668) — 문제 조건·입력 테이블·예제 / task rules, input tables and examples. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_queries.py
```

[입력 테이블과 기대 결과 / Input tables and expected rows](query_fixtures.json) — 공식 입력·빈 테이블·독립 경계 입력에 두 SQL을 실행한 6회 SQLite 호환 검사를 통과했습니다.

Both SQL implementations passed six SQLite compatibility checks across the official-input, empty-table and independent boundary fixtures.
