# 입력 테이블 / Input schema — 5월 식품들의 총매출 조회하기

[문제 풀이 / Solution](README.md) · [Level 4 목록 / Level 4 index](../README.md)

풀이에서 사용하는 테이블의 열·자료형·NULL 허용 여부를 정리했습니다. NULL은 빈 문자열이나 숫자 0과 다른 값이므로 필터와 집계에서 구분합니다.

Columns, types and nullability for the tables used by the solution. NULL is distinct from an empty string or numeric zero and must be handled separately in filtering and aggregation.

## `FOOD_PRODUCT`

| 열 / Column | 자료형 / Type | NULL 허용 / Nullable |
|---|---|---|
| `PRODUCT_ID` | `VARCHAR(10)` | FALSE |
| `PRODUCT_NAME` | `VARCHAR(50)` | FALSE |
| `PRODUCT_CD` | `VARCHAR(10)` | TRUE |
| `CATEGORY` | `VARCHAR(10)` | TRUE |
| `PRICE` | `NUMBER` | TRUE |

## `FOOD_ORDER`

| 열 / Column | 자료형 / Type | NULL 허용 / Nullable |
|---|---|---|
| `ORDER_ID` | `VARCHAR(10)` | FALSE |
| `PRODUCT_ID` | `VARCHAR(5)` | FALSE |
| `AMOUNT` | `NUMBER` | FALSE |
| `PRODUCE_DATE` | `DATE` | TRUE |
| `IN_DATE` | `DATE` | TRUE |
| `OUT_DATE` | `DATE` | TRUE |
| `FACTORY_ID` | `VARCHAR(10)` | FALSE |
| `WAREHOUSE_ID` | `VARCHAR(10)` | FALSE |

자료형 표의 TRUE는 NULL 허용, FALSE는 NULL 불가를 뜻합니다. 기본키·고유성·행 수의 추가 조건은 공식 문제 본문을 따릅니다.

TRUE in a nullability column permits NULL; FALSE does not. Additional primary-key, uniqueness and row-count conditions follow the official statement.

출처 / Source: [Programmers 131117](https://school.programmers.co.kr/learn/courses/30/lessons/131117), 2026-10-19.

[풀이로 돌아가기 / Back to solution](README.md)
