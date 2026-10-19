SELECT ANIMAL_ID, NAME, DATETIME
FROM ANIMAL_INS
ORDER BY NAME ASC, DATETIME DESC

-- 전체 코드 줄별 설명
-- SELECT ANIMAL_ID, NAME, DATETIME  -- SELECT는 출력 열 선택. ID·이름·보호 시작 시각 조회.
-- FROM ANIMAL_INS  -- FROM은 동물 입소 정보 테이블 지정.
-- ORDER BY NAME ASC, DATETIME DESC  -- ORDER BY는 정렬. 이름은 ASC 오름차순, 같은 이름이면 시각은 DESC 내림차순.

-- 풀이 요약
-- 이름순으로 정렬하되 같은 이름 안에서는 나중 입소한 동물을 먼저 배치합니다.
-- 