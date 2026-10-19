SELECT d.ID, d.EMAIL, d.FIRST_NAME, d.LAST_NAME
FROM DEVELOPERS AS d
WHERE EXISTS (
    SELECT 1
    FROM SKILLCODES AS s
    WHERE s.CATEGORY = 'Front End' AND (d.SKILL_CODE & s.CODE) > 0
)
ORDER BY d.ID

-- 전체 코드 줄별 설명
-- SELECT d.ID, d.EMAIL, d.FIRST_NAME, d.LAST_NAME  -- SELECT는 출력 열 지정. d.은 개발자 테이블 별명.
-- FROM DEVELOPERS AS d  -- FROM은 조회 테이블, AS는 별명을 지정.
-- WHERE EXISTS (  -- WHERE는 필터. EXISTS는 안쪽 조회 결과가 한 행이라도 있으면 참.
--     SELECT 1  -- 실제 값 대신 존재 여부만 필요하므로 상수 1을 선택.
--     FROM SKILLCODES AS s  -- 스킬 코드 테이블에 s라는 별명을 지정.
--     WHERE s.CATEGORY = 'Front End' AND (d.SKILL_CODE & s.CODE) > 0  -- AND는 두 조건 모두 참. &는 비트 AND로 해당 스킬 보유 여부 검사.
-- )  -- 존재 여부를 확인하는 하위 쿼리를 닫음. 여러 스킬이 있어도 개발자 한 행만 출력.
-- ORDER BY d.ID  -- ORDER BY는 정렬. ID 오름차순.

-- 풀이 요약
-- 개발자마다 보유 스킬 중 프런트엔드 스킬이 하나라도 있는지 EXISTS로 확인합니다.
-- 예: React와 Vue를 모두 알아도 같은 개발자를 중복 출력하지 않습니다.
-- 