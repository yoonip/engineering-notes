-- 부모 번호와 실제 자식 수 출력.
SELECT p.ID, COUNT(c.ID) AS CHILD_COUNT
FROM ECOLI_DATA AS p
-- 같은 테이블을 자식 c로 다시 조회해 부모 번호가 같은 행을 연결.
LEFT JOIN ECOLI_DATA AS c ON c.PARENT_ID = p.ID
GROUP BY p.ID
-- ORDER BY는 ID 오름차순 정렬.
ORDER BY p.ID
