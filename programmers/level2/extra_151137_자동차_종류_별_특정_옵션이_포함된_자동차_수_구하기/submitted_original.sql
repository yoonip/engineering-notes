SELECT CAR_TYPE, COUNT(*) AS CARS
FROM CAR_RENTAL_COMPANY_CAR
WHERE OPTIONS LIKE '%통풍시트%'
   OR OPTIONS LIKE '%열선시트%'
   OR OPTIONS LIKE '%가죽시트%'
GROUP BY CAR_TYPE
ORDER BY CAR_TYPE

-- 전체 코드 줄별 설명
-- SELECT CAR_TYPE, COUNT(*) AS CARS  -- SELECT는 출력 열, COUNT(*)는 자동차 행 수, AS는 별칭.
-- FROM CAR_RENTAL_COMPANY_CAR  -- 자동차 정보 테이블 조회.
-- WHERE OPTIONS LIKE '%통풍시트%'  -- WHERE는 행 조건. LIKE는 문자열 패턴 비교, %는 임의 길이 문자열. 옵션 목록 안에 통풍시트가 있는지 검사.
--    OR OPTIONS LIKE '%열선시트%'  -- OR는 하나라도 참이면 선택. 열선시트도 허용.
--    OR OPTIONS LIKE '%가죽시트%'  -- 가죽시트도 허용. 여러 옵션이 동시에 있어도 원래 자동차 행은 한 번만 선택됨.
-- GROUP BY CAR_TYPE  -- 같은 자동차 종류별로 묶어 수 집계.
-- ORDER BY CAR_TYPE  -- 자동차 종류 오름차순 정렬.

-- 풀이 요약
-- 옵션 문자열에 세 시트 옵션 중 하나라도 들어 있으면 해당 자동차를 선택한다. 조건 셋을 AND로 묶으면 모두 가진 자동차만 남아 틀린다.
-- 옵션 개수가 아니라 자동차 수를 세므로 각 행을 COUNT(*)로 한 번씩 센다.
-- 