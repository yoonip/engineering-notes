SELECT NAME, COUNT(*) AS COUNT
FROM ANIMAL_INS
WHERE NAME IS NOT NULL
GROUP BY NAME
HAVING COUNT(*) >= 2
ORDER BY NAME

-- 전체 코드 줄별 설명
-- SELECT NAME, COUNT(*) AS COUNT  -- SELECT는 이름·등장 횟수 출력. COUNT(*)는 그룹 안 행 수, AS는 별칭.
-- FROM ANIMAL_INS  -- 입소 동물 테이블 조회.
-- WHERE NAME IS NOT NULL  -- WHERE는 집계 전 필터. IS NOT NULL로 이름 없는 동물 제외.
-- GROUP BY NAME  -- 같은 이름의 동물을 한 그룹으로 묶음.
-- HAVING COUNT(*) >= 2  -- HAVING은 집계 후 조건. 두 번 이상 등장한 이름만 선택.
-- ORDER BY NAME  -- 이름 오름차순 정렬.

-- 풀이 요약
-- NULL 이름을 먼저 빼고 이름별 개수를 구한 뒤 두 마리 이상인 그룹만 남긴다.
-- WHERE는 원래 행, HAVING은 그룹의 COUNT 결과에 적용된다는 차이를 구분한다.
-- 