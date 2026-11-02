# 조회수가 가장 많은 중고거래 게시판의 첨부파일 조회하기

Level 3 · [164671 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/164671)

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건

최대 조회수 게시글의 모든 첨부파일 경로를 만들고 파일 ID 내림차순으로 정렬합니다. 최대 조회수 게시글은 하나입니다.

## 풀이와 정답이 되는 이유

전체 게시글의 최대 조회수와 같은 게시글을 선택하고 그 게시글 ID에 연결된 파일을 구합니다. 파일 경로는 지정된 디렉터리·게시글 ID·파일 ID·이름·확장자를 연결하며, 정렬 기준은 경로가 아니라 파일 ID입니다.

실행 비용: B개 게시글·F개 파일에서 인덱스 없는 중첩 조인 상한 O(BF+F log F), 결과·중간행 공간은 실행계획에 따름

## 다른 방법과 비교

최대 조회수를 먼저 고른 CTE와 파일을 조인합니다.

| 항목 | 기본 풀이 | 최대 조회수 게시물 CTE |
|---|---|---|
| 코드 | [solution.sql](solution.sql) | [alternative.sql](alternative.sql) |
| 비용 | B개 게시글·F개 파일에서 인덱스 없는 중첩 조인 상한 O(BF+F log F), 결과·중간행 공간은 실행계획에 따름 | 행 수·인덱스·조인 계획에 따라 달라집니다 |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

테이블 기반 입력과 결과 열은 [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/164671)에서 확인할 수 있습니다.

The official problem provides the input tables and expected result columns.

SQL은 원본 100점 채점 기록을 보존하며 로컬 호환 검증과 MySQL 채점을 구분합니다.

[입력 테이블과 기대 결과](query_fixtures.json) · [실제 제출 원본](submitted_original.sql)

## English

### Task and constraints

Return every attachment path for the unique maximum-view board, ordered by file ID descending.

`Table keys, nullability and output ordering follow the official statement.`

### Method and correctness

Select the board with the global maximum view count and join its files by board ID. Build each path from the required directory, board ID, file ID, name and extension; sort by file ID rather than the path string.

### Alternative and trade-offs

Select the maximum-view board in a CTE, then join files.

Code: [alternative.sql](alternative.sql). Scope: alternative implementation.

Complexity: SQL runtime depends on row counts, indexes and join plans; sorting R rows costs O(R log R).

### Verification

The original 100-point grading record is retained; local compatibility checks are distinguished from MySQL grading.

[query_fixtures.json](query_fixtures.json) contains input tables and expected rows. The saved original submission received 100 points; running the current queries in SQLite is a separate compatibility check, not a new MySQL submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 조회수가 가장 많은 중고거래 게시판의 첨부파일 조회하기](https://school.programmers.co.kr/learn/courses/30/lessons/164671) — 문제 조건·입력 테이블·예제 / task rules, input tables and examples. 확인 / checked: 2026-10-19.

## 예제 표기 확인 / Example consistency

공식 지시문은 FILE_ID 내림차순을 요구하지만 예제 결과표의 두 파일은 반대 순서로 표시되어 있습니다. 코드는 지시문의 내림차순을 따릅니다.

The instruction requires descending FILE_ID, while the two example output rows are displayed in the opposite order. The query follows the required descending order.

## 실행 / Run

```bash
python test_queries.py
```

[입력 테이블과 기대 결과 / Input tables and expected rows](query_fixtures.json) — 공식 입력·빈 테이블·독립 경계 입력에 두 SQL을 실행한 6회 SQLite 호환 검사를 통과했습니다.

Both SQL implementations passed six SQLite compatibility checks across the official-input, empty-table and independent boundary fixtures.
