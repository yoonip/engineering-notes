WITH rentals AS (
    SELECT h.HISTORY_ID, c.CAR_TYPE, c.DAILY_FEE,
           DATEDIFF(h.END_DATE, h.START_DATE) + 1 AS days
    FROM CAR_RENTAL_COMPANY_RENTAL_HISTORY AS h
    JOIN CAR_RENTAL_COMPANY_CAR AS c ON h.CAR_ID = c.CAR_ID
    WHERE c.CAR_TYPE = '트럭'
)
SELECT r.HISTORY_ID,
       FLOOR(r.DAILY_FEE * r.days * (100 - IFNULL(p.DISCOUNT_RATE, 0)) / 100) AS FEE
FROM rentals AS r
LEFT JOIN CAR_RENTAL_COMPANY_DISCOUNT_PLAN AS p
  ON r.CAR_TYPE = p.CAR_TYPE
 AND p.DURATION_TYPE = CASE WHEN r.days >= 90 THEN '90일 이상'
                            WHEN r.days >= 30 THEN '30일 이상'
                            WHEN r.days >= 7 THEN '7일 이상' END
ORDER BY FEE DESC, r.HISTORY_ID DESC

-- 전체 코드 줄별 설명
-- WITH rentals AS (  -- WITH는 임시 결과 정의. 대여 일수와 일일 요금을 먼저 계산.
--     SELECT h.HISTORY_ID, c.CAR_TYPE, c.DAILY_FEE,  -- 대여 기록 ID, 차종, 일일 요금을 선택.
--            DATEDIFF(h.END_DATE, h.START_DATE) + 1 AS days  -- DATEDIFF는 두 날짜 차이. 시작일과 종료일 모두 포함하므로 1을 더함.
--     FROM CAR_RENTAL_COMPANY_RENTAL_HISTORY AS h  -- 대여 기록 테이블에 h 별명 지정.
--     JOIN CAR_RENTAL_COMPANY_CAR AS c ON h.CAR_ID = c.CAR_ID  -- JOIN으로 같은 자동차 ID의 차종·요금 연결.
--     WHERE c.CAR_TYPE = '트럭'  -- WHERE는 조건 필터. 트럭의 기록만 선택.
-- )  -- 대여 일수 계산 결과 종료.
-- SELECT r.HISTORY_ID,  -- 출력할 대여 기록 ID 선택.
--        FLOOR(r.DAILY_FEE * r.days * (100 - IFNULL(p.DISCOUNT_RATE, 0)) / 100) AS FEE  -- IFNULL은 NULL을 기본값으로 교체. 할인 없으면 0퍼센트, FLOOR는 원 단위 버림.
-- FROM rentals AS r  -- 계산된 트럭 대여 기록 조회.
-- LEFT JOIN CAR_RENTAL_COMPANY_DISCOUNT_PLAN AS p  -- LEFT JOIN은 할인 정책이 없어도 대여 기록을 유지.
--   ON r.CAR_TYPE = p.CAR_TYPE  -- 차종이 같은 할인 정책만 연결.
--  AND p.DURATION_TYPE = CASE WHEN r.days >= 90 THEN '90일 이상'  -- CASE는 조건별 값 선택. 긴 대여 기간부터 검사하여 올바른 할인 구간 선택.
--                             WHEN r.days >= 30 THEN '30일 이상'  -- 30~89일에 해당하는 할인 구간.
--                             WHEN r.days >= 7 THEN '7일 이상' END  -- 7~29일 할인. 나머지는 NULL이어서 정책이 연결되지 않음.
-- ORDER BY FEE DESC, r.HISTORY_ID DESC  -- DESC는 내림차순. 금액이 같으면 대여 기록 ID가 큰 행부터 출력.

-- 풀이 요약
-- 종료일-시작일+1로 대여 일수를 구하고 90일→30일→7일 순서로 할인 구간을 정합니다.
-- 예: 7일 미만 기록은 LEFT JOIN으로 유지하고 할인율 NULL을 0으로 바꿔 정상 요금을 계산합니다.
-- 