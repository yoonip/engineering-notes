SELECT o.ANIMAL_ID, o.NAME
FROM ANIMAL_OUTS AS o
LEFT JOIN ANIMAL_INS AS i ON i.ANIMAL_ID = o.ANIMAL_ID
WHERE i.ANIMAL_ID IS NULL
ORDER BY o.ANIMAL_ID

-- 전체 코드 줄별 설명
-- SELECT o.ANIMAL_ID, o.NAME  -- SELECT는 입양 기록에 남아 있는 동물 ID·이름 출력.
-- FROM ANIMAL_OUTS AS o  -- FROM은 입양 테이블. 입소 누락 여부를 찾으므로 입양을 기준으로 시작.
-- LEFT JOIN ANIMAL_INS AS i ON i.ANIMAL_ID = o.ANIMAL_ID  -- LEFT JOIN으로 입소가 없어도 입양 행을 보존. ON은 같은 동물 ID 연결 조건.
-- WHERE i.ANIMAL_ID IS NULL  -- WHERE는 행 조건, IS NULL은 연결된 입소 기록이 없는지 검사.
-- ORDER BY o.ANIMAL_ID  -- 동물 ID 오름차순 정렬.

-- 풀이 요약
-- 입양은 있지만 입소는 없는 행을 찾으므로 입양 테이블을 LEFT JOIN의 왼쪽에 둔다.
-- 입소 테이블을 왼쪽에 두면 이미 사라진 입소 행을 기준으로 시작해 원하는 동물을 찾을 수 없다.
-- 