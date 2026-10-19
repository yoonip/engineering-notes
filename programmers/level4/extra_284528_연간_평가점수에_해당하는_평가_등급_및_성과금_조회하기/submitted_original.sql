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

-- 전체 코드 줄별 설명
-- SELECT e.EMP_NO, e.EMP_NAME,  -- SELECT는 출력 열 지정. e.은 사원 테이블 별명.
--        CASE WHEN AVG(g.SCORE) >= 96 THEN 'S'  -- CASE는 조건별 값 선택. AVG는 평균, WHEN 조건이 참이면 THEN의 등급 반환.
--             WHEN AVG(g.SCORE) >= 90 THEN 'A'  -- 앞 조건을 만족하지 않은 점수 중 90 이상에 A등급 부여.
--             WHEN AVG(g.SCORE) >= 80 THEN 'B'  -- 평균이 80 이상이면 B등급.
--             ELSE 'C' END AS GRADE,  -- ELSE는 나머지 경우, END는 CASE 종료, AS는 결과 열 이름 지정.
--        e.SAL * CASE WHEN AVG(g.SCORE) >= 96 THEN 0.20  -- 연봉 SAL에 등급별 비율을 곱하여 성과금 계산.
--                     WHEN AVG(g.SCORE) >= 90 THEN 0.15  -- A등급은 연봉의 15퍼센트.
--                     WHEN AVG(g.SCORE) >= 80 THEN 0.10  -- B등급은 연봉의 10퍼센트.
--                     ELSE 0 END AS BONUS  -- C등급은 성과금 0. 결과 열 이름 BONUS.
-- FROM HR_EMPLOYEES AS e  -- FROM은 사원 정보를 읽을 테이블 지정.
-- JOIN HR_GRADE AS g ON e.EMP_NO = g.EMP_NO  -- JOIN과 ON으로 사번이 같은 반기별 평가를 연결.
-- WHERE g.YEAR = 2022  -- WHERE는 조건 필터. 2022년 평가만 사용.
-- GROUP BY e.EMP_NO, e.EMP_NAME, e.SAL  -- GROUP BY는 사원별 묶음 생성. 각 묶음에서 평균 점수 계산.
-- ORDER BY e.EMP_NO  -- ORDER BY는 정렬. 사번 오름차순.

-- 풀이 요약
-- 사원별 상·하반기 점수의 평균으로 등급과 연봉 대비 성과금을 계산합니다.
-- 예: 평균 95점, 연봉 8000이면 A등급이며 성과금은 1200입니다.
-- 