-- A는 Front End 기술과 Python을 모두 보유, B는 A가 아니면서 C# 보유, C는 앞 두 등급이 아니면서 Front End 보유입니다. 해당 개발자만 등급·ID·이메일을 등급과 ID 오름차순으로 구합니다.
-- 기술 코드는 서로 다른 비트이므로 비트 AND로 보유 여부를 확인합니다. CASE를 A→B→C 순서로 평가해 등급 우선순위를 지킵니다.
WITH skills AS (
    SELECT SUM(CASE WHEN CATEGORY = 'Front End' THEN CODE ELSE 0 END) AS front,
           MAX(CASE WHEN NAME = 'Python' THEN CODE ELSE 0 END) AS python,
           MAX(CASE WHEN NAME = 'C#' THEN CODE ELSE 0 END) AS csharp
    FROM SKILLCODES
), classified AS (
    SELECT CASE WHEN (d.SKILL_CODE & s.front) > 0 AND (d.SKILL_CODE & s.python) > 0 THEN 'A'
                WHEN (d.SKILL_CODE & s.csharp) > 0 THEN 'B'
                WHEN (d.SKILL_CODE & s.front) > 0 THEN 'C' END AS GRADE,
           d.ID, d.EMAIL
    FROM DEVELOPERS AS d CROSS JOIN skills AS s
)
SELECT GRADE, ID, EMAIL
FROM classified
WHERE GRADE IS NOT NULL
ORDER BY GRADE, ID
