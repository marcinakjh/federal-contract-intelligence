SELECT type, COUNT(*) AS type_count
FROM contracts
GROUP BY type
ORDER BY type_count DESC;
