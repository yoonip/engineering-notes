SELECT COUNT(*) AS FISH_COUNT
FROM FISH_INFO
WHERE TIME >= '2021-01-01' AND TIME < '2022-01-01'

-- 전체 코드 줄별 설명
-- SELECT COUNT(*) AS FISH_COUNT  -- SELECT는 조회, COUNT(*)는 행 개수, AS는 출력 열 이름 지정.
-- FROM FISH_INFO  -- FROM은 물고기 정보 테이블 지정.
-- WHERE TIME >= '2021-01-01' AND TIME < '2022-01-01'  -- WHERE는 필터, AND는 두 조건 모두 만족. 2021년 전체 날짜를 범위로 선택.

-- 풀이 요약
-- 2021년 1월 1일 이상이며 2022년 1월 1일 미만인 물고기 기록을 셉니다.
-- 