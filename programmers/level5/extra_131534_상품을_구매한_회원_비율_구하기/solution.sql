WITH COHORT AS (
    SELECT USER_ID
    FROM USER_INFO
    WHERE JOINED >= '2021-01-01' AND JOINED < '2022-01-01'
)
SELECT YEAR(S.SALES_DATE) AS YEAR,
       MONTH(S.SALES_DATE) AS MONTH,
       COUNT(DISTINCT S.USER_ID) AS PURCHASED_USERS,
       ROUND(COUNT(DISTINCT S.USER_ID) / (SELECT COUNT(*) FROM COHORT), 1) AS PUCHASED_RATIO
FROM ONLINE_SALE AS S
JOIN COHORT AS C ON S.USER_ID = C.USER_ID
GROUP BY YEAR(S.SALES_DATE), MONTH(S.SALES_DATE)
ORDER BY YEAR, MONTH

-- 전체 코드 줄별 설명
-- WITH COHORT AS (  -- WITH는 이름을 붙인 임시 조회 결과 CTE 정의. 2021년 가입자 집합을 재사용.
--     SELECT USER_ID  -- SELECT는 열 조회. 대상 회원 ID만 선택.
--     FROM USER_INFO  -- FROM은 원본 회원 테이블 지정.
--     WHERE JOINED >= '2021-01-01' AND JOINED < '2022-01-01'  -- WHERE는 필터, AND는 두 조건 모두 만족. 작은따옴표는 날짜 문자열.
-- )  -- COHORT 임시 결과 정의 종료.
-- SELECT YEAR(S.SALES_DATE) AS YEAR,  -- YEAR(날짜)는 연도 추출. AS는 결과 열 이름, 쉼표는 열 구분.
--        MONTH(S.SALES_DATE) AS MONTH,  -- MONTH(날짜)는 월 추출. 판매가 발생한 월 기준으로 집계.
--        COUNT(DISTINCT S.USER_ID) AS PURCHASED_USERS,  -- COUNT는 개수, DISTINCT는 중복 제거. 한 달에 여러 번 사도 한 명으로 셈.
--        ROUND(COUNT(DISTINCT S.USER_ID) / (SELECT COUNT(*) FROM COHORT), 1) AS PUCHASED_RATIO  -- /는 나눗셈, 하위 SELECT는 전체 가입자 수. ROUND(값,1)은 소수 둘째 자리 반올림. 열 이름은 문제 표기 사용.
-- FROM ONLINE_SALE AS S  -- 판매 테이블을 S라는 별칭으로 조회. 점으로 별칭의 열에 접근.
-- JOIN COHORT AS C ON S.USER_ID = C.USER_ID  -- JOIN·ON은 조건에 맞는 행 연결. 2021년 가입자의 구매만 남김.
-- GROUP BY YEAR(S.SALES_DATE), MONTH(S.SALES_DATE)  -- GROUP BY는 같은 값을 묶음. 연도와 월별 구매 회원 수 계산.
-- ORDER BY YEAR, MONTH  -- ORDER BY는 정렬. 연도 오름차순, 같은 연도에서는 월 오름차순.

-- 풀이 요약
-- 2021년 가입자를 먼저 고르고 판매 기록과 연결합니다. 구매 연도는 2021년으로 제한하지 않습니다.
-- 월별 중복 없는 구매자 수를 2021년 전체 가입자 수로 나눕니다. 예제는 2/4=0.5, 1/4를 반올림한 0.3입니다.
-- 