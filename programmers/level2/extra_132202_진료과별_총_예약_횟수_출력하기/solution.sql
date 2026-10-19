-- 5월 1일 이상·6월 1일 미만으로 필터한다. 진료과별 행 수를 세고 건수 오름차순·진료과 코드 오름차순으로 정렬한다.
SELECT MCDP_CD AS `진료과 코드`, COUNT(*) AS `5월예약건수`
FROM APPOINTMENT
WHERE APNT_YMD >= '2022-05-01' AND APNT_YMD < '2022-06-01'
GROUP BY MCDP_CD
ORDER BY COUNT(*), MCDP_CD
