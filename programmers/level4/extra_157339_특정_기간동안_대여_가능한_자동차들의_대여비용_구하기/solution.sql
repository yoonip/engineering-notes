-- 2022년 11월 내내 비어 있는 세단·SUV의 30일 할인 요금을 구합니다. 500,000 이상 2,000,000 미만만 남기고 요금 내림차순·차종 오름차순·ID 내림차순입니다.
-- 대여 구간이 11월과 겹치는 조건은 시작일≤11월30일 AND 종료일≥11월1일입니다. 이런 기록이 없는 차량만 고르고 30일 이상 할인율을 적용해 소수점을 버립니다.
WITH fees AS (
    SELECT c.CAR_ID, c.CAR_TYPE,
           FLOOR(c.DAILY_FEE * 30 * (100 - p.DISCOUNT_RATE) / 100) AS FEE
    FROM CAR_RENTAL_COMPANY_CAR AS c
    JOIN CAR_RENTAL_COMPANY_DISCOUNT_PLAN AS p ON c.CAR_TYPE = p.CAR_TYPE
    WHERE c.CAR_TYPE IN ('세단', 'SUV') AND p.DURATION_TYPE = '30일 이상'
      AND NOT EXISTS (
          SELECT 1 FROM CAR_RENTAL_COMPANY_RENTAL_HISTORY AS h
          WHERE h.CAR_ID = c.CAR_ID
            AND h.START_DATE <= '2022-11-30' AND h.END_DATE >= '2022-11-01'
      )
)
SELECT CAR_ID, CAR_TYPE, FEE FROM fees
WHERE FEE >= 500000 AND FEE < 2000000
ORDER BY FEE DESC, CAR_TYPE ASC, CAR_ID DESC
