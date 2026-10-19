SELECT YEAR(DIFFERENTIATION_DATE) AS YEAR,
       MAX(SIZE_OF_COLONY) OVER (PARTITION BY YEAR(DIFFERENTIATION_DATE)) - SIZE_OF_COLONY AS YEAR_DEV,
       ID
FROM ECOLI_DATA
ORDER BY YEAR, YEAR_DEV

-- 전체 코드 줄별 설명
-- SELECT YEAR(DIFFERENTIATION_DATE) AS YEAR,  -- SELECT는 출력 열 선택, YEAR(날짜)는 연도 추출, AS는 결과 열 별칭.
--        MAX(SIZE_OF_COLONY) OVER (PARTITION BY YEAR(DIFFERENTIATION_DATE)) - SIZE_OF_COLONY AS YEAR_DEV,  -- MAX는 최댓값. OVER·PARTITION BY는 행을 없애지 않고 같은 연도 그룹의 최댓값 계산. 자기 크기를 빼 편차 생성.
--        ID  -- 개체 ID도 함께 출력.
-- FROM ECOLI_DATA  -- 대장균 테이블 조회.
-- ORDER BY YEAR, YEAR_DEV  -- 연도 오름차순, 같은 연도는 편차 오름차순. 기본 방향은 ASC.

-- 풀이 요약
-- 연도마다 가장 큰 크기를 윈도 함수로 각 행에 붙인 뒤 각 개체 크기를 빼 편차를 만든다.
-- 연도별 한 행으로 합치는 GROUP BY를 쓰지 않고 모든 개체의 ID를 보존해야 한다.
-- 