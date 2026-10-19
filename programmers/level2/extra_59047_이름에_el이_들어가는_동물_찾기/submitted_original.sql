SELECT ANIMAL_ID, NAME
FROM ANIMAL_INS
WHERE ANIMAL_TYPE = 'Dog'
  AND LOWER(NAME) LIKE '%el%'
ORDER BY NAME, ANIMAL_ID

-- 전체 코드 줄별 설명
-- SELECT ANIMAL_ID, NAME  -- SELECT는 동물 ID·이름 출력.
-- FROM ANIMAL_INS  -- 입소 동물 테이블 조회.
-- WHERE ANIMAL_TYPE = 'Dog'  -- WHERE는 행 조건. 개만 선택.
--   AND LOWER(NAME) LIKE '%el%'  -- AND는 모두 참. LOWER는 소문자 변환, LIKE의 %는 임의 길이 문자열. 대소문자 무관하게 el이 포함되는지 검사.
-- ORDER BY NAME, ANIMAL_ID  -- 이름 오름차순, 이름 동점이면 ID 오름차순.

-- 풀이 요약
-- 먼저 개를 고르고 이름을 소문자로 바꿔 el 포함 여부를 검사한다. 출력 이름 자체는 원래 대소문자를 유지한다.
-- 이름이 NULL이면 LIKE 비교가 참이 아니어서 자동 제외된다. 이름에 el이 있는 고양이는 조건에 맞지 않는다.
-- 