-- ============================================================
-- Query 2: Contract Volume by Type
-- ============================================================
-- Purpose: Counts the number of contract opportunities posted by
--          each contract type and ranks them in descending order.
--          Reveals the mix of procurement vehicles agencies use
--          most often.
--
-- Output: Two columns: type (the contract type label from SAM.gov)
--         and type_count (number of opportunities of that type).
-- Used in: Dashboard panel showing the breakdown of contract types
--          across the dataset.
-- ============================================================

SELECT type, COUNT(*) AS type_count
FROM contracts
GROUP BY type
ORDER BY type_count DESC;
