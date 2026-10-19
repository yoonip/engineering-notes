-- 2022-04-13의 흉부외과(CS) 진료 중 취소되지 않은 예약의 예약번호·환자정보·진료과·의사명·예약시각을 예약시각 오름차순으로 구합니다.
-- 예약을 기준으로 환자와 의사를 키 조인합니다. 날짜는 자정 이상·다음 자정 미만으로 검사해 하루의 모든 시각을 포함합니다.
SELECT a.APNT_NO, p.PT_NAME, a.PT_NO, a.MCDP_CD, d.DR_NAME, a.APNT_YMD
FROM APPOINTMENT AS a
JOIN PATIENT AS p ON a.PT_NO = p.PT_NO
JOIN DOCTOR AS d ON a.MDDR_ID = d.DR_ID
WHERE a.APNT_YMD >= '2022-04-13' AND a.APNT_YMD < '2022-04-14'
  AND a.MCDP_CD = 'CS' AND a.APNT_CNCL_YN = 'N'
ORDER BY a.APNT_YMD
