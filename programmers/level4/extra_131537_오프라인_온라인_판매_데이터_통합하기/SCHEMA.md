# 입력 테이블 / Input schema — 오프라인/온라인 판매 데이터 통합하기

[문제 풀이 / Solution](README.md) · [Level 4 목록 / Level 4 index](../README.md)

풀이에서 사용하는 테이블의 열·자료형·NULL 허용 여부를 정리했습니다. NULL은 빈 문자열이나 숫자 0과 다른 값이므로 필터와 집계에서 구분합니다.

Columns, types and nullability for the tables used by the solution. NULL is distinct from an empty string or numeric zero and must be handled separately in filtering and aggregation.

## `ONLINE_SALE`

| 열 / Column | 자료형 / Type | NULL 허용 / Nullable |
|---|---|---|
| `ONLINE_SALE_ID` | `INTEGER` | FALSE |
| `USER_ID` | `INTEGER` | FALSE |
| `PRODUCT_ID` | `INTEGER` | FALSE |
| `SALES_AMOUNT` | `INTEGER` | FALSE |
| `SALES_DATE` | `DATE` | FALSE |

## `OFFLINE_SALE`

| 열 / Column | 자료형 / Type | NULL 허용 / Nullable |
|---|---|---|
| `OFFLINE_SALE_ID` | `INTEGER` | FALSE |
| `PRODUCT_ID` | `INTEGER` | FALSE |
| `SALES_AMOUNT` | `INTEGER` | FALSE |
| `SALES_DATE` | `DATE` | FALSE |

자료형 표의 TRUE는 NULL 허용, FALSE는 NULL 불가를 뜻합니다. 기본키·고유성·행 수의 추가 조건은 공식 문제 본문을 따릅니다.

TRUE in a nullability column permits NULL; FALSE does not. Additional primary-key, uniqueness and row-count conditions follow the official statement.

출처 / Source: [Programmers 131537](https://school.programmers.co.kr/learn/courses/30/lessons/131537), 2026-10-19.

[풀이로 돌아가기 / Back to solution](README.md)
