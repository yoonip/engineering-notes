# 자동차 종류 별 특정 옵션이 포함된 자동차 수 구하기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/151137) · Level 2 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

통풍·열선·가죽 시트 옵션 중 하나라도 있는 자동차 수를 종류별로 센다.

## 조건과 입출력

입력은 아래 테이블이고 출력은 쿼리 결과 집합이다. 통풍·열선·가죽 시트 옵션 중 하나라도 있는 자동차 수를 종류별로 센다.

수치 배열 제한 대신 테이블 스키마와 조회 조건을 사용한다.

- `CAR_RENTAL_COMPANY_CAR`: `CAR_ID`, `CAR_TYPE`, `DAILY_FEE`, `OPTIONS`

## 풀이를 따라가기

옵션 문자열에 세 조건을 OR로 적용한다. 조건에 맞는 자동차를 종류별로 묶어 COUNT(*)를 구한다.

[기본 풀이 / Main](solution.sql) · [다른 풀이 / Alternative](alternative.sql) · [제출 원본 / Archived submission](submitted_original.sql)

```sql
-- 옵션 문자열에 세 조건을 OR로 적용한다. 조건에 맞는 자동차를 종류별로 묶어 COUNT(*)를 구한다.
SELECT CAR_TYPE, COUNT(*) AS CARS
FROM CAR_RENTAL_COMPANY_CAR
WHERE OPTIONS LIKE '%통풍시트%'
   OR OPTIONS LIKE '%열선시트%'
   OR OPTIONS LIKE '%가죽시트%'
GROUP BY CAR_TYPE
ORDER BY CAR_TYPE
```

## 왜 맞는가

세 옵션 중 하나라도 있으면 OR 조건을 만족한다. 한 자동차에 여러 옵션이 있어도 원본 행은 하나만 남으므로 COUNT(*)가 중복 없이 자동차를 센다.

N개 옵션 문자열에서 부분 문자열을 찾고 종류별 집계를 한다. 문자열 길이가 L이면 검색은 O(NL) 규모이며 G개 결과 비교 정렬은 O(G log G)이다.

주의할 점: 옵션이 둘 이상 맞아도 자동차는 한 번 센다. AND가 아니라 OR 조건이다.

## 다른 방법: 정규식 조건부 집계

```sql
SELECT CAR_TYPE,
       SUM(CASE WHEN OPTIONS REGEXP '통풍시트|열선시트|가죽시트' THEN 1 ELSE 0 END) AS CARS
FROM CAR_RENTAL_COMPANY_CAR
GROUP BY CAR_TYPE
HAVING CARS>0
ORDER BY CAR_TYPE;
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 옵션 문자열에 세 조건을 OR로 적용한다. 조건에 맞는 자동차를 종류별로 묶어 COUNT(*)를 구한다. | 정규식 조건부 집계 |
| 비용 | N개 옵션 문자열에서 부분 문자열을 찾고 종류별 집계를 한다. 문자열 길이가 L이면 검색은 O(NL) 규모이며 G개 결과 비교 정렬은 O(G log G)이다. | 정규식으로 옵션을 확인하며 종류별 조건부 합계를 구한다. 정규식이 LIKE 세 번보다 빠르다고 단정할 수 없다. |

## 검증

공식 예제 테이블을 로컬 SQLite에서 실행하고 두 쿼리의 결과를 비교했다. YEAR·MONTH·DATE_FORMAT 등은 호환 함수를 사용했다. 이는 MySQL 서버의 실행·성능 검증이나 새 사이트 제출을 뜻하지 않는다.

문제 폴더에서 `python test_query.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Count cars by type when at least one of the requested ventilation, heating or leather-seat options is present.

### Conditions and input/output

The input consists of the tables below; the output is a query result set. Count cars by type when at least one of the requested ventilation, heating or leather-seat options is present.

This SQL task is defined by table schemas and query predicates rather than array-size limits.

- `CAR_RENTAL_COMPANY_CAR`: `CAR_ID`, `CAR_TYPE`, `DAILY_FEE`, `OPTIONS`

### Approach

Combine the three option predicates with OR, then group qualifying cars by type and count rows.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

OR accepts a car with any of the three options. Matching several options still retains only one source row, so COUNT(*) does not double-count that car.

Search N option strings and aggregate car types. For string length L, containment checks have O(NL) scale; sorting G groups costs O(G log G) comparisons.

Boundary cases: Count a car once even when several options match. Combine conditions with OR, not AND.

### Alternative: Conditional aggregation with a regular-expression predicate

Use a regular expression and conditional sums; regex matching is not assumed faster than three LIKE checks.

### Verification

Official example tables were checked locally with SQLite and the two query results were compared. Compatibility functions supplied YEAR, MONTH, DATE_FORMAT and similar MySQL functions. This does not constitute MySQL-server execution/performance testing or a new site submission.

Run `python test_query.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 자동차 종류 별 특정 옵션이 포함된 자동차 수 구하기](https://school.programmers.co.kr/learn/courses/30/lessons/151137) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
