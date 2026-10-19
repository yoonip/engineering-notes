SELECT MIN(DATETIME) AS `시간`
FROM ANIMAL_INS

-- 전체 코드 줄별 설명
-- SELECT MIN(DATETIME) AS `시간`  -- SELECT는 결과 열, MIN은 최솟값. 날짜·시각의 최솟값은 가장 이른 입소 시각이다. AS는 출력 이름, 백틱은 한글 식별자 표시.
-- FROM ANIMAL_INS  -- 입소 동물 정보 테이블 조회.

-- 풀이 요약
-- 가장 먼저 들어온 동물의 입소 시각은 DATETIME의 최소값이다.
-- 이 문제는 동물의 다른 정보를 요구하지 않으므로 별도 정렬·조인 없이 MIN으로 시각 하나만 반환한다.
-- 