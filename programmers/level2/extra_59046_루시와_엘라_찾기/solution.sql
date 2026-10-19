-- SELECT는 동물 ID·이름·성별과 중성화 정보를 출력.
SELECT ANIMAL_ID, NAME, SEX_UPON_INTAKE
FROM ANIMAL_INS
-- IN은 이름이 제시된 여섯 문자열 중 하나와 같은지 검사.
WHERE NAME IN ('Lucy', 'Ella', 'Pickle', 'Rogan', 'Sabrina', 'Mitty')
ORDER BY ANIMAL_ID
