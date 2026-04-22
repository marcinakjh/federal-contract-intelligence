SELECT fullParentPathName, COUNT(*) as contract_count
FROM contracts
GROUP BY fullParentPathName
ORDER BY contract_count desc;