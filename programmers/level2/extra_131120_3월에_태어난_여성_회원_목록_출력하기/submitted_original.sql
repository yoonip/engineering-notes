SELECT MEMBER_ID, MEMBER_NAME, GENDER, DATE_FORMAT(DATE_OF_BIRTH, '%Y-%m-%d') AS DATE_OF_BIRTH
FROM MEMBER_PROFILE
WHERE GENDER = 'W'
  AND MONTH(DATE_OF_BIRTH) = 3
  AND TLNO IS NOT NULL
ORDER BY MEMBER_ID

-- 전체 코드 줄별 설명
-- SELECT MEMBER_ID, MEMBER_NAME, GENDER, DATE_FORMAT(DATE_OF_BIRTH, '%Y-%m-%d') AS DATE_OF_BIRTH  -- SELECT는 출력 열, DATE_FORMAT은 날짜를 연-월-일 문자열로 표시, AS는 열 이름 유지.
-- FROM MEMBER_PROFILE  -- 회원 정보 테이블 조회.
-- WHERE GENDER = 'W'  -- WHERE는 행 조건. 여성 코드 W인 회원만 선택.
--   AND MONTH(DATE_OF_BIRTH) = 3  -- AND는 모두 참. MONTH는 날짜에서 월 추출. 생일이 3월인지 검사.
--   AND TLNO IS NOT NULL  -- IS NOT NULL은 값이 존재하는지 확인. 연락처 미등록 회원 제외.
-- ORDER BY MEMBER_ID  -- 회원 ID 오름차순 정렬.

-- 풀이 요약
-- 여성·3월 생일·전화번호 존재 세 조건을 모두 만족해야 한다. 전화번호 열은 출력하지 않아도 필터에 사용할 수 있다.
-- 특정 출생 연도는 요구하지 않으므로 월만 검사한다. 날짜 표시 형식은 시간 없이 연-월-일이다.
-- 