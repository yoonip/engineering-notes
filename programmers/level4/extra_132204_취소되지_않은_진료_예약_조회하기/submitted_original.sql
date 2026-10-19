SELECT a.APNT_NO, p.PT_NAME, a.PT_NO, a.MCDP_CD, d.DR_NAME, a.APNT_YMD
FROM APPOINTMENT AS a
JOIN PATIENT AS p ON a.PT_NO = p.PT_NO
JOIN DOCTOR AS d ON a.MDDR_ID = d.DR_ID
WHERE a.APNT_YMD >= '2022-04-13' AND a.APNT_YMD < '2022-04-14'
  AND a.MCDP_CD = 'CS' AND a.APNT_CNCL_YN = 'N'
ORDER BY a.APNT_YMD

-- 전체 코드 줄별 설명
-- SELECT a.APNT_NO, p.PT_NAME, a.PT_NO, a.MCDP_CD, d.DR_NAME, a.APNT_YMD  -- SELECT는 출력 열 선택. 예약번호·환자이름·환자번호·진료과·의사이름·예약일시 순서.
-- FROM APPOINTMENT AS a  -- 진료 예약 테이블에 a라는 별명 지정.
-- JOIN PATIENT AS p ON a.PT_NO = p.PT_NO  -- JOIN으로 환자번호가 같은 환자 이름을 연결.
-- JOIN DOCTOR AS d ON a.MDDR_ID = d.DR_ID  -- 담당 의사 ID로 의사 이름 연결.
-- WHERE a.APNT_YMD >= '2022-04-13' AND a.APNT_YMD < '2022-04-14'  -- WHERE는 필터. 시간까지 있는 예약일시에서 4월 13일 하루 전체 선택.
--   AND a.MCDP_CD = 'CS' AND a.APNT_CNCL_YN = 'N'  -- AND는 조건을 모두 만족. 흉부외과이며 취소되지 않은 예약만 유지.
-- ORDER BY a.APNT_YMD  -- ORDER BY는 정렬. 예약일시가 이른 순서로 출력.

-- 풀이 요약
-- 예약을 중심으로 환자·의사 정보를 연결하고 날짜·진료과·취소 여부를 필터링합니다.
-- 예: 4월 13일 오후 예약도 포함해야 하므로 날짜 범위를 다음 날 미만으로 설정합니다.
-- 