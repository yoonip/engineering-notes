# 잔챙이 잡은 수 구하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/293258) · Level 1 · MySQL

## 풀이

10cm 이하 물고기는 LENGTH가 NULL이라는 저장 규칙을 이용해 해당 행을 셉니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.sql) · [채점 기록 / Grade](grading.json)

```sql
SELECT COUNT(*) AS FISH_COUNT
FROM FISH_INFO
WHERE LENGTH IS NULL

-- 전체 코드 줄별 설명
-- SELECT COUNT(*) AS FISH_COUNT  -- SELECT는 조회, COUNT(*)는 조건을 만족하는 행 개수, AS는 결과 열 이름 지정.
-- FROM FISH_INFO  -- FROM은 물고기 정보 테이블 지정.
-- WHERE LENGTH IS NULL  -- WHERE는 조건 필터. IS NULL은 값이 없음 검사. 10cm 이하 물고기는 NULL로 저장됨.

-- 풀이 요약
-- 10cm 이하 물고기는 LENGTH가 NULL이라는 저장 규칙을 이용해 해당 행을 셉니다.
--
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
