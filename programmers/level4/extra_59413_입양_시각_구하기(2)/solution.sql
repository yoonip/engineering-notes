-- 0시부터 23시까지 시간별 입양 건수를 구합니다. 기록이 없는 시간도 0으로 표시하고 시간 오름차순입니다.
-- 24개 시간 행을 재귀 CTE로 만든 뒤 입양을 LEFT JOIN합니다. COUNT(*)가 아니라 오른쪽 ANIMAL_ID를 세어 빈 시간의 가짜 한 행을 0으로 처리합니다.
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
