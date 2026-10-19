SELECT COUNT(*) AS count
FROM ANIMAL_INS

-- 전체 코드 줄별 설명
-- SELECT COUNT(*) AS count  -- SELECT는 결과 열, COUNT(*)는 NULL 여부와 무관하게 전체 행 수 집계, AS는 별칭. 입소 동물 한 행이 한 마리.
-- FROM ANIMAL_INS  -- 입소 동물 테이블 조회.

-- 풀이 요약
-- 동물 전체 수는 이름이 있는지와 무관하므로 COUNT(*)로 모든 행을 센다.
-- COUNT(NAME)을 쓰면 이름 NULL인 동물이 빠진다. 그룹이나 필터가 필요 없는 한 행 집계다.
-- 