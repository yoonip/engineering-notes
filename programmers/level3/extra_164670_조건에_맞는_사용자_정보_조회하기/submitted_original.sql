SELECT u.USER_ID, u.NICKNAME,
       CONCAT_WS(' ', u.CITY, u.STREET_ADDRESS1, u.STREET_ADDRESS2) AS `전체주소`,
       CONCAT(SUBSTRING(u.TLNO, 1, 3), '-', SUBSTRING(u.TLNO, 4, 4), '-', SUBSTRING(u.TLNO, 8, 4)) AS `전화번호`
FROM USED_GOODS_USER AS u
WHERE u.USER_ID IN (
    SELECT WRITER_ID
    FROM USED_GOODS_BOARD
    GROUP BY WRITER_ID
    HAVING COUNT(*) >= 3
)
ORDER BY u.USER_ID DESC

-- 전체 코드 줄별 설명
-- SELECT u.USER_ID, u.NICKNAME,  -- SELECT는 출력 열 선택. u.는 사용자 테이블의 열.
--        CONCAT_WS(' ', u.CITY, u.STREET_ADDRESS1, u.STREET_ADDRESS2) AS `전체주소`,  -- CONCAT_WS는 첫 문자열을 구분자로 나머지를 연결하며 NULL은 건너뜀. 백틱은 한글 열 이름 같은 식별자를 감쌈.
--        CONCAT(SUBSTRING(u.TLNO, 1, 3), '-', SUBSTRING(u.TLNO, 4, 4), '-', SUBSTRING(u.TLNO, 8, 4)) AS `전화번호`  -- SUBSTRING(문자열,시작,길이)는 1부터 세어 부분 추출. CONCAT으로 3-4-4자리 전화번호 구성.
-- FROM USED_GOODS_USER AS u  -- FROM은 사용자 테이블, AS는 별칭.
-- WHERE u.USER_ID IN (  -- WHERE는 조건, IN은 목록에 포함되는지 검사. 게시글 3개 이상인 작성자만 선택.
--     SELECT WRITER_ID  -- 하위 쿼리에서 작성자 ID 출력.
--     FROM USED_GOODS_BOARD  -- 게시글 테이블 조회.
--     GROUP BY WRITER_ID  -- 작성자별로 묶음.
--     HAVING COUNT(*) >= 3  -- HAVING은 집계 조건. COUNT(*)는 게시글 행 수, >=는 이상.
-- )  -- IN 하위 쿼리 종료.
-- ORDER BY u.USER_ID DESC  -- 사용자 ID 내림차순 정렬.

-- 풀이 요약
-- 게시글을 작성자별로 세어 세 건 이상인 사용자를 고른다. 주소는 공백 하나로 연결하고 전화번호에 두 하이픈을 넣는다.
-- IN 하위 쿼리로 필터링하므로 같은 사용자의 게시글 수만큼 사용자 행이 중복되지 않는다. 상세 주소가 NULL이면 CONCAT_WS가 그 항목을 건너뛴다.
-- 