-- ============================================================
-- Query 1: Contract Volume by Federal Agency
-- ============================================================
-- Purpose: Counts the number of contract opportunities posted by
--          each federal agency (or sub-agency hierarchy) and ranks
--          them in descending order. Surfaces which agencies dominate
--          procurement activity in the dataset.
--
-- Output: Two columns: fullParentPathName (the agency hierarchy
--         string from SAM.gov) and contract_count (number of
--         opportunities posted by that agency).
-- Used in: Dashboard panel showing agency activity concentration.
-- ============================================================

SELECT fullParentPathName, COUNT(*) AS contract_count
FROM contracts
GROUP BY fullParentPathName
ORDER BY contract_count DESC;
