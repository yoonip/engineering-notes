SELECT ROUND(AVG(DAILY_FEE), 0) AS AVERAGE_FEE
FROM CAR_RENTAL_COMPANY_CAR
WHERE CAR_TYPE = 'SUV'

-- 전체 코드 줄별 설명
-- SELECT ROUND(AVG(DAILY_FEE), 0) AS AVERAGE_FEE  -- AVG는 평균, ROUND(값,0)는 소수 첫째 자리에서 반올림, AS는 출력 열 별칭.
-- FROM CAR_RENTAL_COMPANY_CAR  -- FROM은 자동차 정보 테이블 지정.
-- WHERE CAR_TYPE = 'SUV'  -- WHERE는 조건 필터, =은 SQL의 같음 비교. SUV 차종만 선택.

-- 풀이 요약
-- SUV 자동차의 일일 요금만 평균 내고 정수 자리까지 반올림합니다.
-- 