# 가격대 별 상품 개수 구하기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/131530) · Level 2 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

가격을 만 원 단위 반열린 구간으로 묶어 상품 수를 셉니다.

## 조건과 입출력

입력은 아래 테이블이고 출력은 쿼리 결과 집합입니다. 가격을 만 원 단위 반열린 구간으로 묶어 상품 수를 셉니다.

수치 배열 제한 대신 테이블 스키마와 조회 조건을 사용합니다.

- `PRODUCT`: `PRODUCT_ID`, `PRODUCT_CODE`, `PRICE`

## 풀이를 따라가기

floor(PRICE/10000)×10000으로 가격대의 시작값을 구합니다. 같은 시작값으로 묶어 개수를 세고 가격대순으로 정렬합니다.

[기본 풀이 / Main](solution.sql) · [다른 풀이 / Alternative](alternative.sql) · [제출 원본 / Archived submission](submitted_original.sql)

```sql
-- floor(PRICE/10000)×10000으로 가격대의 시작값을 구한다. 같은 시작값으로 묶어 개수를 세고 가격대순으로 정렬한다.
SELECT FLOOR(PRICE / 10000) * 10000 AS PRICE_GROUP, COUNT(*) AS PRODUCTS
FROM PRODUCT
GROUP BY PRICE_GROUP
ORDER BY PRICE_GROUP
```

## 정답이 되는 이유

가격을 10,000으로 나눈 몫의 바닥값에 10,000을 곱하면 해당 가격대의 시작값이 됩니다. 같은 시작값으로 묶으므로 경계 가격도 정확한 구간에 들어갑니다.

N개 상품의 구간을 계산해 집계한 뒤 G개 가격대를 정렬합니다. 결과 비교 정렬은 O(G log G); 윈도 대안은 DISTINCT 처리도 필요합니다.

주의할 점: 정확히 10000원인 상품은 10000~19999원 구간입니다. 문자열 앞자리로 나누면 가격 자릿수에 따라 잘못될 수 있습니다.

## 다른 방법: 윈도 COUNT와 중복 가격대 제거

```sql
SELECT DISTINCT FLOOR(PRICE/10000)*10000 AS PRICE_GROUP,
       COUNT(*) OVER (PARTITION BY FLOOR(PRICE/10000)) AS PRODUCTS
FROM PRODUCT ORDER BY PRICE_GROUP;
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | floor(PRICE/10000)×10000으로 가격대의 시작값을 구합니다. 같은 시작값으로 묶어 개수를 세고 가격대순으로 정렬합니다. | 윈도 COUNT와 중복 가격대 제거 |
| 비용 | N개 상품의 구간을 계산해 집계한 뒤 G개 가격대를 정렬합니다. 결과 비교 정렬은 O(G log G); 윈도 대안은 DISTINCT 처리도 필요합니다. | 각 상품 행에 가격대별 개수를 붙인 뒤 DISTINCT로 줄입니다. 윈도 계산과 중복 제거가 추가됩니다. |

## 검증

공식 예제 테이블을 로컬 SQLite에서 실행하고 두 쿼리의 결과를 비교했습니다. YEAR·MONTH·DATE_FORMAT 등은 호환 함수를 사용했습니다. 이는 MySQL 서버의 실행·성능 검증이나 새 사이트 제출을 뜻하지 않습니다.

문제 폴더에서 `python test_query.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Count products in half-open price bands of ten thousand.

### Conditions and input/output

The input consists of the tables below; the output is a query result set. Count products in half-open price bands of ten thousand.

This SQL task is defined by table schemas and query predicates rather than array-size limits.

- `PRODUCT`: `PRODUCT_ID`, `PRODUCT_CODE`, `PRICE`

### Approach

Compute each lower bound as floor(PRICE/10000)×10000, group by that bound and order bands ascending.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Flooring price divided by 10,000 and multiplying back produces its band start. Grouping by that start assigns boundary prices to the correct bands.

Compute and aggregate bands for N products, then sort G results in O(G log G) comparisons. The window alternative also needs DISTINCT.

Boundary cases: A price of exactly 10000 belongs to the 10000–19999 band. String-prefix grouping is unsafe when digit lengths vary.

### Alternative: Window COUNT followed by price-band deduplication

Attach band counts to product rows, then deduplicate; window computation and DISTINCT add work.

### Verification

Official example tables were checked locally with SQLite and the two query results were compared. Compatibility functions supplied YEAR, MONTH, DATE_FORMAT and similar MySQL functions. This does not constitute MySQL-server execution/performance testing or a new site submission.

Run `python test_query.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 가격대 별 상품 개수 구하기](https://school.programmers.co.kr/learn/courses/30/lessons/131530) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
