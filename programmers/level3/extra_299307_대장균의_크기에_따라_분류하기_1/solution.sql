SELECT ID,
       CASE
           -- 작은따옴표는 문자열.
           WHEN SIZE_OF_COLONY <= 100 THEN 'LOW'
           WHEN SIZE_OF_COLONY <= 1000 THEN 'MEDIUM'
           ELSE 'HIGH'
       END AS SIZE
-- FROM은 조회할 테이블 지정.
FROM ECOLI_DATA
ORDER BY ID
