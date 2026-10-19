SELECT ORDER_ID, PRODUCT_ID, DATE_FORMAT(OUT_DATE, '%Y-%m-%d') AS OUT_DATE,
       CASE
           WHEN OUT_DATE IS NULL THEN '출고미정'
           WHEN OUT_DATE <= '2022-05-01' THEN '출고완료'
           ELSE '출고대기'
       END AS `출고여부`
FROM FOOD_ORDER
ORDER BY ORDER_ID

-- 전체 코드 줄별 설명
-- SELECT ORDER_ID, PRODUCT_ID, DATE_FORMAT(OUT_DATE, '%Y-%m-%d') AS OUT_DATE,  -- SELECT는 출력 열 선택. DATE_FORMAT은 날짜 표시 형식 지정. %Y는 네 자리 연도, %m·%d는 두 자리 월·일.
--        CASE  -- CASE는 조건에 따라 값 선택.
--            WHEN OUT_DATE IS NULL THEN '출고미정'  -- IS NULL은 값이 미정인지 검사. NULL은 일반 = 비교로 판정하지 않음.
--            WHEN OUT_DATE <= '2022-05-01' THEN '출고완료'  -- <=는 이하. 기준일 당일까지 출고된 주문.
--            ELSE '출고대기'  -- ELSE는 나머지 조건. 기준일보다 늦은 예정 출고.
--        END AS `출고여부`  -- END는 CASE 종료. AS는 출력 이름, 백틱은 한글 식별자를 감쌈.
-- FROM FOOD_ORDER  -- 주문 테이블 조회.
-- ORDER BY ORDER_ID  -- 주문 ID 오름차순 정렬.

-- 풀이 요약
-- 출고일이 NULL이면 미정, 2022-05-01 이하면 완료, 그 뒤면 대기로 분류한다. 날짜 출력은 연-월-일 형식을 명시한다.
-- 필터로 주문을 제거하는 문제가 아니라 모든 주문에 상태 열을 붙이는 문제이므로 WHERE를 쓰지 않는다.
-- 