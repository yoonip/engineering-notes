# 12세 이하인 여자 환자 목록 출력하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/132201) · Level 1 · MySQL

## 풀이

여성 코드 W와 나이 조건을 함께 적용하고 없는 전화번호만 NONE으로 바꿉니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.sql) · [채점 기록 / Grade](grading.json)

```sql
SELECT PT_NAME, PT_NO, GEND_CD, AGE, IFNULL(TLNO, 'NONE') AS TLNO
FROM PATIENT
WHERE AGE <= 12 AND GEND_CD = 'W'
ORDER BY AGE DESC, PT_NAME ASC

-- 전체 코드 줄별 설명
-- SELECT PT_NAME, PT_NO, GEND_CD, AGE, IFNULL(TLNO, 'NONE') AS TLNO  -- SELECT는 열 조회. IFNULL(값,대체값)은 전화번호가 NULL일 때 NONE 반환. AS는 별칭.
-- FROM PATIENT  -- FROM은 환자 정보 테이블 지정.
-- WHERE AGE <= 12 AND GEND_CD = 'W'  -- WHERE는 조건 필터. <=는 이하, AND는 모두 만족. 12세 이하 여성 선택.
-- ORDER BY AGE DESC, PT_NAME ASC  -- ORDER BY는 정렬. 나이 내림차순, 같으면 이름 오름차순.

-- 풀이 요약
-- 여성 코드 W와 나이 조건을 함께 적용하고 없는 전화번호만 NONE으로 바꿉니다.
--
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
