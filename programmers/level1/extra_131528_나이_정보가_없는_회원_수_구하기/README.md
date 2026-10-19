# 나이 정보가 없는 회원 수 구하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/131528) · Level 1 · MySQL

## 풀이

나이 열이 NULL인 회원만 필터링해 개수를 셉니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.sql) · [채점 기록 / Grade](grading.json)

```sql
SELECT COUNT(*) AS USERS
FROM USER_INFO
WHERE AGE IS NULL

-- 전체 코드 줄별 설명
-- SELECT COUNT(*) AS USERS  -- SELECT는 조회, COUNT(*)는 행 수 집계, AS는 출력 열 별칭.
-- FROM USER_INFO  -- FROM은 회원 정보 테이블 지정.
-- WHERE AGE IS NULL  -- WHERE는 필터. IS NULL은 나이 정보가 없는지 검사. = NULL로 비교하지 않음.

-- 풀이 요약
-- 나이 열이 NULL인 회원만 필터링해 개수를 셉니다.
--
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
