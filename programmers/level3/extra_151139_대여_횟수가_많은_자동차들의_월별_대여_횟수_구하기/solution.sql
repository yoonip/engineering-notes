-- MONTH는 월 추출, COUNT(*)는 기록 수, AS는 결과 별칭.
SELECT MONTH(START_DATE) AS MONTH, CAR_ID, COUNT(*) AS RECORDS
-- 기간 전체 대여 횟수를 계산할 테이블.
FROM CAR_RENTAL_COMPANY_RENTAL_HISTORY
-- 자격 판단에도 동일한 세 달 기간만 적용.
WHERE START_DATE >= '2022-08-01' AND START_DATE < '2022-11-01'
  -- 기간 전체에서 다섯 번 이상 빌린 자동차만 남김.
  AND CAR_ID IN (
      -- 자격을 만족하는 자동차 ID 출력.
      SELECT CAR_ID
      -- 기간 전체 대여 횟수를 계산할 테이블.
      FROM CAR_RENTAL_COMPANY_RENTAL_HISTORY
      -- 자격 판단에도 동일한 세 달 기간만 적용.
      WHERE START_DATE >= '2022-08-01' AND START_DATE < '2022-11-01'
      -- 자동차별로 전체 기간 기록 묶기.
      GROUP BY CAR_ID
      -- 세 달 총 다섯 번 이상인 자동차 선택.
      HAVING COUNT(*) >= 5
  )
-- 기록 없는 월은 생성되지 않음.
GROUP BY MONTH(START_DATE), CAR_ID
-- 월은 기본 오름차순, 같은 월의 자동차 ID는 내림차순.
ORDER BY MONTH, CAR_ID DESC
