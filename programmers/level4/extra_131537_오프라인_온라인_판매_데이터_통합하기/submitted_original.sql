SELECT DATE_FORMAT(SALES_DATE, '%Y-%m-%d') AS SALES_DATE, PRODUCT_ID, USER_ID, SALES_AMOUNT
FROM ONLINE_SALE
WHERE SALES_DATE >= '2022-03-01' AND SALES_DATE < '2022-04-01'
UNION ALL
SELECT DATE_FORMAT(SALES_DATE, '%Y-%m-%d'), PRODUCT_ID, NULL AS USER_ID, SALES_AMOUNT
FROM OFFLINE_SALE
WHERE SALES_DATE >= '2022-03-01' AND SALES_DATE < '2022-04-01'
ORDER BY SALES_DATE, PRODUCT_ID, USER_ID

-- 전체 코드 줄별 설명
-- SELECT DATE_FORMAT(SALES_DATE, '%Y-%m-%d') AS SALES_DATE, PRODUCT_ID, USER_ID, SALES_AMOUNT  -- SELECT는 출력 열 선택. DATE_FORMAT은 날짜를 연-월-일 문자열로 표시하며 AS는 열 이름 지정.
-- FROM ONLINE_SALE  -- 온라인 판매 기록 조회.
-- WHERE SALES_DATE >= '2022-03-01' AND SALES_DATE < '2022-04-01'  -- WHERE와 AND로 2022년 3월 기록만 선택.
-- UNION ALL  -- UNION ALL은 중복을 제거하지 않고 두 결과를 이어 붙임. 각 SELECT의 열 순서가 같아야 함.
-- SELECT DATE_FORMAT(SALES_DATE, '%Y-%m-%d'), PRODUCT_ID, NULL AS USER_ID, SALES_AMOUNT  -- 오프라인에는 회원 정보가 없으므로 NULL을 같은 열 위치에 배치.
-- FROM OFFLINE_SALE  -- 오프라인 판매 기록 조회.
-- WHERE SALES_DATE >= '2022-03-01' AND SALES_DATE < '2022-04-01'  -- 오프라인도 동일하게 3월 데이터만 유지.
-- ORDER BY SALES_DATE, PRODUCT_ID, USER_ID  -- 전체 합친 결과를 판매일→상품 ID→회원 ID 오름차순 정렬.

-- 풀이 요약
-- 온라인·오프라인에서 각각 3월 데이터를 선택하고 동일한 네 열 형태로 맞춰 UNION ALL로 합칩니다.
-- 오프라인의 USER_ID는 문자열 NULL이 아니라 값이 없음을 나타내는 SQL NULL입니다.
-- 