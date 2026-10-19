-- SELECT는 공간 ID·이름·소유자 ID 열을 출력.
SELECT ID, NAME, HOST_ID
-- 공간 등록 정보를 조회.
FROM PLACES
-- 헤비 유저의 모든 공간을 선택.
WHERE HOST_ID IN (
    -- 하위 쿼리에서 헤비 유저의 ID 반환.
    SELECT HOST_ID
    -- 공간 등록 정보를 조회.
    FROM PLACES
    -- 소유자별 공간을 묶음.
    GROUP BY HOST_ID
    -- COUNT(*)는 공간 수, >=는 이상.
    HAVING COUNT(*) >= 2
)
-- 공간 ID 오름차순 정렬.
ORDER BY ID
