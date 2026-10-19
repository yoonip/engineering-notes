# 가장 큰 물고기 10마리 구하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/298517) · Level 1 · MySQL

## 풀이

길이가 큰 순서로 정렬하고 같은 길이는 ID 순으로 정렬한 뒤 앞 10행을 선택합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.sql) · [채점 기록 / Grade](grading.json)

```sql
SELECT ID, LENGTH
FROM FISH_INFO
ORDER BY LENGTH DESC, ID ASC
LIMIT 10

-- 전체 코드 줄별 설명
-- SELECT ID, LENGTH  -- SELECT는 출력 열 선택. 쉼표로 ID와 길이 구분.
-- FROM FISH_INFO  -- FROM은 물고기 정보 테이블 지정.
-- ORDER BY LENGTH DESC, ID ASC  -- ORDER BY는 정렬, DESC는 내림차순, ASC는 오름차순. 길이 동률이면 ID가 작은 순.
-- LIMIT 10  -- LIMIT은 출력 행 수 제한. 정렬 결과 상위 10마리만 출력.

-- 풀이 요약
-- 길이가 큰 순서로 정렬하고 같은 길이는 ID 순으로 정렬한 뒤 앞 10행을 선택합니다.
--
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
