SELECT COUNT(*) AS USERS
FROM USER_INFO
WHERE AGE IS NULL

-- 전체 코드 줄별 설명
-- SELECT COUNT(*) AS USERS  -- SELECT는 조회, COUNT(*)는 행 수 집계, AS는 출력 열 별칭.
-- FROM USER_INFO  -- FROM은 회원 정보 테이블 지정.
-- WHERE AGE IS NULL  -- WHERE는 필터. IS NULL은 나이 정보가 없는지 검사. = NULL로 비교하지 않음.

-- 풀이 요약
-- 나이 열이 NULL인 회원만 필터링해 개수를 셉니다.
-- 