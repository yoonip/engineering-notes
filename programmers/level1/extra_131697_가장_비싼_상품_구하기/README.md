# 가장 비싼 상품 구하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/131697) · Level 1 · MySQL

## 풀이

전체 상품 가격에서 최댓값 하나를 구합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.sql) · [채점 기록 / Grade](grading.json)

```sql
SELECT MAX(PRICE) AS MAX_PRICE
FROM PRODUCT

-- 전체 코드 줄별 설명
-- SELECT MAX(PRICE) AS MAX_PRICE  -- SELECT는 조회, MAX는 최댓값 집계, AS는 출력 열 이름 지정.
-- FROM PRODUCT  -- FROM은 상품 테이블 지정.

-- 풀이 요약
-- 전체 상품 가격에서 최댓값 하나를 구합니다.
--
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
