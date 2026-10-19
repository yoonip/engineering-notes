SELECT i.ANIMAL_ID, i.NAME
FROM ANIMAL_INS AS i
JOIN ANIMAL_OUTS AS o ON o.ANIMAL_ID = i.ANIMAL_ID
WHERE o.DATETIME < i.DATETIME
ORDER BY i.DATETIME

-- 전체 코드 줄별 설명
-- SELECT i.ANIMAL_ID, i.NAME  -- SELECT는 동물 ID·이름 열 출력. 점(.)은 별칭의 열 지정.
-- FROM ANIMAL_INS AS i  -- FROM은 입소 기록 테이블, AS i는 별칭.
-- JOIN ANIMAL_OUTS AS o ON o.ANIMAL_ID = i.ANIMAL_ID  -- JOIN·ON으로 같은 동물의 입소·입양 기록 연결.
-- WHERE o.DATETIME < i.DATETIME  -- WHERE는 행 조건. <는 미만. 입양 시각이 입소 시각보다 이른 오류 기록만 선택.
-- ORDER BY i.DATETIME  -- 보호 시작일 오름차순 정렬.

-- 풀이 요약
-- 같은 동물의 입소 시각과 입양 시각을 조인해 직접 비교한다. 입양이 입소보다 빠른 행이 잘못된 기록이다.
-- 출력 정렬 기준은 잘못된 입양일이 아니라 원래 보호 시작일이다.
-- 