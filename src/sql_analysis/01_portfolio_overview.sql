--------------------------------------------------------------
-- Вывод признаков и их типов данных
--------------------------------------------------------------
SELECT
    name AS column_name,
    type AS data_type
FROM pragma_table_info('borrowers')
ORDER BY cid;
--------------------------------------------------------------
-- Размер датасета, количество bad evetns, bad rate
--------------------------------------------------------------
SELECT
    COUNT(*) as num_borrowers,
    SUM(target) as num_bad_borrowers,
    AVG(target) as bad_rate
FROM borrowers;
--------------------------------------------------------------
-- Вывод количества пропусков по признакам
--------------------------------------------------------------
SELECT
    COUNT(*) - COUNT(target) AS target_mis_count,
    COUNT(*) - COUNT(revolving_utilization) AS rev_util_mis_count,
    COUNT(*) - COUNT(age) AS age_mis_count,
    COUNT(*) - COUNT(num_30_59_days_late) AS DPD_30_59_mis_count,
    COUNT(*) - COUNT(debt_ratio) AS debt_ratio_mis_count,
    COUNT(*) - COUNT(monthly_income) AS monthly_income_mis_count,
    COUNT(*) - COUNT(num_open_credit_lines) AS num_op_cr_lines_mis_count,
    COUNT(*) - COUNT(num_90_days_late) AS DPD_90_mis_count,
    COUNT(*) - COUNT(num_real_estate_loans) AS num_rel_est_ls_mis_count,
    COUNT(*) - COUNT(num_60_89_days_late) AS DPD_60_89_mis_count,
    COUNT(*) - COUNT(num_dependents) AS num_dependents_mis_count,
    COUNT(*) - COUNT(borrower_id) AS borrower_id_mis_count
FROM borrowers;
--------------------------------------------------------------
-- Наличие дубликатов (borrower_id добавлен уже мной) без target
--------------------------------------------------------------
WITH duplicates AS (
SELECT COUNT (*) as duplicated
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
SELECT SUM(duplicated - 1) as num_duplicate_rows
FROM duplicates;
--------------------------------------------------------------
-- Примерный вид датасета
--------------------------------------------------------------
SELECT *
FROM borrowers
LIMIT 5;
--------------------------------------------------------------
-- Получение количественных характеристик признаков
--------------------------------------------------------------
WITH revolving_utilization AS (
SELECT 
    'revolving_utilization' as feature,
    COUNT(*) AS num,
    MIN(revolving_utilization) min,
    AVG(revolving_utilization) avg,
    MAX(revolving_utilization) max
FROM borrowers
),
age AS (
SELECT
    'age' as feature,
    COUNT(*) AS num,
    MIN(age) min,
    AVG(age) avg,
    MAX(age) max
FROM borrowers
),
num_30_59_days_late AS (
SELECT
    'num_30_59_days_late' as feature,
    COUNT(*) AS num,
    MIN(num_30_59_days_late) min,
    AVG(num_30_59_days_late) avg,
    MAX(num_30_59_days_late) max
FROM borrowers
),
debt_ratio AS (
SELECT
    'debt_ratio' as feature,
    COUNT(*) AS num,
    MIN(debt_ratio) min,
    AVG(debt_ratio) avg,
    MAX(debt_ratio) max
FROM borrowers
),
monthly_income AS (
SELECT
    'monthly_income' as feature,
    COUNT(*) AS num,
    MIN(monthly_income) min,
    AVG(monthly_income) avg,
    MAX(monthly_income) max
FROM borrowers
),
num_open_credit_lines AS (
SELECT
    'num_open_credit_lines' as feature,
    COUNT(*) AS num,
    MIN(num_open_credit_lines) min,
    AVG(num_open_credit_lines) avg,
    MAX(num_open_credit_lines) max
FROM borrowers
),
num_90_days_late AS (
SELECT
    'num_90_days_late' as feature,
    COUNT(*) AS num,
    MIN(num_90_days_late) min,
    AVG(num_90_days_late) avg,
    MAX(num_90_days_late) max
FROM borrowers
),
num_real_estate_loans AS (
SELECT
    'num_real_estate_loans' as feature,
    COUNT(*) AS num,
    MIN(num_real_estate_loans) min,
    AVG(num_real_estate_loans) avg,
    MAX(num_real_estate_loans) max
FROM borrowers
),
num_60_89_days_late AS (
SELECT
    'num_60_89_days_late' as feature,
    COUNT(*) AS num,
    MIN(num_60_89_days_late) min,
    AVG(num_60_89_days_late) avg,
    MAX(num_60_89_days_late) max
FROM borrowers
),
num_dependents AS (
SELECT
    'num_dependents' as feature,
    COUNT(*) AS num,
    MIN(num_dependents) min,
    AVG(num_dependents) avg,
    MAX(num_dependents) max
FROM borrowers
)
SELECT *
FROM num_dependents;