SELECT ID, LENGTH
FROM FISH_INFO
ORDER BY LENGTH DESC, ID ASC
LIMIT 10

-- 전체 코드 줄별 설명
-- SELECT ID, LENGTH  -- SELECT는 출력 열 선택. 쉼표로 ID와 길이 구분.
-- FROM FISH_INFO  -- FROM은 물고기 정보 테이블 지정.
-- ORDER BY LENGTH DESC, ID ASC  -- ORDER BY는 정렬, DESC는 내림차순, ASC는 오름차순. 길이 동률이면 ID가 작은 순.
-- LIMIT 10  -- LIMIT은 출력 행 수 제한. 정렬 결과 상위 10마리만 출력.

-- 풀이 요약
-- 길이가 큰 순서로 정렬하고 같은 길이는 ID 순으로 정렬한 뒤 앞 10행을 선택합니다.
-- 