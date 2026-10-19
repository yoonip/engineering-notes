# 여러 기준으로 정렬하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/59404) · Level 1 · MySQL

## 풀이

이름순으로 정렬하되 같은 이름 안에서는 나중 입소한 동물을 먼저 배치합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.sql) · [채점 기록 / Grade](grading.json)

```sql
SELECT ANIMAL_ID, NAME, DATETIME
FROM ANIMAL_INS
ORDER BY NAME ASC, DATETIME DESC

-- 전체 코드 줄별 설명
-- SELECT ANIMAL_ID, NAME, DATETIME  -- SELECT는 출력 열 선택. ID·이름·보호 시작 시각 조회.
-- FROM ANIMAL_INS  -- FROM은 동물 입소 정보 테이블 지정.
-- ORDER BY NAME ASC, DATETIME DESC  -- ORDER BY는 정렬. 이름은 ASC 오름차순, 같은 이름이면 시각은 DESC 내림차순.

-- 풀이 요약
-- 이름순으로 정렬하되 같은 이름 안에서는 나중 입소한 동물을 먼저 배치합니다.
--
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
