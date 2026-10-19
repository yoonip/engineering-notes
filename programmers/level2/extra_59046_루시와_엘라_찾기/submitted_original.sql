SELECT ANIMAL_ID, NAME, SEX_UPON_INTAKE
FROM ANIMAL_INS
WHERE NAME IN ('Lucy', 'Ella', 'Pickle', 'Rogan', 'Sabrina', 'Mitty')
ORDER BY ANIMAL_ID

-- 전체 코드 줄별 설명
-- SELECT ANIMAL_ID, NAME, SEX_UPON_INTAKE  -- SELECT는 동물 ID·이름·성별과 중성화 정보를 출력.
-- FROM ANIMAL_INS  -- 입소 테이블 조회.
-- WHERE NAME IN ('Lucy', 'Ella', 'Pickle', 'Rogan', 'Sabrina', 'Mitty')  -- WHERE는 행 조건. IN은 이름이 제시된 여섯 문자열 중 하나와 같은지 검사.
-- ORDER BY ANIMAL_ID  -- 동물 ID 오름차순으로 일관되게 출력.

-- 풀이 요약
-- 제시된 이름과 완전히 일치하는 동물을 IN으로 한 번에 선택한다.
-- 문자열 포함 검색 LIKE와 달리 Lucy가 이름 일부로만 들어가는 다른 동물은 선택하지 않는다.
-- 