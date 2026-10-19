SELECT DISTINCT c.CAR_ID
FROM CAR_RENTAL_COMPANY_CAR AS c
JOIN CAR_RENTAL_COMPANY_RENTAL_HISTORY AS h ON h.CAR_ID = c.CAR_ID
WHERE c.CAR_TYPE = '세단' AND MONTH(h.START_DATE) = 10
ORDER BY c.CAR_ID DESC

-- 전체 코드 줄별 설명
-- SELECT DISTINCT c.CAR_ID  -- SELECT는 출력 열, DISTINCT는 중복 제거. 대여 기록이 여러 건이어도 자동차 ID는 한 번만 출력.
-- FROM CAR_RENTAL_COMPANY_CAR AS c  -- 자동차 정보 테이블을 c로 조회.
-- JOIN CAR_RENTAL_COMPANY_RENTAL_HISTORY AS h ON h.CAR_ID = c.CAR_ID  -- JOIN·ON으로 같은 자동차의 대여 기록 연결.
-- WHERE c.CAR_TYPE = '세단' AND MONTH(h.START_DATE) = 10  -- WHERE는 행 조건, AND는 모두 참. MONTH는 날짜에서 월 추출. 세단·10월 대여 시작 조건을 함께 검사.
-- ORDER BY c.CAR_ID DESC  -- 자동차 ID 내림차순 정렬.

-- 풀이 요약
-- 자동차 정보와 대여 기록을 조인한 뒤 세단이면서 시작 월이 10인 기록만 고른다.
-- 종료 월이나 10월과의 구간 겹침이 아니라 시작 월 조건이다. 여러 10월 기록이 같은 자동차에 있어도 DISTINCT로 한 번만 출력한다.
-- 