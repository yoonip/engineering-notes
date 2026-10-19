-- 점(.)은 식당 테이블 r의 열 지정.
SELECT r.FOOD_TYPE, r.REST_ID, r.REST_NAME, r.FAVORITES
-- FROM은 테이블, AS r은 별칭.
FROM REST_INFO AS r
-- 괄호 속 같은 음식 종류의 최대 즐겨찾기 수와 비교.
WHERE r.FAVORITES = (
    -- 해당 종류에서 가장 큰 즐겨찾기 수.
    SELECT MAX(other.FAVORITES)
    -- 같은 식당 테이블을 다른 별칭으로 조회하는 자기 비교.
    FROM REST_INFO AS other
    -- 같은 음식 종류만 검사하며 둘 다 NULL인 종류도 같은 그룹으로 취급.
    WHERE other.FOOD_TYPE <=> r.FOOD_TYPE
)
-- 음식 종류 내림차순 정렬.
ORDER BY r.FOOD_TYPE DESC
