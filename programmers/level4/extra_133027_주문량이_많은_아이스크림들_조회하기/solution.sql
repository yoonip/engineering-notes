-- 상반기와 7월의 맛별 주문량을 합쳐 가장 많은 맛 세 개를 구합니다. 7월에는 같은 맛이 여러 출하 번호에 걸쳐 나타날 수 있습니다.
-- UNION ALL로 판매 기록을 모두 보존한 뒤 맛별 SUM으로 묶습니다. UNION은 동일한 수치의 실제 판매 행까지 지울 수 있어 적절하지 않습니다.
SELECT FLAVOR
FROM (
    SELECT FLAVOR, TOTAL_ORDER FROM FIRST_HALF
    UNION ALL
    SELECT FLAVOR, TOTAL_ORDER FROM JULY
) AS orders
GROUP BY FLAVOR
ORDER BY SUM(TOTAL_ORDER) DESC
LIMIT 3
