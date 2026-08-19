--------------------------------------------------------------
--------------------------------------------------------------
--------------------------------------------------------------
--05-1-- Bad contribution по сегментам
--------------------------------------------------------------
--------------------------------------------------------------
--------------------------------------------------------------
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
SELECT feature, segment, borrowers, borrowers_share, bads, bad_share, bad_rate, lift
FROM (
SELECT
    'revolving_utilization' AS feature,
    severity_order,
    segment,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS borrowers_share,
    SUM(target) AS bads,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() AS bad_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SUM(SUM(target)) OVER() * 1.0 / SUM(COUNT(*)) OVER()) AS lift
FROM revolving_utilization_segments
GROUP BY segment, severity_order
UNION ALL
SELECT
    'age' AS feature,
    severity_order,
    segment,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS borrowers_share,
    SUM(target) AS bads,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() AS bad_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SUM(SUM(target)) OVER() * 1.0 / SUM(COUNT(*)) OVER()) AS lift
FROM age_segments
GROUP BY segment, severity_order
UNION ALL
SELECT
    'DPD_30_59' AS feature,
    severity_order,
    segment,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS borrowers_share,
    SUM(target) AS bads,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() AS bad_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SUM(SUM(target)) OVER() * 1.0 / SUM(COUNT(*)) OVER()) AS lift
FROM DPD_30_59_segments
GROUP BY segment, severity_order
UNION ALL
SELECT
    'debt_ratio' AS feature,
    severity_order,
    segment,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS borrowers_share,
    SUM(target) AS bads,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() AS bad_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SUM(SUM(target)) OVER() * 1.0 / SUM(COUNT(*)) OVER()) AS lift
FROM debt_ratio_segments
GROUP BY segment, severity_order
UNION ALL
SELECT
    'monthly_income' AS feature,
    severity_order,
    segment,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS borrowers_share,
    SUM(target) AS bads,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() AS bad_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SUM(SUM(target)) OVER() * 1.0 / SUM(COUNT(*)) OVER()) AS lift
FROM monthly_income_segments
GROUP BY segment, severity_order
UNION ALL
SELECT
    'num_open_credit_lines' AS feature,
    severity_order,
    segment,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS borrowers_share,
    SUM(target) AS bads,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() AS bad_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SUM(SUM(target)) OVER() * 1.0 / SUM(COUNT(*)) OVER()) AS lift
FROM num_open_credit_lines_segments
GROUP BY segment, severity_order
UNION ALL
SELECT
    'DPD_90' AS feature,
    severity_order,
    segment,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS borrowers_share,
    SUM(target) AS bads,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() AS bad_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SUM(SUM(target)) OVER() * 1.0 / SUM(COUNT(*)) OVER()) AS lift
FROM DPD_90_segments
GROUP BY segment, severity_order
UNION ALL
SELECT
    'num_real_estate_loans' AS feature,
    severity_order,
    segment,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS borrowers_share,
    SUM(target) AS bads,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() AS bad_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SUM(SUM(target)) OVER() * 1.0 / SUM(COUNT(*)) OVER()) AS lift
FROM num_real_estate_loans_segments
GROUP BY segment, severity_order
UNION ALL
SELECT
    'DPD_60_89' AS feature,
    severity_order,
    segment,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS borrowers_share,
    SUM(target) AS bads,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() AS bad_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SUM(SUM(target)) OVER() * 1.0 / SUM(COUNT(*)) OVER()) AS lift
FROM DPD_60_89_segments
GROUP BY segment, severity_order
UNION ALL
SELECT
    'num_dependents' AS feature,
    severity_order,
    segment,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS borrowers_share,
    SUM(target) AS bads,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() AS bad_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SUM(SUM(target)) OVER() * 1.0 / SUM(COUNT(*)) OVER()) AS lift
FROM num_dependents_segments
GROUP BY segment, severity_order
) AS t
ORDER BY feature, severity_order;
--------------------------------------------------------------
--------------------------------------------------------------
--------------------------------------------------------------
--05-2 Ранжирование сегментов признаков по bad contribution и bad rate
--------------------------------------------------------------
--------------------------------------------------------------
--------------------------------------------------------------
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
),
segment_metrics AS (
SELECT feature, segment, borrowers, borrowers_share, bads, bad_share, bad_rate, lift
FROM (
SELECT
    'revolving_utilization' AS feature,
    severity_order,
    segment,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS borrowers_share,
    SUM(target) AS bads,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() AS bad_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SUM(SUM(target)) OVER() * 1.0 / SUM(COUNT(*)) OVER()) AS lift
FROM revolving_utilization_segments
GROUP BY segment, severity_order
UNION ALL
SELECT
    'age' AS feature,
    severity_order,
    segment,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS borrowers_share,
    SUM(target) AS bads,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() AS bad_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SUM(SUM(target)) OVER() * 1.0 / SUM(COUNT(*)) OVER()) AS lift
FROM age_segments
GROUP BY segment, severity_order
UNION ALL
SELECT
    'DPD_30_59' AS feature,
    severity_order,
    segment,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS borrowers_share,
    SUM(target) AS bads,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() AS bad_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SUM(SUM(target)) OVER() * 1.0 / SUM(COUNT(*)) OVER()) AS lift
FROM DPD_30_59_segments
GROUP BY segment, severity_order
UNION ALL
SELECT
    'debt_ratio' AS feature,
    severity_order,
    segment,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS borrowers_share,
    SUM(target) AS bads,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() AS bad_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SUM(SUM(target)) OVER() * 1.0 / SUM(COUNT(*)) OVER()) AS lift
FROM debt_ratio_segments
GROUP BY segment, severity_order
UNION ALL
SELECT
    'monthly_income' AS feature,
    severity_order,
    segment,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS borrowers_share,
    SUM(target) AS bads,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() AS bad_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SUM(SUM(target)) OVER() * 1.0 / SUM(COUNT(*)) OVER()) AS lift
FROM monthly_income_segments
GROUP BY segment, severity_order
UNION ALL
SELECT
    'num_open_credit_lines' AS feature,
    severity_order,
    segment,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS borrowers_share,
    SUM(target) AS bads,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() AS bad_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SUM(SUM(target)) OVER() * 1.0 / SUM(COUNT(*)) OVER()) AS lift
FROM num_open_credit_lines_segments
GROUP BY segment, severity_order
UNION ALL
SELECT
    'DPD_90' AS feature,
    severity_order,
    segment,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS borrowers_share,
    SUM(target) AS bads,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() AS bad_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SUM(SUM(target)) OVER() * 1.0 / SUM(COUNT(*)) OVER()) AS lift
FROM DPD_90_segments
GROUP BY segment, severity_order
UNION ALL
SELECT
    'num_real_estate_loans' AS feature,
    severity_order,
    segment,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS borrowers_share,
    SUM(target) AS bads,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() AS bad_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SUM(SUM(target)) OVER() * 1.0 / SUM(COUNT(*)) OVER()) AS lift
FROM num_real_estate_loans_segments
GROUP BY segment, severity_order
UNION ALL
SELECT
    'DPD_60_89' AS feature,
    severity_order,
    segment,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS borrowers_share,
    SUM(target) AS bads,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() AS bad_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SUM(SUM(target)) OVER() * 1.0 / SUM(COUNT(*)) OVER()) AS lift
FROM DPD_60_89_segments
GROUP BY segment, severity_order
UNION ALL
SELECT
    'num_dependents' AS feature,
    severity_order,
    segment,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS borrowers_share,
    SUM(target) AS bads,
    SUM(target) * 1.0 / SUM(SUM(target)) OVER() AS bad_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SUM(SUM(target)) OVER() * 1.0 / SUM(COUNT(*)) OVER()) AS lift
FROM num_dependents_segments
GROUP BY segment, severity_order
) AS t
ORDER BY feature, severity_order
),
ranked AS (
    SELECT
        *,
        RANK() OVER (
            PARTITION BY feature
            ORDER BY bad_rate DESC
        ) AS bad_rate_rank,
        RANK() OVER (
            PARTITION BY feature
            ORDER BY bads DESC
        ) AS bad_contribution_rank
    FROM segment_metrics
)
SELECT *
FROM ranked
ORDER BY feature, bad_rate_rank;
--------------------------------------------------------------
--------------------------------------------------------------
--------------------------------------------------------------
--5-3 Risk markers
--------------------------------------------------------------
--------------------------------------------------------------
--------------------------------------------------------------
WITH risk_markers AS(
SELECT
    borrower_id,
    CASE
        WHEN revolving_utilization > 0.7 AND revolving_utilization <= 2.0 THEN 1 ELSE 0
    END AS high_utilization,
    CASE
        WHEN num_30_59_days_late > 0 AND num_30_59_days_late NOT IN (96, 98) OR
             num_60_89_days_late > 0 AND num_60_89_days_late NOT IN (96, 98) OR
             num_90_days_late > 0 AND num_90_days_late NOT IN (96, 98)
             THEN 1 ELSE 0
    END AS has_previous_dpd,
    CASE
        WHEN debt_ratio > 0.7 AND debt_ratio <= 4.0 THEN 1 ELSE 0
    END AS high_debt_ratio,
    CASE
        WHEN num_open_credit_lines = 0 THEN 1 ELSE 0
    END AS hasnt_credit_lines
FROM borrowers
)
SELECT *
FROM risk_markers;
--------------------------------------------------------------
--------------------------------------------------------------
--------------------------------------------------------------
--5-4 Risk markers report
--------------------------------------------------------------
--------------------------------------------------------------
--------------------------------------------------------------
WITH base_metrics AS (
SELECT
    COUNT(*) AS size,
    SUM(target) AS bads,
    AVG(target) AS bad_rate
FROM borrowers
)
SELECT
    'high_utilization' as marker,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / (SELECT size FROM base_metrics) AS borrowers_share,
    SUM(target) AS bads,
    SUM(target) * 1.0 / (SELECT bads FROM base_metrics) AS bads_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SELECT bad_rate FROM base_metrics) AS lift
FROM borrowers
WHERE revolving_utilization > 0.7 AND revolving_utilization <= 2.0
UNION
SELECT
    'has_previous_dpd' as marker,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / (SELECT size FROM base_metrics) AS borrowers_share,
    SUM(target) AS bads,
    SUM(target) * 1.0 / (SELECT bads FROM base_metrics) AS bads_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SELECT bad_rate FROM base_metrics) AS lift
FROM borrowers
WHERE (
    num_30_59_days_late > 0 AND num_30_59_days_late NOT IN (96, 98) OR
    num_60_89_days_late > 0 AND num_60_89_days_late NOT IN (96, 98) OR
    num_90_days_late > 0 AND num_90_days_late NOT IN (96, 98)
)
UNION
SELECT
    'high_debt_ratio' as marker,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / (SELECT size FROM base_metrics) AS borrowers_share,
    SUM(target) AS bads,
    SUM(target) * 1.0 / (SELECT bads FROM base_metrics) AS bads_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SELECT bad_rate FROM base_metrics) AS lift
FROM borrowers
WHERE debt_ratio > 0.7 AND debt_ratio <= 4.0
UNION
SELECT
    'hasnt_credit_lines' as marker,
    COUNT(*) AS borrowers,
    COUNT(*) * 1.0 / (SELECT size FROM base_metrics) AS borrowers_share,
    SUM(target) AS bads,
    SUM(target) * 1.0 / (SELECT bads FROM base_metrics) AS bads_share,
    AVG(target) AS bad_rate,
    AVG(target) / (SELECT bad_rate FROM base_metrics) AS lift
FROM borrowers
WHERE num_open_credit_lines = 0;