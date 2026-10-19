-- 아이템 관계로 부모와 자식 정보를 연결한다. 부모의 희귀도를 검사하고 자식 정보를 내림차순 ID로 출력한다.
SELECT child.ITEM_ID, child.ITEM_NAME, child.RARITY
FROM ITEM_INFO AS child
JOIN ITEM_TREE AS tree ON tree.ITEM_ID = child.ITEM_ID
JOIN ITEM_INFO AS parent ON parent.ITEM_ID = tree.PARENT_ITEM_ID
WHERE parent.RARITY = 'RARE'
ORDER BY child.ITEM_ID DESC
