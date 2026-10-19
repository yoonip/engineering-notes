-- 트럭의 각 대여 기록별 요금을 구합니다. 시작·종료일을 모두 포함하고 7·30·90일 이상에 해당하는 가장 긴 할인 구간을 적용합니다. 요금·기록 ID 내림차순입니다.
-- DATEDIFF+1로 포함 일수를 구하고 90→30→7 순서로 할인 종류를 고릅니다. 할인 미해당은 0%로 처리하며 마지막에 FLOOR합니다.
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
