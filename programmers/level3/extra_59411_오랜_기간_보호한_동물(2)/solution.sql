-- 입소 정보의 동물 ID·이름 출력.
SELECT i.ANIMAL_ID, i.NAME
-- FROM은 입소 테이블, AS i는 별칭.
FROM ANIMAL_INS AS i
-- 실제 입양된 동물만 선택.
JOIN ANIMAL_OUTS AS o ON o.ANIMAL_ID = i.ANIMAL_ID
-- DESC는 긴 보호 기간부터 정렬.
ORDER BY TIMESTAMPDIFF(SECOND, i.DATETIME, o.DATETIME) DESC
-- 상위 두 마리만 반환.
LIMIT 2
