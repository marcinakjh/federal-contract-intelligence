-- ============================================================
-- Query 4: Upcoming Response Deadlines
-- ============================================================
-- Purpose: Lists the 10 contract opportunities with the earliest
--          upcoming response deadlines, filtered to records with
--          a non-null deadline. Used during analysis to surface
--          time-sensitive opportunities and validate deadline data
--          quality before building the dashboard view.
--
-- Output: Three columns: title, fullParentPathName (agency), and
--         responseDeadLine, ordered from soonest to latest.
-- Used in: Exploratory inspection. The dashboard's deadline panels
--          are built directly in Tableau against the full dataset.
-- ============================================================

SELECT title, fullParentPathName, responseDeadLine
FROM contracts
WHERE responseDeadLine IS NOT NULL
ORDER BY responseDeadLine ASC
LIMIT 10;
