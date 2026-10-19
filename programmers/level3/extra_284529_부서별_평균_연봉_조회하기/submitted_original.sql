SELECT d.DEPT_ID, d.DEPT_NAME_EN, ROUND(AVG(e.SAL), 0) AS AVG_SAL
FROM HR_DEPARTMENT AS d
JOIN HR_EMPLOYEES AS e ON e.DEPT_ID = d.DEPT_ID
GROUP BY d.DEPT_ID, d.DEPT_NAME_EN
ORDER BY AVG_SAL DESC

-- 전체 코드 줄별 설명
-- SELECT d.DEPT_ID, d.DEPT_NAME_EN, ROUND(AVG(e.SAL), 0) AS AVG_SAL  -- SELECT는 출력 열 선택. AVG는 평균, ROUND(값,0)는 소수 첫째 자리에서 반올림한 정수, AS는 별칭.
-- FROM HR_DEPARTMENT AS d  -- 부서 테이블을 d라는 별칭으로 조회.
-- JOIN HR_EMPLOYEES AS e ON e.DEPT_ID = d.DEPT_ID  -- JOIN·ON으로 부서 ID가 같은 사원을 연결.
-- GROUP BY d.DEPT_ID, d.DEPT_NAME_EN  -- 같은 부서 ID·영문명별로 사원을 묶어 평균 계산.
-- ORDER BY AVG_SAL DESC  -- ORDER BY는 정렬, DESC는 내림차순. 평균 연봉이 높은 부서부터 출력.

-- 풀이 요약
-- 부서와 사원을 부서 ID로 조인한 뒤, 부서별 연봉 평균을 구하고 반올림한다.
-- 평균을 먼저 구한 후 ROUND를 적용한다. 출력 열은 부서 ID·영문 부서명·AVG_SAL 순서다.
-- 