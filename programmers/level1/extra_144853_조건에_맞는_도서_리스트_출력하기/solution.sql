SELECT BOOK_ID, DATE_FORMAT(PUBLISHED_DATE, '%Y-%m-%d') AS PUBLISHED_DATE
FROM BOOK
WHERE CATEGORY = '인문'
  AND PUBLISHED_DATE >= '2021-01-01' AND PUBLISHED_DATE < '2022-01-01'
ORDER BY PUBLISHED_DATE

-- 전체 코드 줄별 설명
-- SELECT BOOK_ID, DATE_FORMAT(PUBLISHED_DATE, '%Y-%m-%d') AS PUBLISHED_DATE  -- SELECT는 조회, DATE_FORMAT은 연-월-일 형식 지정, AS는 출력 열 별칭.
-- FROM BOOK  -- FROM은 도서 정보 테이블 지정.
-- WHERE CATEGORY = '인문'  -- WHERE는 필터, =은 같음 비교. 인문 도서 선택.
--   AND PUBLISHED_DATE >= '2021-01-01' AND PUBLISHED_DATE < '2022-01-01'  -- AND는 모두 만족. 2021년에 출판된 도서로 범위 제한.
-- ORDER BY PUBLISHED_DATE  -- ORDER BY는 정렬. 출판일 오름차순 출력.

-- 풀이 요약
-- 카테고리와 출판 연도 조건을 동시에 적용하고 출판일 순으로 정렬합니다.
-- 