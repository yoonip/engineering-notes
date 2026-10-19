-- 자동차 ID를 먼저 출력.
SELECT CAR_ID,
       -- MySQL의 참 1·거짓 0 중 MAX로 하나라도 해당하는지 검사.
       CASE WHEN MAX('2022-10-16' BETWEEN START_DATE AND END_DATE) = 1
            -- 해당 날짜를 포함하는 대여 기록이 하나라도 있으면 이 문자열.
            THEN '대여중'
            -- 모든 기록이 해당 날짜와 무관하면 대여 가능.
            ELSE '대여 가능'
       -- END는 CASE 종료, AS는 상태 열 별칭.
       END AS AVAILABILITY
-- 대여 기록 테이블 조회.
FROM CAR_RENTAL_COMPANY_RENTAL_HISTORY
-- 자동차별로 모든 대여 기록을 한 그룹으로 묶음.
GROUP BY CAR_ID
-- 자동차 ID 내림차순 정렬.
ORDER BY CAR_ID DESC
