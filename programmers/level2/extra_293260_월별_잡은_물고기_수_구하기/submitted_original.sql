SELECT COUNT(*) AS FISH_COUNT, MONTH(TIME) AS MONTH
FROM FISH_INFO
GROUP BY MONTH(TIME)
ORDER BY MONTH

-- 전체 코드 줄별 설명
-- SELECT COUNT(*) AS FISH_COUNT, MONTH(TIME) AS MONTH  -- SELECT는 열 선택. COUNT(*)는 잡은 행 수, MONTH는 날짜의 월을 정수로 추출, AS는 출력 별칭.
-- FROM FISH_INFO  -- 잡은 물고기 테이블 조회.
-- GROUP BY MONTH(TIME)  -- 같은 월의 기록을 묶어 물고기 수 집계. 연도별 구분은 요구하지 않음.
-- ORDER BY MONTH  -- 월 오름차순 정렬. 숫자 월이라 1·2·...·12 순서.

-- 풀이 요약
-- 잡은 날짜에서 MONTH를 추출해 월별 행 수를 센다. 월 출력은 01 같은 문자열이 아니라 숫자 1이다.
-- 원래 기록으로 GROUP BY하므로 물고기를 잡지 않은 월은 자동으로 결과에 나타나지 않는다.
-- 