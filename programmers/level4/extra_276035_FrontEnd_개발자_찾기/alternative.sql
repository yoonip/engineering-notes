-- Front End 코드의 합으로 범주 마스크를 만들고 한 번의 비트 AND로 확인합니다. CODE가 서로 다른 2의 거듭제곱이라는 조건이 필요합니다.
SELECT d.ID,d.EMAIL,d.FIRST_NAME,d.LAST_NAME FROM DEVELOPERS d
WHERE (d.SKILL_CODE & (SELECT SUM(CODE) FROM SKILLCODES WHERE CATEGORY='Front End'))>0 ORDER BY d.ID;
