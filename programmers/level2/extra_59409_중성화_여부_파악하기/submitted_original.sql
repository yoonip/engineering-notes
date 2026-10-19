SELECT ANIMAL_ID, NAME,
       CASE WHEN SEX_UPON_INTAKE LIKE '%Neutered%' OR SEX_UPON_INTAKE LIKE '%Spayed%'
            THEN 'O' ELSE 'X' END AS `중성화`
FROM ANIMAL_INS
ORDER BY ANIMAL_ID

-- 전체 코드 줄별 설명
-- SELECT ANIMAL_ID, NAME,  -- SELECT는 동물 ID·이름과 이어지는 계산 열 출력.
--        CASE WHEN SEX_UPON_INTAKE LIKE '%Neutered%' OR SEX_UPON_INTAKE LIKE '%Spayed%'  -- CASE WHEN은 조건별 값 선택. LIKE의 %는 임의 길이 문자열, OR는 둘 중 하나라도 참.
--             THEN 'O' ELSE 'X' END AS `중성화`  -- THEN은 참이면 O, ELSE는 거짓이면 X. END는 CASE 종료, AS는 한글 열 별칭.
-- FROM ANIMAL_INS  -- 입소 정보 테이블 조회.
-- ORDER BY ANIMAL_ID  -- 동물 ID 오름차순 정렬.

-- 풀이 요약
-- 성별·중성화 정보에 지정된 두 단어 중 하나가 있으면 중성화된 동물이다.
-- 조건에 맞지 않는 동물도 X로 출력해야 하므로 WHERE로 제거하지 않고 CASE로 표시한다.
-- 