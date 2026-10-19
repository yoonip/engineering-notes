-- SUM은 합계, AS는 총거래금액 열 이름.
SELECT u.USER_ID, u.NICKNAME, SUM(b.PRICE) AS TOTAL_SALES
-- 사용자 테이블 별칭 u.
FROM USED_GOODS_USER AS u
-- JOIN·ON으로 작성자 ID가 같은 게시글 연결.
JOIN USED_GOODS_BOARD AS b ON b.WRITER_ID = u.USER_ID
-- 완료 상태인 거래만 합계에 포함.
WHERE b.STATUS = 'DONE'
-- 회원 ID·닉네임별로 거래를 묶음.
GROUP BY u.USER_ID, u.NICKNAME
-- 완료 거래 합계가 70만 원 이상인 회원 선택.
HAVING SUM(b.PRICE) >= 700000
-- 총거래금액 오름차순 정렬.
ORDER BY TOTAL_SALES
