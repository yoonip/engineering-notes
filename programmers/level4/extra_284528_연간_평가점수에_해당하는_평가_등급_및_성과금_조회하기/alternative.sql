-- 사원별 평가를 먼저 집계한 CTE와 급여를 조인합니다. 평균값을 한 번 계산한 뒤 등급과 성과금에 재사용합니다.
WITH scores AS (SELECT EMP_NO,AVG(SCORE) AS average_score FROM HR_GRADE WHERE YEAR=2022 GROUP BY EMP_NO)
SELECT e.EMP_NO,e.EMP_NAME,
 CASE WHEN s.average_score>=96 THEN 'S' WHEN s.average_score>=90 THEN 'A' WHEN s.average_score>=80 THEN 'B' ELSE 'C' END AS GRADE,
 e.SAL*CASE WHEN s.average_score>=96 THEN 0.20 WHEN s.average_score>=90 THEN 0.15 WHEN s.average_score>=80 THEN 0.10 ELSE 0 END AS BONUS
FROM HR_EMPLOYEES e JOIN scores s ON e.EMP_NO=s.EMP_NO ORDER BY e.EMP_NO;
