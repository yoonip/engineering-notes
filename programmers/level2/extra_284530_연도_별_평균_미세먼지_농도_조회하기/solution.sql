-- 지역 조건을 먼저 적용한다. 측정 연도로 그룹을 만든 후 평균을 구하고 마지막에 반올림한다.
SELECT YEAR(YM) AS YEAR,
       ROUND(AVG(PM_VAL1), 2) AS PM10,
       ROUND(AVG(PM_VAL2), 2) AS `PM2.5`
FROM AIR_POLLUTION
WHERE LOCATION2 = '수원'
GROUP BY YEAR(YM)
ORDER BY YEAR
