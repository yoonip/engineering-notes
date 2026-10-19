SELECT p.PRODUCT_CODE, SUM(p.PRICE * s.SALES_AMOUNT) AS SALES
FROM PRODUCT AS p
JOIN OFFLINE_SALE AS s ON s.PRODUCT_ID = p.PRODUCT_ID
GROUP BY p.PRODUCT_CODE
ORDER BY SALES DESC, p.PRODUCT_CODE

-- 전체 코드 줄별 설명
-- SELECT p.PRODUCT_CODE, SUM(p.PRICE * s.SALES_AMOUNT) AS SALES  -- SELECT는 상품코드·매출 출력. *는 곱셈, SUM은 기록별 매출 합계, AS는 별칭.
-- FROM PRODUCT AS p  -- 상품 정보 테이블 별칭 p.
-- JOIN OFFLINE_SALE AS s ON s.PRODUCT_ID = p.PRODUCT_ID  -- JOIN·ON으로 상품 ID가 같은 판매 기록 연결.
-- GROUP BY p.PRODUCT_CODE  -- 상품코드별 판매 기록 묶기.
-- ORDER BY SALES DESC, p.PRODUCT_CODE  -- 매출 내림차순, 같은 매출이면 상품코드 기본 오름차순.

-- 풀이 요약
-- 상품 가격과 판매 기록 수량을 연결해 가격×수량의 합계를 구한다.
-- SUM(가격)이나 COUNT(판매 기록)만 사용하면 수량이 반영되지 않는다. 매출 동점에는 상품코드 오름차순이다.
-- 