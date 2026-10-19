# 최댓값 구하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/59415) · Level 1 · MySQL

## 풀이

날짜·시각의 최댓값은 가장 최근 시각입니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.sql) · [채점 기록 / Grade](grading.json)

```sql
SELECT MAX(DATETIME) AS 시간
FROM ANIMAL_INS

-- 전체 코드 줄별 설명
-- SELECT MAX(DATETIME) AS 시간  -- SELECT는 조회, MAX는 최댓값 집계, AS는 출력 열 별칭. 가장 늦은 보호 시작 시각 계산.
-- FROM ANIMAL_INS  -- FROM은 동물 입소 정보 테이블 지정.

-- 풀이 요약
-- 날짜·시각의 최댓값은 가장 최근 시각입니다.
--
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
