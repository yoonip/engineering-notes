SELECT ANIMAL_ID, NAME
FROM ANIMAL_INS
WHERE INTAKE_CONDITION = 'Sick'
ORDER BY ANIMAL_ID

-- 전체 코드 줄별 설명
-- SELECT ANIMAL_ID, NAME  -- SELECT는 출력 열 선택. 동물 ID와 이름 조회.
-- FROM ANIMAL_INS  -- FROM은 동물 입소 정보 테이블 지정.
-- WHERE INTAKE_CONDITION = 'Sick'  -- WHERE는 조건 필터, =은 같음 비교. 입소 상태가 Sick인 동물만 선택.
-- ORDER BY ANIMAL_ID  -- ORDER BY는 동물 ID 오름차순 정렬.

-- 풀이 요약
-- 문제 각주의 아픈 동물 상태 Sick을 조건으로 사용합니다.
-- 