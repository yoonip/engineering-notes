# 역순 정렬하기

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/59035) · Level 1 · MySQL

## 풀이

조회할 열과 정렬 기준 열이 달라도 됩니다. 이름·시각을 ID 역순으로 출력합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.sql) · [채점 기록 / Grade](grading.json)

```sql
SELECT NAME, DATETIME
FROM ANIMAL_INS
ORDER BY ANIMAL_ID DESC

-- 전체 코드 줄별 설명
-- SELECT NAME, DATETIME  -- SELECT는 출력 열 선택. 이름과 보호 시작 시각 조회.
-- FROM ANIMAL_INS  -- FROM은 동물 입소 정보 테이블 지정.
-- ORDER BY ANIMAL_ID DESC  -- ORDER BY는 정렬, DESC는 내림차순. 출력하지 않는 ID 열도 정렬 기준으로 사용 가능.

-- 풀이 요약
-- 조회할 열과 정렬 기준 열이 달라도 됩니다. 이름·시각을 ID 역순으로 출력합니다.
--
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
