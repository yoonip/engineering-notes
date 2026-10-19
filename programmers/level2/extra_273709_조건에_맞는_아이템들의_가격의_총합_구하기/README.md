# 조건에 맞는 아이템들의 가격의 총합 구하기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/273709) · Level 2 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

희귀도가 LEGEND인 아이템의 가격 합계를 구합니다.

## 조건과 입출력

입력은 아래 테이블이고 출력은 쿼리 결과 집합입니다. 희귀도가 LEGEND인 아이템의 가격 합계를 구합니다.

수치 배열 제한 대신 테이블 스키마와 조회 조건을 사용합니다.

- `ITEM_INFO`: `ITEM_ID`, `ITEM_NAME`, `RARITY`, `PRICE`

## 풀이를 따라가기

LEGEND 행만 필터하고 SUM으로 가격을 더합니다. 그룹 구분이 없으므로 전체 합계 한 행을 출력합니다.

[기본 풀이 / Main](solution.sql) · [다른 풀이 / Alternative](alternative.sql) · [제출 원본 / Archived submission](submitted_original.sql)

```sql
-- LEGEND 행만 필터하고 SUM으로 가격을 더한다. 그룹 구분이 없으므로 전체 합계 한 행을 출력한다.
SELECT SUM(PRICE) AS TOTAL_PRICE
FROM ITEM_INFO
WHERE RARITY = 'LEGEND'
```

## 정답이 되는 이유

WHERE가 LEGEND 행만 남기므로 SUM에는 그 가격들만 들어갑니다. 조건부 SUM도 다른 행을 NULL로 만들어 같은 합을 구하며, 해당 값이 없으면 두 쿼리 모두 NULL을 반환합니다.

N개 아이템을 순차 검사하면 시간 O(N), 누적 합계 상태는 O(1)입니다. 결과는 한 행이며 정렬은 없습니다. 희귀도 인덱스가 있으면 접근 계획이 달라질 수 있습니다.

주의할 점: 개수나 평균이 아니라 가격 합계입니다. 대상 행이 없으면 SQL SUM의 결과는 NULL입니다.

공식 스키마 표의 RARITY 자료형 표기와 달리 예제·조회 조건은 `COMMON`, `RARE`, `LEGEND` 문자열을 사용합니다. 쿼리에서도 이 문자열 값으로 비교합니다.

## 다른 방법: 조건부 SUM

```sql
SELECT SUM(CASE WHEN RARITY='LEGEND' THEN PRICE END) AS TOTAL_PRICE
FROM ITEM_INFO;
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | LEGEND 행만 필터하고 SUM으로 가격을 더합니다. 그룹 구분이 없으므로 전체 합계 한 행을 출력합니다. | 조건부 SUM |
| 비용 | N개 아이템을 순차 검사하면 시간 O(N), 누적 합계 상태는 O(1)입니다. 결과는 한 행이며 정렬은 없습니다. 희귀도 인덱스가 있으면 접근 계획이 달라질 수 있습니다. | N개 행에서 CASE를 평가하며 하나의 합계를 누적합니다. 정렬·윈도 함수 없이 O(N) 순차 집계가 가능합니다. |

## 검증

공식 예제 테이블을 로컬 SQLite에서 실행하고 두 쿼리의 결과를 비교했습니다. YEAR·MONTH·DATE_FORMAT 등은 호환 함수를 사용했습니다. 이는 MySQL 서버의 실행·성능 검증이나 새 사이트 제출을 뜻하지 않습니다.

문제 폴더에서 `python test_query.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Sum prices of items whose rarity is LEGEND.

### Conditions and input/output

The input consists of the tables below; the output is a query result set. Sum prices of items whose rarity is LEGEND.

This SQL task is defined by table schemas and query predicates rather than array-size limits.

- `ITEM_INFO`: `ITEM_ID`, `ITEM_NAME`, `RARITY`, `PRICE`

### Approach

Filter LEGEND rows and sum their prices. With no grouping key, return one aggregate row.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

WHERE restricts SUM to LEGEND prices. Conditional SUM turns other rows into NULL and yields the same aggregate; both return NULL when there are no contributing values.

A sequential scan takes O(N) time and O(1) aggregate state. The result is one row with no sorting. A rarity index can change the access plan.

Boundary cases: Return a price sum, not a count or mean. SQL SUM returns NULL when no rows qualify.

Although the official schema’s RARITY type label is inconsistent, its examples and predicates use string values `COMMON`, `RARE` and `LEGEND`. The queries compare those string values.

### Alternative: Conditional SUM

Evaluate CASE for N rows and accumulate one sum. A sequential O(N) aggregation needs no sorting or window function.

### Verification

Official example tables were checked locally with SQLite and the two query results were compared. Compatibility functions supplied YEAR, MONTH, DATE_FORMAT and similar MySQL functions. This does not constitute MySQL-server execution/performance testing or a new site submission.

Run `python test_query.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 조건에 맞는 아이템들의 가격의 총합 구하기](https://school.programmers.co.kr/learn/courses/30/lessons/273709) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
