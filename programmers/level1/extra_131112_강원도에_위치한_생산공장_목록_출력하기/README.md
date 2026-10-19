# 강원도에 위치한 생산공장 목록 출력하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/131112) · Level 1 · MySQL

## 풀이

강원도에 위치한 공장을 주소의 앞부분으로 골라냅니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.sql) · [채점 기록 / Grade](grading.json)

```sql
SELECT FACTORY_ID, FACTORY_NAME, ADDRESS
FROM FOOD_FACTORY
WHERE ADDRESS LIKE '강원도%'
ORDER BY FACTORY_ID

-- 전체 코드 줄별 설명
-- SELECT FACTORY_ID, FACTORY_NAME, ADDRESS  -- SELECT는 출력 열 지정. 공장 ID·이름·주소 조회.
-- FROM FOOD_FACTORY  -- FROM은 식품공장 정보 테이블 지정.
-- WHERE ADDRESS LIKE '강원도%'  -- WHERE는 필터, LIKE는 패턴 비교, %는 임의 길이 문자열. 강원도로 시작하는 주소 선택.
-- ORDER BY FACTORY_ID  -- ORDER BY는 정렬. 공장 ID 오름차순 출력.

-- 풀이 요약
-- 강원도에 위치한 공장을 주소의 앞부분으로 골라냅니다.
--
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
