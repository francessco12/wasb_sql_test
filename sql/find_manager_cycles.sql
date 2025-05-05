-- Find manager approval loops (e.g. A manages B, B manages A)
-- Recursive CTE that follows reporting chains and detects cycles

WITH RECURSIVE management_chain (employee_id, manager_id, path, has_loop) AS (
    SELECT
        employee_id,
        manager_id,
        CAST(ARRAY[employee_id] AS ARRAY<TINYINT>) AS path,
        FALSE AS has_loop
    FROM memory.default.employee

    UNION ALL

    SELECT
        mc.employee_id,
        m.manager_id,
        mc.path || m.manager_id,
        m.manager_id = mc.path[1] AS has_loop
    FROM management_chain mc
    JOIN memory.default.employee m
        ON mc.manager_id = m.employee_id
    WHERE NOT contains(mc.path, m.manager_id)
)

SELECT DISTINCT
    employee_id,
    path
FROM management_chain
WHERE has_loop = TRUE;

