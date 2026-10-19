SELECT FLOOR(PRICE / 10000) * 10000 AS PRICE_GROUP, COUNT(*) AS PRODUCTS
FROM PRODUCT
GROUP BY PRICE_GROUP
ORDER BY PRICE_GROUP

-- 전체 코드 줄별 설명
-- SELECT FLOOR(PRICE / 10000) * 10000 AS PRICE_GROUP, COUNT(*) AS PRODUCTS  -- SELECT는 출력 열. /는 나눗셈, FLOOR는 내림, *는 곱셈. 만원 미만을 버린 구간 시작값 생성. COUNT(*)는 상품 수, AS는 별칭.
-- FROM PRODUCT  -- 상품 정보 테이블 조회.
-- GROUP BY PRICE_GROUP  -- 같은 가격 구간으로 묶음. MySQL은 GROUP BY에서 SELECT 별칭 사용 가능.
-- ORDER BY PRICE_GROUP  -- 가격 구간 시작값 오름차순 정렬.

-- 풀이 요약
-- 가격을 10000으로 나누어 내림한 뒤 다시 10000을 곱하면 만원 단위 구간의 최솟값을 얻는다.
-- 예: 19999원은 10000 구간, 20000원은 20000 구간이다. 반올림 ROUND가 아니라 내림 FLOOR를 써야 한다.
-- 