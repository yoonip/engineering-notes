WITH RECURSIVE GENERATIONS AS (
    SELECT ID, 1 AS GENERATION
    FROM ECOLI_DATA
    WHERE PARENT_ID IS NULL
    UNION ALL
    SELECT CHILD.ID, PARENT.GENERATION + 1
    FROM ECOLI_DATA AS CHILD
    JOIN GENERATIONS AS PARENT ON CHILD.PARENT_ID = PARENT.ID
)
SELECT COUNT(*) AS COUNT, G.GENERATION
FROM GENERATIONS AS G
WHERE NOT EXISTS (
    SELECT 1
    FROM ECOLI_DATA AS CHILD
    WHERE CHILD.PARENT_ID = G.ID
)
GROUP BY G.GENERATION
ORDER BY G.GENERATION

-- 전체 코드 줄별 설명
-- WITH RECURSIVE GENERATIONS AS (  -- WITH는 임시 결과에 이름을 붙임. RECURSIVE는 자기 결과를 다시 참조하는 재귀 CTE.
--     SELECT ID, 1 AS GENERATION  -- SELECT는 열 조회. AS는 별칭. 부모 없는 개체를 1세대로 지정.
--     FROM ECOLI_DATA  -- FROM은 데이터를 읽을 원본 테이블 지정.
--     WHERE PARENT_ID IS NULL  -- WHERE는 조건 필터. IS NULL은 부모 값이 없음을 검사.
--     UNION ALL  -- 두 조회 결과를 중복 제거 없이 이어 붙여 다음 세대도 누적.
--     SELECT CHILD.ID, PARENT.GENERATION + 1  -- 부모 세대에 1을 더해 자식 세대 계산. 점은 테이블 별칭의 열 접근.
--     FROM ECOLI_DATA AS CHILD  -- 원본 테이블을 CHILD라는 자식 별칭으로 사용.
--     JOIN GENERATIONS AS PARENT ON CHILD.PARENT_ID = PARENT.ID  -- JOIN·ON은 조건이 맞는 행 연결. 자식을 이미 구한 부모와 연결.
-- )  -- 괄호로 임시 결과 GENERATIONS의 정의 종료.
-- SELECT COUNT(*) AS COUNT, G.GENERATION  -- COUNT(*)는 행 개수. 세대별로 자식 없는 개체 수를 계산.
-- FROM GENERATIONS AS G  -- 앞에서 세대를 계산한 임시 결과 사용.
-- WHERE NOT EXISTS (  -- NOT EXISTS는 하위 조회 결과가 한 행도 없을 때 참. 자식 없는 개체만 선택.
--     SELECT 1  -- 존재 여부만 확인하므로 임의 상수 1 조회.
--     FROM ECOLI_DATA AS CHILD  -- 자식 후보가 있는 원본 테이블 조회.
--     WHERE CHILD.PARENT_ID = G.ID  -- 현재 개체 ID를 부모로 갖는 행이 있는지 검사.
-- )  -- 자식 존재 여부를 검사하는 하위 조회 종료.
-- GROUP BY G.GENERATION  -- GROUP BY는 같은 값을 묶음. 세대별로 COUNT를 각각 계산.
-- ORDER BY G.GENERATION  -- ORDER BY는 정렬. 기본 ASC로 세대 오름차순 정렬.

-- 풀이 요약
-- 부모 없는 개체부터 세대를 1씩 늘리며 전체 계보를 조회합니다.
-- 자식을 갖지 않는 행만 남겨 세대별로 세고 정렬합니다. 예제의 세대별 개수는 1, 2, 1, 1입니다.
-- 