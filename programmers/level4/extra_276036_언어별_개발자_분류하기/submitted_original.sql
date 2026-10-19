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

-- 전체 코드 줄별 설명
-- WITH skills AS (  -- WITH는 임시 결과인 공통 테이블 식 정의. skills라는 이름으로 스킬 비트 묶음 준비.
--     SELECT SUM(CASE WHEN CATEGORY = 'Front End' THEN CODE ELSE 0 END) AS front,  -- SUM은 합계. 프런트엔드 스킬 비트를 모두 합침.
--            MAX(CASE WHEN NAME = 'Python' THEN CODE ELSE 0 END) AS python,  -- CASE는 조건별 값 선택. Python의 비트 코드를 추출.
--            MAX(CASE WHEN NAME = 'C#' THEN CODE ELSE 0 END) AS csharp  -- MAX는 최댓값. C# 스킬 코드 하나를 추출.
--     FROM SKILLCODES  -- 스킬 이름·범주·코드가 저장된 테이블 조회.
-- ), classified AS (  -- 첫 임시 결과를 닫고, 개발자의 등급을 계산하는 두 번째 임시 결과 정의.
--     SELECT CASE WHEN (d.SKILL_CODE & s.front) > 0 AND (d.SKILL_CODE & s.python) > 0 THEN 'A'  -- &는 비트 AND. 프런트엔드와 Python 스킬을 모두 보유하면 A.
--                 WHEN (d.SKILL_CODE & s.csharp) > 0 THEN 'B'  -- 앞 조건에 해당하지 않고 C# 비트가 켜져 있으면 B.
--                 WHEN (d.SKILL_CODE & s.front) > 0 THEN 'C' END AS GRADE,  -- 나머지 프런트엔드 개발자는 C. ELSE 생략 시 해당하지 않으면 NULL.
--            d.ID, d.EMAIL  -- 개발자 식별자와 이메일을 함께 선택.
--     FROM DEVELOPERS AS d CROSS JOIN skills AS s  -- CROSS JOIN은 모든 행 조합. 한 행인 스킬 요약을 모든 개발자에 연결.
-- )  -- 등급 계산 임시 결과 종료.
-- SELECT GRADE, ID, EMAIL  -- 최종적으로 필요한 세 열을 출력.
-- FROM classified  -- 앞에서 계산한 개발자 등급 결과 조회.
-- WHERE GRADE IS NOT NULL  -- IS NOT NULL은 값이 존재함을 검사. 등급이 없는 개발자 제외.
-- ORDER BY GRADE, ID  -- 등급 우선, 같은 등급은 ID 오름차순 정렬.

-- 풀이 요약
-- 서로 다른 스킬은 서로 다른 비트이므로 & 결과가 0보다 크면 해당 스킬을 보유합니다.
-- A→B→C 순서로 CASE를 검사하여 여러 조건을 만족해도 가장 높은 등급 하나만 부여합니다.
-- 