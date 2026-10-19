SELECT WAREHOUSE_ID, WAREHOUSE_NAME, ADDRESS, IFNULL(FREEZER_YN, 'N') AS FREEZER_YN
FROM FOOD_WAREHOUSE
WHERE ADDRESS LIKE '경기도%'
ORDER BY WAREHOUSE_ID

-- 전체 코드 줄별 설명
-- SELECT WAREHOUSE_ID, WAREHOUSE_NAME, ADDRESS, IFNULL(FREEZER_YN, 'N') AS FREEZER_YN  -- SELECT는 열 조회. IFNULL은 NULL을 N으로 대체, AS는 출력 열 별칭.
-- FROM FOOD_WAREHOUSE  -- FROM은 식품창고 정보 테이블 지정.
-- WHERE ADDRESS LIKE '경기도%'  -- WHERE는 필터, LIKE는 패턴 검사. %는 뒤에 임의 문자열 허용. 경기도로 시작하는 주소 선택.
-- ORDER BY WAREHOUSE_ID  -- ORDER BY는 정렬. 기본 ASC로 창고 ID 오름차순.

-- 풀이 요약
-- 주소의 시작이 경기도인 창고를 고르고 냉동시설 정보가 없으면 N으로 표시합니다.
-- 