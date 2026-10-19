SELECT COUNT(*) AS USERS
FROM USER_INFO
WHERE JOINED >= '2021-01-01' AND JOINED < '2022-01-01'
  AND AGE BETWEEN 20 AND 29

-- 전체 코드 줄별 설명
-- SELECT COUNT(*) AS USERS  -- SELECT는 조회, COUNT(*)는 행 수 집계, AS는 출력 열 별칭.
-- FROM USER_INFO  -- FROM은 회원 정보 테이블 지정.
-- WHERE JOINED >= '2021-01-01' AND JOINED < '2022-01-01'  -- WHERE는 필터, AND는 모두 만족. 가입 연도를 2021년으로 제한.
--   AND AGE BETWEEN 20 AND 29  -- BETWEEN a AND b는 양 끝을 포함한 범위 검사. 20세 이상 29세 이하 선택.

-- 풀이 요약
-- 가입 연도와 나이 범위를 모두 만족하는 회원 행을 셉니다.
-- 