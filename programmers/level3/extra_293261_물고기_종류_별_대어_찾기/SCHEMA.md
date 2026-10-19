# 입력 테이블 / Input schema — 물고기 종류 별 대어 찾기

풀이에서 사용하는 테이블의 열·자료형·NULL 허용 여부를 정리했습니다. NULL은 빈 문자열이나 숫자 0과 다른 값이므로 필터와 집계에서 구분합니다.

Columns, types and nullability for the tables used by the solution. NULL is distinct from an empty string or numeric zero and must be handled separately in filtering and aggregation.

## `FISH_INFO`

| 열 / Column | 자료형 / Type | NULL 허용 / Nullable |
|---|---|---|
| `ID` | `INTEGER` | FALSE |
| `FISH_TYPE` | `INTEGER` | FALSE |
| `LENGTH` | `FLOAT` | TRUE |
| `TIME` | `DATE` | FALSE |

## `FISH_NAME_INFO`

| 열 / Column | 자료형 / Type | NULL 허용 / Nullable |
|---|---|---|
| `FISH_TYPE` | `INTEGER` | FALSE |
| `FISH_NAME` | `VARCHAR` | FALSE |

자료형 표의 TRUE는 NULL 허용, FALSE는 NULL 불가를 뜻합니다. 기본키·고유성·행 수의 추가 조건은 공식 문제 본문을 따릅니다.

TRUE in a nullability column permits NULL; FALSE does not. Additional primary-key, uniqueness and row-count conditions follow the official statement.

출처 / Source: [Programmers 293261](https://school.programmers.co.kr/learn/courses/30/lessons/293261), 2026-10-19.

[풀이로 돌아가기 / Back to solution](README.md)
