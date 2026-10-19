SELECT HISTORY_ID, CAR_ID,
       DATE_FORMAT(START_DATE, '%Y-%m-%d') AS START_DATE,
       DATE_FORMAT(END_DATE, '%Y-%m-%d') AS END_DATE,
       CASE WHEN DATEDIFF(END_DATE, START_DATE) + 1 >= 30 THEN '장기 대여'
            ELSE '단기 대여' END AS RENT_TYPE
FROM CAR_RENTAL_COMPANY_RENTAL_HISTORY
WHERE START_DATE >= '2022-09-01' AND START_DATE < '2022-10-01'
ORDER BY HISTORY_ID DESC

-- 전체 코드 줄별 설명
-- SELECT HISTORY_ID, CAR_ID,  -- SELECT는 출력 열 선택. 기록 ID와 자동차 ID 조회.
--        DATE_FORMAT(START_DATE, '%Y-%m-%d') AS START_DATE,  -- DATE_FORMAT은 날짜 표시 형식 지정. 연-월-일 형식으로 시작일 출력.
--        DATE_FORMAT(END_DATE, '%Y-%m-%d') AS END_DATE,  -- 같은 형식으로 종료일 출력. AS는 결과 열 별칭.
--        CASE WHEN DATEDIFF(END_DATE, START_DATE) + 1 >= 30 THEN '장기 대여'  -- CASE·WHEN·THEN은 조건별 값 선택. DATEDIFF는 날짜 차이, 양 끝 날짜 포함하려고 1을 더함.
--             ELSE '단기 대여' END AS RENT_TYPE  -- ELSE는 나머지 경우, END는 CASE 종료. 대여 유형 열 이름 지정.
-- FROM CAR_RENTAL_COMPANY_RENTAL_HISTORY  -- FROM은 대여 기록 테이블 지정.
-- WHERE START_DATE >= '2022-09-01' AND START_DATE < '2022-10-01'  -- WHERE는 필터, AND는 모두 만족. 2022년 9월 시작한 기록 선택.
-- ORDER BY HISTORY_ID DESC  -- ORDER BY는 정렬, DESC는 내림차순. 기록 ID가 큰 순으로 출력.

-- 풀이 요약
-- 대여 기간은 종료일-시작일+1입니다. 시작일이 9월인 기록에만 기간별 유형을 붙입니다.
-- 