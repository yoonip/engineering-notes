SELECT child.ITEM_ID, child.ITEM_NAME, child.RARITY
FROM ITEM_INFO AS child
JOIN ITEM_TREE AS tree ON tree.ITEM_ID = child.ITEM_ID
JOIN ITEM_INFO AS parent ON parent.ITEM_ID = tree.PARENT_ITEM_ID
WHERE parent.RARITY = 'RARE'
ORDER BY child.ITEM_ID DESC

-- 전체 코드 줄별 설명
-- SELECT child.ITEM_ID, child.ITEM_NAME, child.RARITY  -- SELECT는 다음 업그레이드 결과인 자식 아이템의 정보를 출력.
-- FROM ITEM_INFO AS child  -- 아이템 테이블을 자식 역할로 조회.
-- JOIN ITEM_TREE AS tree ON tree.ITEM_ID = child.ITEM_ID  -- JOIN·ON으로 현재 아이템의 부모 관계 연결.
-- JOIN ITEM_INFO AS parent ON parent.ITEM_ID = tree.PARENT_ITEM_ID  -- 아이템 테이블을 부모 역할로 다시 조인.
-- WHERE parent.RARITY = 'RARE'  -- WHERE는 행 조건. 부모 아이템의 희귀도가 RARE인 경우 선택.
-- ORDER BY child.ITEM_ID DESC  -- 출력할 자식 아이템 ID 내림차순 정렬.

-- 풀이 요약
-- 관계 테이블의 PARENT_ITEM_ID로 이전 단계 아이템을 찾고, 부모가 RARE인지 검사한다.
-- 모든 자손을 재귀 탐색하는 것이 아니라 바로 다음 업그레이드 아이템만 출력한다. 결과 아이템 자체가 RARE일 필요는 없다.
-- 