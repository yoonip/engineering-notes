-- 리뷰 수가 가장 많은 회원들의 모든 리뷰를 구합니다. 공동 최다인 회원도 포함하고 리뷰 날짜·리뷰 내용 오름차순입니다.
-- 회원별 리뷰 수를 먼저 세고 그 최댓값과 같은 회원을 모두 선택합니다. LIMIT 1은 공동 최다 회원을 빠뜨릴 수 있으므로 사용하지 않습니다.
WITH counts AS (SELECT MEMBER_ID,COUNT(*) AS cnt FROM REST_REVIEW GROUP BY MEMBER_ID)
SELECT m.MEMBER_NAME,r.REVIEW_TEXT,DATE_FORMAT(r.REVIEW_DATE,'%Y-%m-%d') AS REVIEW_DATE
FROM REST_REVIEW r JOIN MEMBER_PROFILE m ON m.MEMBER_ID=r.MEMBER_ID
JOIN counts c ON c.MEMBER_ID=r.MEMBER_ID
WHERE c.cnt=(SELECT MAX(cnt) FROM counts)
ORDER BY r.REVIEW_DATE,r.REVIEW_TEXT;
