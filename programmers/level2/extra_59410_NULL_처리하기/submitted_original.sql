SELECT ANIMAL_TYPE, COALESCE(NAME, 'No name') AS NAME, SEX_UPON_INTAKE
FROM ANIMAL_INS
ORDER BY ANIMAL_ID

-- 전체 코드 줄별 설명
-- SELECT ANIMAL_TYPE, COALESCE(NAME, 'No name') AS NAME, SEX_UPON_INTAKE  -- SELECT는 종·이름·성별 상태 출력. COALESCE는 첫 NULL이 아닌 값 선택. 이름이 NULL이면 대체 문자열 사용, AS는 열 이름 유지.
-- FROM ANIMAL_INS  -- 입소 정보 테이블 조회.
-- ORDER BY ANIMAL_ID  -- 출력에 ID 열이 없어도 ID 오름차순으로 정렬 가능.

-- 풀이 요약
-- 이름이 NULL인 경우만 No name으로 표시하고 나머지 동물 정보는 그대로 출력한다.
-- NULL을 문자열 'NULL'과 비교하지 않고 COALESCE로 대체한다. 빈 문자열과 NULL은 서로 다른 값이다.
-- 