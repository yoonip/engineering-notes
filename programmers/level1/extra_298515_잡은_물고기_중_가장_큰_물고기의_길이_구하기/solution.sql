SELECT CONCAT(MAX(LENGTH), 'cm') AS MAX_LENGTH
FROM FISH_INFO

-- 전체 코드 줄별 설명
-- SELECT CONCAT(MAX(LENGTH), 'cm') AS MAX_LENGTH  -- MAX는 최댓값, CONCAT은 문자열 연결, AS는 별칭. 최대 길이에 단위 cm를 붙임.
-- FROM FISH_INFO  -- FROM은 조회할 물고기 정보 테이블 지정.

-- 풀이 요약
-- MAX는 NULL을 제외하고 최대 길이를 구합니다. 숫자 뒤에 cm를 붙여 한 행으로 출력합니다.
-- 