SELECT p.ID, COUNT(c.ID) AS CHILD_COUNT
FROM ECOLI_DATA AS p
LEFT JOIN ECOLI_DATA AS c ON c.PARENT_ID = p.ID
GROUP BY p.ID
ORDER BY p.ID

-- 전체 코드 줄별 설명
-- SELECT p.ID, COUNT(c.ID) AS CHILD_COUNT  -- SELECT는 출력 열 선택, COUNT(열)은 NULL을 제외한 개수. AS는 결과 별칭. 부모 번호와 실제 자식 수 출력.
-- FROM ECOLI_DATA AS p  -- p는 부모 역할로 조회할 테이블 별칭.
-- LEFT JOIN ECOLI_DATA AS c ON c.PARENT_ID = p.ID  -- LEFT JOIN은 왼쪽 행을 모두 보존하는 결합. 같은 테이블을 자식 c로 다시 조회해 부모 번호가 같은 행을 연결.
-- GROUP BY p.ID  -- GROUP BY는 같은 부모 ID별로 묶어 자식 개수 집계.
-- ORDER BY p.ID  -- ORDER BY는 ID 오름차순 정렬.

-- 풀이 요약
-- 부모 행에 자식 행을 자기 조인한다. LEFT JOIN으로 자식 없는 부모도 남긴다.
-- COUNT(*)는 자식 없는 결합 행도 한 개로 세므로 COUNT(c.ID)를 사용해 0을 얻는다.
-- 