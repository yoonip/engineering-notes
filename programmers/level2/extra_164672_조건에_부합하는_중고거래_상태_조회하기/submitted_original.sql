SELECT BOARD_ID, WRITER_ID, TITLE, PRICE,
       CASE STATUS
           WHEN 'SALE' THEN '판매중'
           WHEN 'RESERVED' THEN '예약중'
           WHEN 'DONE' THEN '거래완료'
       END AS STATUS
FROM USED_GOODS_BOARD
WHERE CREATED_DATE >= '2022-10-05' AND CREATED_DATE < '2022-10-06'
ORDER BY BOARD_ID DESC

-- 전체 코드 줄별 설명
-- SELECT BOARD_ID, WRITER_ID, TITLE, PRICE,  -- SELECT는 게시글 ID·작성자 ID·제목·가격을 순서대로 출력.
--        CASE STATUS  -- CASE는 STATUS 값에 따라 다른 문자열 선택.
--            WHEN 'SALE' THEN '판매중'  -- WHEN·THEN은 값이 일치할 때의 출력. 작은따옴표는 문자열.
--            WHEN 'RESERVED' THEN '예약중'  -- 예약 상태를 한글로 변환.
--            WHEN 'DONE' THEN '거래완료'  -- 완료 상태를 한글로 변환.
--        END AS STATUS  -- END는 CASE 종료, AS는 변환 결과 열 이름 지정.
-- FROM USED_GOODS_BOARD  -- 중고 거래 게시글 테이블 조회.
-- WHERE CREATED_DATE >= '2022-10-05' AND CREATED_DATE < '2022-10-06'  -- WHERE는 행 필터, AND는 모두 참. 10월 5일 하루에 등록된 글만 선택.
-- ORDER BY BOARD_ID DESC  -- 게시글 ID 내림차순 정렬.

-- 풀이 요약
-- 등록일이 2022년 10월 5일인 글만 남기고 영어 상태 코드 세 개를 CASE로 한글에 대응시킨다.
-- 거래 완료일이 아니라 게시글 등록일 기준이다. 날짜 범위를 다음 날 미만으로 잡으면 시간이 포함되어도 하루 전체가 선택된다.
-- 