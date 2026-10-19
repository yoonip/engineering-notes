SELECT MCDP_CD AS `진료과 코드`, COUNT(*) AS `5월예약건수`
FROM APPOINTMENT
WHERE APNT_YMD >= '2022-05-01' AND APNT_YMD < '2022-06-01'
GROUP BY MCDP_CD
ORDER BY COUNT(*), MCDP_CD

-- 전체 코드 줄별 설명
-- SELECT MCDP_CD AS `진료과 코드`, COUNT(*) AS `5월예약건수`  -- SELECT는 출력 열, COUNT(*)는 예약 행 수, AS는 별칭. 백틱은 공백·숫자가 포함된 결과 열 이름을 감쌈.
-- FROM APPOINTMENT  -- 예약 정보 테이블 조회.
-- WHERE APNT_YMD >= '2022-05-01' AND APNT_YMD < '2022-06-01'  -- WHERE는 행 필터, AND는 모두 참. 시간까지 포함된 2022년 5월 전체 범위 선택.
-- GROUP BY MCDP_CD  -- 같은 진료과 코드별로 예약을 묶어 집계.
-- ORDER BY COUNT(*), MCDP_CD  -- 예약 수 오름차순, 동점이면 진료과 코드 오름차순.

-- 풀이 요약
-- 진료과별 5월 예약 건수를 세는 문제다. 취소 여부 필터나 환자 중복 제거는 지문에서 요구하지 않으므로 추가하지 않는다.
-- 날짜 범위를 다음 달 시작 미만으로 잡아 5월 31일의 모든 예약 시각도 포함한다.
-- 