# 입력 테이블 / Input schema — 조건에 맞는 개발자 찾기

[문제 풀이 / Solution](README.md) · [Level 2 목록 / Level 2 index](../README.md)

풀이에서 사용하는 테이블의 열·자료형·NULL 허용 여부를 정리했습니다. NULL은 빈 문자열이나 숫자 0과 다른 값이므로 필터와 집계에서 구분합니다.

Columns, types and nullability for the tables used by the solution. NULL is distinct from an empty string or numeric zero and must be handled separately in filtering and aggregation.

## `SKILLCODES`

| 열 / Column | 자료형 / Type | 고유성 / Unique | NULL 허용 / Nullable |
|---|---|---|---|
| `NAME` | `VARCHAR(N)` | Y | N |
| `CATEGORY` | `VARCHAR(N)` | N | N |
| `CODE` | `INTEGER` | Y | N |

## `DEVELOPERS`

| 열 / Column | 자료형 / Type | 고유성 / Unique | NULL 허용 / Nullable |
|---|---|---|---|
| `ID` | `VARCHAR(N)` | Y | N |
| `FIRST_NAME` | `VARCHAR(N)` | N | Y |
| `LAST_NAME` | `VARCHAR(N)` | N | Y |
| `EMAIL` | `VARCHAR(N)` | Y | N |
| `SKILL_CODE` | `INTEGER` | N | N |

고유성 열의 Y는 값이 중복되지 않는다는 뜻이고, NULL 허용 열의 Y는 값이 없어도 된다는 뜻입니다. 두 조건은 서로 다릅니다.

Y in Unique means values must be unique; Y in Nullable permits NULL. These are separate constraints.

출처 / Source: [Programmers 276034](https://school.programmers.co.kr/learn/courses/30/lessons/276034), 2026-10-19.

[풀이로 돌아가기 / Back to solution](README.md)
