-- COUNT(*)는 각 종의 동물 행 수, AS는 결과 별칭.
SELECT ANIMAL_TYPE, COUNT(*) AS count
FROM ANIMAL_INS
-- 고양이·개만 선택.
WHERE ANIMAL_TYPE IN ('Cat', 'Dog')
GROUP BY ANIMAL_TYPE
-- 문자열 오름차순에서 Cat이 Dog보다 앞서므로 고양이 먼저 출력.
ORDER BY ANIMAL_TYPE
