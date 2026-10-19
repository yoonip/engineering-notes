-- CONCAT은 여러 문자열을 순서대로 연결, AS는 경로 열 별칭.
SELECT CONCAT('/home/grep/src/', f.BOARD_ID, '/', f.FILE_ID, f.FILE_NAME, f.FILE_EXT) AS FILE_PATH
-- 첨부파일 테이블을 f로 조회.
FROM USED_GOODS_FILE AS f
-- JOIN·ON으로 파일과 해당 게시글을 게시글 ID로 연결.
JOIN USED_GOODS_BOARD AS b ON b.BOARD_ID = f.BOARD_ID
-- 괄호 안 하위 쿼리로 전체 조회수 최댓값을 구해 해당 글만 선택.
WHERE b.VIEWS = (SELECT MAX(VIEWS) FROM USED_GOODS_BOARD)
-- 경로 문자열 전체로 정렬하지 않음.
ORDER BY f.FILE_ID DESC
