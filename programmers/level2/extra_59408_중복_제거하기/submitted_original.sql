SELECT COUNT(DISTINCT NAME) AS count
FROM ANIMAL_INS

-- 전체 코드 줄별 설명
-- SELECT COUNT(DISTINCT NAME) AS count  -- SELECT는 결과 열, DISTINCT는 같은 이름 중복 제거, COUNT(열)은 NULL을 세지 않는 개수 집계. AS는 별칭.
-- FROM ANIMAL_INS  -- 입소 동물 테이블 조회.

-- 풀이 요약
-- 서로 다른 실제 이름 수를 센다. COUNT(DISTINCT NAME)은 중복 제거와 NULL 제외를 동시에 수행한다.
-- COUNT(*)는 동물 수이고 DISTINCT 없이 COUNT(NAME)은 동명이인까지 따로 세므로 요구와 다르다.
-- 