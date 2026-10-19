WITH RECURSIVE hours AS (
    SELECT 0 AS hour
    UNION ALL
    SELECT hour + 1 FROM hours WHERE hour < 23
)
SELECT h.hour AS HOUR, COUNT(a.ANIMAL_ID) AS COUNT
FROM hours AS h
LEFT JOIN ANIMAL_OUTS AS a ON HOUR(a.DATETIME) = h.hour
GROUP BY h.hour
ORDER BY h.hour

-- 전체 코드 줄별 설명
-- WITH RECURSIVE hours AS (  -- WITH RECURSIVE는 자기 결과를 참조하는 공통 테이블 식. 24개 시간대를 직접 생성.
--     SELECT 0 AS hour  -- SELECT로 시작값 0을 만들고 AS로 열 이름 지정.
--     UNION ALL  -- 중복 제거 없이 시작 행과 이후 생성 행을 이어 붙임.
--     SELECT hour + 1 FROM hours WHERE hour < 23  -- 현재 시간에 1을 더해 23까지 생성. WHERE로 재귀 종료 조건 지정.
-- )  -- 시간대 생성 결과 종료.
-- SELECT h.hour AS HOUR, COUNT(a.ANIMAL_ID) AS COUNT  -- 시간과 실제 입양 동물 수 출력. COUNT(열)는 NULL을 세지 않음.
-- FROM hours AS h  -- 생성한 0~23시 전체 목록 조회.
-- LEFT JOIN ANIMAL_OUTS AS a ON HOUR(a.DATETIME) = h.hour  -- HOUR 함수는 일시의 시각 추출. LEFT JOIN으로 입양이 없는 시간도 유지.
-- GROUP BY h.hour  -- GROUP BY로 같은 시각의 입양 기록을 묶음.
-- ORDER BY h.hour  -- ORDER BY는 정렬. 0시부터 23시 순서로 출력.

-- 풀이 요약
-- 0~23시를 먼저 생성하고 실제 입양 기록을 LEFT JOIN합니다. 기록이 없는 시간도 한 행이 남아 0건으로 출력됩니다.
-- COUNT(*)는 빈 시간의 연결 행도 1로 세므로, 반드시 실제 동물 ID 열을 셉니다.
-- 