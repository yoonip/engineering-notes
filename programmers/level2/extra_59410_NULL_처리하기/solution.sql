-- 이름이 NULL이면 대체 문자열 사용, AS는 열 이름 유지.
SELECT ANIMAL_TYPE, COALESCE(NAME, 'No name') AS NAME, SEX_UPON_INTAKE
FROM ANIMAL_INS
-- 출력에 ID 열이 없어도 ID 오름차순으로 정렬 가능.
ORDER BY ANIMAL_ID
