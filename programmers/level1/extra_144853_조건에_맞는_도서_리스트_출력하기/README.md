# 조건에 맞는 도서 리스트 출력하기

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/144853) · Level 1 · MySQL

## 풀이

카테고리와 출판 연도 조건을 동시에 적용하고 출판일 순으로 정렬합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.sql) · [채점 기록 / Grade](grading.json)

```sql
SELECT BOOK_ID, DATE_FORMAT(PUBLISHED_DATE, '%Y-%m-%d') AS PUBLISHED_DATE
FROM BOOK
WHERE CATEGORY = '인문'
  AND PUBLISHED_DATE >= '2021-01-01' AND PUBLISHED_DATE < '2022-01-01'
ORDER BY PUBLISHED_DATE

-- 전체 코드 줄별 설명
-- SELECT BOOK_ID, DATE_FORMAT(PUBLISHED_DATE, '%Y-%m-%d') AS PUBLISHED_DATE  -- SELECT는 조회, DATE_FORMAT은 연-월-일 형식 지정, AS는 출력 열 별칭.
-- FROM BOOK  -- FROM은 도서 정보 테이블 지정.
-- WHERE CATEGORY = '인문'  -- WHERE는 필터, =은 같음 비교. 인문 도서 선택.
--   AND PUBLISHED_DATE >= '2021-01-01' AND PUBLISHED_DATE < '2022-01-01'  -- AND는 모두 만족. 2021년에 출판된 도서로 범위 제한.
-- ORDER BY PUBLISHED_DATE  -- ORDER BY는 정렬. 출판일 오름차순 출력.

-- 풀이 요약
-- 카테고리와 출판 연도 조건을 동시에 적용하고 출판일 순으로 정렬합니다.
--
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
