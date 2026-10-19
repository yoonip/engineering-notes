SELECT MAX(DATETIME) AS 시간
FROM ANIMAL_INS

-- 전체 코드 줄별 설명
-- SELECT MAX(DATETIME) AS 시간  -- SELECT는 조회, MAX는 최댓값 집계, AS는 출력 열 별칭. 가장 늦은 보호 시작 시각 계산.
-- FROM ANIMAL_INS  -- FROM은 동물 입소 정보 테이블 지정.

-- 풀이 요약
-- 날짜·시각의 최댓값은 가장 최근 시각입니다.
-- 