SELECT FLAVOR
FROM FIRST_HALF
ORDER BY TOTAL_ORDER DESC, SHIPMENT_ID ASC

-- 전체 코드 줄별 설명
-- SELECT FLAVOR  -- SELECT는 출력 열 선택. 아이스크림 맛만 조회.
-- FROM FIRST_HALF  -- FROM은 상반기 주문 테이블 지정.
-- ORDER BY TOTAL_ORDER DESC, SHIPMENT_ID ASC  -- ORDER BY는 정렬. DESC는 주문량 내림차순, 동률일 때 ASC로 출하 번호 오름차순.

-- 풀이 요약
-- 주문량이 같을 때의 두 번째 정렬 기준도 함께 지정합니다.
-- 