# 어린 동물 찾기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/59037) · Level 1 · MySQL

## 풀이

문제 각주에서 젊은 동물은 INTAKE_CONDITION이 Aged가 아닌 경우로 정의합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.sql) · [채점 기록 / Grade](grading.json)

```sql
SELECT ANIMAL_ID, NAME
FROM ANIMAL_INS
WHERE INTAKE_CONDITION <> 'Aged'
ORDER BY ANIMAL_ID

-- 전체 코드 줄별 설명
-- SELECT ANIMAL_ID, NAME  -- SELECT는 출력 열 선택. 동물 ID와 이름 조회.
-- FROM ANIMAL_INS  -- FROM은 동물 입소 정보 테이블 지정.
-- WHERE INTAKE_CONDITION <> 'Aged'  -- WHERE는 조건 필터, <>는 같지 않음. 문제의 젊은 동물 정의에 따라 Aged가 아닌 상태 선택.
-- ORDER BY ANIMAL_ID  -- ORDER BY는 동물 ID 오름차순 정렬.

-- 풀이 요약
-- 문제 각주에서 젊은 동물은 INTAKE_CONDITION이 Aged가 아닌 경우로 정의합니다.
--
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
