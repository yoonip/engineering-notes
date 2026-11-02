# 조건에 맞는 사용자 정보 조회하기

Level 3 · [164670 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/164670)

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건

게시글을 3개 이상 작성한 사용자의 ID·닉네임·전체주소·전화번호를 구합니다. 주소는 공백으로 연결하고 전화번호는 3-4-4 자리로 나누며 ID 내림차순입니다.

## 풀이와 정답이 되는 이유

작성자별 게시글 수가 3 이상인 ID 집합을 먼저 구합니다. 이 집합에 속한 사용자만 선택하므로 게시글 수만큼 사용자가 중복되지 않으며, 주소와 전화번호는 마지막에 출력 형식으로 조합합니다.

실행 비용: U명 사용자·B개 게시글에서 단순 집계·멤버십 상한 O(B log B+UB+U log U)

## 다른 방법과 비교

3개 이상 작성한 사용자 집계를 먼저 만들고 사용자 테이블에 조인합니다.

| 항목 | 기본 풀이 | 집계 결과 조인 |
|---|---|---|
| 코드 | [solution.sql](solution.sql) | [alternative.sql](alternative.sql) |
| 비용 | U명 사용자·B개 게시글에서 단순 집계·멤버십 상한 O(B log B+UB+U log U) | 행 수·인덱스·조인 계획에 따라 달라집니다 |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

테이블 기반 입력과 결과 열은 [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/164670)에서 확인할 수 있습니다.

The official problem provides the input tables and expected result columns.

SQL은 원본 100점 채점 기록을 보존하며 로컬 호환 검증과 MySQL 채점을 구분합니다.

[입력 테이블과 기대 결과](query_fixtures.json) · [실제 제출 원본](submitted_original.sql)

## English

### Task and constraints

Return ID, nickname, space-joined full address, and 3-4-4 formatted phone number for users with at least three posts, ordered by user ID descending.

`Table keys, nullability and output ordering follow the official statement.`

### Method and correctness

First identify author IDs with at least three posts. Select users belonging to that set without duplicating them for each post, then format their address and telephone number.

### Alternative and trade-offs

Aggregate users with at least three posts, then join user details.

Code: [alternative.sql](alternative.sql). Scope: alternative implementation.

Complexity: SQL runtime depends on row counts, indexes and join plans; sorting R rows costs O(R log R).

### Verification

The original 100-point grading record is retained; local compatibility checks are distinguished from MySQL grading.

[query_fixtures.json](query_fixtures.json) contains input tables and expected rows. The saved original submission received 100 points; running the current queries in SQLite is a separate compatibility check, not a new MySQL submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 조건에 맞는 사용자 정보 조회하기](https://school.programmers.co.kr/learn/courses/30/lessons/164670) — 문제 조건·입력 테이블·예제 / task rules, input tables and examples. 확인 / checked: 2026-10-19.

## 예제 표기 확인 / Example consistency

공식 스키마 표에는 닉네임 열이 NICKANME로 적힌 곳이 있지만 본문·예제와 제출 인터페이스는 NICKNAME입니다. 코드는 NICKNAME을 사용합니다.

The schema table contains a NICKANME typo; the prose, examples and submission interface use NICKNAME, which the query follows.

## 실행 / Run

```bash
python test_queries.py
```

[입력 테이블과 기대 결과 / Input tables and expected rows](query_fixtures.json) — 공식 입력·빈 테이블·독립 경계 입력에 두 SQL을 실행한 6회 SQLite 호환 검사를 통과했습니다.

Both SQL implementations passed six SQLite compatibility checks across the official-input, empty-table and independent boundary fixtures.
