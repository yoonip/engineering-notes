SELECT LEFT(PRODUCT_CODE, 2) AS CATEGORY, COUNT(*) AS PRODUCTS
FROM PRODUCT
GROUP BY CATEGORY
ORDER BY CATEGORY

-- 전체 코드 줄별 설명
-- SELECT LEFT(PRODUCT_CODE, 2) AS CATEGORY, COUNT(*) AS PRODUCTS  -- SELECT는 출력 열. LEFT(문자열,길이)는 앞 두 글자 추출, COUNT(*)는 상품 수, AS는 별칭.
-- FROM PRODUCT  -- 상품 테이블 조회.
-- GROUP BY CATEGORY  -- 같은 앞 두 글자 카테고리로 묶어 집계.
-- ORDER BY CATEGORY  -- 카테고리 코드 오름차순 정렬.

-- 풀이 요약
-- 전체 상품코드가 아니라 앞 두 글자가 같은 상품을 한 카테고리로 묶는다.
-- 코드를 숫자로 바꾸지 않고 문자열로 추출하므로 01처럼 앞에 0이 붙은 코드도 유지된다.
-- 