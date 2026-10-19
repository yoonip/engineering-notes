SELECT ANIMAL_ID, NAME
FROM ANIMAL_INS
WHERE INTAKE_CONDITION <> 'Aged'
ORDER BY ANIMAL_ID

-- 전체 코드 줄별 설명
-- SELECT ANIMAL_ID, NAME  -- SELECT는 출력 열 선택. 동물 ID와 이름 조회.
-- FROM ANIMAL_INS  -- FROM은 동물 입소 정보 테이블 지정.
-- WHERE INTAKE_CONDITION <> 'Aged'  -- WHERE는 조건 필터, <>는 같지 않음. 문제의 젊은 동물 정의에 따라 Aged가 아닌 상태 선택.
-- ORDER BY ANIMAL_ID  -- ORDER BY는 동물 ID 오름차순 정렬.

-- 풀이 요약
-- 문제 각주에서 젊은 동물은 INTAKE_CONDITION이 Aged가 아닌 경우로 정의합니다.
-- 