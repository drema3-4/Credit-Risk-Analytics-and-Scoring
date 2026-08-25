import sqlite3
import pandas as pd

db_path = "D:\Pet Projects\Analytics\Credit Risk Analytics & Scoring\src\sql_analysis\db.db"
conn = sqlite3.connect(db_path)


query_vw_portfolio_summary = """
WITH borrowers_with_score AS (
SELECT b.borrower_id, b.target, s.score
FROM borrowers b
INNER JOIN borrowers_score s ON s.borrower_id = b.borrower_id
)
SELECT
    COUNT(*) AS borrowers,
    SUM(target) AS bads,
    AVG(target) AS bad_rate,
    AVG(score) AS avg_pd
FROM borrowers_with_score
"""

query_vw_risk_segments = """
WITH revolving_utilization_segments AS(
SELECT
    CASE
        WHEN revolving_utilization >= 0.0 AND revolving_utilization <= 0.2 THEN '[0.0, 0.2]'
        WHEN revolving_utilization > 0.2 AND revolving_utilization <= 0.4 THEN '(0.2, 0.4]'
        WHEN revolving_utilization > 0.4 AND revolving_utilization <= 0.5 THEN '(0.4, 0.5]'
        WHEN revolving_utilization > 0.5 AND revolving_utilization <= 0.7 THEN '(0.5, 0.7]'
        WHEN revolving_utilization > 0.7 AND revolving_utilization <= 1.0 THEN '(0.7, 1.0]'
        WHEN revolving_utilization > 1.0 AND revolving_utilization <= 2.0 THEN '(1.0, 2.0]'
        WHEN revolving_utilization > 2.0 AND revolving_utilization <= 5.0 THEN '(2.0, 5.0]'
        WHEN revolving_utilization > 5.0 THEN '(5.0, inf]'
    END AS segment,
    CASE
        WHEN revolving_utilization >= 0.0 AND revolving_utilization <= 0.2 THEN 1
        WHEN revolving_utilization > 0.2 AND revolving_utilization <= 0.4 THEN 2
        WHEN revolving_utilization > 0.4 AND revolving_utilization <= 0.5 THEN 3
        WHEN revolving_utilization > 0.5 AND revolving_utilization <= 0.7 THEN 4
        WHEN revolving_utilization > 0.7 AND revolving_utilization <= 1.0 THEN 5
        WHEN revolving_utilization > 1.0 AND revolving_utilization <= 2.0 THEN 6
        WHEN revolving_utilization > 2.0 AND revolving_utilization <= 5.0 THEN 7
        WHEN revolving_utilization > 5.0 THEN 8
    END AS severity_order,
    target
FROM borrowers
),
age_segments AS(
SELECT
    CASE
        WHEN age >= 0.0 AND age <= 22.0 THEN '[0.0, 22.0]'
        WHEN age > 22.0 AND age <= 30.0 THEN '(22.0, 30.0]'
        WHEN age > 30.0 AND age <= 45.0 THEN '(30.0, 45.0]'
        WHEN age > 45.0 AND age <= 55.0 THEN '(45.0, 55.0]'
        WHEN age > 55.0 AND age <= 75.0 THEN '(55.0, 75.0]'
        WHEN age > 75.0 THEN '(75.0, inf]'
    END AS segment,
    CASE
        WHEN age >= 0.0 AND age <= 22.0 THEN 1
        WHEN age > 22.0 AND age <= 30.0 THEN 2
        WHEN age > 30.0 AND age <= 45.0 THEN 3
        WHEN age > 45.0 AND age <= 55.0 THEN 4
        WHEN age > 55.0 AND age <= 75.0 THEN 5
        WHEN age > 75.0 THEN 6
    END AS severity_order,
    target
FROM borrowers
),
DPD_30_59_segments AS(
SELECT
    CASE
        WHEN num_30_59_days_late = 0 THEN '0'
        WHEN num_30_59_days_late >= 1 AND num_30_59_days_late <= 2 THEN '[1, 2]'
        WHEN num_30_59_days_late > 2 AND num_30_59_days_late <= 13 THEN '(2, 13]'
        WHEN num_30_59_days_late = 96 THEN '96'
        WHEN num_30_59_days_late = 98 THEN '98'
    END AS segment,
    CASE
        WHEN num_30_59_days_late = 0 THEN 1
        WHEN num_30_59_days_late >= 1 AND num_30_59_days_late <= 2 THEN 2
        WHEN num_30_59_days_late > 2 AND num_30_59_days_late <= 13 THEN 3
        WHEN num_30_59_days_late = 96 THEN 4
        WHEN num_30_59_days_late = 98 THEN 5
    END AS severity_order,
    target
FROM borrowers
),
debt_ratio_segments AS(
SELECT
    CASE
        WHEN debt_ratio >= 0.0 AND debt_ratio <= 0.1 THEN '[0.0, 0.1]'
        WHEN debt_ratio > 0.1 AND debt_ratio <= 0.7 THEN '(0.1, 0.7]'
        WHEN debt_ratio > 0.7 AND debt_ratio <= 1.0 THEN '(0.7, 1.0]'
        WHEN debt_ratio > 1.0 AND debt_ratio <= 4.0 THEN '(1.0, 4.0]'
        WHEN debt_ratio > 4.0 THEN '(4.0, inf]'
    END AS segment,
    CASE
        WHEN debt_ratio >= 0.0 AND debt_ratio <= 0.1 THEN 1
        WHEN debt_ratio > 0.1 AND debt_ratio <= 0.7 THEN 2
        WHEN debt_ratio > 0.7 AND debt_ratio <= 1.0 THEN 3
        WHEN debt_ratio > 1.0 AND debt_ratio <= 4.0 THEN 4
        WHEN debt_ratio > 4.0 THEN 5
    END AS severity_order,
    target
FROM borrowers
),
monthly_income_segments AS(
SELECT
    CASE
        WHEN monthly_income >= 0.0 AND monthly_income <= 900.0 THEN '[0.0, 900.0]'
        WHEN monthly_income > 900.0 AND monthly_income <= 3000.0 THEN '(900.0, 3000.0]'
        WHEN monthly_income > 3000.0 AND monthly_income <= 4500.0 THEN '(3000.0, 4500.0]'
        WHEN monthly_income > 4500.0 AND monthly_income <= 6500.0 THEN '(4500.0, 6500.0]'
        WHEN monthly_income > 6500.0 AND monthly_income <= 13000.0 THEN '(6500.0, 13000.0]'
        WHEN monthly_income > 13000.0 THEN '(13000.0, inf]'
        WHEN monthly_income IS NULL THEN 'NULL'
    END AS segment,
    CASE
        WHEN monthly_income >= 0.0 AND monthly_income <= 900.0 THEN 1
        WHEN monthly_income > 900.0 AND monthly_income <= 3000.0 THEN 2
        WHEN monthly_income > 3000.0 AND monthly_income <= 4500.0 THEN 3
        WHEN monthly_income > 4500.0 AND monthly_income <= 6500.0 THEN 4
        WHEN monthly_income > 6500.0 AND monthly_income <= 13000.0 THEN 5
        WHEN monthly_income > 13000.0 THEN 6
        WHEN monthly_income IS NULL THEN 7
    END AS severity_order,
    target
FROM borrowers
),
num_open_credit_lines_segments AS(
SELECT
    CASE
        WHEN num_open_credit_lines = 0 THEN '0'
        WHEN num_open_credit_lines >= 1 AND num_open_credit_lines <= 2 THEN '[1, 2]'
        WHEN num_open_credit_lines > 2 AND num_open_credit_lines <= 58 THEN '(2, 58]'
    END AS segment,
    CASE
        WHEN num_open_credit_lines = 0 THEN 1
        WHEN num_open_credit_lines >= 1 AND num_open_credit_lines <= 2 THEN 2
        WHEN num_open_credit_lines > 2 AND num_open_credit_lines <= 58 THEN 3
    END AS severity_order,
    target
FROM borrowers
),
DPD_90_segments AS(
SELECT
    CASE
        WHEN num_90_days_late = 0 THEN '0'
        WHEN num_90_days_late >= 1 AND num_90_days_late <= 2 THEN '[1, 2]'
        WHEN num_90_days_late > 2 AND num_90_days_late <= 17 THEN '(2, 17]'
        WHEN num_90_days_late = 96 THEN '96'
        WHEN num_90_days_late = 98 THEN '98'
    END AS segment,
    CASE
        WHEN num_90_days_late = 0 THEN 1
        WHEN num_90_days_late >= 1 AND num_90_days_late <= 2 THEN 2
        WHEN num_90_days_late > 2 AND num_90_days_late <= 17 THEN 3
        WHEN num_90_days_late = 96 THEN 4
        WHEN num_90_days_late = 98 THEN 5
    END AS severity_order,
    target
FROM borrowers
),
num_real_estate_loans_segments AS(
SELECT
    CASE
        WHEN num_real_estate_loans = 0 THEN '0'
        WHEN num_real_estate_loans >= 1 AND num_real_estate_loans <= 3 THEN '[1, 3]'
        WHEN num_real_estate_loans > 3 AND num_real_estate_loans <= 54 THEN '(3, 54]'
    END AS segment,
    CASE
        WHEN num_real_estate_loans = 0 THEN 1
        WHEN num_real_estate_loans >= 1 AND num_real_estate_loans <= 3 THEN 2
        WHEN num_real_estate_loans > 3 AND num_real_estate_loans <= 54 THEN 3
    END AS severity_order,
    target
FROM borrowers
),
DPD_60_89_segments AS(
SELECT
    CASE
        WHEN num_60_89_days_late = 0 THEN '0'
        WHEN num_60_89_days_late >= 1 AND num_60_89_days_late <= 2 THEN '[1, 2]'
        WHEN num_60_89_days_late > 2 AND num_60_89_days_late <= 11 THEN '(2, 11]'
        WHEN num_60_89_days_late = 96 THEN '96'
        WHEN num_60_89_days_late = 98 THEN '98'
    END AS segment,
    CASE
        WHEN num_60_89_days_late = 0 THEN 1
        WHEN num_60_89_days_late >= 1 AND num_60_89_days_late <= 2 THEN 2
        WHEN num_60_89_days_late > 2 AND num_60_89_days_late <= 11 THEN 3
        WHEN num_60_89_days_late = 96 THEN 4
        WHEN num_60_89_days_late = 98 THEN 5
    END AS severity_order,
    target
FROM borrowers
),
num_dependents_segments AS(
SELECT
    CASE
        WHEN num_dependents = 0 THEN '0'
        WHEN num_dependents >= 1 AND num_dependents <= 2 THEN '[1, 2]'
        WHEN num_dependents > 2 AND num_dependents <= 20 THEN '(2, 20]'
        WHEN num_dependents IS NULL THEN 'NULL'
    END AS segment,
    CASE
        WHEN num_dependents = 0 THEN 1
        WHEN num_dependents >= 1 AND num_dependents <= 2 THEN 2
        WHEN num_dependents > 2 AND num_dependents <= 20 THEN 3
        WHEN num_dependents IS NULL THEN 4
    END AS severity_order,
    target
FROM borrowers
)
SELECT feature, segment, borrowers, dataset_share, bad_rate, lift, bad_share
FROM (
SELECT
    'revolving_utilization' AS feature,
    severity_order,
    segment,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS dataset_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SUM(SUM(target)) OVER() * 1.0 / SUM(COUNT(*)) OVER()) AS lift,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() as bad_share
FROM revolving_utilization_segments
GROUP BY segment, severity_order
UNION ALL
SELECT
    'age' AS feature,
    severity_order,
    segment,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS dataset_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SUM(SUM(target)) OVER() * 1.0 / SUM(COUNT(*)) OVER()) AS lift,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() as bad_share
FROM age_segments
GROUP BY segment, severity_order
UNION ALL
SELECT
    'DPD_30_59' AS feature,
    severity_order,
    segment,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS dataset_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SUM(SUM(target)) OVER() * 1.0 / SUM(COUNT(*)) OVER()) AS lift,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() as bad_share
FROM DPD_30_59_segments
GROUP BY segment, severity_order
UNION ALL
SELECT
    'debt_ratio' AS feature,
    severity_order,
    segment,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS dataset_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SUM(SUM(target)) OVER() * 1.0 / SUM(COUNT(*)) OVER()) AS lift,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() as bad_share
FROM debt_ratio_segments
GROUP BY segment, severity_order
UNION ALL
SELECT
    'monthly_income' AS feature,
    severity_order,
    segment,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS dataset_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SUM(SUM(target)) OVER() * 1.0 / SUM(COUNT(*)) OVER()) AS lift,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() as bad_share
FROM monthly_income_segments
GROUP BY segment, severity_order
UNION ALL
SELECT
    'num_open_credit_lines' AS feature,
    severity_order,
    segment,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS dataset_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SUM(SUM(target)) OVER() * 1.0 / SUM(COUNT(*)) OVER()) AS lift,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() as bad_share
FROM num_open_credit_lines_segments
GROUP BY segment, severity_order
UNION ALL
SELECT
    'DPD_90' AS feature,
    severity_order,
    segment,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS dataset_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SUM(SUM(target)) OVER() * 1.0 / SUM(COUNT(*)) OVER()) AS lift,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() as bad_share
FROM DPD_90_segments
GROUP BY segment, severity_order
UNION ALL
SELECT
    'num_real_estate_loans' AS feature,
    severity_order,
    segment,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS dataset_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SUM(SUM(target)) OVER() * 1.0 / SUM(COUNT(*)) OVER()) AS lift,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() as bad_share
FROM num_real_estate_loans_segments
GROUP BY segment, severity_order
UNION ALL
SELECT
    'DPD_60_89' AS feature,
    severity_order,
    segment,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS dataset_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SUM(SUM(target)) OVER() * 1.0 / SUM(COUNT(*)) OVER()) AS lift,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() as bad_share
FROM DPD_60_89_segments
GROUP BY segment, severity_order
UNION ALL
SELECT
    'num_dependents' AS feature,
    severity_order,
    segment,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS dataset_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SUM(SUM(target)) OVER() * 1.0 / SUM(COUNT(*)) OVER()) AS lift,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() as bad_share
FROM num_dependents_segments
GROUP BY segment, severity_order
) AS t
ORDER BY feature, severity_order;
"""

query_vw_risk_grades = """
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
    END AS pd_segment,
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
    pd_segment,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS dataset_share,
    AVG(score) AS avg_pd,
    AVG(target) AS bad_rate,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() bads_share
FROM risk_segmented_borrowers
GROUP BY risk_grade, pd_segment, severity_order
ORDER BY severity_order;
"""

query_vw_score_deciles = """
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
    COUNT(*) AS borrowers,
    AVG(score) AS avg_pd,
    AVG(target) AS bad_rate,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() AS bads_share,
    (
        SUM(SUM(target)) OVER(ORDER BY decile ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
        *
        1.0
        /
        SUM(SUM(target)) OVER()
    ) AS cumulative_bads_share
FROM deciles
GROUP BY decile;
"""

query_vw_credit_policy = """
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
"""

query_vw_scored_borrowers = """
SELECT
    b.borrower_id,
    b.target,
    s.score,
    b.revolving_utilization,
    b.age,
    b.debt_ratio,
    b.monthly_income,
    b.num_open_credit_lines,
    b.num_90_days_late,
    b.num_real_estate_loans,
    b.num_60_89_days_late,
    b.num_dependents
FROM borrowers b
INNER JOIN borrowers_score s ON s.borrower_id = b.borrower_id;
"""

vw_portfolio_summary = pd.read_sql_query(query_vw_portfolio_summary, conn)
vw_risk_segments = pd.read_sql_query(query_vw_risk_segments, conn)
vw_risk_grades = pd.read_sql_query(query_vw_risk_grades, conn)
vw_score_deciles = pd.read_sql_query(query_vw_score_deciles, conn)
vw_credit_policy = pd.read_sql_query(query_vw_credit_policy, conn)
vw_scored_borrowers = pd.read_sql_query(query_vw_scored_borrowers, conn)

conn.close()