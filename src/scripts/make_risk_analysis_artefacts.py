import pandas as pd
import numpy as np

from utils.risk_analysis.make_segment_report_plot import (
    plot_prebin_bad_rate_continuos_feature,
    plot_prebin_bad_rate_count_or_cat_feature
)
from utils.risk_analysis.make_segmet_report import (
    make_segment_report_continuos_feature,
    make_segment_report_count_or_cat_feature
)


FEATURES = [
    "revolving_utilization",
    "age",
    "num_30_59_days_late",
    "num_60_89_days_late",
    "num_90_days_late",
    "debt_ratio",
    "monthly_income",
    "num_open_credit_lines",
    "num_real_estate_loans",
    "num_dependents"
]

SEGMENTS = [
    [0.0, 0.2, 0.4, 0.5, 0.7, 1.0, 2.0, 5.0, np.inf],
    [0.0, 22.0, 30.0, 45.0, 55.0, 75.0, np.inf],
    [1, 2, 13],
    [1, 2, 11],
    [1, 2, 17],
    [0.0, 0.1, 0.7, 1.0, 4.0, np.inf],
    [0.0, 900.0, 3000.0, 4500.0, 6500.0, 13000.0, np.inf],
    [1, 2, 58],
    [1, 3, 54],
    [1, 2, 20]
]

SPECIAL_VALUES = [
    [],
    [],
    [96, 98],
    [96, 98],
    [96, 98],
    [],
    [np.nan],
    [],
    [],
    [np.nan]
]

FEATUES_TYPES = [
    "continuos",
    "continuos",
    "count",
    "count",
    "count",
    "continuos",
    "continuos",
    "count",
    "count",
    "count"
]

BASE_PATH = "../docs/risk_analysis"


def make_plots_risk_analysis() -> None:
    data = pd.read_csv("data/interim/borrowers.csv")
    data["borrower_id"] = np.arange(1, data.shape[0] + 1)

    for feature, segments, special_values, feature_type in zip(
        FEATURES,
        SEGMENTS,
        SPECIAL_VALUES,
        FEATUES_TYPES
    ):
        if feature_type == "continuos":
            plot_prebin_bad_rate_continuos_feature(
                data=data,
                feature=feature,
                segments=segments,
                special_values=special_values,
                out_path=f"{BASE_PATH}/{feature}/{feature}_graphic.png",
                target_feature="target"
            )
        elif feature_type == "count":
            plot_prebin_bad_rate_count_or_cat_feature(
                data=data,
                feature=feature,
                segments=segments,
                special_values=special_values,
                out_path=f"{BASE_PATH}/{feature}/{feature}_graphic.png",
                target_feature="target"
            )

def make_reports_risk_analysis() -> None:
    data = pd.read_csv("data/interim/borrowers.csv")
    data["borrower_id"] = np.arange(1, data.shape[0] + 1)

    for feature, segments, special_values, feature_type in zip(
        FEATURES,
        SEGMENTS,
        SPECIAL_VALUES,
        FEATUES_TYPES
    ):
        if feature_type == "continuos":
            make_segment_report_continuos_feature(
                data=data,
                feature=feature,
                segments=segments,
                special_values=special_values,
                out_path=f"{BASE_PATH}/{feature}/{feature}_report.png",
                target_feature="target"
            )
        elif feature_type == "count":
            make_segment_report_count_or_cat_feature(
                data=data,
                feature=feature,
                segments=segments,
                special_values=special_values,
                out_path=f"{BASE_PATH}/{feature}/{feature}_report.png",
                target_feature="target"
            )