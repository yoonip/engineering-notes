SELECT YEAR(s.SALES_DATE) AS YEAR, MONTH(s.SALES_DATE) AS MONTH, u.GENDER,
       COUNT(DISTINCT s.USER_ID) AS USERS
FROM ONLINE_SALE AS s
JOIN USER_INFO AS u ON s.USER_ID = u.USER_ID
WHERE u.GENDER IS NOT NULL
GROUP BY YEAR(s.SALES_DATE), MONTH(s.SALES_DATE), u.GENDER
ORDER BY YEAR, MONTH, u.GENDER

-- 전체 코드 줄별 설명
-- SELECT YEAR(s.SALES_DATE) AS YEAR, MONTH(s.SALES_DATE) AS MONTH, u.GENDER,  -- YEAR와 MONTH는 날짜의 연도·월 추출. AS는 결과 열 이름 지정.
--        COUNT(DISTINCT s.USER_ID) AS USERS  -- COUNT는 개수, DISTINCT는 중복 제거. 같은 회원의 반복 구매를 한 번만 셈.
-- FROM ONLINE_SALE AS s  -- 판매 기록 테이블을 s라는 별명으로 조회.
-- JOIN USER_INFO AS u ON s.USER_ID = u.USER_ID  -- JOIN과 ON으로 같은 회원 ID의 성별 정보 연결.
-- WHERE u.GENDER IS NOT NULL  -- WHERE는 필터, IS NOT NULL은 값이 존재함을 검사. 성별 미상 제외.
-- GROUP BY YEAR(s.SALES_DATE), MONTH(s.SALES_DATE), u.GENDER  -- GROUP BY는 연도·월·성별이 같은 행을 묶어 집계.
-- ORDER BY YEAR, MONTH, u.GENDER  -- ORDER BY는 정렬. 연도→월→성별 오름차순.

-- 풀이 요약
-- 연도·월·성별로 묶은 뒤 회원 ID를 중복 없이 셉니다. 판매 건수나 판매량을 세는 문제가 아닙니다.
-- 예: 같은 회원이 3월에 세 번 구매해도 3월 구매 회원 수에는 한 명으로 포함됩니다.
-- 