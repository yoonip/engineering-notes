SELECT HOUR(DATETIME) AS HOUR, COUNT(*) AS COUNT
FROM ANIMAL_OUTS
WHERE HOUR(DATETIME) BETWEEN 9 AND 19
GROUP BY HOUR(DATETIME)
ORDER BY HOUR

-- 전체 코드 줄별 설명
-- SELECT HOUR(DATETIME) AS HOUR, COUNT(*) AS COUNT  -- SELECT는 출력 열, HOUR는 시각의 시간 0~23 추출, COUNT(*)는 입양 건수, AS는 결과 별칭.
-- FROM ANIMAL_OUTS  -- 입양 기록 테이블 조회.
-- WHERE HOUR(DATETIME) BETWEEN 9 AND 19  -- WHERE는 행 조건. BETWEEN은 양 끝 포함. 9시부터 19시 59분 59초까지 선택.
-- GROUP BY HOUR(DATETIME)  -- 같은 시간대의 입양을 묶어 집계.
-- ORDER BY HOUR  -- 시간 숫자 오름차순 정렬.

-- 풀이 요약
-- 입양 시각에서 시 단위만 추출해 9~19인 기록을 센다. 19시는 포함하고 20시는 제외한다.
-- 19:00까지만 필터링하면 19:59 기록을 놓치므로 시간 추출 값으로 구간을 검사한다.
-- 