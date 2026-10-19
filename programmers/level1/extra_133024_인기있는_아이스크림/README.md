# 인기있는 아이스크림

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/133024) · Level 1 · MySQL

## 풀이

주문량이 같을 때의 두 번째 정렬 기준도 함께 지정합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.sql) · [채점 기록 / Grade](grading.json)

```sql
SELECT FLAVOR
FROM FIRST_HALF
ORDER BY TOTAL_ORDER DESC, SHIPMENT_ID ASC

-- 전체 코드 줄별 설명
-- SELECT FLAVOR  -- SELECT는 출력 열 선택. 아이스크림 맛만 조회.
-- FROM FIRST_HALF  -- FROM은 상반기 주문 테이블 지정.
-- ORDER BY TOTAL_ORDER DESC, SHIPMENT_ID ASC  -- ORDER BY는 정렬. DESC는 주문량 내림차순, 동률일 때 ASC로 출하 번호 오름차순.

-- 풀이 요약
-- 주문량이 같을 때의 두 번째 정렬 기준도 함께 지정합니다.
--
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
