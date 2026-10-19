SELECT i.NAME, i.DATETIME
FROM ANIMAL_INS AS i
LEFT JOIN ANIMAL_OUTS AS o ON o.ANIMAL_ID = i.ANIMAL_ID
WHERE o.ANIMAL_ID IS NULL
ORDER BY i.DATETIME
LIMIT 3

-- 전체 코드 줄별 설명
-- SELECT i.NAME, i.DATETIME  -- SELECT는 이름·보호 시작 시각 열 출력. i.는 입소 테이블의 열.
-- FROM ANIMAL_INS AS i  -- 입소 기록 테이블 조회. AS는 별칭 지정.
-- LEFT JOIN ANIMAL_OUTS AS o ON o.ANIMAL_ID = i.ANIMAL_ID  -- LEFT JOIN은 입양 기록이 없는 입소 동물도 보존. ON은 같은 동물 ID 연결 조건.
-- WHERE o.ANIMAL_ID IS NULL  -- WHERE는 행 필터. IS NULL로 입양 기록이 없는 동물만 선택.
-- ORDER BY i.DATETIME  -- 보호 시작일 오름차순. 먼저 들어온 동물일수록 오래 보호됨.
-- LIMIT 3  -- LIMIT는 최대 출력 수. 가장 오래 보호한 세 마리만 반환.

-- 풀이 요약
-- 입양 기록이 없는 동물을 찾는 왼쪽 반조인 문제다. 입소 기록을 모두 보존하고 연결된 입양 ID가 NULL인 행만 선택한다.
-- 아직 입양하지 않아 종료 시각이 없으므로 오래 보호한 순서는 입소 시각이 빠른 순서와 같다.
-- 