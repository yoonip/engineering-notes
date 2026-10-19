SELECT ROUND(AVG(IFNULL(LENGTH, 10)), 2) AS AVERAGE_LENGTH
FROM FISH_INFO

-- 전체 코드 줄별 설명
-- SELECT ROUND(AVG(IFNULL(LENGTH, 10)), 2) AS AVERAGE_LENGTH  -- IFNULL(값,대체값)은 NULL 대체, AVG는 평균, ROUND(값,2)는 소수 둘째 자리까지 반올림, AS는 별칭.
-- FROM FISH_INFO  -- FROM은 물고기 정보 테이블 지정.

-- 풀이 요약
-- NULL 길이를 10으로 바꾼 뒤 평균을 구하고 소수 셋째 자리에서 반올림합니다.
-- 