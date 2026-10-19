SELECT CONCAT(QUARTER(DIFFERENTIATION_DATE), 'Q') AS QUARTER, COUNT(*) AS ECOLI_COUNT
FROM ECOLI_DATA
GROUP BY QUARTER(DIFFERENTIATION_DATE)
ORDER BY QUARTER

-- 전체 코드 줄별 설명
-- SELECT CONCAT(QUARTER(DIFFERENTIATION_DATE), 'Q') AS QUARTER, COUNT(*) AS ECOLI_COUNT  -- SELECT는 열 선택. QUARTER는 날짜의 분기 1~4 추출, CONCAT은 문자열 연결, COUNT(*)는 행 수, AS는 별칭.
-- FROM ECOLI_DATA  -- 대장균 테이블 조회.
-- GROUP BY QUARTER(DIFFERENTIATION_DATE)  -- 같은 분기로 묶어 개체 수 집계.
-- ORDER BY QUARTER  -- 1Q·2Q·3Q·4Q 순으로 오름차순 정렬.

-- 풀이 요약
-- 분화 날짜에서 분기를 추출해 그룹별 개체 수를 센다. 1~3월은 1Q, 4~6월은 2Q다.
-- 분기 뒤에 Q를 붙이며 모든 분기에 데이터가 있어 별도로 빈 분기를 생성할 필요가 없다.
-- 