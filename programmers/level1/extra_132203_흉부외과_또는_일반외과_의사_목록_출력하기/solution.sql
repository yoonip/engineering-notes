SELECT DR_NAME, DR_ID, MCDP_CD, DATE_FORMAT(HIRE_YMD, '%Y-%m-%d') AS HIRE_YMD
FROM DOCTOR
WHERE MCDP_CD IN ('CS', 'GS')
ORDER BY HIRE_YMD DESC, DR_NAME ASC

-- 전체 코드 줄별 설명
-- SELECT DR_NAME, DR_ID, MCDP_CD, DATE_FORMAT(HIRE_YMD, '%Y-%m-%d') AS HIRE_YMD  -- SELECT는 출력 열 선택. DATE_FORMAT은 연-월-일 형식 변환, AS는 별칭.
-- FROM DOCTOR  -- FROM은 의사 정보 테이블 지정.
-- WHERE MCDP_CD IN ('CS', 'GS')  -- WHERE는 필터. IN은 목록 중 하나와 같은지 검사. 흉부외과 또는 일반외과 선택.
-- ORDER BY HIRE_YMD DESC, DR_NAME ASC  -- ORDER BY는 정렬. DESC는 고용일 내림차순, 같으면 ASC로 이름 오름차순.

-- 풀이 요약
-- 진료과가 CS나 GS인 의사를 고르고 고용일·이름 순으로 정렬합니다.
-- 