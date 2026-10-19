SELECT ID, NAME, HOST_ID
FROM PLACES
WHERE HOST_ID IN (
    SELECT HOST_ID
    FROM PLACES
    GROUP BY HOST_ID
    HAVING COUNT(*) >= 2
)
ORDER BY ID

-- 전체 코드 줄별 설명
-- SELECT ID, NAME, HOST_ID  -- SELECT는 공간 ID·이름·소유자 ID 열을 출력.
-- FROM PLACES  -- FROM은 공간 테이블 지정.
-- WHERE HOST_ID IN (  -- WHERE는 행 조건, IN은 목록 포함 여부. 헤비 유저의 모든 공간을 선택.
--     SELECT HOST_ID  -- 하위 쿼리에서 헤비 유저의 ID 반환.
--     FROM PLACES  -- 공간 등록 정보를 조회.
--     GROUP BY HOST_ID  -- 소유자별 공간을 묶음.
--     HAVING COUNT(*) >= 2  -- HAVING은 집계 후 조건. COUNT(*)는 공간 수, >=는 이상.
-- )  -- 하위 쿼리 종료.
-- ORDER BY ID  -- 공간 ID 오름차순 정렬.

-- 풀이 요약
-- 소유자별 등록 수가 둘 이상인 HOST_ID를 찾고, 바깥 쿼리에서 그 소유자의 원래 공간 행들을 조회한다.
-- 소유자당 한 행만 출력하는 것이 아니라 해당 소유자의 모든 공간 정보를 ID순으로 출력해야 한다.
-- 