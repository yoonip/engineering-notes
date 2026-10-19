-- 2022년 1월 매출을 저자·카테고리별로 합산합니다. 매출은 판매량×책 가격이고 저자 ID 오름차순·카테고리 내림차순입니다.
-- 도서·저자·판매를 키로 조인하고 기간을 제한한 뒤 같은 저자·카테고리의 금액을 합칩니다.
SELECT a.AUTHOR_ID, a.AUTHOR_NAME, b.CATEGORY,
       SUM(s.SALES * b.PRICE) AS TOTAL_SALES
FROM BOOK AS b
JOIN AUTHOR AS a ON b.AUTHOR_ID = a.AUTHOR_ID
JOIN BOOK_SALES AS s ON b.BOOK_ID = s.BOOK_ID
WHERE s.SALES_DATE >= '2022-01-01' AND s.SALES_DATE < '2022-02-01'
GROUP BY a.AUTHOR_ID, a.AUTHOR_NAME, b.CATEGORY
ORDER BY a.AUTHOR_ID ASC, b.CATEGORY DESC
