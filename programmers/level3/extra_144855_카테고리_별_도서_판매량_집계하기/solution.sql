-- SUM은 판매량 합산, AS는 집계 열 별칭.
SELECT b.CATEGORY, SUM(s.SALES) AS TOTAL_SALES
-- BOOK을 b라는 별칭으로 조회해 카테고리 정보 사용.
FROM BOOK AS b
-- JOIN·ON으로 도서 ID가 같은 판매 기록 연결.
JOIN BOOK_SALES AS s ON s.BOOK_ID = b.BOOK_ID
-- 2022년 1월 판매 기록만 포함.
WHERE s.SALES_DATE >= '2022-01-01' AND s.SALES_DATE < '2022-02-01'
-- 카테고리별로 묶어 해당 도서들의 판매량을 합산.
GROUP BY b.CATEGORY
-- 카테고리명 오름차순 정렬.
ORDER BY b.CATEGORY
