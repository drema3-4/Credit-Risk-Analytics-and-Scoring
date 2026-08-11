import pandas as pd
from pathlib import Path


def data_quality_prepare(data_path: Path, out_path: Path) -> None:
    data = pd.read_csv(data_path)
    data = data.drop(columns=["Unnamed: 0"])

    data = data.rename(columns={
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

    data["age_error"] = (data["age"] < 18).astype(int)

    dpd_columns = [
        "num_30_59_days_late",
        "num_60_89_days_late",
        "num_90_days_late"
    ]
    data["days_late_system_code"] = (
        data[dpd_columns]
        .isin([96, 98])
        .any(axis=1)
        .astype(int)
    )

    data["monthly_income_is_missing"] = (data["monthly_income"].isna()).astype(int)

    data["num_dependents_is_missing"] = (data["num_dependents"].isna()).astype(int)

    data.to_csv(out_path, index=False)