SELECT F.FLAVOR
FROM FIRST_HALF AS F
JOIN ICECREAM_INFO AS I ON F.FLAVOR = I.FLAVOR
WHERE F.TOTAL_ORDER > 3000 AND I.INGREDIENT_TYPE = 'fruit_based'
ORDER BY F.TOTAL_ORDER DESC

-- 전체 코드 줄별 설명
-- SELECT F.FLAVOR  -- SELECT는 출력 열 선택. F 별칭의 아이스크림 맛 조회.
-- FROM FIRST_HALF AS F  -- FROM은 상반기 주문 테이블, AS는 별칭 지정.
-- JOIN ICECREAM_INFO AS I ON F.FLAVOR = I.FLAVOR  -- JOIN·ON은 같은 맛의 주문·성분 정보를 연결.
-- WHERE F.TOTAL_ORDER > 3000 AND I.INGREDIENT_TYPE = 'fruit_based'  -- WHERE는 필터, AND는 모두 만족. 주문량 3000 초과이면서 과일 성분인 맛 선택.
-- ORDER BY F.TOTAL_ORDER DESC  -- ORDER BY는 정렬, DESC는 내림차순. 주문량 큰 순서로 출력.

-- 풀이 요약
-- 맛을 기준으로 두 테이블을 연결한 뒤 주문량과 성분 조건을 함께 적용합니다.
-- 