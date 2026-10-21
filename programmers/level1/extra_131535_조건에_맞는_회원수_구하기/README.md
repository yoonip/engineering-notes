# 조건에 맞는 회원수 구하기

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/131535) · Level 1 · MySQL

## 풀이

가입 연도와 나이 범위를 모두 만족하는 회원 행을 셉니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.sql) · [채점 기록 / Grade](grading.json)

```sql
SELECT COUNT(*) AS USERS
FROM USER_INFO
WHERE JOINED >= '2021-01-01' AND JOINED < '2022-01-01'
  AND AGE BETWEEN 20 AND 29

-- 전체 코드 줄별 설명
-- SELECT COUNT(*) AS USERS  -- SELECT는 조회, COUNT(*)는 행 수 집계, AS는 출력 열 별칭.
-- FROM USER_INFO  -- FROM은 회원 정보 테이블 지정.
-- WHERE JOINED >= '2021-01-01' AND JOINED < '2022-01-01'  -- WHERE는 필터, AND는 모두 만족. 가입 연도를 2021년으로 제한.
--   AND AGE BETWEEN 20 AND 29  -- BETWEEN a AND b는 양 끝을 포함한 범위 검사. 20세 이상 29세 이하 선택.

-- 풀이 요약
-- 가입 연도와 나이 범위를 모두 만족하는 회원 행을 셉니다.
--
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
