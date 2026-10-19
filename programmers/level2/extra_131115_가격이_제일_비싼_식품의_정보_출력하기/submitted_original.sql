SELECT PRODUCT_ID, PRODUCT_NAME, PRODUCT_CD, CATEGORY, PRICE
FROM FOOD_PRODUCT
WHERE PRICE = (SELECT MAX(PRICE) FROM FOOD_PRODUCT)

-- 전체 코드 줄별 설명
-- SELECT PRODUCT_ID, PRODUCT_NAME, PRODUCT_CD, CATEGORY, PRICE  -- SELECT는 최고가 식품의 다섯 정보를 원래 행에서 출력.
-- FROM FOOD_PRODUCT  -- FROM은 식품 테이블 조회.
-- WHERE PRICE = (SELECT MAX(PRICE) FROM FOOD_PRODUCT)  -- WHERE는 행 조건. 괄호 안 하위 쿼리의 MAX로 최고 가격을 구한 뒤 같은 가격의 식품 행을 선택.

-- 풀이 요약
-- MAX(PRICE)만 출력하면 식품 이름·ID가 사라진다. 최대 가격을 하위 쿼리로 구하고 바깥에서 그 가격인 원래 행을 찾는다.
-- 최고 가격이 같은 식품이 여러 개라면 모두 선택되는 구조다. 가격 NULL은 MAX에서 제외된다.
-- 