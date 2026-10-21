# 특정 옵션이 포함된 자동차 리스트 구하기

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/157343) · Level 1 · MySQL

## 풀이

옵션 문자열에 네비게이션이 포함된 자동차만 고릅니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.sql) · [채점 기록 / Grade](grading.json)

```sql
SELECT CAR_ID, CAR_TYPE, DAILY_FEE, OPTIONS
FROM CAR_RENTAL_COMPANY_CAR
WHERE OPTIONS LIKE '%네비게이션%'
ORDER BY CAR_ID DESC

-- 전체 코드 줄별 설명
-- SELECT CAR_ID, CAR_TYPE, DAILY_FEE, OPTIONS  -- SELECT는 출력 열 선택. 자동차 정보의 모든 열 조회.
-- FROM CAR_RENTAL_COMPANY_CAR  -- FROM은 자동차 정보 테이블 지정.
-- WHERE OPTIONS LIKE '%네비게이션%'  -- WHERE는 필터, LIKE는 패턴 비교, %는 임의 길이 문자열. 옵션에 네비게이션 포함 여부 검사.
-- ORDER BY CAR_ID DESC  -- ORDER BY는 정렬, DESC는 내림차순. 자동차 ID가 큰 순으로 출력.

-- 풀이 요약
-- 옵션 문자열에 네비게이션이 포함된 자동차만 고릅니다.
--
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
