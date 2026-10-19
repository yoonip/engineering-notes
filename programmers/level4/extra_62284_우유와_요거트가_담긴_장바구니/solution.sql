-- Milk와 Yogurt를 둘 다 담은 장바구니 ID를 중복 없이 오름차순으로 구합니다. 같은 제품이 여러 번 있어도 종류는 한 번만 셉니다.
-- 두 제품만 남기고 장바구니별 서로 다른 NAME의 수가 2인지 확인합니다.
SELECT CART_ID
FROM CART_PRODUCTS
WHERE NAME IN ('Milk', 'Yogurt')
GROUP BY CART_ID
HAVING COUNT(DISTINCT NAME) = 2
ORDER BY CART_ID
