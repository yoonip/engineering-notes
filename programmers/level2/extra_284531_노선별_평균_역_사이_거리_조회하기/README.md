# 노선별 평균 역 사이 거리 조회하기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/284531) · Level 2 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

노선별 역 사이 거리 합과 평균을 지정 자릿수로 반올림해 km 단위를 붙입니다.

## 조건과 입출력

입력은 아래 테이블이고 출력은 쿼리 결과 집합입니다. 노선별 역 사이 거리 합과 평균을 지정 자릿수로 반올림해 km 단위를 붙입니다.

수치 배열 제한 대신 테이블 스키마와 조회 조건을 사용합니다.

- `SUBWAY_DISTANCE`: `LINE`, `NO`, `ROUTE`, `STATION_NAME`, `D_BETWEEN_DIST`, `D_CUMULATIVE`

## 풀이를 따라가기

노선별 SUM·AVG를 구합니다. 출력 직전에 반올림과 단위 문자열 처리를 하고 정렬에는 숫자 SUM을 씁니다.

[기본 풀이 / Main](solution.sql) · [다른 풀이 / Alternative](alternative.sql) · [제출 원본 / Archived submission](submitted_original.sql)

```sql
-- 노선별 SUM·AVG를 구한다. 출력 직전에 반올림과 단위 문자열 처리를 하고 정렬에는 숫자 SUM을 쓴다.
SELECT ROUTE,
       CONCAT(ROUND(SUM(D_BETWEEN_DIST), 1), 'km') AS TOTAL_DISTANCE,
       CONCAT(ROUND(AVG(D_BETWEEN_DIST), 2), 'km') AS AVERAGE_DISTANCE
FROM SUBWAY_DISTANCE
GROUP BY ROUTE
ORDER BY SUM(D_BETWEEN_DIST) DESC
```

## 정답이 되는 이유

같은 노선의 구간 거리로 SUM과 AVG를 구합니다. km 문자열은 출력할 때만 붙이고 정렬에는 숫자 합계를 사용하므로 문자열 사전순 정렬을 피합니다.

N개 구간을 G개 노선으로 집계하고 G개 합계를 정렬합니다. 결과 비교 정렬은 O(G log G); 윈도 대안은 노선별 중복 제거도 필요합니다.

주의할 점: 누계 거리 열을 다시 합산하지 않습니다. km가 붙은 문자열을 정렬하면 숫자순이 아닙니다.

## 다른 방법: 윈도 집계 후 중복 노선 제거

```sql
WITH x AS (
    SELECT ROUTE, SUM(D_BETWEEN_DIST) OVER (PARTITION BY ROUTE) AS TOTAL,
           AVG(D_BETWEEN_DIST) OVER (PARTITION BY ROUTE) AS MEAN
    FROM SUBWAY_DISTANCE
)
SELECT ROUTE, CONCAT(ROUND(TOTAL,1),'km') AS TOTAL_DISTANCE,
       CONCAT(ROUND(MEAN,2),'km') AS AVERAGE_DISTANCE
FROM (SELECT DISTINCT ROUTE,TOTAL,MEAN FROM x) AS unique_routes
ORDER BY TOTAL DESC;
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 노선별 SUM·AVG를 구합니다. 출력 직전에 반올림과 단위 문자열 처리를 하고 정렬에는 숫자 SUM을 씁니다. | 윈도 집계 후 중복 노선 제거 |
| 비용 | N개 구간을 G개 노선으로 집계하고 G개 합계를 정렬합니다. 결과 비교 정렬은 O(G log G); 윈도 대안은 노선별 중복 제거도 필요합니다. | 각 구간에 노선 합계와 평균을 붙인 뒤 DISTINCT로 노선을 줄입니다. |

## 검증

공식 예제 테이블을 로컬 SQLite에서 실행하고 두 쿼리의 결과를 비교했습니다. YEAR·MONTH·DATE_FORMAT 등은 호환 함수를 사용했습니다. 이는 MySQL 서버의 실행·성능 검증이나 새 사이트 제출을 뜻하지 않습니다.

문제 폴더에서 `python test_query.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Sum and average interstation distances by route, round as requested and append km.

### Conditions and input/output

The input consists of the tables below; the output is a query result set. Sum and average interstation distances by route, round as requested and append km.

This SQL task is defined by table schemas and query predicates rather than array-size limits.

- `SUBWAY_DISTANCE`: `LINE`, `NO`, `ROUTE`, `STATION_NAME`, `D_BETWEEN_DIST`, `D_CUMULATIVE`

### Approach

Compute SUM and AVG by route. Round and format only the output, while sorting by numeric SUM.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

SUM and AVG operate on segment distances within each route. Add km only for display and order by numeric totals, avoiding lexicographic string order.

Aggregate N segments into G routes and sort their totals in O(G log G) comparisons. The window alternative also deduplicates route results.

Boundary cases: Do not sum a cumulative-distance column. Sorting formatted km strings is not numeric sorting.

### Alternative: Window aggregation followed by route deduplication

Attach route totals and means to segments, then deduplicate route rows.

### Verification

Official example tables were checked locally with SQLite and the two query results were compared. Compatibility functions supplied YEAR, MONTH, DATE_FORMAT and similar MySQL functions. This does not constitute MySQL-server execution/performance testing or a new site submission.

Run `python test_query.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 노선별 평균 역 사이 거리 조회하기](https://school.programmers.co.kr/learn/courses/30/lessons/284531) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
