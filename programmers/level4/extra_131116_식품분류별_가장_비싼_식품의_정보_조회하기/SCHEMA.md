# 입력 테이블 / Input schema — 식품분류별 가장 비싼 식품의 정보 조회하기

풀이에서 사용하는 테이블의 열·자료형·NULL 허용 여부를 정리했다. NULL은 빈 문자열이나 숫자 0과 다른 값이므로 필터와 집계에서 구분한다.

Columns, types and nullability for the tables used by the solution. NULL is distinct from an empty string or numeric zero and must be handled separately in filtering and aggregation.

## `FOOD_PRODUCT`

| 열 / Column | 자료형 / Type | NULL 허용 / Nullable |
|---|---|---|
| `PRODUCT_ID` | `VARCHAR(10)` | FALSE |
| `PRODUCT_NAME` | `VARCHAR(50)` | FALSE |
| `PRODUCT_CD` | `VARCHAR(10)` | TRUE |
| `CATEGORY` | `VARCHAR(10)` | TRUE |
| `PRICE` | `NUMBER` | TRUE |

자료형 표의 TRUE는 NULL 허용, FALSE는 NULL 불가를 뜻한다. 기본키·고유성·행 수의 추가 조건은 공식 문제 본문을 따른다.

TRUE in a nullability column permits NULL; FALSE does not. Additional primary-key, uniqueness and row-count conditions follow the official statement.

출처 / Source: [Programmers 131116](https://school.programmers.co.kr/learn/courses/30/lessons/131116), 2026-10-19.

[풀이로 돌아가기 / Back to solution](README.md)
