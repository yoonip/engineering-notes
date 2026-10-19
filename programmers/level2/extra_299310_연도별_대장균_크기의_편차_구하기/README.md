# 연도별 대장균 크기의 편차 구하기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/299310) · Level 2 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

각 개체의 크기를 같은 분화 연도 최댓값에서 뺀 편차를 구한다.

## 조건과 입출력

입력은 아래 테이블이고 출력은 쿼리 결과 집합이다. 각 개체의 크기를 같은 분화 연도 최댓값에서 뺀 편차를 구한다.

수치 배열 제한 대신 테이블 스키마와 조회 조건을 사용한다.

- `ECOLI_DATA`: `ID`, `PARENT_ID`, `SIZE_OF_COLONY`, `DIFFERENTIATION_DATE`, `GENOTYPE`

## 풀이를 따라가기

연도별 윈도 MAX로 각 행에 최댓값을 붙이고 자기 크기를 뺀다. ID를 보존하면서 연도·편차 오름차순으로 정렬한다.

[기본 풀이 / Main](solution.sql) · [다른 풀이 / Alternative](alternative.sql) · [제출 원본 / Archived submission](submitted_original.sql)

```sql
-- 연도별 윈도 MAX로 각 행에 최댓값을 붙이고 자기 크기를 뺀다. ID를 보존하면서 연도·편차 오름차순으로 정렬한다.
SELECT YEAR(DIFFERENTIATION_DATE) AS YEAR,
       MAX(SIZE_OF_COLONY) OVER (PARTITION BY YEAR(DIFFERENTIATION_DATE)) - SIZE_OF_COLONY AS YEAR_DEV,
       ID
FROM ECOLI_DATA
ORDER BY YEAR, YEAR_DEV
```

## 왜 맞는가

행 조건을 먼저 적용하고, 필요한 키로 연결·집계한 뒤 요구한 열과 정렬을 만든다. 이 순서를 바꾸어 행을 누락하거나 중복하지 않는 것이 핵심이다.

N=입력 행 수, G=출력 그룹 수. 논리적으로 입력을 읽고 결과를 정렬한다. 실제 시간·공간은 인덱스, 조인 방식, 윈도 정렬과 실행 계획에 따라 달라진다. / N=input rows, G=output groups. Scanning and result ordering are required logically; physical cost depends on indexes, joins, window sorts and the query plan.

주의할 점: GROUP BY만으로 원본 개체 행을 합치지 않는다. 같은 연도 최고 크기는 편차 0이다.

## 다른 방법: 연도별 집계 테이블 조인

기본 풀이와 같은 결과를 구하되 중간 상태와 계산 방식이 다르다.

```sql
SELECT YEAR(c.DIFFERENTIATION_DATE) AS YEAR,
       a.BIGGEST-c.SIZE_OF_COLONY AS YEAR_DEV, c.ID
FROM ECOLI_DATA c
JOIN (
    SELECT YEAR(DIFFERENTIATION_DATE) AS Y, MAX(SIZE_OF_COLONY) AS BIGGEST
    FROM ECOLI_DATA GROUP BY YEAR(DIFFERENTIATION_DATE)
) a ON a.Y=YEAR(c.DIFFERENTIATION_DATE)
ORDER BY YEAR, YEAR_DEV;
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 연도별 윈도 MAX로 각 행에 최댓값을 붙이고 자기 크기를 뺀다. ID를 보존하면서 연도·편차 오름차순으로 정렬한다. | 연도별 집계 테이블 조인 |
| 비용 | N=입력 행 수, G=출력 그룹 수. 논리적으로 입력을 읽고 결과를 정렬한다. 실제 시간·공간은 인덱스, 조인 방식, 윈도 정렬과 실행 계획에 따라 달라진다. / N=input rows, G=output groups. Scanning and result ordering are required logically; physical cost depends on indexes, joins, window sorts and the query plan. | 대안도 같은 결과를 내지만 중간 집계·윈도·서브쿼리의 비용이 다르다. 성능 우열은 실행 계획으로 확인한다. / Equivalent results with different intermediate grouping, window or subquery costs; inspect the execution plan before comparing performance. |

## 검증

공식 예제 테이블을 로컬 SQLite에서 실행하고 두 쿼리의 결과를 비교했다. YEAR·MONTH·DATE_FORMAT 등은 호환 함수를 사용했다. 이는 MySQL 서버의 실행·성능 검증이나 새 사이트 제출을 뜻하지 않는다.

문제 폴더에서 `python test_query.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

For each colony, subtract its size from the maximum size in its differentiation year.

### Conditions and input/output

The input consists of the tables below; the output is a query result set. For each colony, subtract its size from the maximum size in its differentiation year.

This SQL task is defined by table schemas and query predicates rather than array-size limits.

- `ECOLI_DATA`: `ID`, `PARENT_ID`, `SIZE_OF_COLONY`, `DIFFERENTIATION_DATE`, `GENOTYPE`

### Approach

Attach the yearly maximum using a window MAX and subtract each row’s size. Preserve IDs and sort by year and deviation.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Apply row predicates, join or aggregate on the required keys, then produce the requested projection and ordering. Correctness depends on neither dropping nor duplicating qualifying rows.

N=입력 행 수, G=출력 그룹 수. 논리적으로 입력을 읽고 결과를 정렬한다. 실제 시간·공간은 인덱스, 조인 방식, 윈도 정렬과 실행 계획에 따라 달라진다. / N=input rows, G=output groups. Scanning and result ordering are required logically; physical cost depends on indexes, joins, window sorts and the query plan.

Boundary cases: Do not collapse colony rows with a standalone GROUP BY. The yearly maximum has deviation zero.

### Alternative: Join against a yearly aggregate table

It computes the same result using different intermediate states or evaluation steps. 대안도 같은 결과를 내지만 중간 집계·윈도·서브쿼리의 비용이 다르다. 성능 우열은 실행 계획으로 확인한다. / Equivalent results with different intermediate grouping, window or subquery costs; inspect the execution plan before comparing performance.

The main approach follows the steps described above. The alternative uses join against a yearly aggregate table; compare its intermediate state and cost with the main implementation before choosing it.

### Verification

Official example tables were checked locally with SQLite and the two query results were compared. Compatibility functions supplied YEAR, MONTH, DATE_FORMAT and similar MySQL functions. This does not constitute MySQL-server execution/performance testing or a new site submission.

Run `python test_query.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 연도별 대장균 크기의 편차 구하기](https://school.programmers.co.kr/learn/courses/30/lessons/299310) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
