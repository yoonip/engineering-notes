-- 2022년 사원별 평균 평가점수로 S(96 이상)·A(90 이상)·B(80 이상)·C 등급을 매기고 연봉의 20%·15%·10%·0%를 성과금으로 구합니다. 사원번호 오름차순입니다.
-- 연도 조건을 먼저 적용하고 사원별 AVG를 구합니다. 높은 경계부터 CASE로 비교해야 96점이 A나 B로 잘못 분류되지 않습니다.
SELECT e.EMP_NO, e.EMP_NAME,
       CASE WHEN AVG(g.SCORE) >= 96 THEN 'S'
            WHEN AVG(g.SCORE) >= 90 THEN 'A'
            WHEN AVG(g.SCORE) >= 80 THEN 'B'
            ELSE 'C' END AS GRADE,
       e.SAL * CASE WHEN AVG(g.SCORE) >= 96 THEN 0.20
                    WHEN AVG(g.SCORE) >= 90 THEN 0.15
                    WHEN AVG(g.SCORE) >= 80 THEN 0.10
                    ELSE 0 END AS BONUS
FROM HR_EMPLOYEES AS e
JOIN HR_GRADE AS g ON e.EMP_NO = g.EMP_NO
WHERE g.YEAR = 2022
GROUP BY e.EMP_NO, e.EMP_NAME, e.SAL
ORDER BY e.EMP_NO
