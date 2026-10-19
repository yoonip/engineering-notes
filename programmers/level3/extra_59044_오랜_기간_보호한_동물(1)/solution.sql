-- i.는 입소 테이블의 열.
SELECT i.NAME, i.DATETIME
-- AS는 별칭 지정.
FROM ANIMAL_INS AS i
-- ON은 같은 동물 ID 연결 조건.
LEFT JOIN ANIMAL_OUTS AS o ON o.ANIMAL_ID = i.ANIMAL_ID
-- IS NULL로 입양 기록이 없는 동물만 선택.
WHERE o.ANIMAL_ID IS NULL
-- 먼저 들어온 동물일수록 오래 보호됨.
ORDER BY i.DATETIME
-- 가장 오래 보호한 세 마리만 반환.
LIMIT 3
