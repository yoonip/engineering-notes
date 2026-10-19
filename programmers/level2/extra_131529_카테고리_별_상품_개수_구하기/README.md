# 카테고리 별 상품 개수 구하기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/131529) · Level 2 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

상품 코드의 앞 두 글자를 카테고리로 보고 상품 수를 셉니다.

## 조건과 입출력

입력은 아래 테이블이고 출력은 쿼리 결과 집합입니다. 상품 코드의 앞 두 글자를 카테고리로 보고 상품 수를 셉니다.

수치 배열 제한 대신 테이블 스키마와 조회 조건을 사용합니다.

- `PRODUCT`: `PRODUCT_ID`, `PRODUCT_CODE`, `PRICE`

## 풀이를 따라가기

LEFT(PRODUCT_CODE,2)로 카테고리 키를 만들고 GROUP BY합니다. 카테고리 오름차순으로 출력합니다.

[기본 풀이 / Main](solution.sql) · [다른 풀이 / Alternative](alternative.sql) · [제출 원본 / Archived submission](submitted_original.sql)

```sql
-- LEFT(PRODUCT_CODE,2)로 카테고리 키를 만들고 GROUP BY한다. 카테고리 오름차순으로 출력한다.
SELECT LEFT(PRODUCT_CODE, 2) AS CATEGORY, COUNT(*) AS PRODUCTS
FROM PRODUCT
GROUP BY CATEGORY
ORDER BY CATEGORY
```

## 정답이 되는 이유

상품 코드의 앞 두 글자가 같을 때만 같은 그룹에 들어갑니다. COUNT(*)는 그 그룹의 모든 상품 행을 세므로 카테고리별 개수가 됩니다.

N개 상품을 집계하고 G개 카테고리를 정렬합니다. 결과 비교 정렬은 O(G log G)이며, 대안은 행별 윈도 결과에서 중복도 제거합니다.

주의할 점: 상품 코드 전체가 아니라 처음 두 글자만 씁니다. 숫자로 바꾸지 않아 앞의 0을 보존합니다.

## 다른 방법: 윈도 COUNT로 원본 행 보존 후 DISTINCT

```sql
SELECT DISTINCT SUBSTR(PRODUCT_CODE,1,2) AS CATEGORY,
       COUNT(*) OVER (PARTITION BY SUBSTR(PRODUCT_CODE,1,2)) AS PRODUCTS
FROM PRODUCT ORDER BY CATEGORY;
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | LEFT(PRODUCT_CODE,2)로 카테고리 키를 만들고 GROUP BY합니다. 카테고리 오름차순으로 출력합니다. | 윈도 COUNT로 원본 행 보존 후 DISTINCT |
| 비용 | N개 상품을 집계하고 G개 카테고리를 정렬합니다. 결과 비교 정렬은 O(G log G)이며, 대안은 행별 윈도 결과에서 중복도 제거합니다. | 각 상품 행에 카테고리별 개수를 붙인 뒤 DISTINCT로 한 행만 남깁니다. GROUP BY보다 중간 결과가 많습니다. |

## 검증

공식 예제 테이블을 로컬 SQLite에서 실행하고 두 쿼리의 결과를 비교했습니다. YEAR·MONTH·DATE_FORMAT 등은 호환 함수를 사용했습니다. 이는 MySQL 서버의 실행·성능 검증이나 새 사이트 제출을 뜻하지 않습니다.

문제 폴더에서 `python test_query.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Count products by the first two characters of the product code.

### Conditions and input/output

The input consists of the tables below; the output is a query result set. Count products by the first two characters of the product code.

This SQL task is defined by table schemas and query predicates rather than array-size limits.

- `PRODUCT`: `PRODUCT_ID`, `PRODUCT_CODE`, `PRICE`

### Approach

Create the category key with LEFT(PRODUCT_CODE,2), group by it and order categories ascending.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Rows share a group exactly when their first two product-code characters match. COUNT(*) therefore gives the product count for each category.

Aggregate N products and sort G categories, with O(G log G) comparison sorting. The window alternative also deduplicates per-row results.

Boundary cases: Use only the first two characters, preserving leading zeros by keeping them as text.

### Alternative: Preserve rows with window COUNT, then deduplicate

Attach a category count to each product row, then deduplicate. This retains more intermediate rows than GROUP BY.

### Verification

Official example tables were checked locally with SQLite and the two query results were compared. Compatibility functions supplied YEAR, MONTH, DATE_FORMAT and similar MySQL functions. This does not constitute MySQL-server execution/performance testing or a new site submission.

Run `python test_query.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 카테고리 별 상품 개수 구하기](https://school.programmers.co.kr/learn/courses/30/lessons/131529) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
