-- u.는 사용자 테이블의 열.
SELECT u.USER_ID, u.NICKNAME,
       -- 백틱은 한글 열 이름 같은 식별자를 감쌈.
       CONCAT_WS(' ', u.CITY, u.STREET_ADDRESS1, u.STREET_ADDRESS2) AS `전체주소`,
       -- CONCAT으로 3-4-4자리 전화번호 구성.
       CONCAT(SUBSTRING(u.TLNO, 1, 3), '-', SUBSTRING(u.TLNO, 4, 4), '-', SUBSTRING(u.TLNO, 8, 4)) AS `전화번호`
-- FROM은 사용자 테이블, AS는 별칭.
FROM USED_GOODS_USER AS u
-- 게시글 3개 이상인 작성자만 선택.
WHERE u.USER_ID IN (
    -- 하위 쿼리에서 작성자 ID 출력.
    SELECT WRITER_ID
    -- 게시글 테이블 조회.
    FROM USED_GOODS_BOARD
    -- 작성자별로 묶음.
    GROUP BY WRITER_ID
    -- COUNT(*)는 게시글 행 수, >=는 이상.
    HAVING COUNT(*) >= 3
)
-- 사용자 ID 내림차순 정렬.
ORDER BY u.USER_ID DESC
