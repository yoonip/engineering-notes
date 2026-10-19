SELECT b.CATEGORY, SUM(s.SALES) AS TOTAL_SALES
FROM BOOK AS b
JOIN BOOK_SALES AS s ON s.BOOK_ID = b.BOOK_ID
WHERE s.SALES_DATE >= '2022-01-01' AND s.SALES_DATE < '2022-02-01'
GROUP BY b.CATEGORY
ORDER BY b.CATEGORY

-- 전체 코드 줄별 설명
-- SELECT b.CATEGORY, SUM(s.SALES) AS TOTAL_SALES  -- SELECT는 출력 열 선택. SUM은 판매량 합산, AS는 집계 열 별칭.
-- FROM BOOK AS b  -- BOOK을 b라는 별칭으로 조회해 카테고리 정보 사용.
-- JOIN BOOK_SALES AS s ON s.BOOK_ID = b.BOOK_ID  -- JOIN·ON으로 도서 ID가 같은 판매 기록 연결.
-- WHERE s.SALES_DATE >= '2022-01-01' AND s.SALES_DATE < '2022-02-01'  -- WHERE는 집계 전 필터, AND는 모두 참. 2022년 1월 판매 기록만 포함.
-- GROUP BY b.CATEGORY  -- 카테고리별로 묶어 해당 도서들의 판매량을 합산.
-- ORDER BY b.CATEGORY  -- 카테고리명 오름차순 정렬.

-- 풀이 요약
-- 도서에서 카테고리, 판매 테이블에서 판매량·판매일을 가져와 조인한다. 판매일이 2022년 1월인 기록만 합산한다.
-- 판매 기록 행 수를 세는 COUNT가 아니라 각 행의 SALES를 SUM해야 한다. 출판일은 이 문제의 날짜 필터가 아니다.
-- 