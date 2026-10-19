SELECT u.USER_ID, u.NICKNAME, SUM(b.PRICE) AS TOTAL_SALES
FROM USED_GOODS_USER AS u
JOIN USED_GOODS_BOARD AS b ON b.WRITER_ID = u.USER_ID
WHERE b.STATUS = 'DONE'
GROUP BY u.USER_ID, u.NICKNAME
HAVING SUM(b.PRICE) >= 700000
ORDER BY TOTAL_SALES

-- 전체 코드 줄별 설명
-- SELECT u.USER_ID, u.NICKNAME, SUM(b.PRICE) AS TOTAL_SALES  -- SELECT는 출력 열 선택. SUM은 합계, AS는 총거래금액 열 이름.
-- FROM USED_GOODS_USER AS u  -- 사용자 테이블 별칭 u.
-- JOIN USED_GOODS_BOARD AS b ON b.WRITER_ID = u.USER_ID  -- JOIN·ON으로 작성자 ID가 같은 게시글 연결.
-- WHERE b.STATUS = 'DONE'  -- WHERE는 집계 전 행 필터. 완료 상태인 거래만 합계에 포함.
-- GROUP BY u.USER_ID, u.NICKNAME  -- 회원 ID·닉네임별로 거래를 묶음.
-- HAVING SUM(b.PRICE) >= 700000  -- HAVING은 그룹 집계 조건. 완료 거래 합계가 70만 원 이상인 회원 선택.
-- ORDER BY TOTAL_SALES  -- 총거래금액 오름차순 정렬.

-- 풀이 요약
-- 완료 거래만 WHERE로 먼저 고르고 회원별 가격 합계를 구한다. 합계 조건은 HAVING에서 검사한다.
-- 진행 중인 거래까지 더한 뒤 상태를 검사하면 합계가 틀리므로 필터 순서를 구분한다.
-- 