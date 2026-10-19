WITH ranked AS (
    SELECT ID, ROW_NUMBER() OVER (ORDER BY SIZE_OF_COLONY DESC) AS rn,
           COUNT(*) OVER () AS total
    FROM ECOLI_DATA
)
SELECT ID,
       CASE WHEN 4 * rn <= total THEN 'CRITICAL'
            WHEN 2 * rn <= total THEN 'HIGH'
            WHEN 4 * rn <= 3 * total THEN 'MEDIUM'
            ELSE 'LOW' END AS COLONY_NAME
FROM ranked
ORDER BY ID;
