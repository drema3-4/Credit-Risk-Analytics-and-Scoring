--------------------------------------------------------------
--03-1-- Сегменты клиентов по наличию просрочек
--------------------------------------------------------------
WITH dpd_segments AS (
SELECT
    CASE
        WHEN num_30_59_days_late = 0 AND num_60_89_days_late = 0 AND num_90_days_late = 0 THEN 'No DPD'
        WHEN num_30_59_days_late > 0 AND num_30_59_days_late NOT IN (96, 98) OR
                num_60_89_days_late > 0 AND num_60_89_days_late NOT IN (96, 98) OR
                num_90_days_late > 0 AND num_90_days_late NOT IN (96, 98)
                THEN 'Previous DPD'
        WHEN num_30_59_days_late IN (96, 98) AND
                num_60_89_days_late IN (96, 98) AND
                num_90_days_late IN (96, 98)
                THEN 'Special Code'
    END AS segment,
    CASE
        WHEN num_30_59_days_late = 0 AND num_60_89_days_late = 0 AND num_90_days_late = 0 THEN 1
        WHEN num_30_59_days_late > 0 AND num_30_59_days_late NOT IN (96, 98) OR
                num_60_89_days_late > 0 AND num_60_89_days_late NOT IN (96, 98) OR
                num_90_days_late > 0 AND num_90_days_late NOT IN (96, 98)
                THEN 2
        WHEN num_30_59_days_late IN (96, 98) AND
                num_60_89_days_late IN (96, 98) AND
                num_90_days_late IN (96, 98)
                THEN 3
    END AS severity_order,
    *
FROM borrowers
)
SELECT
    segment, 
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS portfolio_share,
    SUM(target) AS bads,
    AVG(target) AS bad_rate
FROM dpd_segments
GROUP BY segment
ORDER BY severity_order;
--------------------------------------------------------------
--03-2-- Сегменты клиентов с разными просрочками
--------------------------------------------------------------
WITH dpd_segments AS (
SELECT
    CASE
        WHEN num_30_59_days_late = 0 AND num_60_89_days_late = 0 AND num_90_days_late = 0 THEN 'No DPD'
        WHEN num_30_59_days_late > 0 AND num_30_59_days_late NOT IN (96, 98) AND
             num_60_89_days_late = 0 AND num_90_days_late = 0
             THEN '30-59 DPD'
        WHEN num_60_89_days_late > 0 AND num_60_89_days_late NOT IN (96, 98) AND
             num_30_59_days_late = 0 AND num_90_days_late = 0
             THEN '60-89 DPD'
        WHEN num_90_days_late > 0 AND num_90_days_late NOT IN (96, 98) AND
             num_30_59_days_late = 0 AND num_60_89_days_late = 0
             THEN '90+ DPD'
        WHEN num_30_59_days_late IN (96, 98) AND
             num_60_89_days_late IN (96, 98) AND
             num_90_days_late IN (96, 98)
             THEN 'Special Code'
        ELSE 'Several DPD'
    END AS segment,
    CASE
        WHEN num_30_59_days_late = 0 AND num_60_89_days_late = 0 AND num_90_days_late = 0 THEN 1
        WHEN num_30_59_days_late > 0 AND num_30_59_days_late NOT IN (96, 98) AND
             num_60_89_days_late = 0 AND num_90_days_late = 0
             THEN 2
        WHEN num_60_89_days_late > 0 AND num_60_89_days_late NOT IN (96, 98) AND
             num_30_59_days_late = 0 AND num_90_days_late = 0
             THEN 3
        WHEN num_90_days_late > 0 AND num_90_days_late NOT IN (96, 98) AND
             num_30_59_days_late = 0 AND num_60_89_days_late = 0
             THEN 4
        WHEN num_30_59_days_late IN (96, 98) AND
             num_60_89_days_late IN (96, 98) AND
             num_90_days_late IN (96, 98)
             THEN 6
        ELSE 5
    END AS severity_order,
    *
FROM borrowers
)
SELECT 
    segment, 
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS portfolio_share,
    SUM(target) AS bads,
    AVG(target) AS bad_rate,
    AVG(target) / (SUM(SUM(target)) OVER() * 1.0 / SUM(COUNT(*)) OVER()) AS lift
FROM dpd_segments
GROUP BY segment
ORDER BY severity_order;
--------------------------------------------------------------
--03-3-- Сегменты клиентов с разными просрочками (модифицированный вариант)
--------------------------------------------------------------
WITH dpd_segments AS (
SELECT
    CASE
        WHEN num_30_59_days_late = 0 AND num_60_89_days_late = 0 AND num_90_days_late = 0 THEN 'No DPD'
        WHEN num_30_59_days_late > 0 AND num_30_59_days_late NOT IN (96, 98) AND
             num_60_89_days_late = 0 AND num_90_days_late = 0
             THEN '30-59 DPD'
        WHEN num_60_89_days_late > 0 AND num_60_89_days_late NOT IN (96, 98) AND
             num_30_59_days_late = 0 AND num_90_days_late = 0
             THEN '60-89 DPD'
        WHEN num_90_days_late > 0 AND num_90_days_late NOT IN (96, 98) AND
             num_30_59_days_late = 0 AND num_60_89_days_late = 0
             THEN '90+ DPD'
        WHEN num_30_59_days_late > 0 AND num_30_59_days_late NOT IN (96, 98) AND
             num_60_89_days_late > 0 AND num_60_89_days_late NOT IN (96, 98) AND
             num_90_days_late = 0
             THEN '30-59 + 60-89 DPD'
        WHEN num_30_59_days_late > 0 AND num_30_59_days_late NOT IN (96, 98) AND
             num_90_days_late > 0 AND num_90_days_late NOT IN (96, 98) AND
             num_60_89_days_late = 0
             THEN '30-59 + 90+ DPD'
        WHEN num_60_89_days_late > 0 AND num_60_89_days_late NOT IN (96, 98) AND
             num_90_days_late > 0 AND num_90_days_late NOT IN (96, 98) AND
             num_30_59_days_late = 0
             THEN '60-89 + 90+ DPD'
        WHEN num_30_59_days_late > 0 AND num_30_59_days_late NOT IN (96, 98) AND
             num_60_89_days_late > 0 AND num_60_89_days_late NOT IN (96, 98) AND
             num_90_days_late > 0 AND num_90_days_late NOT IN (96, 98)
             THEN 'ALL DPD'
        WHEN num_30_59_days_late IN (96, 98) AND
             num_60_89_days_late IN (96, 98) AND
             num_90_days_late IN (96, 98)
             THEN 'Special Code'
        ELSE 'Several DPD'
    END AS segment,
    CASE
        WHEN num_30_59_days_late = 0 AND num_60_89_days_late = 0 AND num_90_days_late = 0 THEN 1
        WHEN num_30_59_days_late > 0 AND num_30_59_days_late NOT IN (96, 98) AND
             num_60_89_days_late = 0 AND num_90_days_late = 0
             THEN 2
        WHEN num_60_89_days_late > 0 AND num_60_89_days_late NOT IN (96, 98) AND
             num_30_59_days_late = 0 AND num_90_days_late = 0
             THEN 3
        WHEN num_90_days_late > 0 AND num_90_days_late NOT IN (96, 98) AND
             num_30_59_days_late = 0 AND num_60_89_days_late = 0
             THEN 4
        WHEN num_30_59_days_late > 0 AND num_30_59_days_late NOT IN (96, 98) AND
             num_60_89_days_late > 0 AND num_60_89_days_late NOT IN (96, 98) AND
             num_90_days_late = 0
             THEN 5
        WHEN num_30_59_days_late > 0 AND num_30_59_days_late NOT IN (96, 98) AND
             num_90_days_late > 0 AND num_90_days_late NOT IN (96, 98) AND
             num_60_89_days_late = 0
             THEN 6
        WHEN num_60_89_days_late > 0 AND num_60_89_days_late NOT IN (96, 98) AND
             num_90_days_late > 0 AND num_90_days_late NOT IN (96, 98) AND
             num_30_59_days_late = 0
             THEN 7
        WHEN num_30_59_days_late > 0 AND num_30_59_days_late NOT IN (96, 98) AND
             num_60_89_days_late > 0 AND num_60_89_days_late NOT IN (96, 98) AND
             num_90_days_late > 0 AND num_90_days_late NOT IN (96, 98)
             THEN 8
        WHEN num_30_59_days_late IN (96, 98) AND
             num_60_89_days_late IN (96, 98) AND
             num_90_days_late IN (96, 98)
             THEN 9
    END AS severity_order,
    *
FROM borrowers
)
SELECT 
    segment, 
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS portfolio_share,
    SUM(target) AS bads,
    AVG(target) AS bad_rate,
    AVG(target) / (SUM(SUM(target)) OVER() * 1.0 / SUM(COUNT(*)) OVER()) AS lift,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() AS bad_share
FROM dpd_segments
GROUP BY segment
ORDER BY severity_order;
--------------------------------------------------------------
--03-4-- Кумулятивный охват bad borrowers по сегментам просрочек
--------------------------------------------------------------
WITH dpd_segments AS (
SELECT
    CASE
        WHEN num_30_59_days_late > 0 AND num_30_59_days_late NOT IN (96, 98) THEN '30-59 DPD'
        WHEN num_60_89_days_late > 0 AND num_60_89_days_late NOT IN (96, 98) THEN '60-89 DPD'
        WHEN num_90_days_late > 0 AND num_90_days_late NOT IN (96, 98) THEN '90+ DPD'
        ELSE 'No DPD OR Special Codes'
    END AS segment,
    CASE
        WHEN num_30_59_days_late > 0 AND num_30_59_days_late NOT IN (96, 98) THEN 1
        WHEN num_60_89_days_late > 0 AND num_60_89_days_late NOT IN (96, 98) THEN 2
        WHEN num_90_days_late > 0 AND num_90_days_late NOT IN (96, 98) THEN 3
        ELSE 4
    END AS severity_order,
    target
FROM borrowers
)
SELECT 
    segment, 
    SUM(COUNT(*)) OVER(ORDER BY severity_order ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_borrowers,
    SUM(SUM(target)) OVER(ORDER BY severity_order ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_bads
FROM dpd_segments
GROUP BY segment;