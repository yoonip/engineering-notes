-- AVG는 평균, ROUND(값,0)는 소수 첫째 자리에서 반올림한 정수, AS는 별칭.
SELECT d.DEPT_ID, d.DEPT_NAME_EN, ROUND(AVG(e.SAL), 0) AS AVG_SAL
FROM HR_DEPARTMENT AS d
-- JOIN·ON으로 부서 ID가 같은 사원을 연결.
JOIN HR_EMPLOYEES AS e ON e.DEPT_ID = d.DEPT_ID
GROUP BY d.DEPT_ID, d.DEPT_NAME_EN
-- 평균 연봉이 높은 부서부터 출력.
ORDER BY AVG_SAL DESC
