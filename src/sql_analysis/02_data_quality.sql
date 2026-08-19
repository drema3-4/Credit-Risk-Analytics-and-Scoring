--------------------------------------------------------------
--------------------------------------------------------------
-- Дубликаты
--------------------------------------------------------------
--------------------------------------------------------------
--------------------------------------------------------------
--02-1-- Duplicate profiles (без target)
--------------------------------------------------------------
WITH duplicates AS (
SELECT COUNT(*) as cnt
FROM borrowers
GROUP BY
    revolving_utilization,
    age,
    num_30_59_days_late,
    debt_ratio,
    monthly_income,
    num_open_credit_lines,
    num_90_days_late,
    num_real_estate_loans,
    num_60_89_days_late,
    num_dependents
HAVING COUNT(*) > 1
)
SELECT SUM(cnt - 1) as num_duplicate_profile_rows
FROM duplicates;
--------------------------------------------------------------
--02-2-- Полные дубликаты, включая target
--------------------------------------------------------------
WITH duplicates AS (
SELECT COUNT(*) as cnt
FROM borrowers
GROUP BY
    target,
    revolving_utilization,
    age,
    num_30_59_days_late,
    debt_ratio,
    monthly_income,
    num_open_credit_lines,
    num_90_days_late,
    num_real_estate_loans,
    num_60_89_days_late,
    num_dependents
HAVING COUNT(*) > 1
)
SELECT SUM(cnt - 1) as num_duplicate_profile_rows
FROM duplicates;
--------------------------------------------------------------
--02-3-- Дубликаты с разными target
--------------------------------------------------------------
WITH duplicates AS (
SELECT COUNT(DISTINCT target) > 1 as cnt
FROM borrowers
GROUP BY
    revolving_utilization,
    age,
    num_30_59_days_late,
    debt_ratio,
    monthly_income,
    num_open_credit_lines,
    num_90_days_late,
    num_real_estate_loans,
    num_60_89_days_late,
    num_dependents
HAVING COUNT(*) > 1
)
SELECT SUM(cnt) as num_duplicate_profile_rows
FROM duplicates;
--------------------------------------------------------------
--------------------------------------------------------------
-- Валидация значений признаков
--------------------------------------------------------------
--------------------------------------------------------------
--------------------------------------------------------------
--02-4-- Наличие у признаков ошибочных значений
--------------------------------------------------------------
SELECT
    SUM(CASE WHEN target <> 0 AND target <> 1 THEN 1 ELSE 0 END) AS num_invalid_target,
    SUM(CASE WHEN revolving_utilization < 0 THEN 1 ELSE 0 END) AS num_invalid_revolving_utilization,
    SUM(CASE WHEN age < 18 THEN 1 ELSE 0 END) AS num_invalid_age,
    SUM(CASE WHEN num_30_59_days_late < 0 THEN 1 ELSE 0 END) AS num_invalid_num_30_59_days_late,
    SUM(CASE WHEN debt_ratio < 0 THEN 1 ELSE 0 END) AS num_invalid_debt_ratio,
    SUM(CASE WHEN monthly_income < 0 THEN 1 ELSE 0 END) AS num_invalid_monthly_income,
    SUM(CASE WHEN num_open_credit_lines < 0 THEN 1 ELSE 0 END) AS num_invalid_num_open_credit_lines,
    SUM(CASE WHEN num_90_days_late < 0 THEN 1 ELSE 0 END) AS num_invalid_num_90_days_late,
    SUM(CASE WHEN num_real_estate_loans < 0 THEN 1 ELSE 0 END) AS num_invalid_num_real_estate_loans,
    SUM(CASE WHEN num_60_89_days_late < 0 THEN 1 ELSE 0 END) AS num_invalid_num_60_89_days_late,
    SUM(CASE WHEN num_dependents < 0 THEN 1 ELSE 0 END) AS num_invalid_num_dependents
FROM borrowers;
--------------------------------------------------------------
--02-5-- Наличие логически несовместимых значений признаков
--------------------------------------------------------------
SELECT
    SUM(CASE WHEN revolving_utilization > 0 AND num_open_credit_lines = 0 THEN 1 ELSE 0 END) AS invalid_rev_ut_AND_num_op_cr_lines,
    SUM(CASE WHEN num_open_credit_lines < num_real_estate_loans THEN 1 ELSE 0 END) AS invalid_num_op_cr_lines_AND_num_r_es_loans
FROM borrowers;
--------------------------------------------------------------
--02-6-- Специальные коды 96/98
--------------------------------------------------------------
SELECT SUM (
    CASE
        WHEN num_30_59_days_late = 96 THEN 1
        WHEN num_30_59_days_late = 98 THEN 1
        WHEN num_60_89_days_late = 96 THEN 1
        WHEN num_60_89_days_late = 98 THEN 1
        WHEN num_90_days_late = 96 THEN 1
        WHEN num_90_days_late = 98 THEN 1
    END
) AS rows_with_special_codes
FROM borrowers;
--------------------------------------------------------------
--02-7-- Согласованность специальных кодов 96/98
--------------------------------------------------------------
SELECT
    SUM (
        CASE
            WHEN num_30_59_days_late = 96 OR num_30_59_days_late = 98 THEN 1
            WHEN num_60_89_days_late = 96 OR num_60_89_days_late = 98 THEN 1
            WHEN num_90_days_late = 96 OR num_90_days_late = 98 THEN 1
        END
    ) - SUM (
        CASE
            WHEN num_30_59_days_late = 96 AND num_60_89_days_late = 96 AND num_90_days_late = 96 THEN 1
            WHEN num_30_59_days_late = 98 AND num_60_89_days_late = 98 AND num_90_days_late = 98 THEN 1
        END
    ) AS not_consistency_special_codes
FROM borrowers;