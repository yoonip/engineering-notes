SELECT CAR_ID, CAR_TYPE, DAILY_FEE, OPTIONS
FROM CAR_RENTAL_COMPANY_CAR
WHERE OPTIONS LIKE '%네비게이션%'
ORDER BY CAR_ID DESC

-- 전체 코드 줄별 설명
-- SELECT CAR_ID, CAR_TYPE, DAILY_FEE, OPTIONS  -- SELECT는 출력 열 선택. 자동차 정보의 모든 열 조회.
-- FROM CAR_RENTAL_COMPANY_CAR  -- FROM은 자동차 정보 테이블 지정.
-- WHERE OPTIONS LIKE '%네비게이션%'  -- WHERE는 필터, LIKE는 패턴 비교, %는 임의 길이 문자열. 옵션에 네비게이션 포함 여부 검사.
-- ORDER BY CAR_ID DESC  -- ORDER BY는 정렬, DESC는 내림차순. 자동차 ID가 큰 순으로 출력.

-- 풀이 요약
-- 옵션 문자열에 네비게이션이 포함된 자동차만 고릅니다.
-- 