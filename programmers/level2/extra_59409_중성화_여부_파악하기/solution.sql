-- SELECT는 동물 ID·이름과 이어지는 계산 열 출력.
SELECT ANIMAL_ID, NAME,
       CASE WHEN SEX_UPON_INTAKE LIKE '%Neutered%' OR SEX_UPON_INTAKE LIKE '%Spayed%'
            -- END는 CASE 종료, AS는 한글 열 별칭.
            THEN 'O' ELSE 'X' END AS `중성화`
FROM ANIMAL_INS
-- 동물 ID 오름차순 정렬.
ORDER BY ANIMAL_ID
