# 조건에 맞는 사원 정보 조회하기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/284527) · Level 2 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

2022년 평가 점수 합계가 가장 높은 사원 정보를 찾는다.

## 조건과 입출력

입력은 아래 테이블이고 출력은 쿼리 결과 집합이다. 2022년 평가 점수 합계가 가장 높은 사원 정보를 찾는다.

수치 배열 제한 대신 테이블 스키마와 조회 조건을 사용한다.

- `HR_DEPARTMENT`: `DEPT_ID`, `DEPT_NAME_KR`, `DEPT_NAME_EN`, `LOCATION`
- `HR_EMPLOYEES`: `EMP_NO`, `EMP_NAME`, `DEPT_ID`, `POSITION`, `EMAIL`, `COMP_TEL`, `HIRE_DATE`, `SAL`
- `HR_GRADE`: `EMP_NO`, `YEAR`, `HALF_YEAR`, `SCORE`

## 풀이를 따라가기

사원별 상·하반기 점수를 합산한다. 합계 내림차순 DENSE_RANK가 1인 행에 사원 정보를 붙인다.

[기본 풀이 / Main](solution.sql) · [다른 풀이 / Alternative](alternative.sql) · [제출 원본 / Archived submission](submitted_original.sql)

```sql
-- 사원별 상·하반기 점수를 합산한다. 합계 내림차순 DENSE_RANK가 1인 행에 사원 정보를 붙인다.
SELECT g.SCORE, e.EMP_NO, e.EMP_NAME, e.POSITION, e.EMAIL
FROM (
    SELECT EMP_NO, SUM(SCORE) AS SCORE,
           DENSE_RANK() OVER (ORDER BY SUM(SCORE) DESC) AS SCORE_RANK
    FROM HR_GRADE
    WHERE YEAR = 2022
    GROUP BY EMP_NO
) AS g
JOIN HR_EMPLOYEES AS e ON e.EMP_NO = g.EMP_NO
WHERE g.SCORE_RANK = 1
ORDER BY e.EMP_NO
```

## 왜 맞는가

행 조건을 먼저 적용하고, 필요한 키로 연결·집계한 뒤 요구한 열과 정렬을 만든다. 이 순서를 바꾸어 행을 누락하거나 중복하지 않는 것이 핵심이다.

N=입력 행 수, G=출력 그룹 수. 논리적으로 입력을 읽고 결과를 정렬한다. 실제 시간·공간은 인덱스, 조인 방식, 윈도 정렬과 실행 계획에 따라 달라진다. / N=input rows, G=output groups. Scanning and result ordering are required logically; physical cost depends on indexes, joins, window sorts and the query plan.

주의할 점: 공동 최고점이 있다면 함께 보존한다. 집계 전에 연도를 필터해야 다른 연도 점수가 섞이지 않는다.

공식 예제의 사원 원본 키는 `2020002`인데 결과 표에는 `202002`로 적혀 있다. 이 기록에서는 원본 테이블의 키를 유지한다.

## 다른 방법: 합계 CTE와 MAX 서브쿼리

기본 풀이와 같은 결과를 구하되 중간 상태와 계산 방식이 다르다.

```sql
WITH totals AS (
    SELECT EMP_NO,SUM(SCORE) AS SCORE FROM HR_GRADE
    WHERE YEAR=2022 GROUP BY EMP_NO
)
SELECT t.SCORE,e.EMP_NO,e.EMP_NAME,e.POSITION,e.EMAIL
FROM totals t JOIN HR_EMPLOYEES e ON e.EMP_NO=t.EMP_NO
WHERE t.SCORE=(SELECT MAX(SCORE) FROM totals)
ORDER BY e.EMP_NO;
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 사원별 상·하반기 점수를 합산한다. 합계 내림차순 DENSE_RANK가 1인 행에 사원 정보를 붙인다. | 합계 CTE와 MAX 서브쿼리 |
| 비용 | N=입력 행 수, G=출력 그룹 수. 논리적으로 입력을 읽고 결과를 정렬한다. 실제 시간·공간은 인덱스, 조인 방식, 윈도 정렬과 실행 계획에 따라 달라진다. / N=input rows, G=output groups. Scanning and result ordering are required logically; physical cost depends on indexes, joins, window sorts and the query plan. | 대안도 같은 결과를 내지만 중간 집계·윈도·서브쿼리의 비용이 다르다. 성능 우열은 실행 계획으로 확인한다. / Equivalent results with different intermediate grouping, window or subquery costs; inspect the execution plan before comparing performance. |

## 검증

공식 예제 테이블을 로컬 SQLite에서 실행하고 두 쿼리의 결과를 비교했다. YEAR·MONTH·DATE_FORMAT 등은 호환 함수를 사용했다. 이는 MySQL 서버의 실행·성능 검증이나 새 사이트 제출을 뜻하지 않는다.

문제 폴더에서 `python test_query.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Find employee details for the highest total evaluation score in 2022.

### Conditions and input/output

The input consists of the tables below; the output is a query result set. Find employee details for the highest total evaluation score in 2022.

This SQL task is defined by table schemas and query predicates rather than array-size limits.

- `HR_DEPARTMENT`: `DEPT_ID`, `DEPT_NAME_KR`, `DEPT_NAME_EN`, `LOCATION`
- `HR_EMPLOYEES`: `EMP_NO`, `EMP_NAME`, `DEPT_ID`, `POSITION`, `EMAIL`, `COMP_TEL`, `HIRE_DATE`, `SAL`
- `HR_GRADE`: `EMP_NO`, `YEAR`, `HALF_YEAR`, `SCORE`

### Approach

Sum evaluation scores per employee. Select DENSE_RANK 1 by descending total and join employee details.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Apply row predicates, join or aggregate on the required keys, then produce the requested projection and ordering. Correctness depends on neither dropping nor duplicating qualifying rows.

N=입력 행 수, G=출력 그룹 수. 논리적으로 입력을 읽고 결과를 정렬한다. 실제 시간·공간은 인덱스, 조인 방식, 윈도 정렬과 실행 계획에 따라 달라진다. / N=input rows, G=output groups. Scanning and result ordering are required logically; physical cost depends on indexes, joins, window sorts and the query plan.

Boundary cases: Preserve tied maxima. Filter the year before aggregation to avoid mixing years.

The official example input uses employee key `2020002`, while its result table prints `202002`. These queries preserve the key in the input table.

### Alternative: Grouped totals CTE with a MAX subquery

It computes the same result using different intermediate states or evaluation steps. 대안도 같은 결과를 내지만 중간 집계·윈도·서브쿼리의 비용이 다르다. 성능 우열은 실행 계획으로 확인한다. / Equivalent results with different intermediate grouping, window or subquery costs; inspect the execution plan before comparing performance.

The main approach follows the steps described above. The alternative uses grouped totals cte with a max subquery; compare its intermediate state and cost with the main implementation before choosing it.

### Verification

Official example tables were checked locally with SQLite and the two query results were compared. Compatibility functions supplied YEAR, MONTH, DATE_FORMAT and similar MySQL functions. This does not constitute MySQL-server execution/performance testing or a new site submission.

Run `python test_query.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 조건에 맞는 사원 정보 조회하기](https://school.programmers.co.kr/learn/courses/30/lessons/284527) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
