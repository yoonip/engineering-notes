SELECT i.ITEM_ID, i.ITEM_NAME, i.RARITY
FROM ITEM_INFO AS i
LEFT JOIN ITEM_TREE AS child ON child.PARENT_ITEM_ID = i.ITEM_ID
WHERE child.ITEM_ID IS NULL
ORDER BY i.ITEM_ID DESC

-- 전체 코드 줄별 설명
-- SELECT i.ITEM_ID, i.ITEM_NAME, i.RARITY  -- SELECT는 출력 열 선택. i.는 아이템 정보 테이블의 열 지정.
-- FROM ITEM_INFO AS i  -- FROM은 조회 테이블, AS i는 별칭.
-- LEFT JOIN ITEM_TREE AS child ON child.PARENT_ITEM_ID = i.ITEM_ID  -- LEFT JOIN으로 현재 아이템을 부모로 갖는 업그레이드 결과를 연결. 자식이 없어도 현재 행 유지.
-- WHERE child.ITEM_ID IS NULL  -- WHERE는 행 조건. IS NULL은 연결된 자식이 없는지 검사. = NULL은 사용하지 않음.
-- ORDER BY i.ITEM_ID DESC  -- 아이템 ID 내림차순 정렬. DESC는 큰 값부터.

-- 풀이 요약
-- 업그레이드 가능한 다음 아이템이 없는 노드, 즉 트리의 잎을 찾는다. 현재 아이템이 다른 행의 부모로 등장하는지를 왼쪽 조인한다.
-- 자식의 ITEM_ID가 NULL인 행만 남기면 더 업그레이드할 수 없는 아이템이다. 자기 부모가 NULL인 ROOT를 찾는 문제와 다르다.
-- 