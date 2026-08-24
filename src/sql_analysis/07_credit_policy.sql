--------------------------------------------------------------
--07-1-- Сценарии и их approval bad rate
--------------------------------------------------------------
WITH cutoffs AS (
SELECT 0 AS reject_pct
UNION ALL SELECT 5
UNION ALL SELECT 10
UNION ALL SELECT 15
UNION ALL SELECT 20
UNION ALL SELECT 25
UNION ALL SELECT 30
),
borrowers_with_score AS (
SELECT b.borrower_id, b.target, s.score
FROM borrowers b
INNER JOIN borrowers_score s ON s.borrower_id = b.borrower_id
),
scored AS (
SELECT
    borrower_id,
    score,
    target,
    NTILE(100) OVER (
        ORDER BY score DESC, borrower_id
    ) AS risk_percentile
FROM borrowers_with_score
)
SELECT
    c.reject_pct,
    COUNT(*) AS total_borrowers,
    SUM(
        CASE
            WHEN s.risk_percentile <= c.reject_pct
            THEN 1
            ELSE 0
        END
    ) AS rejected,
    SUM(
        CASE
            WHEN s.risk_percentile > c.reject_pct
            THEN 1
            ELSE 0
        END
    ) AS approved,
    AVG(
        CASE
            WHEN s.risk_percentile > c.reject_pct
            THEN s.target * 1.0
        END
    ) AS approved_bad_rate
FROM scored s
CROSS JOIN cutoffs c
GROUP BY c.reject_pct
ORDER BY c.reject_pct;
--------------------------------------------------------------
--07-2-- Сценарии и сколько каждый отсекает bad events
--------------------------------------------------------------
WITH cutoffs AS (
SELECT 0 AS reject_pct
UNION ALL SELECT 5
UNION ALL SELECT 10
UNION ALL SELECT 15
UNION ALL SELECT 20
UNION ALL SELECT 25
UNION ALL SELECT 30
),
borrowers_with_score AS (
SELECT b.borrower_id, b.target, s.score
FROM borrowers b
INNER JOIN borrowers_score s ON s.borrower_id = b.borrower_id
),
scored AS (
SELECT
    borrower_id,
    score,
    target,
    NTILE(100) OVER (
        ORDER BY score DESC, borrower_id
    ) AS risk_percentile
FROM borrowers_with_score
)
SELECT
    c.reject_pct,
    COUNT(*) AS total_borrowers,
    SUM(
        CASE
            WHEN s.risk_percentile <= c.reject_pct
            THEN 1
            ELSE 0
        END
    ) AS rejected,
    SUM(
        CASE
            WHEN s.risk_percentile > c.reject_pct
            THEN 1
            ELSE 0
        END
    ) AS approved,
    SUM(
        CASE
            WHEN s.risk_percentile <= c.reject_pct
            THEN target
            ELSE 0
        END
    ) AS bads_rejected,
    SUM(
        CASE
            WHEN s.risk_percentile > c.reject_pct
            THEN target
            ELSE 0
        END
    ) AS bads_approved,
    AVG(
        CASE
            WHEN s.risk_percentile > c.reject_pct
            THEN s.target * 1.0
        END
    ) AS approved_bad_rate
FROM scored s
CROSS JOIN cutoffs c
GROUP BY c.reject_pct
ORDER BY c.reject_pct;
--------------------------------------------------------------
--07-3-- Качество approved части в разных сценариях
--------------------------------------------------------------
WITH cutoffs AS (
SELECT 0 AS reject_pct
UNION ALL SELECT 5
UNION ALL SELECT 10
UNION ALL SELECT 15
UNION ALL SELECT 20
UNION ALL SELECT 25
UNION ALL SELECT 30
),
borrowers_with_score AS (
SELECT b.borrower_id, b.target, s.score
FROM borrowers b
INNER JOIN borrowers_score s ON s.borrower_id = b.borrower_id
),
scored AS (
SELECT
    borrower_id,
    score,
    target,
    NTILE(100) OVER (
        ORDER BY score DESC, borrower_id
    ) AS risk_percentile
FROM borrowers_with_score
)
SELECT
    c.reject_pct,
    SUM(
        CASE
            WHEN s.risk_percentile > c.reject_pct
            THEN 1.0
            ELSE 0.0
        END
    ) AS approved,
    SUM(
        CASE
            WHEN s.risk_percentile > c.reject_pct
            THEN target * 1.0
            ELSE 0.0
        END
    ) / SUM(target) AS approved_bads_share,
    AVG(
        CASE
            WHEN s.risk_percentile > c.reject_pct
            THEN s.target * 1.0
        END
    ) AS approved_bad_rate
FROM scored s
CROSS JOIN cutoffs c
GROUP BY c.reject_pct
ORDER BY c.reject_pct;
--------------------------------------------------------------
--07-4-- Bads capture in rejected population
--------------------------------------------------------------
WITH cutoffs AS (
SELECT 0 AS reject_pct
UNION ALL SELECT 5
UNION ALL SELECT 10
UNION ALL SELECT 15
UNION ALL SELECT 20
UNION ALL SELECT 25
UNION ALL SELECT 30
),
borrowers_with_score AS (
SELECT b.borrower_id, b.target, s.score
FROM borrowers b
INNER JOIN borrowers_score s ON s.borrower_id = b.borrower_id
),
scored AS (
SELECT
    borrower_id,
    score,
    target,
    NTILE(100) OVER (
        ORDER BY score DESC, borrower_id
    ) AS risk_percentile
FROM borrowers_with_score
)
SELECT
    c.reject_pct AS reject_rate,
    SUM(
        CASE
            WHEN s.risk_percentile > c.reject_pct
            THEN 1.0
            ELSE 0.0
        END
    ) / COUNT(*) AS approved_rate,
    AVG(
        CASE
            WHEN s.risk_percentile > c.reject_pct
            THEN s.target * 1.0
        END
    ) AS approved_bad_rate,
    SUM (
        CASE
            WHEN s.risk_percentile <= c.reject_pct
            THEN target * 1.0
            ELSE 0
        END
    ) / SUM(target) AS bads_rejected_percent 
FROM scored s
CROSS JOIN cutoffs c
GROUP BY c.reject_pct
ORDER BY c.reject_pct;
--------------------------------------------------------------
--07-5-- Дополнительный эффект от повышения процента отсечения
--------------------------------------------------------------
WITH cutoffs AS (
SELECT 0 AS reject_pct
UNION ALL SELECT 5
UNION ALL SELECT 10
UNION ALL SELECT 15
UNION ALL SELECT 20
UNION ALL SELECT 25
UNION ALL SELECT 30
),
borrowers_with_score AS (
SELECT b.borrower_id, b.target, s.score
FROM borrowers b
INNER JOIN borrowers_score s ON s.borrower_id = b.borrower_id
),
scored AS (
SELECT
    borrower_id,
    score,
    target,
    NTILE(100) OVER (
        ORDER BY score DESC, borrower_id
    ) AS risk_percentile
FROM borrowers_with_score
),
scenario AS (
SELECT
    c.reject_pct AS reject_rate,
    AVG(
        CASE
            WHEN s.risk_percentile > c.reject_pct
            THEN s.target * 1.0
        END
    ) AS bad_rate,
    SUM (
        CASE
            WHEN s.risk_percentile <= c.reject_pct
            THEN target
            ELSE 0
        END
    ) AS bads_rejected 
FROM scored s
CROSS JOIN cutoffs c
GROUP BY c.reject_pct
)
SELECT
    reject_rate,
    bad_rate,
    LAG(bad_rate) OVER(ORDER BY reject_rate) - bad_rate AS delta_bad_rate,
    bads_rejected,
    bads_rejected - LAG(bads_rejected) OVER(ORDER BY reject_rate) AS additional_rejected_bads
FROM scenario