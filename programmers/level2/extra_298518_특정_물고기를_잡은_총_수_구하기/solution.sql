-- 물고기 종류 번호로 이름을 조인하고 두 이름을 고른 뒤 COUNT(*)로 행을 센다.
SELECT COUNT(*) AS FISH_COUNT
FROM FISH_INFO AS f
JOIN FISH_NAME_INFO AS names ON names.FISH_TYPE = f.FISH_TYPE
WHERE names.FISH_NAME IN ('BASS', 'SNAPPER')
