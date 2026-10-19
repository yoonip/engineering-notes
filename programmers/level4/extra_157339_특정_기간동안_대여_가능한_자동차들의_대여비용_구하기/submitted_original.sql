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

-- 전체 코드 줄별 설명
-- WITH fees AS (  -- WITH는 임시 결과 정의. 자동차별 30일 대여 금액 계산.
--     SELECT c.CAR_ID, c.CAR_TYPE,  -- SELECT는 출력 열 선택. 자동차 ID와 종류를 가져옴.
--            FLOOR(c.DAILY_FEE * 30 * (100 - p.DISCOUNT_RATE) / 100) AS FEE  -- FLOOR는 소수점 이하 버림. 30일 요금에 할인율을 반영.
--     FROM CAR_RENTAL_COMPANY_CAR AS c  -- 자동차 테이블을 c라는 별명으로 조회.
--     JOIN CAR_RENTAL_COMPANY_DISCOUNT_PLAN AS p ON c.CAR_TYPE = p.CAR_TYPE  -- JOIN으로 자동차 종류에 맞는 할인 정책 연결.
--     WHERE c.CAR_TYPE IN ('세단', 'SUV') AND p.DURATION_TYPE = '30일 이상'  -- IN은 목록 중 하나인지 검사. 두 차종의 30일 할인만 사용.
--       AND NOT EXISTS (  -- NOT EXISTS는 아래 조건에 맞는 대여 기록이 없음을 검사.
--           SELECT 1 FROM CAR_RENTAL_COMPANY_RENTAL_HISTORY AS h  -- 대여 기록의 값 대신 존재 여부만 조회.
--           WHERE h.CAR_ID = c.CAR_ID  -- 현재 자동차의 대여 기록만 검사.
--             AND h.START_DATE <= '2022-11-30' AND h.END_DATE >= '2022-11-01'  -- 시작이 기간 끝 이전이고 종료가 기간 시작 이후면 기간이 겹침. 경계 날짜도 포함.
--       )  -- 겹치는 대여 기록을 찾는 하위 쿼리 종료.
-- )  -- 금액 계산 임시 결과 종료.
-- SELECT CAR_ID, CAR_TYPE, FEE FROM fees  -- 계산된 자동차별 금액에서 필요한 세 열 출력.
-- WHERE FEE >= 500000 AND FEE < 2000000  -- AND는 두 조건 모두 참. 50만원 이상 200만원 미만만 선택.
-- ORDER BY FEE DESC, CAR_TYPE ASC, CAR_ID DESC  -- DESC는 내림차순, ASC는 오름차순. 금액→종류→ID 순서 정렬.

-- 풀이 요약
-- 11월과 하루라도 겹치는 대여 기록이 있는 차는 제외하고 30일 할인 요금을 계산합니다.
-- 예: 10월 20일~11월 2일 대여도 11월 전체 대여가 불가능하므로 제외합니다.
-- 