SELECT b.BOOK_ID, a.AUTHOR_NAME, DATE_FORMAT(b.PUBLISHED_DATE, '%Y-%m-%d') AS PUBLISHED_DATE
FROM BOOK AS b
JOIN AUTHOR AS a ON a.AUTHOR_ID = b.AUTHOR_ID
WHERE b.CATEGORY = '경제'
ORDER BY b.PUBLISHED_DATE

-- 전체 코드 줄별 설명
-- SELECT b.BOOK_ID, a.AUTHOR_NAME, DATE_FORMAT(b.PUBLISHED_DATE, '%Y-%m-%d') AS PUBLISHED_DATE  -- SELECT는 도서 ID·저자명·출판일 출력. DATE_FORMAT은 날짜 형식 지정. %Y·%m·%d는 연·월·일, AS는 별칭.
-- FROM BOOK AS b  -- 도서 정보를 b로 조회.
-- JOIN AUTHOR AS a ON a.AUTHOR_ID = b.AUTHOR_ID  -- JOIN·ON으로 저자 ID가 같은 저자 정보 연결.
-- WHERE b.CATEGORY = '경제'  -- WHERE는 행 조건. 경제 분야 도서만 선택.
-- ORDER BY b.PUBLISHED_DATE  -- 실제 출판 날짜 오름차순 정렬.

-- 풀이 요약
-- 도서의 AUTHOR_ID로 저자명을 찾아 연결하고 경제 카테고리만 선택한다.
-- 출판일은 연-월-일로 표시하고 빠른 날짜부터 출력한다. 판매 기록이나 가격은 이 문제에 필요 없다.
-- 