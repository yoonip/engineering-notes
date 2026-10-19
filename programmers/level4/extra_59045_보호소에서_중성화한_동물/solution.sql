-- 입소 당시 Intact였지만 입양 때 Neutered 또는 Spayed가 된 동물의 ID·종류·이름을 ID 오름차순으로 구합니다.
-- ID로 입소·입양을 조인하고 전후 중성화 상태의 접두어를 각각 확인합니다. 성별이 아니라 중성화 상태 변화를 비교합니다.
SELECT i.ANIMAL_ID, i.ANIMAL_TYPE, i.NAME
FROM ANIMAL_INS AS i
JOIN ANIMAL_OUTS AS o ON i.ANIMAL_ID = o.ANIMAL_ID
WHERE i.SEX_UPON_INTAKE LIKE 'Intact%'
  AND (o.SEX_UPON_OUTCOME LIKE 'Neutered%' OR o.SEX_UPON_OUTCOME LIKE 'Spayed%')
ORDER BY i.ANIMAL_ID
