SELECT p.PRODUCT_ID, p.PRODUCT_NAME, SUM(p.PRICE * o.AMOUNT) AS TOTAL_SALES
FROM FOOD_PRODUCT AS p
JOIN FOOD_ORDER AS o ON p.PRODUCT_ID = o.PRODUCT_ID
WHERE o.PRODUCE_DATE >= '2022-05-01' AND o.PRODUCE_DATE < '2022-06-01'
GROUP BY p.PRODUCT_ID, p.PRODUCT_NAME
ORDER BY TOTAL_SALES DESC, p.PRODUCT_ID ASC

-- 전체 코드 줄별 설명
-- SELECT p.PRODUCT_ID, p.PRODUCT_NAME, SUM(p.PRICE * o.AMOUNT) AS TOTAL_SALES  -- SELECT는 출력 열 선택. SUM으로 가격×주문량을 합산하여 총매출 계산.
-- FROM FOOD_PRODUCT AS p  -- 식품 정보 테이블에 p 별명 지정.
-- JOIN FOOD_ORDER AS o ON p.PRODUCT_ID = o.PRODUCT_ID  -- JOIN으로 같은 식품 ID의 주문 기록 연결.
-- WHERE o.PRODUCE_DATE >= '2022-05-01' AND o.PRODUCE_DATE < '2022-06-01'  -- WHERE와 AND로 생산일이 2022년 5월인 주문만 선택.
-- GROUP BY p.PRODUCT_ID, p.PRODUCT_NAME  -- GROUP BY로 식품별 주문을 묶어 총매출 합산.
-- ORDER BY TOTAL_SALES DESC, p.PRODUCT_ID ASC  -- DESC는 내림차순, ASC는 오름차순. 매출이 같으면 식품 ID가 작은 순서.

-- 풀이 요약
-- 주문일·출고일이 아니라 생산일자를 기준으로 5월 주문을 골라 식품별 가격×수량을 합산합니다.
-- 예: 가격 2000원인 식품의 5월 생산 주문이 10개·20개라면 총매출은 6만원입니다.
-- 