# 재구매가 일어난 상품과 회원 리스트 구하기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/131536) · Level 2 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

같은 회원이 같은 상품을 두 번 이상 구매한 회원·상품 쌍을 찾습니다.

## 조건과 입출력

입력은 아래 테이블이고 출력은 쿼리 결과 집합입니다. 같은 회원이 같은 상품을 두 번 이상 구매한 회원·상품 쌍을 찾습니다.

수치 배열 제한 대신 테이블 스키마와 조회 조건을 사용합니다.

- `ONLINE_SALE`: `ONLINE_SALE_ID`, `USER_ID`, `PRODUCT_ID`, `SALES_AMOUNT`, `SALES_DATE`

## 풀이를 따라가기

USER_ID와 PRODUCT_ID를 함께 GROUP BY합니다. COUNT(*)가 2 이상인 그룹만 HAVING으로 남깁니다.

[기본 풀이 / Main](solution.sql) · [다른 풀이 / Alternative](alternative.sql) · [제출 원본 / Archived submission](submitted_original.sql)

```sql
-- USER_ID와 PRODUCT_ID를 함께 GROUP BY한다. COUNT(*)가 2 이상인 그룹만 HAVING으로 남긴다.
SELECT USER_ID, PRODUCT_ID
FROM ONLINE_SALE
GROUP BY USER_ID, PRODUCT_ID
HAVING COUNT(*) >= 2
ORDER BY USER_ID, PRODUCT_ID DESC
```

## 정답이 되는 이유

회원과 상품을 함께 묶어야 같은 회원이 같은 상품을 산 횟수가 됩니다. HAVING의 2회 이상 조건이 재구매인 쌍만 남깁니다.

N개 판매를 회원·상품 쌍으로 집계한 뒤 R개 해당 쌍을 정렬합니다. 결과 비교 정렬은 O(R log R); 윈도 대안은 행별 횟수 계산과 DISTINCT도 수행합니다.

주의할 점: 회원 또는 상품 하나만으로 묶으면 다른 구매가 섞입니다. 결과는 회원 오름차순·상품 내림차순입니다.

## 다른 방법: 회원·상품별 윈도 COUNT

```sql
WITH counted AS (
    SELECT USER_ID,PRODUCT_ID,COUNT(*) OVER (PARTITION BY USER_ID,PRODUCT_ID) AS N
    FROM ONLINE_SALE
)
SELECT DISTINCT USER_ID,PRODUCT_ID FROM counted
WHERE N>=2 ORDER BY USER_ID,PRODUCT_ID DESC;
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | USER_ID와 PRODUCT_ID를 함께 GROUP BY합니다. COUNT(*)가 2 이상인 그룹만 HAVING으로 남깁니다. | 회원·상품별 윈도 COUNT |
| 비용 | N개 판매를 회원·상품 쌍으로 집계한 뒤 R개 해당 쌍을 정렬합니다. 결과 비교 정렬은 O(R log R); 윈도 대안은 행별 횟수 계산과 DISTINCT도 수행합니다. | 각 판매 행에 쌍별 구매 횟수를 붙이고 DISTINCT로 회원·상품 쌍을 한 번만 출력합니다. |

## 검증

공식 예제 테이블을 로컬 SQLite에서 실행하고 두 쿼리의 결과를 비교했습니다. YEAR·MONTH·DATE_FORMAT 등은 호환 함수를 사용했습니다. 이는 MySQL 서버의 실행·성능 검증이나 새 사이트 제출을 뜻하지 않습니다.

문제 폴더에서 `python test_query.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Find user-product pairs with at least two purchases.

### Conditions and input/output

The input consists of the tables below; the output is a query result set. Find user-product pairs with at least two purchases.

This SQL task is defined by table schemas and query predicates rather than array-size limits.

- `ONLINE_SALE`: `ONLINE_SALE_ID`, `USER_ID`, `PRODUCT_ID`, `SALES_AMOUNT`, `SALES_DATE`

### Approach

Group jointly by USER_ID and PRODUCT_ID, keeping groups whose COUNT(*) is at least two.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Grouping by both member and product counts repeated purchases of that exact pair. HAVING retains only pairs with at least two purchases.

Aggregate N sales by member-product pair and sort R qualifying pairs in O(R log R) comparisons. The window version also deduplicates per-row counts.

Boundary cases: Grouping on only one key mixes unrelated purchases. Sort users ascending and products descending.

### Alternative: Window COUNT per user-product pair

Annotate each sale with its pair count, then deduplicate member-product pairs.

### Verification

Official example tables were checked locally with SQLite and the two query results were compared. Compatibility functions supplied YEAR, MONTH, DATE_FORMAT and similar MySQL functions. This does not constitute MySQL-server execution/performance testing or a new site submission.

Run `python test_query.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 재구매가 일어난 상품과 회원 리스트 구하기](https://school.programmers.co.kr/learn/courses/30/lessons/131536) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
