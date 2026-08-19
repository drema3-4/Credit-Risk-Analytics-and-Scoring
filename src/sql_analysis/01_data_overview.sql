--------------------------------------------------------------
--01-1-- Вывод признаков и их типов данных
--------------------------------------------------------------
SELECT
    name AS column_name,
    type AS data_type
FROM pragma_table_info('borrowers')
ORDER BY cid;
--------------------------------------------------------------
--01-2-- Пример данных
--------------------------------------------------------------
SELECT *
FROM borrowers
LIMIT 5;
--------------------------------------------------------------
--01-3-- Размер датасета, good borrowers, bad borrowers, bad rate
--------------------------------------------------------------
SELECT
    COUNT(*) AS num_borrowers,
    SUM(CASE WHEN target = 0 THEN 1 ELSE 0 END) AS good_borrowers,
    SUM(target) AS bad_borrowers,
    AVG(target) as bad_rate
FROM borrowers;
--------------------------------------------------------------
--01-4-- Вывод количества пропусков по признакам
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