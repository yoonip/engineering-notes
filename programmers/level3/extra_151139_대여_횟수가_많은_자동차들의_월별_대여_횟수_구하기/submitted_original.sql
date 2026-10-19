SELECT MONTH(START_DATE) AS MONTH, CAR_ID, COUNT(*) AS RECORDS
FROM CAR_RENTAL_COMPANY_RENTAL_HISTORY
WHERE START_DATE >= '2022-08-01' AND START_DATE < '2022-11-01'
  AND CAR_ID IN (
      SELECT CAR_ID
      FROM CAR_RENTAL_COMPANY_RENTAL_HISTORY
      WHERE START_DATE >= '2022-08-01' AND START_DATE < '2022-11-01'
      GROUP BY CAR_ID
      HAVING COUNT(*) >= 5
  )
GROUP BY MONTH(START_DATE), CAR_ID
ORDER BY MONTH, CAR_ID DESC

-- 전체 코드 줄별 설명
-- SELECT MONTH(START_DATE) AS MONTH, CAR_ID, COUNT(*) AS RECORDS  -- SELECT는 출력 열 선택. MONTH는 월 추출, COUNT(*)는 기록 수, AS는 결과 별칭.
-- FROM CAR_RENTAL_COMPANY_RENTAL_HISTORY  -- 대여 기록 테이블 조회.
-- WHERE START_DATE >= '2022-08-01' AND START_DATE < '2022-11-01'  -- WHERE는 집계 전 조건, AND는 모두 참. 2022년 8~10월에 시작한 대여만 선택.
--   AND CAR_ID IN (  -- IN은 하위 쿼리 결과 목록에 포함되는지 확인. 기간 전체에서 다섯 번 이상 빌린 자동차만 남김.
--       SELECT CAR_ID  -- 자격을 만족하는 자동차 ID 출력.
--       FROM CAR_RENTAL_COMPANY_RENTAL_HISTORY  -- 기간 전체 대여 횟수를 계산할 테이블.
--       WHERE START_DATE >= '2022-08-01' AND START_DATE < '2022-11-01'  -- 자격 판단에도 동일한 세 달 기간만 적용.
--       GROUP BY CAR_ID  -- 자동차별로 전체 기간 기록 묶기.
--       HAVING COUNT(*) >= 5  -- HAVING은 집계 조건. 세 달 총 다섯 번 이상인 자동차 선택.
--   )  -- IN 하위 쿼리 종료.
-- GROUP BY MONTH(START_DATE), CAR_ID  -- 월·자동차별로 묶어 월별 대여 수 집계. 기록 없는 월은 생성되지 않음.
-- ORDER BY MONTH, CAR_ID DESC  -- 월은 기본 오름차순, 같은 월의 자동차 ID는 내림차순.

-- 풀이 요약
-- 먼저 세 달 합계가 5회 이상인 자동차를 찾고, 그 자동차들의 같은 기간 기록을 월별로 다시 센다.
-- 매월 5회 조건이 아니라 전체 기간 5회 조건이다. 시작 날짜로 필터링하며 대여 기간이 해당 월과 겹치는지는 검사하지 않는다.
-- 