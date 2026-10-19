-- LEGEND 행만 필터하고 SUM으로 가격을 더한다. 그룹 구분이 없으므로 전체 합계 한 행을 출력한다.
SELECT SUM(PRICE) AS TOTAL_PRICE
FROM ITEM_INFO
WHERE RARITY = 'LEGEND'
