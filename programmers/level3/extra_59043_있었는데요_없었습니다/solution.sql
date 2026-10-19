-- 점(.)은 별칭의 열 지정.
SELECT i.ANIMAL_ID, i.NAME
-- FROM은 입소 기록 테이블, AS i는 별칭.
FROM ANIMAL_INS AS i
-- JOIN·ON으로 같은 동물의 입소·입양 기록 연결.
JOIN ANIMAL_OUTS AS o ON o.ANIMAL_ID = i.ANIMAL_ID
-- 입양 시각이 입소 시각보다 이른 오류 기록만 선택.
WHERE o.DATETIME < i.DATETIME
-- 보호 시작일 오름차순 정렬.
ORDER BY i.DATETIME
