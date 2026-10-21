# 상품 별 오프라인 매출 구하기

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/131533) · Level 2 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

상품별 가격과 오프라인 판매 수량을 곱해 매출을 계산합니다.

## 조건과 입출력

입력은 아래 테이블이고 출력은 쿼리 결과 집합입니다. 상품별 가격과 오프라인 판매 수량을 곱해 매출을 계산합니다.

수치 배열 제한 대신 테이블 스키마와 조회 조건을 사용합니다.

- `PRODUCT`: `PRODUCT_ID`, `PRODUCT_CODE`, `PRICE`
- `OFFLINE_SALE`: `OFFLINE_SALE_ID`, `PRODUCT_ID`, `SALES_AMOUNT`, `SALES_DATE`

## 풀이를 따라가기

PRODUCT_ID로 상품과 판매 기록을 연결합니다. PRODUCT_CODE별 PRICE×SALES_AMOUNT 합계를 구하고 매출 내림차순·코드 오름차순으로 출력합니다.

[기본 풀이 / Main](solution.sql) · [다른 풀이 / Alternative](alternative.sql) · [제출 원본 / Archived submission](submitted_original.sql)

```sql
-- PRODUCT_ID로 상품과 판매 기록을 연결한다. PRODUCT_CODE별 PRICE×SALES_AMOUNT 합계를 구하고 매출 내림차순·코드 오름차순으로 출력한다.
SELECT p.PRODUCT_CODE, SUM(p.PRICE * s.SALES_AMOUNT) AS SALES
FROM PRODUCT AS p
JOIN OFFLINE_SALE AS s ON s.PRODUCT_ID = p.PRODUCT_ID
GROUP BY p.PRODUCT_CODE
ORDER BY SALES DESC, p.PRODUCT_CODE
```

## 정답이 되는 이유

판매 행을 상품 키로 연결하면 각 판매 수량에 해당 상품 가격을 곱할 수 있습니다. 이를 상품 코드별로 더하면 오프라인 매출이 됩니다. 대안은 수량을 먼저 합쳐 같은 곱셈의 분배법칙을 적용합니다.

상품 P개와 판매 S개의 조인·집계 뒤 G개 매출을 정렬합니다. 조인 비용은 키 인덱스와 계획에 따르며 결과 비교 정렬은 O(G log G)입니다.

주의할 점: 판매 기록 수가 아니라 판매 수량을 곱합니다. 판매가 없는 상품은 내부 조인 결과에 없습니다.

## 다른 방법: 상품별 판매 수량 선집계

```sql
WITH quantities AS (
    SELECT PRODUCT_ID,SUM(SALES_AMOUNT) AS AMOUNT FROM OFFLINE_SALE GROUP BY PRODUCT_ID
)
SELECT p.PRODUCT_CODE,SUM(p.PRICE*q.AMOUNT) AS SALES
FROM PRODUCT p JOIN quantities q ON q.PRODUCT_ID=p.PRODUCT_ID
GROUP BY p.PRODUCT_CODE ORDER BY SALES DESC,p.PRODUCT_CODE;
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | PRODUCT_ID로 상품과 판매 기록을 연결합니다. PRODUCT_CODE별 PRICE×SALES_AMOUNT 합계를 구하고 매출 내림차순·코드 오름차순으로 출력합니다. | 상품별 판매 수량 선집계 |
| 비용 | 상품 P개와 판매 S개의 조인·집계 뒤 G개 매출을 정렬합니다. 조인 비용은 키 인덱스와 계획에 따르며 결과 비교 정렬은 O(G log G)입니다. | 판매 수량을 상품별로 먼저 합쳐 조인 행 수를 줄입니다. 상품당 판매가 여러 건일 때 중간 조인 크기가 작아집니다. |

## 검증

공식 예제 테이블을 로컬 SQLite에서 실행하고 두 쿼리의 결과를 비교했습니다. YEAR·MONTH·DATE_FORMAT 등은 호환 함수를 사용했습니다. 이는 MySQL 서버의 실행·성능 검증이나 새 사이트 제출을 뜻하지 않습니다.

문제 폴더에서 `python test_query.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Compute product revenue from unit price times offline sales quantity.

### Conditions and input/output

The input consists of the tables below; the output is a query result set. Compute product revenue from unit price times offline sales quantity.

This SQL task is defined by table schemas and query predicates rather than array-size limits.

- `PRODUCT`: `PRODUCT_ID`, `PRODUCT_CODE`, `PRICE`
- `OFFLINE_SALE`: `OFFLINE_SALE_ID`, `PRODUCT_ID`, `SALES_AMOUNT`, `SALES_DATE`

### Approach

Join product and sale records by PRODUCT_ID, sum PRICE×SALES_AMOUNT per PRODUCT_CODE, then sort revenue descending and code ascending.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

The product-key join attaches a unit price to each sale. Summing price times quantity by product code gives revenue. Preaggregating quantities uses the same distributive identity.

Join P products with S sales, aggregate and sort G totals. Key indexes and the plan determine join cost; result comparison sorting is O(G log G).

Boundary cases: Multiply by sales quantity, not sale-record count. Products without sales are absent from the inner join.

### Alternative: Preaggregate sold quantities per product

Preaggregate quantities by product, reducing joined rows when products have multiple sales.

### Verification

Official example tables were checked locally with SQLite and the two query results were compared. Compatibility functions supplied YEAR, MONTH, DATE_FORMAT and similar MySQL functions. This does not constitute MySQL-server execution/performance testing or a new site submission.

Run `python test_query.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 상품 별 오프라인 매출 구하기](https://school.programmers.co.kr/learn/courses/30/lessons/131533) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
