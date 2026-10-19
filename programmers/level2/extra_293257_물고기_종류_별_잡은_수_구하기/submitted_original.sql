SELECT COUNT(*) AS FISH_COUNT, names.FISH_NAME
FROM FISH_INFO AS f
JOIN FISH_NAME_INFO AS names ON names.FISH_TYPE = f.FISH_TYPE
GROUP BY f.FISH_TYPE, names.FISH_NAME
ORDER BY FISH_COUNT DESC

-- 전체 코드 줄별 설명
-- SELECT COUNT(*) AS FISH_COUNT, names.FISH_NAME  -- SELECT는 출력 열, COUNT(*)는 잡은 기록 수, AS는 집계 별칭. 수를 먼저, 이름을 뒤에 출력.
-- FROM FISH_INFO AS f  -- 잡은 물고기 테이블 별칭 f.
-- JOIN FISH_NAME_INFO AS names ON names.FISH_TYPE = f.FISH_TYPE  -- JOIN·ON으로 종류 번호에 이름 연결.
-- GROUP BY f.FISH_TYPE, names.FISH_NAME  -- 종류 번호·이름이 같은 물고기끼리 묶음.
-- ORDER BY FISH_COUNT DESC  -- 잡은 수가 많은 종류부터 내림차순 정렬.

-- 풀이 요약
-- 잡은 기록에 종류 이름을 붙인 다음 종류별 행 수를 센다. 길이가 NULL인 작은 물고기도 COUNT(*)에 포함된다.
-- COUNT(LENGTH)를 쓰면 길이 NULL인 물고기가 빠지므로 전체 행 수를 사용한다.
-- 