SELECT CART_ID
FROM CART_PRODUCTS
WHERE NAME IN ('Milk', 'Yogurt')
GROUP BY CART_ID
HAVING COUNT(DISTINCT NAME) = 2
ORDER BY CART_ID

-- 전체 코드 줄별 설명
-- SELECT CART_ID  -- SELECT는 출력 열 선택. 조건에 맞는 장바구니 ID 출력.
-- FROM CART_PRODUCTS  -- 장바구니별 상품 기록 조회.
-- WHERE NAME IN ('Milk', 'Yogurt')  -- WHERE는 필터, IN은 목록 포함 검사. 우유·요거트 기록만 남김.
-- GROUP BY CART_ID  -- GROUP BY로 같은 장바구니의 상품들을 묶음.
-- HAVING COUNT(DISTINCT NAME) = 2  -- HAVING은 집계 후 조건. DISTINCT로 중복 상품을 제거했을 때 두 종류가 모두 있는지 검사.
-- ORDER BY CART_ID  -- ORDER BY는 정렬. 장바구니 ID 오름차순.

-- 풀이 요약
-- 우유·요거트만 남긴 뒤 장바구니별 서로 다른 상품 종류가 두 개이면 둘 다 구매한 장바구니입니다.
-- 예: 우유만 두 개 담은 경우 DISTINCT로 한 종류만 계산되어 제외됩니다.
-- 