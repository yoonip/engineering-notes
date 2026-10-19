SELECT extracted.hour_value AS HOUR, COUNT(*) AS COUNT
FROM (SELECT HOUR(DATETIME) AS hour_value FROM ANIMAL_OUTS) AS extracted
WHERE extracted.hour_value >= 9 AND extracted.hour_value < 20
GROUP BY extracted.hour_value
ORDER BY extracted.hour_value;
