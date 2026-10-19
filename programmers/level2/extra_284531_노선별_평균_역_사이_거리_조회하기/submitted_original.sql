SELECT ROUTE,
       CONCAT(ROUND(SUM(D_BETWEEN_DIST), 1), 'km') AS TOTAL_DISTANCE,
       CONCAT(ROUND(AVG(D_BETWEEN_DIST), 2), 'km') AS AVERAGE_DISTANCE
FROM SUBWAY_DISTANCE
GROUP BY ROUTE
ORDER BY SUM(D_BETWEEN_DIST) DESC

-- 전체 코드 줄별 설명
-- SELECT ROUTE,  -- SELECT는 출력 열 선택. 노선명을 먼저 출력.
--        CONCAT(ROUND(SUM(D_BETWEEN_DIST), 1), 'km') AS TOTAL_DISTANCE,  -- SUM은 역 사이 거리 합, ROUND(값,1)은 소수 첫째 자리까지 반올림. CONCAT은 km 문자열 연결, AS는 별칭.
--        CONCAT(ROUND(AVG(D_BETWEEN_DIST), 2), 'km') AS AVERAGE_DISTANCE  -- AVG는 평균, ROUND(값,2)는 소수 둘째 자리까지 반올림.
-- FROM SUBWAY_DISTANCE  -- 역 사이 거리 테이블 조회.
-- GROUP BY ROUTE  -- 같은 노선별로 역들을 묶어 합계·평균 계산.
-- ORDER BY SUM(D_BETWEEN_DIST) DESC  -- 원래 숫자 합계 기준 내림차순 정렬. km가 붙은 문자열로 정렬하면 9km가 10km보다 앞서는 오류 가능.

-- 풀이 요약
-- 누계 거리 열을 다시 더하는 것이 아니라 각 역 사이 거리의 SUM을 사용한다. 평균도 같은 열의 AVG다.
-- 출력은 단위를 붙인 문자열이지만 정렬은 숫자 합계로 한다. 총 거리는 한 자리·평균은 두 자리까지 반올림한다.
-- 