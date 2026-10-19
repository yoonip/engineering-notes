SELECT ID,
       -- NTILE(4)는 행을 네 균등 그룹으로 나누는 윈도 함수, OVER는 적용 순서, DESC는 크기 내림차순.
       CASE NTILE(4) OVER (ORDER BY SIZE_OF_COLONY DESC)
           WHEN 1 THEN 'CRITICAL'
           -- 두 번째 25% 그룹의 이름.
           WHEN 2 THEN 'HIGH'
           WHEN 3 THEN 'MEDIUM'
           ELSE 'LOW'
       -- AS는 출력 열에 별칭 부여.
       END AS COLONY_NAME
FROM ECOLI_DATA
ORDER BY ID
