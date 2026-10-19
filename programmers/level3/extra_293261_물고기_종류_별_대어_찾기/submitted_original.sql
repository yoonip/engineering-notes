SELECT f.ID, names.FISH_NAME, f.LENGTH
FROM FISH_INFO AS f
JOIN FISH_NAME_INFO AS names ON names.FISH_TYPE = f.FISH_TYPE
WHERE f.LENGTH = (
    SELECT MAX(other.LENGTH)
    FROM FISH_INFO AS other
    WHERE other.FISH_TYPE = f.FISH_TYPE
)
ORDER BY f.ID

-- 전체 코드 줄별 설명
-- SELECT f.ID, names.FISH_NAME, f.LENGTH  -- SELECT는 출력 열 선택. 점(.)은 테이블 별칭의 열을 지정.
-- FROM FISH_INFO AS f  -- FROM은 물고기 정보 테이블, AS f는 짧은 별칭.
-- JOIN FISH_NAME_INFO AS names ON names.FISH_TYPE = f.FISH_TYPE  -- JOIN·ON은 같은 종류 번호를 가진 이름 정보를 연결.
-- WHERE f.LENGTH = (  -- WHERE는 행 조건. 괄호 안 하위 쿼리의 최대 길이와 같은 물고기 선택.
--     SELECT MAX(other.LENGTH)  -- MAX는 최댓값. 같은 종류의 최대 길이 계산.
--     FROM FISH_INFO AS other  -- 같은 테이블을 다른 별칭으로 다시 조회.
--     WHERE other.FISH_TYPE = f.FISH_TYPE  -- 바깥 행 f의 종류만 검사하는 상관 하위 쿼리.
-- )  -- 하위 쿼리 괄호 종료.
-- ORDER BY f.ID  -- 물고기 ID 오름차순 정렬.

-- 풀이 요약
-- 각 물고기의 길이가 자기 종류의 최대 길이와 같은지 비교하고 종류 이름을 조인한다.
-- 종류별 최대는 한 마리라는 조건이 있으므로 한 종류마다 한 행이 선택된다. 최대가 아닌 행의 이름이나 ID를 GROUP BY만으로 임의 선택하지 않는다.
-- 