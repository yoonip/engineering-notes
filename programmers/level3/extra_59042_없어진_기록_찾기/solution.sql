-- SELECT는 입양 기록에 남아 있는 동물 ID·이름 출력.
SELECT o.ANIMAL_ID, o.NAME
-- 입소 누락 여부를 찾으므로 입양을 기준으로 시작.
FROM ANIMAL_OUTS AS o
-- ON은 같은 동물 ID 연결 조건.
LEFT JOIN ANIMAL_INS AS i ON i.ANIMAL_ID = o.ANIMAL_ID
-- WHERE는 행 조건, IS NULL은 연결된 입소 기록이 없는지 검사.
WHERE i.ANIMAL_ID IS NULL
-- 동물 ID 오름차순 정렬.
ORDER BY o.ANIMAL_ID
