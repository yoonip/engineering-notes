SELECT NAME
FROM ANIMAL_INS
ORDER BY DATETIME
LIMIT 1

-- 전체 코드 줄별 설명
-- SELECT NAME  -- SELECT는 출력 열 선택. 동물 이름 조회.
-- FROM ANIMAL_INS  -- FROM은 동물 입소 정보 테이블 지정.
-- ORDER BY DATETIME  -- ORDER BY는 정렬. 보호 시작 시각이 이른 순서로 정렬.
-- LIMIT 1  -- LIMIT은 행 수 제한. 가장 먼저 들어온 동물 한 행만 선택.

-- 풀이 요약
-- 입소 시각 오름차순으로 정렬한 뒤 첫 행의 이름을 가져옵니다.
-- 