-- 기술 코드 표에서 두 언어에 해당하는 행을 찾는다. 개발자 코드와 비트 AND한 값이 0이 아닌 행이 있는지 EXISTS로 확인한다.
SELECT d.ID, d.EMAIL, d.FIRST_NAME, d.LAST_NAME
FROM DEVELOPERS AS d
WHERE EXISTS (
    SELECT 1
    FROM SKILLCODES AS s
    WHERE s.NAME IN ('Python', 'C#')
      AND (d.SKILL_CODE & s.CODE) <> 0
)
ORDER BY d.ID
