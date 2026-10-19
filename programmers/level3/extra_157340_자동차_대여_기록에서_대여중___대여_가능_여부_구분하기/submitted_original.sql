SELECT CAR_ID,
       CASE WHEN MAX('2022-10-16' BETWEEN START_DATE AND END_DATE) = 1
            THEN '대여중'
            ELSE '대여 가능'
       END AS AVAILABILITY
FROM CAR_RENTAL_COMPANY_RENTAL_HISTORY
GROUP BY CAR_ID
ORDER BY CAR_ID DESC

-- 전체 코드 줄별 설명
-- SELECT CAR_ID,  -- SELECT는 출력 열 선택. 자동차 ID를 먼저 출력.
--        CASE WHEN MAX('2022-10-16' BETWEEN START_DATE AND END_DATE) = 1  -- CASE WHEN은 조건별 값 선택. BETWEEN A AND B는 양 끝 포함 범위. MySQL의 참 1·거짓 0 중 MAX로 하나라도 해당하는지 검사.
--             THEN '대여중'  -- 해당 날짜를 포함하는 대여 기록이 하나라도 있으면 이 문자열.
--             ELSE '대여 가능'  -- ELSE는 나머지. 모든 기록이 해당 날짜와 무관하면 대여 가능.
--        END AS AVAILABILITY  -- END는 CASE 종료, AS는 상태 열 별칭.
-- FROM CAR_RENTAL_COMPANY_RENTAL_HISTORY  -- 대여 기록 테이블 조회.
-- GROUP BY CAR_ID  -- 자동차별로 모든 대여 기록을 한 그룹으로 묶음.
-- ORDER BY CAR_ID DESC  -- 자동차 ID 내림차순 정렬.

-- 풀이 요약
-- 자동차별로 10월 16일이 대여 구간 안에 있는 기록이 하나라도 있는지 집계한다. BETWEEN은 반납 날짜도 포함한다.
-- WHERE로 해당 날짜 기록만 남기면 대여 가능한 자동차가 사라지므로 전체 자동차를 그룹으로 유지하고 CASE로 표시한다.
-- 