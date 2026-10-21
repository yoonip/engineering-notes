# 가격이 제일 비싼 식품의 정보 출력하기

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/131115) · Level 2 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

가장 비싼 식품의 전체 정보를 조회합니다.

## 조건과 입출력

입력은 아래 테이블이고 출력은 쿼리 결과 집합입니다. 가장 비싼 식품의 전체 정보를 조회합니다.

수치 배열 제한 대신 테이블 스키마와 조회 조건을 사용합니다.

- `FOOD_PRODUCT`: `PRODUCT_ID`, `PRODUCT_NAME`, `PRODUCT_CD`, `CATEGORY`, `PRICE`

## 풀이를 따라가기

하위 쿼리 MAX(PRICE)로 최고 가격을 구합니다. 그 값과 같은 가격을 가진 원본 행을 선택합니다.

[기본 풀이 / Main](solution.sql) · [다른 풀이 / Alternative](alternative.sql) · [제출 원본 / Archived submission](submitted_original.sql)

```sql
-- 하위 쿼리 MAX(PRICE)로 최고 가격을 구한다. 그 값과 같은 가격을 가진 원본 행을 선택한다.
SELECT PRODUCT_ID, PRODUCT_NAME, PRODUCT_CD, CATEGORY, PRICE
FROM FOOD_PRODUCT
WHERE PRICE = (SELECT MAX(PRICE) FROM FOOD_PRODUCT)
```

## 정답이 되는 이유

MAX가 전체 최고 가격을 한 값으로 구하고, 바깥 WHERE가 그 값과 같은 행을 모두 남깁니다. 최고가가 같은 상품이 있어도 빠뜨리지 않습니다.

순차 스캔으로 최대값과 일치 행을 찾으면 O(N)입니다. 대안의 순위 계산은 가격 정렬이 필요할 수 있습니다.

주의할 점: 최댓값만 출력하는 것이 아니라 해당 상품 정보가 필요합니다. 일반적으로 동점 행을 함께 보존합니다.

## 다른 방법: DENSE_RANK로 최고 가격 선택

```sql
WITH ranked AS (
    SELECT PRODUCT_ID,PRODUCT_NAME,PRODUCT_CD,CATEGORY,PRICE,
           DENSE_RANK() OVER (ORDER BY PRICE DESC) AS R
    FROM FOOD_PRODUCT
)
SELECT PRODUCT_ID,PRODUCT_NAME,PRODUCT_CD,CATEGORY,PRICE
FROM ranked WHERE R=1 AND PRICE IS NOT NULL;
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 하위 쿼리 MAX(PRICE)로 최고 가격을 구합니다. 그 값과 같은 가격을 가진 원본 행을 선택합니다. | DENSE_RANK로 최고 가격 선택 |
| 비용 | 순차 스캔으로 최대값과 일치 행을 찾으면 O(N)입니다. 대안의 순위 계산은 가격 정렬이 필요할 수 있습니다. | DENSE_RANK가 가격순으로 순위를 계산하므로, 정렬이 필요한 계획에서는 MAX 스캔보다 비용이 큽니다. |

## 검증

공식 예제 테이블을 로컬 SQLite에서 실행하고 두 쿼리의 결과를 비교했습니다. YEAR·MONTH·DATE_FORMAT 등은 호환 함수를 사용했습니다. 이는 MySQL 서버의 실행·성능 검증이나 새 사이트 제출을 뜻하지 않습니다.

문제 폴더에서 `python test_query.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Return full information for the most expensive food product.

### Conditions and input/output

The input consists of the tables below; the output is a query result set. Return full information for the most expensive food product.

This SQL task is defined by table schemas and query predicates rather than array-size limits.

- `FOOD_PRODUCT`: `PRODUCT_ID`, `PRODUCT_NAME`, `PRODUCT_CD`, `CATEGORY`, `PRICE`

### Approach

Compute MAX(PRICE) in a scalar subquery, then select original rows whose price equals it.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

MAX finds the global maximum price, and the outer equality retains every row with that price, including ties.

Sequential maximum and equality scans take O(N); the ranking alternative may require sorting prices.

Boundary cases: Return the product information, not just the maximum price. The query also preserves tied maxima.

### Alternative: Select top prices with DENSE_RANK

DENSE_RANK orders prices; a sorting plan costs more than a maximum scan.

### Verification

Official example tables were checked locally with SQLite and the two query results were compared. Compatibility functions supplied YEAR, MONTH, DATE_FORMAT and similar MySQL functions. This does not constitute MySQL-server execution/performance testing or a new site submission.

Run `python test_query.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 가격이 제일 비싼 식품의 정보 출력하기](https://school.programmers.co.kr/learn/courses/30/lessons/131115) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
