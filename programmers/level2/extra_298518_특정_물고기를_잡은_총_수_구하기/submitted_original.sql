SELECT COUNT(*) AS FISH_COUNT
FROM FISH_INFO AS f
JOIN FISH_NAME_INFO AS names ON names.FISH_TYPE = f.FISH_TYPE
WHERE names.FISH_NAME IN ('BASS', 'SNAPPER')

-- 전체 코드 줄별 설명
-- SELECT COUNT(*) AS FISH_COUNT  -- SELECT는 출력 열, COUNT(*)는 행 수, AS는 결과 이름. 두 종류를 합한 전체 수 한 행 출력.
-- FROM FISH_INFO AS f  -- 잡은 물고기 테이블 별칭 f.
-- JOIN FISH_NAME_INFO AS names ON names.FISH_TYPE = f.FISH_TYPE  -- JOIN·ON으로 종류 번호에 해당하는 물고기 이름 연결.
-- WHERE names.FISH_NAME IN ('BASS', 'SNAPPER')  -- WHERE는 행 조건, IN은 목록 중 하나와 같은지 검사. 작은따옴표는 문자열.

-- 풀이 요약
-- 종류 번호와 이름 테이블을 연결해 BASS 또는 SNAPPER인 잡은 물고기만 센다.
-- 두 종류를 나눠 출력하는 문제가 아니므로 GROUP BY 없이 COUNT 전체 합계를 반환한다. 해당 물고기가 없어도 0 한 행이 나온다.
-- 