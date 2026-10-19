-- 주소가 서울로 시작하고 리뷰가 있는 식당의 평균 리뷰점수를 소수 둘째 자리까지 반올림합니다. 점수·즐겨찾기 내림차순입니다.
-- 식당별 리뷰 평균을 구하려면 식당 ID로 묶습니다. ROUND는 평균을 계산한 뒤 적용하고 리뷰 없는 식당은 내부 조인으로 제외합니다.
SELECT i.REST_ID, i.REST_NAME, i.FOOD_TYPE, i.FAVORITES, i.ADDRESS,
       ROUND(AVG(r.REVIEW_SCORE), 2) AS SCORE
FROM REST_INFO AS i
JOIN REST_REVIEW AS r ON i.REST_ID = r.REST_ID
WHERE i.ADDRESS LIKE '서울%'
GROUP BY i.REST_ID, i.REST_NAME, i.FOOD_TYPE, i.FAVORITES, i.ADDRESS
ORDER BY SCORE DESC, i.FAVORITES DESC
