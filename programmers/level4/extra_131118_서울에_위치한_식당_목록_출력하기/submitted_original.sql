SELECT i.REST_ID, i.REST_NAME, i.FOOD_TYPE, i.FAVORITES, i.ADDRESS,
       ROUND(AVG(r.REVIEW_SCORE), 2) AS SCORE
FROM REST_INFO AS i
JOIN REST_REVIEW AS r ON i.REST_ID = r.REST_ID
WHERE i.ADDRESS LIKE '서울%'
GROUP BY i.REST_ID, i.REST_NAME, i.FOOD_TYPE, i.FAVORITES, i.ADDRESS
ORDER BY SCORE DESC, i.FAVORITES DESC

-- 전체 코드 줄별 설명
-- SELECT i.REST_ID, i.REST_NAME, i.FOOD_TYPE, i.FAVORITES, i.ADDRESS,  -- SELECT는 결과 열 선택. 식당 기본 정보를 출력.
--        ROUND(AVG(r.REVIEW_SCORE), 2) AS SCORE  -- AVG는 평균, ROUND(x,2)는 소수점 둘째 자리까지 반올림. AS로 SCORE라는 열 이름 지정.
-- FROM REST_INFO AS i  -- 식당 테이블에 i라는 별명 지정.
-- JOIN REST_REVIEW AS r ON i.REST_ID = r.REST_ID  -- JOIN으로 식당별 리뷰 연결. 리뷰가 없는 식당은 제외.
-- WHERE i.ADDRESS LIKE '서울%'  -- LIKE는 문자열 패턴 비교. %는 뒤에 어떤 문자열이 와도 허용.
-- GROUP BY i.REST_ID, i.REST_NAME, i.FOOD_TYPE, i.FAVORITES, i.ADDRESS  -- GROUP BY는 식당별 묶음 생성. 각 식당의 리뷰 평균을 계산.
-- ORDER BY SCORE DESC, i.FAVORITES DESC  -- DESC는 내림차순. 평점이 높을수록 먼저, 같으면 즐겨찾기 수가 많은 순서.

-- 풀이 요약
-- 서울 주소의 식당과 리뷰를 연결한 뒤 식당별 평균 평점을 소수 둘째 자리까지 계산합니다.
-- 예: 평균 4.666…은 4.67로 표시합니다. 리뷰가 없는 식당은 평균을 낼 수 없어 제외합니다.
-- 