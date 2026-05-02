-- ============================================================
-- Query 3: Contract Posting Volume by Month
-- ============================================================
-- Purpose: Aggregates contract opportunities by year-month to
--          surface seasonality in posting activity. Reveals the
--          federal "use it or lose it" budget cycle, where postings
--          peak in July through September ahead of the fiscal
--          year-end on September 30, then drop in October.
--
-- Notes: postedDate is stored as TEXT in the source table, so it
--        is cast to DATE before being formatted to 'YYYY-MM' for
--        clean monthly grouping. Sorted chronologically.
--
-- Output: Two columns: month ('YYYY-MM' format) and contract_count
--         (number of opportunities posted in that month).
-- Used in: Dashboard panel showing posting volume over time.
-- ============================================================

SELECT
    TO_CHAR(postedDate::date, 'YYYY-MM') AS month,
    COUNT(*) AS contract_count
FROM contracts
GROUP BY month
ORDER BY month ASC;
