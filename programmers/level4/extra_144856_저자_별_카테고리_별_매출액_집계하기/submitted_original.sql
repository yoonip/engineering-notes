SELECT a.AUTHOR_ID, a.AUTHOR_NAME, b.CATEGORY,
       SUM(s.SALES * b.PRICE) AS TOTAL_SALES
FROM BOOK AS b
JOIN AUTHOR AS a ON b.AUTHOR_ID = a.AUTHOR_ID
JOIN BOOK_SALES AS s ON b.BOOK_ID = s.BOOK_ID
WHERE s.SALES_DATE >= '2022-01-01' AND s.SALES_DATE < '2022-02-01'
GROUP BY a.AUTHOR_ID, a.AUTHOR_NAME, b.CATEGORY
ORDER BY a.AUTHOR_ID ASC, b.CATEGORY DESC

-- 전체 코드 줄별 설명
-- SELECT a.AUTHOR_ID, a.AUTHOR_NAME, b.CATEGORY,  -- SELECT는 결과 열 선택. 저자 식별자·이름과 도서 카테고리 출력.
--        SUM(s.SALES * b.PRICE) AS TOTAL_SALES  -- SUM은 합계. 판매량×판매가를 합산하고 AS로 결과 열 이름 지정.
-- FROM BOOK AS b  -- 도서 테이블에 b라는 별명 지정.
-- JOIN AUTHOR AS a ON b.AUTHOR_ID = a.AUTHOR_ID  -- JOIN으로 해당 도서의 저자 연결.
-- JOIN BOOK_SALES AS s ON b.BOOK_ID = s.BOOK_ID  -- 도서 ID가 같은 날짜별 판매량을 연결.
-- WHERE s.SALES_DATE >= '2022-01-01' AND s.SALES_DATE < '2022-02-01'  -- WHERE와 AND로 2022년 1월 판매 기록만 선택.
-- GROUP BY a.AUTHOR_ID, a.AUTHOR_NAME, b.CATEGORY  -- GROUP BY는 묶음별 집계. 같은 저자의 같은 카테고리 매출을 합침.
-- ORDER BY a.AUTHOR_ID ASC, b.CATEGORY DESC  -- ASC는 오름차순, DESC는 내림차순. 저자 ID 우선 정렬.

-- 풀이 요약
-- 도서→저자→판매 기록을 연결하고 1월 판매만 남겨 저자·카테고리별로 금액을 합산합니다.
-- 예: 같은 저자의 경제 도서 두 권이 각각 1만원×2권, 2만원×3권 판매되면 총매출 8만원입니다.
-- 