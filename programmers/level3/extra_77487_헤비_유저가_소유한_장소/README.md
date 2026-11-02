# 헤비 유저가 소유한 장소

Level 3 · [77487 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/77487)

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건

장소를 2개 이상 등록한 호스트가 가진 모든 장소의 ID·이름·호스트 ID를 출력하고 장소 ID 오름차순으로 정렬합니다.

## 풀이와 정답이 되는 이유

소유자별 공간 수를 세어 두 개 이상인 소유자 ID를 구한 뒤 그 소유자의 모든 공간을 출력합니다. 소유자별 한 행을 출력하는 것이 아니라 해당 소유자가 등록한 공간 각각을 남깁니다.

실행 비용: P개 장소에서 단순 멤버십 탐색 상한 O(P²+P log P)

## 다른 방법과 비교

호스트별 행 수를 윈도 함수로 붙이고 2개 이상 소유한 행을 남깁니다.

| 항목 | 기본 풀이 | 윈도 COUNT |
|---|---|---|
| 코드 | [solution.sql](solution.sql) | [alternative.sql](alternative.sql) |
| 비용 | P개 장소에서 단순 멤버십 탐색 상한 O(P²+P log P) | 행 수·인덱스·조인 계획에 따라 달라집니다 |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

테이블 기반 입력과 결과 열은 [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/77487)에서 확인할 수 있습니다.

The official problem provides the input tables and expected result columns.

SQL은 원본 100점 채점 기록을 보존하며 로컬 호환 검증과 MySQL 채점을 구분합니다.

[입력 테이블과 기대 결과](query_fixtures.json) · [실제 제출 원본](submitted_original.sql)

## English

### Task and constraints

Return all places owned by hosts with at least two places, ordered by place ID ascending.

`Table keys, nullability and output ordering follow the official statement.`

### Method and correctness

Count spaces per owner, identify owners with at least two, and return every space belonging to those owners. The output contains spaces rather than one summary row per owner.

### Alternative and trade-offs

Attach a host-level window count and retain hosts owning at least two places.

Code: [alternative.sql](alternative.sql). Scope: alternative implementation.

Complexity: SQL runtime depends on row counts, indexes and join plans; sorting R rows costs O(R log R).

### Verification

The original 100-point grading record is retained; local compatibility checks are distinguished from MySQL grading.

[query_fixtures.json](query_fixtures.json) contains input tables and expected rows. The saved original submission received 100 points; running the current queries in SQLite is a separate compatibility check, not a new MySQL submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 헤비 유저가 소유한 장소](https://school.programmers.co.kr/learn/courses/30/lessons/77487) — 문제 조건·입력 테이블·예제 / task rules, input tables and examples. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_queries.py
```

[입력 테이블과 기대 결과 / Input tables and expected rows](query_fixtures.json) — 공식 입력·빈 테이블·독립 경계 입력에 두 SQL을 실행한 6회 SQLite 호환 검사를 통과했습니다.

Both SQL implementations passed six SQLite compatibility checks across the official-input, empty-table and independent boundary fixtures.
