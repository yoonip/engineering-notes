SELECT ANIMAL_TYPE, COUNT(*) AS count
FROM ANIMAL_INS
WHERE ANIMAL_TYPE IN ('Cat', 'Dog')
GROUP BY ANIMAL_TYPE
ORDER BY ANIMAL_TYPE

-- 전체 코드 줄별 설명
-- SELECT ANIMAL_TYPE, COUNT(*) AS count  -- SELECT는 종·개수 출력. COUNT(*)는 각 종의 동물 행 수, AS는 결과 별칭.
-- FROM ANIMAL_INS  -- 입소 동물 정보 조회.
-- WHERE ANIMAL_TYPE IN ('Cat', 'Dog')  -- WHERE는 행 필터, IN은 두 값 중 하나와 같은지 검사. 고양이·개만 선택.
-- GROUP BY ANIMAL_TYPE  -- 종별로 묶어 수 집계.
-- ORDER BY ANIMAL_TYPE  -- 문자열 오름차순에서 Cat이 Dog보다 앞서므로 고양이 먼저 출력.

-- 풀이 요약
-- 고양이와 개 행을 각각 그룹화해 센다. 이름이 NULL이어도 동물 수에는 포함된다.
-- 결과는 Cat·Dog 순서여야 하므로 종 이름 오름차순을 사용한다.
-- 