SELECT CAR_ID, ROUND(AVG(DATEDIFF(END_DATE, START_DATE) + 1), 1) AS AVERAGE_DURATION
FROM CAR_RENTAL_COMPANY_RENTAL_HISTORY
GROUP BY CAR_ID
HAVING AVG(DATEDIFF(END_DATE, START_DATE) + 1) >= 7
ORDER BY AVERAGE_DURATION DESC, CAR_ID DESC

-- 전체 코드 줄별 설명
-- SELECT CAR_ID, ROUND(AVG(DATEDIFF(END_DATE, START_DATE) + 1), 1) AS AVERAGE_DURATION  -- SELECT는 출력 열, DATEDIFF는 날짜 차이. +1은 시작·종료일 모두 포함. AVG는 평균, ROUND(값,1)은 소수 둘째 자리에서 반올림.
-- FROM CAR_RENTAL_COMPANY_RENTAL_HISTORY  -- 대여 기록 테이블 조회.
-- GROUP BY CAR_ID  -- 자동차별 모든 대여 기간을 묶음.
-- HAVING AVG(DATEDIFF(END_DATE, START_DATE) + 1) >= 7  -- HAVING은 집계 후 조건. 반올림 전 실제 평균이 7일 이상인지 검사.
-- ORDER BY AVERAGE_DURATION DESC, CAR_ID DESC  -- 표시한 평균 기간 내림차순, 동점이면 자동차 ID도 내림차순.

-- 풀이 요약
-- 같은 날 빌리고 반납해도 1일이므로 DATEDIFF+1로 각 기간을 계산한다. 기간들의 평균을 낸 뒤 한 자리로 반올림한다.
-- 6.96일이 반올림해 7.0이 되더라도 실제 평균이 7 미만이면 제외해야 하므로 HAVING에는 원래 평균식을 사용한다.
-- 