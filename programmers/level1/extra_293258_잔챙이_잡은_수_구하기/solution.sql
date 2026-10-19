SELECT COUNT(*) AS FISH_COUNT
FROM FISH_INFO
WHERE LENGTH IS NULL

-- 전체 코드 줄별 설명
-- SELECT COUNT(*) AS FISH_COUNT  -- SELECT는 조회, COUNT(*)는 조건을 만족하는 행 개수, AS는 결과 열 이름 지정.
-- FROM FISH_INFO  -- FROM은 물고기 정보 테이블 지정.
-- WHERE LENGTH IS NULL  -- WHERE는 조건 필터. IS NULL은 값이 없음 검사. 10cm 이하 물고기는 NULL로 저장됨.

-- 풀이 요약
-- 10cm 이하 물고기는 LENGTH가 NULL이라는 저장 규칙을 이용해 해당 행을 셉니다.
-- 