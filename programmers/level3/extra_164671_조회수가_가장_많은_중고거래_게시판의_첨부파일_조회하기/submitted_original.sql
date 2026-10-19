SELECT CONCAT('/home/grep/src/', f.BOARD_ID, '/', f.FILE_ID, f.FILE_NAME, f.FILE_EXT) AS FILE_PATH
FROM USED_GOODS_FILE AS f
JOIN USED_GOODS_BOARD AS b ON b.BOARD_ID = f.BOARD_ID
WHERE b.VIEWS = (SELECT MAX(VIEWS) FROM USED_GOODS_BOARD)
ORDER BY f.FILE_ID DESC

-- 전체 코드 줄별 설명
-- SELECT CONCAT('/home/grep/src/', f.BOARD_ID, '/', f.FILE_ID, f.FILE_NAME, f.FILE_EXT) AS FILE_PATH  -- SELECT는 출력 열 선택. CONCAT은 여러 문자열을 순서대로 연결, AS는 경로 열 별칭.
-- FROM USED_GOODS_FILE AS f  -- 첨부파일 테이블을 f로 조회.
-- JOIN USED_GOODS_BOARD AS b ON b.BOARD_ID = f.BOARD_ID  -- JOIN·ON으로 파일과 해당 게시글을 게시글 ID로 연결.
-- WHERE b.VIEWS = (SELECT MAX(VIEWS) FROM USED_GOODS_BOARD)  -- WHERE는 행 조건. 괄호 안 하위 쿼리로 전체 조회수 최댓값을 구해 해당 글만 선택.
-- ORDER BY f.FILE_ID DESC  -- 파일 ID 내림차순 정렬. 경로 문자열 전체로 정렬하지 않음.

-- 풀이 요약
-- 가장 많이 조회한 게시글의 첨부파일만 선택한 뒤 기본 경로/게시글 ID/파일 ID+이름+확장자를 연결한다.
-- 확장자에는 점이 포함되어 있으므로 점을 다시 넣지 않는다. 최다 조회 게시물은 하나라는 조건이 있다.
-- 