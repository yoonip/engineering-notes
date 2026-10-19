-- i.는 아이템 정보 테이블의 열 지정.
SELECT i.ITEM_ID, i.ITEM_NAME, i.RARITY
FROM ITEM_INFO AS i
-- 자식이 없어도 현재 행 유지.
LEFT JOIN ITEM_TREE AS child ON child.PARENT_ITEM_ID = i.ITEM_ID
WHERE child.ITEM_ID IS NULL
-- DESC는 큰 값부터.
ORDER BY i.ITEM_ID DESC
