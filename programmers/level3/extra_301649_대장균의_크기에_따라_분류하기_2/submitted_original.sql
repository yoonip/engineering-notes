SELECT ID,
       CASE NTILE(4) OVER (ORDER BY SIZE_OF_COLONY DESC)
           WHEN 1 THEN 'CRITICAL'
           WHEN 2 THEN 'HIGH'
           WHEN 3 THEN 'MEDIUM'
           ELSE 'LOW'
       END AS COLONY_NAME
FROM ECOLI_DATA
ORDER BY ID

-- 전체 코드 줄별 설명
-- SELECT ID,  -- SELECT는 출력할 열 선택. ID는 개체 번호, 쉼표는 다음 출력 열 구분.
--        CASE NTILE(4) OVER (ORDER BY SIZE_OF_COLONY DESC)  -- CASE는 조건별 값 선택. NTILE(4)는 행을 네 균등 그룹으로 나누는 윈도 함수, OVER는 적용 순서, DESC는 크기 내림차순.
--            WHEN 1 THEN 'CRITICAL'  -- WHEN·THEN은 값이 1인 그룹의 출력 문자열 지정. 작은따옴표는 문자열.
--            WHEN 2 THEN 'HIGH'  -- 두 번째 25% 그룹의 이름.
--            WHEN 3 THEN 'MEDIUM'  -- 세 번째 25% 그룹의 이름.
--            ELSE 'LOW'  -- ELSE는 나머지 경우. 네 번째 그룹의 이름.
--        END AS COLONY_NAME  -- END는 CASE 종료. AS는 출력 열에 별칭 부여.
-- FROM ECOLI_DATA  -- FROM은 조회할 테이블 지정.
-- ORDER BY ID  -- ORDER BY는 결과 정렬. 기본 ASC는 오름차순. 주석을 포함한 하나의 SELECT 문으로 제출.

-- 풀이 요약
-- 크기 내림차순으로 정렬한 순서를 NTILE(4)로 네 등분하고 각 그룹에 이름을 붙인다.
-- 전체 개수는 4의 배수이며 동일 크기가 다른 그룹으로 나뉘지 않는다는 조건이 있으므로 정확히 25%씩 분류할 수 있다.
-- 마지막 출력은 크기 순서가 아니라 ID 오름차순이다. 정렬을 포함해 일반적으로 O(N log N).
-- 