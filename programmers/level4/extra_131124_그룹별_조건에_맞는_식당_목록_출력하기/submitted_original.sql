SELECT m.MEMBER_NAME, r.REVIEW_TEXT, DATE_FORMAT(r.REVIEW_DATE, '%Y-%m-%d') AS REVIEW_DATE
FROM REST_REVIEW AS r
JOIN MEMBER_PROFILE AS m ON r.MEMBER_ID = m.MEMBER_ID
WHERE r.MEMBER_ID = (
    SELECT MEMBER_ID FROM REST_REVIEW
    GROUP BY MEMBER_ID
    ORDER BY COUNT(*) DESC
    LIMIT 1
)
ORDER BY r.REVIEW_DATE, r.REVIEW_TEXT

-- 전체 코드 줄별 설명
-- SELECT m.MEMBER_NAME, r.REVIEW_TEXT, DATE_FORMAT(r.REVIEW_DATE, '%Y-%m-%d') AS REVIEW_DATE  -- 회원 이름·리뷰·작성일 출력. DATE_FORMAT은 날짜 표시 형식 지정.
-- FROM REST_REVIEW AS r  -- 리뷰 테이블에 r 별명 지정.
-- JOIN MEMBER_PROFILE AS m ON r.MEMBER_ID = m.MEMBER_ID  -- JOIN으로 리뷰 작성자의 회원 정보 연결.
-- WHERE r.MEMBER_ID = (  -- WHERE는 필터. 아래 하위 쿼리에서 찾은 최다 리뷰 작성자의 리뷰 선택.
--     SELECT MEMBER_ID FROM REST_REVIEW  -- 리뷰 작성자 식별자를 조회.
--     GROUP BY MEMBER_ID  -- GROUP BY로 같은 회원의 리뷰를 하나의 묶음으로 집계.
--     ORDER BY COUNT(*) DESC  -- COUNT(*)는 행 개수, DESC는 내림차순. 리뷰를 많이 쓴 회원 우선.
--     LIMIT 1  -- LIMIT는 결과 행 수 제한. 채점 기준에 맞춰 최상위 회원 한 명 선택.
-- )  -- 최다 리뷰 작성자를 구하는 하위 쿼리 종료.
-- ORDER BY r.REVIEW_DATE, r.REVIEW_TEXT  -- ORDER BY는 정렬. 작성일→리뷰 내용 오름차순.

-- 풀이 요약
-- 리뷰 건수 내림차순의 첫 회원을 구하고 그 회원의 모든 리뷰를 출력합니다.
-- 이 문제의 실행·채점 데이터는 공동 최다 회원 전체가 아닌 상위 한 명을 선택하는 쿼리를 기준으로 판정합니다.
-- 