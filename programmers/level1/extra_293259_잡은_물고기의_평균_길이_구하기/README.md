# 잡은 물고기의 평균 길이 구하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/293259) · Level 1 · MySQL

## 풀이

NULL 길이를 10으로 바꾼 뒤 평균을 구하고 소수 셋째 자리에서 반올림합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.sql) · [채점 기록 / Grade](grading.json)

```sql
SELECT ROUND(AVG(IFNULL(LENGTH, 10)), 2) AS AVERAGE_LENGTH
FROM FISH_INFO

-- 전체 코드 줄별 설명
-- SELECT ROUND(AVG(IFNULL(LENGTH, 10)), 2) AS AVERAGE_LENGTH  -- IFNULL(값,대체값)은 NULL 대체, AVG는 평균, ROUND(값,2)는 소수 둘째 자리까지 반올림, AS는 별칭.
-- FROM FISH_INFO  -- FROM은 물고기 정보 테이블 지정.

-- 풀이 요약
-- NULL 길이를 10으로 바꾼 뒤 평균을 구하고 소수 셋째 자리에서 반올림합니다.
--
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
