SELECT i.ITEM_ID, i.ITEM_NAME
FROM ITEM_INFO AS i
JOIN ITEM_TREE AS tree ON tree.ITEM_ID = i.ITEM_ID
WHERE tree.PARENT_ITEM_ID IS NULL
ORDER BY i.ITEM_ID

-- 전체 코드 줄별 설명
-- SELECT i.ITEM_ID, i.ITEM_NAME  -- SELECT는 아이템 ID·이름 열 선택.
-- FROM ITEM_INFO AS i  -- FROM은 정보 테이블, AS i는 별칭.
-- JOIN ITEM_TREE AS tree ON tree.ITEM_ID = i.ITEM_ID  -- JOIN·ON으로 각 아이템의 부모 관계 연결.
-- WHERE tree.PARENT_ITEM_ID IS NULL  -- WHERE는 행 조건. IS NULL로 부모가 없는 ROOT 아이템 선택.
-- ORDER BY i.ITEM_ID  -- 아이템 ID 오름차순 정렬.

-- 풀이 요약
-- ROOT는 더 이상 업그레이드할 수 없는 잎이 아니라 이전 부모가 없는 시작 아이템이다.
-- 관계 테이블에서 PARENT_ITEM_ID가 NULL인 아이템을 고르고 정보 테이블에서 이름을 가져온다.
-- 