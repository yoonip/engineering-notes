# 입력 테이블 / Input schema — 서울에 위치한 식당 목록 출력하기

풀이에서 사용하는 테이블의 열·자료형·NULL 허용 여부를 정리했습니다. NULL은 빈 문자열이나 숫자 0과 다른 값이므로 필터와 집계에서 구분합니다.

Columns, types and nullability for the tables used by the solution. NULL is distinct from an empty string or numeric zero and must be handled separately in filtering and aggregation.

## `REST_INFO`

| 열 / Column | 자료형 / Type | NULL 허용 / Nullable |
|---|---|---|
| `REST_ID` | `VARCHAR(5)` | FALSE |
| `REST_NAME` | `VARCHAR(50)` | FALSE |
| `FOOD_TYPE` | `VARCHAR(20)` | TRUE |
| `VIEWS` | `NUMBER` | TRUE |
| `FAVORITES` | `NUMBER` | TRUE |
| `PARKING_LOT` | `VARCHAR(1)` | TRUE |
| `ADDRESS` | `VARCHAR(100)` | TRUE |
| `TEL` | `VARCHAR(100)` | TRUE |

## `REST_REVIEW`

| 열 / Column | 자료형 / Type | NULL 허용 / Nullable |
|---|---|---|
| `REVIEW_ID` | `VARCHAR(10)` | FALSE |
| `REST_ID` | `VARCHAR(10)` | TRUE |
| `MEMBER_ID` | `VARCHAR(100)` | TRUE |
| `REVIEW_SCORE` | `NUMBER` | TRUE |
| `REVIEW_TEXT` | `VARCHAR(1000)` | TRUE |
| `REVIEW_DATE` | `DATE` | TRUE |

자료형 표의 TRUE는 NULL 허용, FALSE는 NULL 불가를 뜻합니다. 기본키·고유성·행 수의 추가 조건은 공식 문제 본문을 따릅니다.

TRUE in a nullability column permits NULL; FALSE does not. Additional primary-key, uniqueness and row-count conditions follow the official statement.

출처 / Source: [Programmers 131118](https://school.programmers.co.kr/learn/courses/30/lessons/131118), 2026-10-19.

[풀이로 돌아가기 / Back to solution](README.md)
