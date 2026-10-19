SELECT d.ID, d.EMAIL, d.FIRST_NAME, d.LAST_NAME
FROM DEVELOPERS AS d
WHERE EXISTS (
    SELECT 1
    FROM SKILLCODES AS s
    WHERE s.NAME IN ('Python', 'C#')
      AND (d.SKILL_CODE & s.CODE) <> 0
)
ORDER BY d.ID

-- 전체 코드 줄별 설명
-- SELECT d.ID, d.EMAIL, d.FIRST_NAME, d.LAST_NAME  -- SELECT는 개발자의 ID·이메일·이름·성 열 선택.
-- FROM DEVELOPERS AS d  -- FROM은 개발자 테이블, AS d는 별칭.
-- WHERE EXISTS (  -- WHERE는 행 조건. EXISTS는 하위 쿼리 결과가 한 행이라도 있는지 검사.
--     SELECT 1  -- 존재 여부만 중요하므로 상수 1을 반환하는 하위 쿼리.
--     FROM SKILLCODES AS s  -- 기술 이름·비트 코드 표 조회.
--     WHERE s.NAME IN ('Python', 'C#')  -- IN은 목록 포함 여부. 목표 언어 두 개 중 하나 선택.
--       AND (d.SKILL_CODE & s.CODE) <> 0  -- AND는 모두 참, &는 비트 AND, <>는 다름. 목표 기술 비트가 개발자 코드에 켜져 있는지 검사.
-- )  -- EXISTS 하위 쿼리 종료.
-- ORDER BY d.ID  -- 개발자 ID 오름차순 정렬.

-- 풀이 요약
-- 기술 이름으로 Python·C#의 비트를 찾고 개발자의 비트 코드와 AND해 하나라도 있으면 선택한다.
-- EXISTS는 존재 여부만 반환하므로 두 언어를 모두 가진 개발자도 중복 행 없이 한 번만 출력된다.
-- 