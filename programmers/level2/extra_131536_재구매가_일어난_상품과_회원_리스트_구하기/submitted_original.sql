SELECT USER_ID, PRODUCT_ID
FROM ONLINE_SALE
GROUP BY USER_ID, PRODUCT_ID
HAVING COUNT(*) >= 2
ORDER BY USER_ID, PRODUCT_ID DESC

-- 전체 코드 줄별 설명
-- SELECT USER_ID, PRODUCT_ID  -- SELECT는 회원 ID·상품 ID 열 출력.
-- FROM ONLINE_SALE  -- 온라인 판매 기록 테이블 조회.
-- GROUP BY USER_ID, PRODUCT_ID  -- GROUP BY는 같은 회원·같은 상품의 구매 기록을 한 그룹으로 묶음.
-- HAVING COUNT(*) >= 2  -- HAVING은 집계 조건, COUNT(*)는 구매 기록 수. 두 번 이상 기록이 있으면 재구매.
-- ORDER BY USER_ID, PRODUCT_ID DESC  -- 회원 ID 오름차순, 같은 회원이면 상품 ID 내림차순 정렬.

-- 풀이 요약
-- 재구매는 같은 사용자가 같은 상품을 두 번 이상 산 경우다. 두 열을 함께 그룹화해야 한다.
-- 한 번에 수량을 여러 개 산 것과 재구매는 다르므로 판매량 SUM이 아니라 구매 기록 COUNT를 검사한다.
-- 