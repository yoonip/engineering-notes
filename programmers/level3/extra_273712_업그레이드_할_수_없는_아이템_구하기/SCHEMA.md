# 입력 테이블 / Input schema — 업그레이드 할 수 없는 아이템 구하기

풀이에서 사용하는 테이블의 열·자료형·NULL 허용 여부를 정리했다. NULL은 빈 문자열이나 숫자 0과 다른 값이므로 필터와 집계에서 구분한다.

Columns, types and nullability for the tables used by the solution. NULL is distinct from an empty string or numeric zero and must be handled separately in filtering and aggregation.

## `ITEM_INFO`

| 열 / Column | 자료형 / Type | NULL 허용 / Nullable |
|---|---|---|
| `ITEM_ID` | `INTEGER` | FALSE |
| `ITEM_NAME` | `VARCHAR(N)` | FALSE |
| `RARITY` | `INTEGER` | FALSE |
| `PRICE` | `INTEGER` | FALSE |

## `ITEM_TREE`

| 열 / Column | 자료형 / Type | NULL 허용 / Nullable |
|---|---|---|
| `ITEM_ID` | `INTEGER` | FALSE |
| `PARENT_ITEM_ID` | `INTEGER` | TRUE |

자료형 표의 TRUE는 NULL 허용, FALSE는 NULL 불가를 뜻한다. 기본키·고유성·행 수의 추가 조건은 공식 문제 본문을 따른다.

TRUE in a nullability column permits NULL; FALSE does not. Additional primary-key, uniqueness and row-count conditions follow the official statement.

출처 / Source: [Programmers 273712](https://school.programmers.co.kr/learn/courses/30/lessons/273712), 2026-10-19.

[풀이로 돌아가기 / Back to solution](README.md)
