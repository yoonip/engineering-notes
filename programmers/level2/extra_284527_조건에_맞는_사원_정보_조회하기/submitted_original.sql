SELECT g.SCORE, e.EMP_NO, e.EMP_NAME, e.POSITION, e.EMAIL
FROM (
    SELECT EMP_NO, SUM(SCORE) AS SCORE,
           DENSE_RANK() OVER (ORDER BY SUM(SCORE) DESC) AS SCORE_RANK
    FROM HR_GRADE
    WHERE YEAR = 2022
    GROUP BY EMP_NO
) AS g
JOIN HR_EMPLOYEES AS e ON e.EMP_NO = g.EMP_NO
WHERE g.SCORE_RANK = 1
ORDER BY e.EMP_NO

-- 전체 코드 줄별 설명
-- SELECT g.SCORE, e.EMP_NO, e.EMP_NAME, e.POSITION, e.EMAIL  -- SELECT는 점수·사번·이름·직책·이메일을 순서대로 출력. 점(.)은 별칭의 열 지정.
-- FROM (  -- FROM의 괄호 안은 중간 결과 테이블을 만드는 하위 쿼리.
--     SELECT EMP_NO, SUM(SCORE) AS SCORE,  -- SUM은 상·하반기 점수 합계, AS는 결과 열 이름.
--            DENSE_RANK() OVER (ORDER BY SUM(SCORE) DESC) AS SCORE_RANK  -- DENSE_RANK는 동점에 같은 순위를 주는 윈도 함수. OVER의 ORDER BY로 합계 내림차순 순위 생성.
--     FROM HR_GRADE  -- 평가 기록 테이블 조회.
--     WHERE YEAR = 2022  -- WHERE는 집계 전 필터. 2022년 평가만 선택.
--     GROUP BY EMP_NO  -- 사원별로 상·하반기 기록을 묶음.
-- ) AS g  -- 하위 쿼리 결과를 g라는 테이블 별칭으로 사용.
-- JOIN HR_EMPLOYEES AS e ON e.EMP_NO = g.EMP_NO  -- JOIN·ON으로 합계에 사원 상세 정보 연결.
-- WHERE g.SCORE_RANK = 1  -- 집계 결과 중 공동 1위까지 모두 선택. LIMIT 1로 동점자를 버리지 않음.
-- ORDER BY e.EMP_NO  -- 같은 최고점 사원들은 사번순으로 일관되게 출력.

-- 풀이 요약
-- 평가 기록을 연도 필터→사원별 합계→합계 순위 순서로 계산한다. 최고점인 사원들의 정보를 원래 사원 테이블에서 조인한다.
-- 부서 테이블은 요구한 출력 열이나 조건에 필요하지 않아 조인하지 않는다. 같은 최고점 사원이 여러 명이면 모두 1위로 반환한다.
-- 