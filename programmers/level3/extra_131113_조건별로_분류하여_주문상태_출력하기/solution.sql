-- %Y는 네 자리 연도, %m·%d는 두 자리 월·일.
SELECT ORDER_ID, PRODUCT_ID, DATE_FORMAT(OUT_DATE, '%Y-%m-%d') AS OUT_DATE,
       CASE
           -- NULL은 일반 = 비교로 판정하지 않음.
           WHEN OUT_DATE IS NULL THEN '출고미정'
           -- 기준일 당일까지 출고된 주문.
           WHEN OUT_DATE <= '2022-05-01' THEN '출고완료'
           -- 기준일보다 늦은 예정 출고.
           ELSE '출고대기'
       -- AS는 출력 이름, 백틱은 한글 식별자를 감쌈.
       END AS `출고여부`
-- 주문 테이블 조회.
FROM FOOD_ORDER
-- 주문 ID 오름차순 정렬.
ORDER BY ORDER_ID
