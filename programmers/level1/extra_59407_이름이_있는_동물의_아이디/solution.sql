SELECT ANIMAL_ID
FROM ANIMAL_INS
WHERE NAME IS NOT NULL
ORDER BY ANIMAL_ID

-- 전체 코드 줄별 설명
-- SELECT ANIMAL_ID  -- SELECT는 출력 열 선택. 동물 ID 조회.
-- FROM ANIMAL_INS  -- FROM은 동물 입소 정보 테이블 지정.
-- WHERE NAME IS NOT NULL  -- WHERE는 조건 필터. IS NOT NULL은 값이 존재하는지 검사. 이름 있는 동물만 선택.
-- ORDER BY ANIMAL_ID  -- ORDER BY는 정렬. 동물 ID 오름차순 출력.

-- 풀이 요약
-- 이름 열이 NULL이 아닌 동물의 ID를 조회합니다.
-- 