SELECT i.ANIMAL_ID, i.ANIMAL_TYPE, i.NAME
FROM ANIMAL_INS AS i
JOIN ANIMAL_OUTS AS o ON i.ANIMAL_ID = o.ANIMAL_ID
WHERE i.SEX_UPON_INTAKE LIKE 'Intact%'
  AND (o.SEX_UPON_OUTCOME LIKE 'Neutered%' OR o.SEX_UPON_OUTCOME LIKE 'Spayed%')
ORDER BY i.ANIMAL_ID

-- 전체 코드 줄별 설명
-- SELECT i.ANIMAL_ID, i.ANIMAL_TYPE, i.NAME  -- SELECT는 출력 열 선택. 동물 ID·생물 종·이름을 조회.
-- FROM ANIMAL_INS AS i  -- 보호 시작 기록 테이블에 i 별명 지정.
-- JOIN ANIMAL_OUTS AS o ON i.ANIMAL_ID = o.ANIMAL_ID  -- JOIN과 ON으로 같은 동물의 입소·입양 기록 연결.
-- WHERE i.SEX_UPON_INTAKE LIKE 'Intact%'  -- WHERE는 조건 필터. LIKE의 %는 임의의 뒤 문자열이며 입소 당시 미중성화인 동물 선택.
--   AND (o.SEX_UPON_OUTCOME LIKE 'Neutered%' OR o.SEX_UPON_OUTCOME LIKE 'Spayed%')  -- AND는 모두 참, OR는 둘 중 하나 참. ()로 두 중성화 유형을 한 조건으로 묶음.
-- ORDER BY i.ANIMAL_ID  -- ORDER BY는 정렬. 동물 ID 오름차순.

-- 풀이 요약
-- 같은 동물의 입소·입양 정보를 연결해 Intact에서 Neutered 또는 Spayed로 바뀐 동물만 고릅니다.
-- 입소 전에 이미 중성화된 동물은 제외합니다.
-- 