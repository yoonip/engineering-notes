# 오랜 기간 보호한 동물(1)

Level 3 · [59044 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/59044)

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건

아직 입양 기록이 없는 동물 중 입소가 가장 이른 세 마리의 이름·입소일을 입소일 오름차순으로 구합니다.

## 풀이와 정답이 되는 이유

입양 기록이 없는 동물만 남기고 입소 시각을 오름차순으로 정렬합니다. 같은 현재 시점에서 더 일찍 입소한 동물이 더 오래 보호되었으므로 앞의 세 행을 선택합니다.

실행 비용: I개 입소·O개 입양에서 중첩 조인과 정렬 상한 O(IO+I log I)

## 다른 방법과 비교

입양 기록이 없는 동물만 반조인으로 남긴 뒤 입소가 이른 순서로 세 마리를 고릅니다.

| 항목 | 기본 풀이 | NOT EXISTS |
|---|---|---|
| 코드 | [solution.sql](solution.sql) | [alternative.sql](alternative.sql) |
| 비용 | I개 입소·O개 입양에서 중첩 조인과 정렬 상한 O(IO+I log I) | 행 수·인덱스·조인 계획에 따라 달라집니다 |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

테이블 기반 입력과 결과 열은 [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/59044)에서 확인할 수 있습니다.

The official problem provides the input tables and expected result columns.

SQL은 원본 100점 채점 기록을 보존하며 로컬 호환 검증과 MySQL 채점을 구분합니다.

[입력 테이블과 기대 결과](query_fixtures.json) · [실제 제출 원본](submitted_original.sql)

## English

### Task and constraints

Return the names and arrival dates of the three earliest admitted animals without adoption records, ordered by admission time.

`Table keys, nullability and output ordering follow the official statement.`

### Method and correctness

Keep animals with no adoption record and order by admission time ascending. At a common present time, earlier admission means a longer stay, so select the first three rows.

### Alternative and trade-offs

Use NOT EXISTS for animals without an adoption record, then select the three earliest arrivals.

Code: [alternative.sql](alternative.sql). Scope: alternative implementation.

Complexity: SQL runtime depends on row counts, indexes and join plans; sorting R rows costs O(R log R).

### Verification

The original 100-point grading record is retained; local compatibility checks are distinguished from MySQL grading.

[query_fixtures.json](query_fixtures.json) contains input tables and expected rows. The saved original submission received 100 points; running the current queries in SQLite is a separate compatibility check, not a new MySQL submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 오랜 기간 보호한 동물(1)](https://school.programmers.co.kr/learn/courses/30/lessons/59044) — 문제 조건·입력 테이블·예제 / task rules, input tables and examples. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_queries.py
```

[입력 테이블과 기대 결과 / Input tables and expected rows](query_fixtures.json) — 공식 입력·빈 테이블·독립 경계 입력에 두 SQL을 실행한 6회 SQLite 호환 검사를 통과했습니다.

Both SQL implementations passed six SQLite compatibility checks across the official-input, empty-table and independent boundary fixtures.
