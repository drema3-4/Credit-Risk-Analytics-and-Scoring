import sqlite3
import pandas as pd


def make_db() -> None:
    dataset = pd.read_csv("data/raw/cs-training.csv")
    dataset = dataset.drop(columns=["Unnamed: 0"])
    
    dataset = dataset.rename(columns={
        "SeriousDlqin2yrs": "target",
        "RevolvingUtilizationOfUnsecuredLines": "revolving_utilization",
        "age": "age",
        "NumberOfTime30-59DaysPastDueNotWorse": "num_30_59_days_late",
        "DebtRatio": "debt_ratio",
        "MonthlyIncome": "monthly_income",
        "NumberOfOpenCreditLinesAndLoans": "num_open_credit_lines",
        "NumberOfTimes90DaysLate": "num_90_days_late",
        "NumberRealEstateLoansOrLines": "num_real_estate_loans",
        "NumberOfTime60-89DaysPastDueNotWorse": "num_60_89_days_late",
        "NumberOfDependents": "num_dependents"
    })

    dataset["borrower_id"] = list(range(dataset.shape[0]))

    conn = sqlite3.connect("sql_analysis/db.db")

    dataset.to_sql(
        "borrowers",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()