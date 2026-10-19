SELECT ID,
       CASE
           WHEN SIZE_OF_COLONY <= 100 THEN 'LOW'
           WHEN SIZE_OF_COLONY <= 1000 THEN 'MEDIUM'
           ELSE 'HIGH'
       END AS SIZE
FROM ECOLI_DATA
ORDER BY ID

-- 전체 코드 줄별 설명
-- SELECT ID,  -- SELECT는 출력 열 선택. ID는 개체 번호, 쉼표는 다음 열 구분.
--        CASE  -- CASE는 조건에 따라 다른 값을 만드는 표현식.
--            WHEN SIZE_OF_COLONY <= 100 THEN 'LOW'  -- WHEN은 조건, <=는 이하, THEN은 참일 때의 값. 작은따옴표는 문자열.
--            WHEN SIZE_OF_COLONY <= 1000 THEN 'MEDIUM'  -- 앞 조건이 거짓인 100 초과만 여기로 오므로 1000 이하를 중간 크기로 분류.
--            ELSE 'HIGH'  -- ELSE는 나머지 경우. 1000 초과.
--        END AS SIZE  -- END는 CASE 종료, AS는 결과 열 이름을 SIZE로 지정.
-- FROM ECOLI_DATA  -- FROM은 조회할 테이블 지정.
-- ORDER BY ID  -- ORDER BY는 정렬. 기본 오름차순으로 개체 번호 출력.

-- 풀이 요약
-- 크기 100 이하·1000 이하·나머지 순서로 CASE 조건을 검사한다. 먼저 만족한 조건의 이름이 선택된다.
-- 100은 LOW, 1000은 MEDIUM이므로 경계에서 <=를 사용한다. 최종 결과는 ID 오름차순.
-- 