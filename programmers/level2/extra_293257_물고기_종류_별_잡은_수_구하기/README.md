# 물고기 종류 별 잡은 수 구하기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/293257) · Level 2 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

물고기 종류마다 잡은 수와 이름을 출력한다.

## 조건과 입출력

입력은 아래 테이블이고 출력은 쿼리 결과 집합이다. 물고기 종류마다 잡은 수와 이름을 출력한다.

수치 배열 제한 대신 테이블 스키마와 조회 조건을 사용한다.

- `FISH_INFO`: `ID`, `FISH_TYPE`, `LENGTH`, `TIME`
- `FISH_NAME_INFO`: `FISH_TYPE`, `FISH_NAME`

## 풀이를 따라가기

이름 테이블과 연결하고 종류별 COUNT(*)를 구한다. 잡은 수를 내림차순으로 정렬한다.

[기본 풀이 / Main](solution.sql) · [다른 풀이 / Alternative](alternative.sql) · [제출 원본 / Archived submission](submitted_original.sql)

```sql
-- 이름 테이블과 연결하고 종류별 COUNT(*)를 구한다. 잡은 수를 내림차순으로 정렬한다.
SELECT COUNT(*) AS FISH_COUNT, names.FISH_NAME
FROM FISH_INFO AS f
JOIN FISH_NAME_INFO AS names ON names.FISH_TYPE = f.FISH_TYPE
GROUP BY f.FISH_TYPE, names.FISH_NAME
ORDER BY FISH_COUNT DESC
```

## 왜 맞는가

행 조건을 먼저 적용하고, 필요한 키로 연결·집계한 뒤 요구한 열과 정렬을 만든다. 이 순서를 바꾸어 행을 누락하거나 중복하지 않는 것이 핵심이다.

N=입력 행 수, G=출력 그룹 수. 논리적으로 입력을 읽고 결과를 정렬한다. 실제 시간·공간은 인덱스, 조인 방식, 윈도 정렬과 실행 계획에 따라 달라진다. / N=input rows, G=output groups. Scanning and result ordering are required logically; physical cost depends on indexes, joins, window sorts and the query plan.

주의할 점: COUNT(LENGTH)는 NULL 길이 행을 누락한다. 이름을 붙이는 조인이 포획 기록을 증식시키지 않아야 한다.

## 다른 방법: 포획 수 선집계 후 이름 조인

기본 풀이와 같은 결과를 구하되 중간 상태와 계산 방식이 다르다.

```sql
SELECT x.FISH_COUNT, n.FISH_NAME
FROM (SELECT FISH_TYPE,COUNT(*) AS FISH_COUNT FROM FISH_INFO GROUP BY FISH_TYPE) x
JOIN FISH_NAME_INFO n ON n.FISH_TYPE=x.FISH_TYPE
ORDER BY x.FISH_COUNT DESC;
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 이름 테이블과 연결하고 종류별 COUNT(*)를 구한다. 잡은 수를 내림차순으로 정렬한다. | 포획 수 선집계 후 이름 조인 |
| 비용 | N=입력 행 수, G=출력 그룹 수. 논리적으로 입력을 읽고 결과를 정렬한다. 실제 시간·공간은 인덱스, 조인 방식, 윈도 정렬과 실행 계획에 따라 달라진다. / N=input rows, G=output groups. Scanning and result ordering are required logically; physical cost depends on indexes, joins, window sorts and the query plan. | 대안도 같은 결과를 내지만 중간 집계·윈도·서브쿼리의 비용이 다르다. 성능 우열은 실행 계획으로 확인한다. / Equivalent results with different intermediate grouping, window or subquery costs; inspect the execution plan before comparing performance. |

## 검증

공식 예제 테이블을 로컬 SQLite에서 실행하고 두 쿼리의 결과를 비교했다. YEAR·MONTH·DATE_FORMAT 등은 호환 함수를 사용했다. 이는 MySQL 서버의 실행·성능 검증이나 새 사이트 제출을 뜻하지 않는다.

문제 폴더에서 `python test_query.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Return catch counts and species names for each fish type.

### Conditions and input/output

The input consists of the tables below; the output is a query result set. Return catch counts and species names for each fish type.

This SQL task is defined by table schemas and query predicates rather than array-size limits.

- `FISH_INFO`: `ID`, `FISH_TYPE`, `LENGTH`, `TIME`
- `FISH_NAME_INFO`: `FISH_TYPE`, `FISH_NAME`

### Approach

Join the name table, count all records per type, and sort counts in descending order.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Apply row predicates, join or aggregate on the required keys, then produce the requested projection and ordering. Correctness depends on neither dropping nor duplicating qualifying rows.

N=입력 행 수, G=출력 그룹 수. 논리적으로 입력을 읽고 결과를 정렬한다. 실제 시간·공간은 인덱스, 조인 방식, 윈도 정렬과 실행 계획에 따라 달라진다. / N=input rows, G=output groups. Scanning and result ordering are required logically; physical cost depends on indexes, joins, window sorts and the query plan.

Boundary cases: COUNT(LENGTH) would omit NULL lengths. The name join must not multiply catch rows.

### Alternative: Preaggregate catches before joining names

It computes the same result using different intermediate states or evaluation steps. 대안도 같은 결과를 내지만 중간 집계·윈도·서브쿼리의 비용이 다르다. 성능 우열은 실행 계획으로 확인한다. / Equivalent results with different intermediate grouping, window or subquery costs; inspect the execution plan before comparing performance.

The main approach follows the steps described above. The alternative uses preaggregate catches before joining names; compare its intermediate state and cost with the main implementation before choosing it.

### Verification

Official example tables were checked locally with SQLite and the two query results were compared. Compatibility functions supplied YEAR, MONTH, DATE_FORMAT and similar MySQL functions. This does not constitute MySQL-server execution/performance testing or a new site submission.

Run `python test_query.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 물고기 종류 별 잡은 수 구하기](https://school.programmers.co.kr/learn/courses/30/lessons/293257) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
