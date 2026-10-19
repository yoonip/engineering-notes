SELECT NAME, DATETIME
FROM ANIMAL_INS
ORDER BY ANIMAL_ID DESC

-- 전체 코드 줄별 설명
-- SELECT NAME, DATETIME  -- SELECT는 출력 열 선택. 이름과 보호 시작 시각 조회.
-- FROM ANIMAL_INS  -- FROM은 동물 입소 정보 테이블 지정.
-- ORDER BY ANIMAL_ID DESC  -- ORDER BY는 정렬, DESC는 내림차순. 출력하지 않는 ID 열도 정렬 기준으로 사용 가능.

-- 풀이 요약
-- 조회할 열과 정렬 기준 열이 달라도 됩니다. 이름·시각을 ID 역순으로 출력합니다.
-- 