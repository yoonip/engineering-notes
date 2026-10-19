# 흉부외과 또는 일반외과 의사 목록 출력하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/132203) · Level 1 · MySQL

## 풀이

진료과가 CS나 GS인 의사를 고르고 고용일·이름 순으로 정렬합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.sql) · [채점 기록 / Grade](grading.json)

```sql
SELECT DR_NAME, DR_ID, MCDP_CD, DATE_FORMAT(HIRE_YMD, '%Y-%m-%d') AS HIRE_YMD
FROM DOCTOR
WHERE MCDP_CD IN ('CS', 'GS')
ORDER BY HIRE_YMD DESC, DR_NAME ASC

-- 전체 코드 줄별 설명
-- SELECT DR_NAME, DR_ID, MCDP_CD, DATE_FORMAT(HIRE_YMD, '%Y-%m-%d') AS HIRE_YMD  -- SELECT는 출력 열 선택. DATE_FORMAT은 연-월-일 형식 변환, AS는 별칭.
-- FROM DOCTOR  -- FROM은 의사 정보 테이블 지정.
-- WHERE MCDP_CD IN ('CS', 'GS')  -- WHERE는 필터. IN은 목록 중 하나와 같은지 검사. 흉부외과 또는 일반외과 선택.
-- ORDER BY HIRE_YMD DESC, DR_NAME ASC  -- ORDER BY는 정렬. DESC는 고용일 내림차순, 같으면 ASC로 이름 오름차순.

-- 풀이 요약
-- 진료과가 CS나 GS인 의사를 고르고 고용일·이름 순으로 정렬합니다.
--
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
