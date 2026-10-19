SELECT FLAVOR
FROM (
    SELECT FLAVOR, TOTAL_ORDER FROM FIRST_HALF
    UNION ALL
    SELECT FLAVOR, TOTAL_ORDER FROM JULY
) AS orders
GROUP BY FLAVOR
ORDER BY SUM(TOTAL_ORDER) DESC
LIMIT 3

-- 전체 코드 줄별 설명
-- SELECT FLAVOR  -- SELECT는 출력 열 선택. 주문량 상위 아이스크림 맛을 출력.
-- FROM (  -- FROM 안의 하위 쿼리로 합쳐진 주문 기록을 조회.
--     SELECT FLAVOR, TOTAL_ORDER FROM FIRST_HALF  -- 상반기 맛과 총주문량 선택.
--     UNION ALL  -- UNION ALL은 중복을 제거하지 않고 두 결과의 행을 이어 붙임.
--     SELECT FLAVOR, TOTAL_ORDER FROM JULY  -- 7월 맛과 주문량 선택. 같은 맛의 여러 출하 기록도 모두 유지.
-- ) AS orders  -- 하위 쿼리 결과에 orders라는 별명을 지정.
-- GROUP BY FLAVOR  -- GROUP BY는 같은 맛끼리 묶어 집계.
-- ORDER BY SUM(TOTAL_ORDER) DESC  -- SUM은 합계, DESC는 내림차순. 상반기+7월 총주문량이 큰 순서 정렬.
-- LIMIT 3  -- LIMIT는 출력 행 수 제한. 상위 세 맛만 반환.

-- 풀이 요약
-- 두 기간의 주문 기록을 UNION ALL로 합쳐 맛별 합계를 계산하면 조인으로 상반기 주문량이 중복 합산되는 일을 피할 수 있습니다.
-- 예: 상반기 100, 7월 출하 두 건이 30·40이면 합계는 170입니다.
-- 