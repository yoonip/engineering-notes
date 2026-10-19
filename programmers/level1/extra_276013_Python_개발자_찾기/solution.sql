SELECT ID, EMAIL, FIRST_NAME, LAST_NAME
FROM DEVELOPER_INFOS
WHERE 'Python' IN (SKILL_1, SKILL_2, SKILL_3)
ORDER BY ID

-- 전체 코드 줄별 설명
-- SELECT ID, EMAIL, FIRST_NAME, LAST_NAME  -- SELECT는 출력 열 선택. 쉼표로 ID·이메일·이름·성 구분.
-- FROM DEVELOPER_INFOS  -- FROM은 개발자 정보 테이블 지정.
-- WHERE 'Python' IN (SKILL_1, SKILL_2, SKILL_3)  -- WHERE는 필터, IN은 괄호 안 값 중 하나와 같은지 검사. 세 스킬 중 Python 보유자 선택.
-- ORDER BY ID  -- ORDER BY는 정렬. 기본 ASC로 ID 오름차순 정렬.

-- 풀이 요약
-- 세 스킬 열 중 하나라도 Python인 개발자를 조회하고 ID 순으로 정렬합니다.
-- 