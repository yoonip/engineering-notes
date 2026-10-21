# 월별 잡은 물고기 수 구하기

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/293260) · Level 2 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

포획 기록이 있는 월별로 물고기 수를 셉니다.

## 조건과 입출력

입력은 아래 테이블이고 출력은 쿼리 결과 집합입니다. 포획 기록이 있는 월별로 물고기 수를 셉니다.

수치 배열 제한 대신 테이블 스키마와 조회 조건을 사용합니다.

- `FISH_INFO`: `ID`, `FISH_TYPE`, `LENGTH`, `TIME`

## 풀이를 따라가기

날짜에서 MONTH를 추출하고 같은 월끼리 묶습니다. 월은 숫자로 출력하고 오름차순 정렬합니다.

[기본 풀이 / Main](solution.sql) · [다른 풀이 / Alternative](alternative.sql) · [제출 원본 / Archived submission](submitted_original.sql)

```sql
-- 날짜에서 MONTH를 추출하고 같은 월끼리 묶는다. 월은 숫자로 출력하고 오름차순 정렬한다.
SELECT COUNT(*) AS FISH_COUNT, MONTH(TIME) AS MONTH
FROM FISH_INFO
GROUP BY MONTH(TIME)
ORDER BY MONTH
```

## 정답이 되는 이유

MONTH로 같은 월 번호를 그룹 키로 만들고 COUNT(*)로 모든 포획 행을 셉니다. 문제는 연도별이 아닌 월별 집계이므로 연도를 추가 키로 두지 않습니다.

N개 날짜를 읽고 최대 12개 월 그룹을 집계합니다. 순차 집계가 가능하면 O(N) 규모이며 월 결과의 정렬 크기는 12 이하로 고정됩니다.

주의할 점: 연도가 다른 같은 월도 함께 셉니다. 포획이 없는 월은 출력하지 않습니다.

## 다른 방법: 윈도 COUNT와 DISTINCT

```sql
SELECT DISTINCT COUNT(*) OVER (PARTITION BY MONTH(TIME)) AS FISH_COUNT,
                MONTH(TIME) AS MONTH
FROM FISH_INFO ORDER BY MONTH;
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 날짜에서 MONTH를 추출하고 같은 월끼리 묶습니다. 월은 숫자로 출력하고 오름차순 정렬합니다. | 윈도 COUNT와 DISTINCT |
| 비용 | N개 날짜를 읽고 최대 12개 월 그룹을 집계합니다. 순차 집계가 가능하면 O(N) 규모이며 월 결과의 정렬 크기는 12 이하로 고정됩니다. | 각 포획 행에 월별 횟수를 붙인 뒤 DISTINCT를 적용합니다. 월 그룹은 같지만 중간 행 수는 줄지 않습니다. |

## 검증

공식 예제 테이블을 로컬 SQLite에서 실행하고 두 쿼리의 결과를 비교했습니다. YEAR·MONTH·DATE_FORMAT 등은 호환 함수를 사용했습니다. 이는 MySQL 서버의 실행·성능 검증이나 새 사이트 제출을 뜻하지 않습니다.

문제 폴더에서 `python test_query.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Count catches for each month represented in the data.

### Conditions and input/output

The input consists of the tables below; the output is a query result set. Count catches for each month represented in the data.

This SQL task is defined by table schemas and query predicates rather than array-size limits.

- `FISH_INFO`: `ID`, `FISH_TYPE`, `LENGTH`, `TIME`

### Approach

Extract MONTH and group identical months. Output numeric months in ascending order.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

MONTH supplies the month-number grouping key and COUNT(*) counts catch rows. The task groups by month rather than by year-month, so no year key is added.

Read N dates and aggregate at most 12 month groups. A sequential aggregation has O(N) scale, with a final sort bounded by 12 results.

Boundary cases: Combine the same month across years. Omit months without catches.

### Alternative: Window COUNT followed by DISTINCT

Attach monthly counts to every catch, then apply DISTINCT. The intermediate row count remains the number of catches.

### Verification

Official example tables were checked locally with SQLite and the two query results were compared. Compatibility functions supplied YEAR, MONTH, DATE_FORMAT and similar MySQL functions. This does not constitute MySQL-server execution/performance testing or a new site submission.

Run `python test_query.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 월별 잡은 물고기 수 구하기](https://school.programmers.co.kr/learn/courses/30/lessons/293260) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
