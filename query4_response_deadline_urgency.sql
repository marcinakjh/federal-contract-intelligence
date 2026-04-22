SELECT title, fullParentPathName, responseDeadLine
FROM contracts
WHERE responseDeadLine IS NOT NULL
ORDER BY responseDeadLine ASC
LIMIT 10;