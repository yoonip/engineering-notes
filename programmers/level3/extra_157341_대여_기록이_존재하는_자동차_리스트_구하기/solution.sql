-- 대여 기록이 여러 건이어도 자동차 ID는 한 번만 출력.
SELECT DISTINCT c.CAR_ID
-- 자동차 정보 테이블을 c로 조회.
FROM CAR_RENTAL_COMPANY_CAR AS c
-- JOIN·ON으로 같은 자동차의 대여 기록 연결.
JOIN CAR_RENTAL_COMPANY_RENTAL_HISTORY AS h ON h.CAR_ID = c.CAR_ID
-- 세단·10월 대여 시작 조건을 함께 검사.
WHERE c.CAR_TYPE = '세단' AND MONTH(h.START_DATE) = 10
-- 자동차 ID 내림차순 정렬.
ORDER BY c.CAR_ID DESC
