# 모든 레코드 조회하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/59034) · Level 1 · MySQL

## 풀이

모든 열을 조회하되 출력 순서를 ID 기준으로 명시합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.sql) · [채점 기록 / Grade](grading.json)

```sql
SELECT *
FROM ANIMAL_INS
ORDER BY ANIMAL_ID

-- 전체 코드 줄별 설명
-- SELECT *  -- SELECT는 조회, *는 테이블의 모든 열 선택.
-- FROM ANIMAL_INS  -- FROM은 동물 입소 정보 테이블 지정.
-- ORDER BY ANIMAL_ID  -- ORDER BY는 정렬. 동물 ID 오름차순으로 모든 행 출력.

-- 풀이 요약
-- 모든 열을 조회하되 출력 순서를 ID 기준으로 명시합니다.
--
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
