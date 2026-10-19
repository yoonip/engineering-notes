-- 재귀 CTE로 루트부터 세대 번호를 붙입니다. 깊이를 3으로 제한해 불필요한 후손 확장을 막습니다.
WITH RECURSIVE generations AS (
 SELECT ID,1 AS generation FROM ECOLI_DATA WHERE PARENT_ID IS NULL
 UNION ALL
 SELECT e.ID,g.generation+1 FROM ECOLI_DATA e JOIN generations g ON e.PARENT_ID=g.ID WHERE g.generation<3
)
SELECT ID FROM generations WHERE generation=3 ORDER BY ID;
