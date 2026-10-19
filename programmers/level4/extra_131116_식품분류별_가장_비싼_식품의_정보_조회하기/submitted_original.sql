SELECT p.CATEGORY, p.PRICE AS MAX_PRICE, p.PRODUCT_NAME
FROM FOOD_PRODUCT AS p
WHERE p.CATEGORY IN ('과자', '국', '김치', '식용유')
  AND p.PRICE = (
      SELECT MAX(q.PRICE) FROM FOOD_PRODUCT AS q
      WHERE q.CATEGORY = p.CATEGORY
  )
ORDER BY p.PRICE DESC

-- 전체 코드 줄별 설명
-- SELECT p.CATEGORY, p.PRICE AS MAX_PRICE, p.PRODUCT_NAME  -- SELECT는 분류·가격·이름 출력. AS로 최고가 열 이름 지정.
-- FROM FOOD_PRODUCT AS p  -- 식품 테이블을 p라는 별명으로 조회.
-- WHERE p.CATEGORY IN ('과자', '국', '김치', '식용유')  -- WHERE는 필터, IN은 목록에 속하는지 검사. 지정한 네 분류만 선택.
--   AND p.PRICE = (  -- AND는 조건 추가. 현재 식품의 가격이 같은 분류의 최고가인지 확인.
--       SELECT MAX(q.PRICE) FROM FOOD_PRODUCT AS q  -- MAX는 최댓값. 식품 테이블을 별명 q로 다시 조회.
--       WHERE q.CATEGORY = p.CATEGORY  -- 바깥 행과 같은 분류만 검사하는 상관 하위 쿼리.
--   )  -- 최고가 조회 하위 쿼리 종료.
-- ORDER BY p.PRICE DESC  -- DESC는 내림차순. 가격이 높은 식품부터 출력.

-- 풀이 요약
-- 분류별 최고가와 현재 식품 가격을 비교하여 해당하는 식품 이름을 정확히 선택합니다.
-- 단순 GROUP BY에서 이름을 임의로 선택하면 최고가 식품의 이름과 다를 수 있으므로 가격 조건으로 행을 고릅니다.
-- 