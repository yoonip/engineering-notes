SELECT i.INGREDIENT_TYPE, SUM(h.TOTAL_ORDER) AS TOTAL_ORDER
FROM FIRST_HALF AS h
JOIN ICECREAM_INFO AS i ON i.FLAVOR = h.FLAVOR
GROUP BY i.INGREDIENT_TYPE
ORDER BY TOTAL_ORDER

-- 전체 코드 줄별 설명
-- SELECT i.INGREDIENT_TYPE, SUM(h.TOTAL_ORDER) AS TOTAL_ORDER  -- SELECT는 성분 타입·주문량 합계 출력. SUM은 합계, AS는 결과 열 이름.
-- FROM FIRST_HALF AS h  -- 상반기 주문 테이블을 h로 조회.
-- JOIN ICECREAM_INFO AS i ON i.FLAVOR = h.FLAVOR  -- JOIN·ON으로 같은 맛의 성분 정보 연결.
-- GROUP BY i.INGREDIENT_TYPE  -- 맛이 아니라 성분 타입별로 주문량을 묶음.
-- ORDER BY TOTAL_ORDER  -- 성분별 총주문량이 작은 순서로 오름차순 정렬.

-- 풀이 요약
-- 각 맛의 상반기 주문량에 성분 타입을 연결한 뒤 성분별 SUM을 계산한다.
-- 설탕 기반 여러 맛의 주문은 한 성분 그룹으로 합산한다. 출하 번호는 성분 연결 키가 아니므로 FLAVOR로 조인한다.
-- 