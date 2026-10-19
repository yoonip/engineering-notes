SELECT ANIMAL_ID, NAME, DATE_FORMAT(DATETIME, '%Y-%m-%d') AS DATETIME
FROM ANIMAL_INS
ORDER BY ANIMAL_ID

-- 전체 코드 줄별 설명
-- SELECT ANIMAL_ID, NAME, DATE_FORMAT(DATETIME, '%Y-%m-%d') AS DATETIME  -- SELECT는 출력 열, DATE_FORMAT은 날짜·시각을 지정 문자열로 변환. %Y·%m·%d는 연·월·일이므로 시간 부분 제외. AS는 결과 열 이름.
-- FROM ANIMAL_INS  -- 입소 정보 테이블 조회.
-- ORDER BY ANIMAL_ID  -- 동물 ID 오름차순 정렬.

-- 풀이 요약
-- 모든 동물의 입소 시각을 연-월-일 형태로 표시한다. 행을 제거하거나 그룹화하는 조건은 없다.
-- DATETIME에는 시·분·초가 있지만 DATE_FORMAT의 출력 형식에서 시간 부분을 생략하면 날짜만 반환된다.
-- 