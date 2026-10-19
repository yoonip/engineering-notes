# 잡은 물고기 중 가장 큰 물고기의 길이 구하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/298515) · Level 1 · MySQL

## 풀이

MAX는 NULL을 제외하고 최대 길이를 구합니다. 숫자 뒤에 cm를 붙여 한 행으로 출력합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.sql) · [채점 기록 / Grade](grading.json)

```sql
SELECT CONCAT(MAX(LENGTH), 'cm') AS MAX_LENGTH
FROM FISH_INFO

-- 전체 코드 줄별 설명
-- SELECT CONCAT(MAX(LENGTH), 'cm') AS MAX_LENGTH  -- MAX는 최댓값, CONCAT은 문자열 연결, AS는 별칭. 최대 길이에 단위 cm를 붙임.
-- FROM FISH_INFO  -- FROM은 조회할 물고기 정보 테이블 지정.

-- 풀이 요약
-- MAX는 NULL을 제외하고 최대 길이를 구합니다. 숫자 뒤에 cm를 붙여 한 행으로 출력합니다.
--
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
