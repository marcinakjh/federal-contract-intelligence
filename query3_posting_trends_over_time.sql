SELECT COUNT(*) AS contract_count,
TO_CHAR(postedDate::date, 'YYYY-MM') AS month
FROM contracts
GROUP BY month
ORDER BY month ASC;
