SELECT i.ANIMAL_ID, i.NAME
FROM ANIMAL_INS AS i
JOIN ANIMAL_OUTS AS o ON o.ANIMAL_ID = i.ANIMAL_ID
ORDER BY TIMESTAMPDIFF(SECOND, i.DATETIME, o.DATETIME) DESC
LIMIT 2

-- 전체 코드 줄별 설명
-- SELECT i.ANIMAL_ID, i.NAME  -- SELECT는 출력 열 선택. 입소 정보의 동물 ID·이름 출력.
-- FROM ANIMAL_INS AS i  -- FROM은 입소 테이블, AS i는 별칭.
-- JOIN ANIMAL_OUTS AS o ON o.ANIMAL_ID = i.ANIMAL_ID  -- JOIN·ON으로 같은 동물의 입양 기록 연결. 실제 입양된 동물만 선택.
-- ORDER BY TIMESTAMPDIFF(SECOND, i.DATETIME, o.DATETIME) DESC  -- TIMESTAMPDIFF는 두 시각 차이를 지정 단위인 SECOND(초)로 계산. DESC는 긴 보호 기간부터 정렬.
-- LIMIT 2  -- LIMIT는 출력 행 수 제한. 상위 두 마리만 반환.

-- 풀이 요약
-- 입소와 입양 기록을 같은 ID로 연결하고 입양 시각-입소 시각이 긴 두 마리를 고른다.
-- 날짜 문자열을 직접 빼면 날짜 간격이 되지 않으므로 TIMESTAMPDIFF로 실제 시간 차이를 구한다.
-- 