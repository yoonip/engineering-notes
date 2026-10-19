# 입력 테이블 / Input schema — 조회수가 가장 많은 중고거래 게시판의 첨부파일 조회하기

풀이에서 사용하는 테이블의 열·자료형·NULL 허용 여부를 정리했습니다. NULL은 빈 문자열이나 숫자 0과 다른 값이므로 필터와 집계에서 구분합니다.

Columns, types and nullability for the tables used by the solution. NULL is distinct from an empty string or numeric zero and must be handled separately in filtering and aggregation.

## `USED_GOODS_BOARD`

| 열 / Column | 자료형 / Type | NULL 허용 / Nullable |
|---|---|---|
| `BOARD_ID` | `VARCHAR(5)` | FALSE |
| `WRITER_ID` | `VARCHAR(50)` | FALSE |
| `TITLE` | `VARCHAR(100)` | FALSE |
| `CONTENTS` | `VARCHAR(1000)` | FALSE |
| `PRICE` | `NUMBER` | FALSE |
| `CREATED_DATE` | `DATE` | FALSE |
| `STATUS` | `VARCHAR(10)` | FALSE |
| `VIEWS` | `NUMBER` | FALSE |

## `USED_GOODS_FILE`

| 열 / Column | 자료형 / Type | NULL 허용 / Nullable |
|---|---|---|
| `FILE_ID` | `VARCHAR(10)` | FALSE |
| `FILE_EXT` | `VARCHAR(5)` | FALSE |
| `FILE_NAME` | `VARCHAR(256)` | FALSE |
| `BOARD_ID` | `VARCHAR(10)` | FALSE |

자료형 표의 TRUE는 NULL 허용, FALSE는 NULL 불가를 뜻합니다. 기본키·고유성·행 수의 추가 조건은 공식 문제 본문을 따릅니다.

TRUE in a nullability column permits NULL; FALSE does not. Additional primary-key, uniqueness and row-count conditions follow the official statement.

출처 / Source: [Programmers 164671](https://school.programmers.co.kr/learn/courses/30/lessons/164671), 2026-10-19.

[풀이로 돌아가기 / Back to solution](README.md)
