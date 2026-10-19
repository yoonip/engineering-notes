# 분기별 분화된 대장균의 개체 수 구하기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/299308) · Level 2 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

분화한 달을 분기로 묶어 개체 수를 셉니다.

## 조건과 입출력

입력은 아래 테이블이고 출력은 쿼리 결과 집합입니다. 분화한 달을 분기로 묶어 개체 수를 셉니다.

수치 배열 제한 대신 테이블 스키마와 조회 조건을 사용합니다.

- `ECOLI_DATA`: `ID`, `PARENT_ID`, `SIZE_OF_COLONY`, `DIFFERENTIATION_DATE`, `GENOTYPE`

## 풀이를 따라가기

QUARTER로 1~4분기를 구해 GROUP BY한 뒤 Q를 붙입니다. 집계 결과를 분기순으로 출력합니다.

[기본 풀이 / Main](solution.sql) · [다른 풀이 / Alternative](alternative.sql) · [제출 원본 / Archived submission](submitted_original.sql)

```sql
-- QUARTER로 1~4분기를 구해 GROUP BY한 뒤 Q를 붙인다. 집계 결과를 분기순으로 출력한다.
SELECT CONCAT(QUARTER(DIFFERENTIATION_DATE), 'Q') AS QUARTER, COUNT(*) AS ECOLI_COUNT
FROM ECOLI_DATA
GROUP BY QUARTER(DIFFERENTIATION_DATE)
ORDER BY QUARTER
```

## 정답이 되는 이유

QUARTER는 각 날짜를 정확히 1~4분기 중 하나에 배정합니다. 같은 분기를 세고 Q를 붙이며, 1Q~4Q의 문자열 순서는 분기 숫자순과 같습니다.

N개 날짜를 읽고 최대 4개 그룹을 집계합니다. 순차 집계가 가능하면 O(N) 규모이며 결과 정렬 크기는 4 이하로 고정됩니다.

주의할 점: 연도가 아니라 분기만 묶습니다. 실제 행이 없는 그룹을 임의로 추가하지 않습니다.

## 다른 방법: CASE로 분기를 계산한 뒤 집계

```sql
WITH categorized AS (
    SELECT CASE
        WHEN MONTH(DIFFERENTIATION_DATE)<=3 THEN 1
        WHEN MONTH(DIFFERENTIATION_DATE)<=6 THEN 2
        WHEN MONTH(DIFFERENTIATION_DATE)<=9 THEN 3
        ELSE 4 END AS Q
    FROM ECOLI_DATA
)
SELECT CONCAT(Q,'Q') AS QUARTER, COUNT(*) AS ECOLI_COUNT
FROM categorized GROUP BY Q ORDER BY Q;
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | QUARTER로 1~4분기를 구해 GROUP BY한 뒤 Q를 붙입니다. 집계 결과를 분기순으로 출력합니다. | CASE로 분기를 계산한 뒤 집계 |
| 비용 | N개 날짜를 읽고 최대 4개 그룹을 집계합니다. 순차 집계가 가능하면 O(N) 규모이며 결과 정렬 크기는 4 이하로 고정됩니다. | MONTH의 범위를 CASE로 나눠 분기 번호를 만든 뒤 집계합니다. QUARTER를 이용한 집계와 같은 네 그룹을 만듭니다. |

## 검증

공식 예제 테이블을 로컬 SQLite에서 실행하고 두 쿼리의 결과를 비교했습니다. YEAR·MONTH·DATE_FORMAT 등은 호환 함수를 사용했습니다. 이는 MySQL 서버의 실행·성능 검증이나 새 사이트 제출을 뜻하지 않습니다.

문제 폴더에서 `python test_query.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Group differentiation months into quarters and count colonies.

### Conditions and input/output

The input consists of the tables below; the output is a query result set. Group differentiation months into quarters and count colonies.

This SQL task is defined by table schemas and query predicates rather than array-size limits.

- `ECOLI_DATA`: `ID`, `PARENT_ID`, `SIZE_OF_COLONY`, `DIFFERENTIATION_DATE`, `GENOTYPE`

### Approach

Extract QUARTER, group quarters 1 through 4, append Q, and order the grouped result.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

QUARTER assigns every date to one of four quarters. Count equal quarters and append Q; ordering 1Q through 4Q matches numeric quarter order.

Read N dates and aggregate at most four groups. Sequential aggregation has O(N) scale, with sorting bounded by four quarter results.

Boundary cases: Group by quarter rather than year. Do not invent groups absent from the input.

### Alternative: Compute quarter with CASE before grouping

Map month ranges with CASE and aggregate the same four quarter groups as QUARTER.

### Verification

Official example tables were checked locally with SQLite and the two query results were compared. Compatibility functions supplied YEAR, MONTH, DATE_FORMAT and similar MySQL functions. This does not constitute MySQL-server execution/performance testing or a new site submission.

Run `python test_query.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 분기별 분화된 대장균의 개체 수 구하기](https://school.programmers.co.kr/learn/courses/30/lessons/299308) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
