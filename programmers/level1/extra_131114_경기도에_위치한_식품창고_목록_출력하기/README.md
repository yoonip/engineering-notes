# 경기도에 위치한 식품창고 목록 출력하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/131114) · Level 1 · MySQL

## 풀이

주소의 시작이 경기도인 창고를 고르고 냉동시설 정보가 없으면 N으로 표시합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.sql) · [채점 기록 / Grade](grading.json)

```sql
SELECT WAREHOUSE_ID, WAREHOUSE_NAME, ADDRESS, IFNULL(FREEZER_YN, 'N') AS FREEZER_YN
FROM FOOD_WAREHOUSE
WHERE ADDRESS LIKE '경기도%'
ORDER BY WAREHOUSE_ID

-- 전체 코드 줄별 설명
-- SELECT WAREHOUSE_ID, WAREHOUSE_NAME, ADDRESS, IFNULL(FREEZER_YN, 'N') AS FREEZER_YN  -- SELECT는 열 조회. IFNULL은 NULL을 N으로 대체, AS는 출력 열 별칭.
-- FROM FOOD_WAREHOUSE  -- FROM은 식품창고 정보 테이블 지정.
-- WHERE ADDRESS LIKE '경기도%'  -- WHERE는 필터, LIKE는 패턴 검사. %는 뒤에 임의 문자열 허용. 경기도로 시작하는 주소 선택.
-- ORDER BY WAREHOUSE_ID  -- ORDER BY는 정렬. 기본 ASC로 창고 ID 오름차순.

-- 풀이 요약
-- 주소의 시작이 경기도인 창고를 고르고 냉동시설 정보가 없으면 N으로 표시합니다.
--
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
