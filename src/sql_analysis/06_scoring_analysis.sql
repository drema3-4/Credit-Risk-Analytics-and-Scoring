--------------------------------------------------------------
--06-1-- заёмщики и их default score
--------------------------------------------------------------
SELECT *
FROM borrowers b
INNER JOIN borrowers_score s ON s.borrower_id = b.borrower_id;
--------------------------------------------------------------
--06-2-- Получение score deciles
--------------------------------------------------------------
SELECT
    *,
    NTILE(10) OVER (ORDER BY score) AS decile
FROM borrowers b
INNER JOIN borrowers_score s ON s.borrower_id = b.borrower_id
ORDER BY decile;
--------------------------------------------------------------
--06-3-- Формирование отчёта по deciles
--------------------------------------------------------------
WITH deciles AS (
SELECT
    b.borrower_id,
    b.target,
    s.score,
    NTILE(10) OVER (ORDER BY s.score) AS decile
FROM borrowers b
INNER JOIN borrowers_score s ON s.borrower_id = b.borrower_id
)
SELECT
    decile,
    COUNT(*) AS num_borrowers,
    AVG(score) AS avg_risk_score,
    AVG(target) AS bad_rate
FROM deciles
GROUP BY decile;
--------------------------------------------------------------
--06-4-- Bad distribution by decile
--------------------------------------------------------------
WITH deciles AS (
SELECT
    b.borrower_id,
    b.target,
    s.score,
    NTILE(10) OVER (ORDER BY s.score) AS decile
FROM borrowers b
INNER JOIN borrowers_score s ON s.borrower_id = b.borrower_id
)
SELECT
    decile,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS dataset_share,
    AVG(target) AS bad_rate,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() AS bads_share
FROM deciles
GROUP BY decile;
--------------------------------------------------------------
--06-5-- Cumulative bads in deciles
--------------------------------------------------------------
WITH deciles AS (
SELECT
    b.borrower_id,
    b.target,
    NTILE(10) OVER (ORDER BY s.score) AS decile
FROM borrowers b
INNER JOIN borrowers_score s ON s.borrower_id = b.borrower_id
)
SELECT
    decile,
    SUM(SUM(target)) OVER(ORDER BY decile ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) * 1.0 / SUM(SUM(target)) OVER() AS cumulative_bads_share
FROM deciles
GROUP BY decile;
--------------------------------------------------------------
--06-6-- Risk Grades
--------------------------------------------------------------
WITH borrowers_with_deciles AS (
SELECT *
FROM borrowers b
INNER JOIN borrowers_score s ON s.borrower_id = b.borrower_id
),
risk_segmented_borrowers AS (
SELECT
    borrower_id,
    score,
    target,
    CASE
        WHEN 0.0 <= score AND score <= 0.04 THEN '[0.0, 0.04]'
        WHEN 0.04 < score AND score <= 0.06 THEN '(0.04, 0.06]'
        WHEN 0.06 < score AND score <= 0.1 THEN '(0.06, 0.1]'
        WHEN 0.1 < score AND score <= 0.2 THEN '(0.1, 0.2]'
        WHEN score > 0.2 THEN '(0.2, inf]'
    END AS risk_segment,
    CASE
        WHEN 0.0 <= score AND score <= 0.04 THEN 'safest'
        WHEN 0.04 < score AND score <= 0.06 THEN 'low risk'
        WHEN 0.06 < score AND score <= 0.1 THEN 'medium risk'
        WHEN 0.1 < score AND score <= 0.2 THEN 'high risk'
        WHEN score > 0.2 THEN 'riskiest'
    END AS risk_grade,
    CASE
        WHEN 0.0 <= score AND score <= 0.04 THEN 1
        WHEN 0.04 < score AND score <= 0.06 THEN 2
        WHEN 0.06 < score AND score <= 0.1 THEN 3
        WHEN 0.1 < score AND score <= 0.2 THEN 4
        WHEN score > 0.2 THEN 5
    END AS severity_order
FROM borrowers_with_deciles
)
SELECT
    risk_grade,
    risk_segment,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS dataset_share,
    AVG(score) AS avg_pd,
    AVG(target) AS bad_rate,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() bads_share
FROM risk_segmented_borrowers
GROUP BY risk_grade, risk_segment, severity_order
ORDER BY severity_order;