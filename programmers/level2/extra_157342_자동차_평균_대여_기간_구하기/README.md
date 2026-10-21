# 자동차 평균 대여 기간 구하기

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/157342) · Level 2 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

평균 대여 기간이 7일 이상인 자동차를 평균 기간·ID 내림차순으로 출력합니다.

## 조건과 입출력

입력은 아래 테이블이고 출력은 쿼리 결과 집합입니다. 평균 대여 기간이 7일 이상인 자동차를 평균 기간·ID 내림차순으로 출력합니다.

수치 배열 제한 대신 테이블 스키마와 조회 조건을 사용합니다.

- `CAR_RENTAL_COMPANY_RENTAL_HISTORY`: `HISTORY_ID`, `CAR_ID`, `START_DATE`, `END_DATE`

## 풀이를 따라가기

종료일−시작일에 1을 더해 양 끝 날짜를 포함합니다. 자동차별 평균을 구하고 반올림 전 평균으로 7일 조건을 검사합니다.

[기본 풀이 / Main](solution.sql) · [다른 풀이 / Alternative](alternative.sql) · [제출 원본 / Archived submission](submitted_original.sql)

```sql
-- 종료일−시작일에 1을 더해 양 끝 날짜를 포함한다. 자동차별 평균을 구하고 반올림 전 평균으로 7일 조건을 검사한다.
SELECT CAR_ID, ROUND(AVG(DATEDIFF(END_DATE, START_DATE) + 1), 1) AS AVERAGE_DURATION
FROM CAR_RENTAL_COMPANY_RENTAL_HISTORY
GROUP BY CAR_ID
HAVING AVG(DATEDIFF(END_DATE, START_DATE) + 1) >= 7
ORDER BY AVERAGE_DURATION DESC, CAR_ID DESC
```

## 정답이 되는 이유

DATEDIFF에 1을 더해야 대여 시작일과 종료일을 모두 셉니다. HAVING은 반올림 전 평균으로 7일을 검사하므로 6.96일 같은 값이 잘못 포함되지 않습니다.

N개 대여 이력을 자동차별로 집계하고 R개 통과 차량을 정렬합니다. 결과 비교 정렬은 O(R log R)이며 집계 방식은 실행계획에 따릅니다.

주의할 점: 하루 대여도 1일입니다. 반올림해서 7.0이 된 6.96일을 조건에 통과시키면 안 됩니다.

## 다른 방법: 기간 합계와 횟수로 평균 계산

```sql
WITH totals AS (
    SELECT CAR_ID,SUM(DATEDIFF(END_DATE,START_DATE)+1) AS DAYS,COUNT(*) AS N
    FROM CAR_RENTAL_COMPANY_RENTAL_HISTORY GROUP BY CAR_ID
)
SELECT CAR_ID,ROUND(1.0*DAYS/N,1) AS AVERAGE_DURATION
FROM totals WHERE DAYS>=7*N
ORDER BY AVERAGE_DURATION DESC,CAR_ID DESC;
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 종료일−시작일에 1을 더해 양 끝 날짜를 포함합니다. 자동차별 평균을 구하고 반올림 전 평균으로 7일 조건을 검사합니다. | 기간 합계와 횟수로 평균 계산 |
| 비용 | N개 대여 이력을 자동차별로 집계하고 R개 통과 차량을 정렬합니다. 결과 비교 정렬은 O(R log R)이며 집계 방식은 실행계획에 따릅니다. | 자동차별 총 대여 일수와 횟수를 구해 평균을 계산합니다. 두 방법 모두 대여 이력별 기간을 집계합니다. |

## 검증

공식 예제 테이블을 로컬 SQLite에서 실행하고 두 쿼리의 결과를 비교했습니다. YEAR·MONTH·DATE_FORMAT 등은 호환 함수를 사용했습니다. 이는 MySQL 서버의 실행·성능 검증이나 새 사이트 제출을 뜻하지 않습니다.

문제 폴더에서 `python test_query.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Return cars with an average rental duration of at least seven days, ordered by average duration and ID descending.

### Conditions and input/output

The input consists of the tables below; the output is a query result set. Return cars with an average rental duration of at least seven days, ordered by average duration and ID descending.

This SQL task is defined by table schemas and query predicates rather than array-size limits.

- `CAR_RENTAL_COMPANY_RENTAL_HISTORY`: `HISTORY_ID`, `CAR_ID`, `START_DATE`, `END_DATE`

### Approach

Add one to end-date minus start-date to include both endpoints. Group by car and test the unrounded average against seven days.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Adding one to DATEDIFF includes both rental endpoints. HAVING checks the unrounded average, preventing a value such as 6.96 days from qualifying after display rounding.

Aggregate N rentals by car and sort R qualifying cars in O(R log R) comparisons; aggregation strategy depends on the execution plan.

Boundary cases: A same-day rental lasts one day. An average of 6.96 must not qualify merely because it rounds to 7.0.

### Alternative: Compute the mean from total duration and rental count

Compute total days and rental counts per car. Both approaches aggregate rental durations.

### Verification

Official example tables were checked locally with SQLite and the two query results were compared. Compatibility functions supplied YEAR, MONTH, DATE_FORMAT and similar MySQL functions. This does not constitute MySQL-server execution/performance testing or a new site submission.

Run `python test_query.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 자동차 평균 대여 기간 구하기](https://school.programmers.co.kr/learn/courses/30/lessons/157342) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
