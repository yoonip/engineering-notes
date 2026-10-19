SELECT COUNT(*) AS FISH_COUNT, MAX(LENGTH) AS MAX_LENGTH, FISH_TYPE
FROM FISH_INFO
GROUP BY FISH_TYPE
HAVING AVG(COALESCE(LENGTH, 10)) >= 33
ORDER BY FISH_TYPE

-- 전체 코드 줄별 설명
-- SELECT COUNT(*) AS FISH_COUNT, MAX(LENGTH) AS MAX_LENGTH, FISH_TYPE  -- SELECT는 출력 열 선택. COUNT(*)는 행 수, MAX는 최댓값, AS는 출력 열 별칭.
-- FROM FISH_INFO  -- FROM은 잡은 물고기 테이블 지정.
-- GROUP BY FISH_TYPE  -- 종류가 같은 물고기끼리 묶어 집계.
-- HAVING AVG(COALESCE(LENGTH, 10)) >= 33  -- HAVING은 집계 후 그룹 조건, AVG는 평균, COALESCE는 NULL이면 다음 값 10 사용. 평균 33cm 이상인 종류만 선택.
-- ORDER BY FISH_TYPE  -- 종류 번호 오름차순 정렬.

-- 풀이 요약
-- 10cm 이하 물고기의 NULL 길이는 평균 계산에서 10으로 대체한다. 종류별로 묶은 뒤 평균 조건은 WHERE가 아닌 HAVING으로 검사한다.
-- 합격한 종류의 전체 잡은 수와 최대 길이를 출력한다. 길이 NULL만 있는 종류의 평균은 10이라 조건에서 제외된다.
-- 