SELECT YEAR(YM) AS YEAR,
       ROUND(AVG(PM_VAL1), 2) AS PM10,
       ROUND(AVG(PM_VAL2), 2) AS `PM2.5`
FROM AIR_POLLUTION
WHERE LOCATION2 = '수원'
GROUP BY YEAR(YM)
ORDER BY YEAR

-- 전체 코드 줄별 설명
-- SELECT YEAR(YM) AS YEAR,  -- SELECT는 열 선택. YEAR(날짜)는 연도 추출, AS는 결과 이름.
--        ROUND(AVG(PM_VAL1), 2) AS PM10,  -- AVG는 평균, ROUND(값,2)는 소수 셋째 자리에서 반올림해 둘째 자리까지 출력.
--        ROUND(AVG(PM_VAL2), 2) AS `PM2.5`  -- 초미세먼지 평균 계산. 백틱은 점이 포함된 열 이름을 하나의 식별자로 감쌈.
-- FROM AIR_POLLUTION  -- 대기 오염도 테이블 조회.
-- WHERE LOCATION2 = '수원'  -- WHERE는 집계 전 조건. 두 번째 지역 구분이 수원인 측정만 선택.
-- GROUP BY YEAR(YM)  -- 같은 측정 연도별로 그룹 생성.
-- ORDER BY YEAR  -- 연도 오름차순 정렬.

-- 풀이 요약
-- 수원 측정 행만 고른 뒤 연도별로 두 오염도 평균을 구한다. 월별 값을 먼저 반올림하지 않고 평균을 낸 뒤 반올림한다.
-- PM2.5는 점을 포함한 출력 이름이므로 백틱으로 감싸 테이블.열 표현과 구분한다.
-- 