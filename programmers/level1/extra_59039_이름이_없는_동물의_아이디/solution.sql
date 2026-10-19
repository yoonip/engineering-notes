SELECT ANIMAL_ID
FROM ANIMAL_INS
WHERE NAME IS NULL
ORDER BY ANIMAL_ID

-- 전체 코드 줄별 설명
-- SELECT ANIMAL_ID  -- SELECT는 출력 열 선택. 동물 ID 조회.
-- FROM ANIMAL_INS  -- FROM은 동물 입소 정보 테이블 지정.
-- WHERE NAME IS NULL  -- WHERE는 필터. IS NULL은 이름 값이 없는 행 검사.
-- ORDER BY ANIMAL_ID  -- ORDER BY는 동물 ID 오름차순 정렬.

-- 풀이 요약
-- 이름이 NULL인 동물의 ID를 순서대로 조회합니다.
-- 