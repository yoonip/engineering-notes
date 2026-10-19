SELECT r.FOOD_TYPE, r.REST_ID, r.REST_NAME, r.FAVORITES
FROM REST_INFO AS r
WHERE r.FAVORITES = (
    SELECT MAX(other.FAVORITES)
    FROM REST_INFO AS other
    WHERE other.FOOD_TYPE <=> r.FOOD_TYPE
)
ORDER BY r.FOOD_TYPE DESC

-- 전체 코드 줄별 설명
-- SELECT r.FOOD_TYPE, r.REST_ID, r.REST_NAME, r.FAVORITES  -- SELECT는 출력 열 선택. 점(.)은 식당 테이블 r의 열 지정.
-- FROM REST_INFO AS r  -- FROM은 테이블, AS r은 별칭.
-- WHERE r.FAVORITES = (  -- WHERE는 행 조건. 괄호 속 같은 음식 종류의 최대 즐겨찾기 수와 비교.
--     SELECT MAX(other.FAVORITES)  -- MAX는 최댓값. 해당 종류에서 가장 큰 즐겨찾기 수.
--     FROM REST_INFO AS other  -- 같은 식당 테이블을 다른 별칭으로 조회하는 자기 비교.
--     WHERE other.FOOD_TYPE <=> r.FOOD_TYPE  -- <=>는 MySQL의 NULL 안전 동등 비교. 같은 음식 종류만 검사하며 둘 다 NULL인 종류도 같은 그룹으로 취급.
-- )  -- 상관 하위 쿼리 종료.
-- ORDER BY r.FOOD_TYPE DESC  -- 음식 종류 내림차순 정렬.

-- 풀이 요약
-- 각 행의 즐겨찾기 수를 같은 음식 종류의 최대 수와 비교해 최대인 식당의 원래 ID·이름까지 함께 가져온다.
-- GROUP BY와 MAX만 적고 ID·이름을 임의로 출력하면 최대를 가진 행의 정보와 어긋날 수 있으므로 원래 행을 조건으로 선택한다.
-- 