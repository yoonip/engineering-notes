-- 점(.)은 테이블 별칭의 열을 지정.
SELECT f.ID, names.FISH_NAME, f.LENGTH
FROM FISH_INFO AS f
-- JOIN·ON은 같은 종류 번호를 가진 이름 정보를 연결.
JOIN FISH_NAME_INFO AS names ON names.FISH_TYPE = f.FISH_TYPE
WHERE f.LENGTH = (
    -- 같은 종류의 최대 길이 계산.
    SELECT MAX(other.LENGTH)
    FROM FISH_INFO AS other
    -- 바깥 행 f의 종류만 검사하는 상관 하위 쿼리.
    WHERE other.FISH_TYPE = f.FISH_TYPE
)
ORDER BY f.ID
