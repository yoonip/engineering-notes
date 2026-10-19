SELECT SUM(PRICE) AS TOTAL_PRICE
FROM ITEM_INFO
WHERE RARITY = 'LEGEND'

-- 전체 코드 줄별 설명
-- SELECT SUM(PRICE) AS TOTAL_PRICE  -- SELECT는 결과 열 선택. SUM은 가격 합계, AS는 출력 열 이름 지정.
-- FROM ITEM_INFO  -- FROM은 아이템 정보 테이블 지정.
-- WHERE RARITY = 'LEGEND'  -- WHERE는 합산 전 행 필터. =는 같음, 작은따옴표는 문자열. 전설 희귀도 아이템만 합산.

-- 풀이 요약
-- LEGEND 아이템 행만 고른 다음 가격 합계를 한 행으로 반환한다.
-- 종류별 집계를 요구하지 않으므로 GROUP BY는 필요 없다. 개수 COUNT나 평균 AVG가 아닌 합계 SUM을 사용한다.
-- 