-- 과자·국·김치·식용유 분류의 최고가 상품을 구하고 가격 내림차순으로 출력합니다.
-- 각 상품의 가격을 같은 분류의 MAX 가격과 비교합니다. 가격 동률이 있다면 최댓값과 같은 행을 모두 보존합니다.
SELECT p.CATEGORY, p.PRICE AS MAX_PRICE, p.PRODUCT_NAME
FROM FOOD_PRODUCT AS p
WHERE p.CATEGORY IN ('과자', '국', '김치', '식용유')
  AND p.PRICE = (
      SELECT MAX(q.PRICE) FROM FOOD_PRODUCT AS q
      WHERE q.CATEGORY = p.CATEGORY
  )
ORDER BY p.PRICE DESC
