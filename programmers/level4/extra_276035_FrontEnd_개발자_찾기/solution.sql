-- Front End 범주 기술을 하나 이상 가진 개발자의 ID·이메일·이름·성을 ID 오름차순으로 구합니다.
-- 개발자의 SKILL_CODE와 각 Front End CODE를 AND해 0이 아닌 기술이 존재하는지 확인합니다. EXISTS는 기술 개수와 관계없이 한 개발자를 한 번 반환합니다.
SELECT d.ID, d.EMAIL, d.FIRST_NAME, d.LAST_NAME
FROM DEVELOPERS AS d
WHERE EXISTS (
    SELECT 1
    FROM SKILLCODES AS s
    WHERE s.CATEGORY = 'Front End' AND (d.SKILL_CODE & s.CODE) > 0
)
ORDER BY d.ID
