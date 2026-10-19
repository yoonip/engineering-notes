SELECT FACTORY_ID, FACTORY_NAME, ADDRESS
FROM FOOD_FACTORY
WHERE ADDRESS LIKE '강원도%'
ORDER BY FACTORY_ID

-- 전체 코드 줄별 설명
-- SELECT FACTORY_ID, FACTORY_NAME, ADDRESS  -- SELECT는 출력 열 지정. 공장 ID·이름·주소 조회.
-- FROM FOOD_FACTORY  -- FROM은 식품공장 정보 테이블 지정.
-- WHERE ADDRESS LIKE '강원도%'  -- WHERE는 필터, LIKE는 패턴 비교, %는 임의 길이 문자열. 강원도로 시작하는 주소 선택.
-- ORDER BY FACTORY_ID  -- ORDER BY는 정렬. 공장 ID 오름차순 출력.

-- 풀이 요약
-- 강원도에 위치한 공장을 주소의 앞부분으로 골라냅니다.
-- 