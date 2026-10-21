# 입력 테이블 / Input schema — 취소되지 않은 진료 예약 조회하기

[문제 풀이 / Solution](README.md) · [Level 4 목록 / Level 4 index](../README.md)

풀이에서 사용하는 테이블의 열·자료형·NULL 허용 여부를 정리했습니다. NULL은 빈 문자열이나 숫자 0과 다른 값이므로 필터와 집계에서 구분합니다.

Columns, types and nullability for the tables used by the solution. NULL is distinct from an empty string or numeric zero and must be handled separately in filtering and aggregation.

## `PATIENT`

| 열 / Column | 자료형 / Type | NULL 허용 / Nullable |
|---|---|---|
| `PT_NO` | `VARCHAR(N)` | FALSE |
| `PT_NAME` | `VARCHAR(N)` | FALSE |
| `GEND_CD` | `VARCHAR(N)` | FALSE |
| `AGE` | `INTEGER` | FALSE |
| `TLNO` | `VARCHAR(N)` | TRUE |

## `DOCTOR`

| 열 / Column | 자료형 / Type | NULL 허용 / Nullable |
|---|---|---|
| `DR_NAME` | `VARCHAR(N)` | FALSE |
| `DR_ID` | `VARCHAR(N)` | FALSE |
| `LCNS_NO` | `VARCHAR(N)` | FALSE |
| `HIRE_YMD` | `DATE` | FALSE |
| `MCDP_CD` | `VARCHAR(N)` | TRUE |
| `TLNO` | `VARCHAR(N)` | TRUE |

## `APPOINTMENT`

| 열 / Column | 자료형 / Type | NULL 허용 / Nullable |
|---|---|---|
| `APNT_YMD` | `TIMESTAMP` | FALSE |
| `APNT_NO` | `INTEGER` | FALSE |
| `PT_NO` | `VARCHAR(N)` | FALSE |
| `MCDP_CD` | `VARCHAR(N)` | FALSE |
| `MDDR_ID` | `VARCHAR(N)` | FALSE |
| `APNT_CNCL_YN` | `VARCHAR(N)` | TRUE |
| `APNT_CNCL_YMD` | `DATE` | TRUE |

자료형 표의 TRUE는 NULL 허용, FALSE는 NULL 불가를 뜻합니다. 기본키·고유성·행 수의 추가 조건은 공식 문제 본문을 따릅니다.

TRUE in a nullability column permits NULL; FALSE does not. Additional primary-key, uniqueness and row-count conditions follow the official statement.

출처 / Source: [Programmers 132204](https://school.programmers.co.kr/learn/courses/30/lessons/132204), 2026-10-19.

[풀이로 돌아가기 / Back to solution](README.md)
