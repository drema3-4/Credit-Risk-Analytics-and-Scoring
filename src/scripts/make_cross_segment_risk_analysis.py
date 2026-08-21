import pandas as pd
from pathlib import Path
import dataframe_image as dfi

from utils.risk_analysis.make_pairwise_segments_analysis import (
    make_pairwise_segments_analysis
)
from utils.risk_analysis.make_prettier_pairwise_report import (
    make_prettier_pairwise_report
)





def make_cross_segment_risk_analysis() -> None:
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

    FEATURES_SEGMENTED_DATAS = [
        pd.read_csv(f"data/segmented_data/{feature}.csv") for feature in FEATURES
    ]

    SEGMENTS = [
        feature_segmented_data[f"{feature}_segments"].unique().tolist()
        for feature, feature_segmented_data in zip(
            FEATURES,
            FEATURES_SEGMENTED_DATAS
        )
    ]

    DATA = pd.read_csv("data/interim/borrowers.csv")
    DATASET_SIZE = DATA.shape[0]
    DATASET_NUM_BAD_EVENTS = DATA["target"].sum()
    DATASET_BAD_RATE = DATA["target"].mean()

    pairwise_report = make_pairwise_segments_analysis(
        features_segmented_datas=FEATURES_SEGMENTED_DATAS,
        features=FEATURES,
        segments=SEGMENTS,
        dataset_size=DATASET_SIZE,
        dataset_num_bad_events=DATASET_NUM_BAD_EVENTS,
        dataset_bad_rate=DATASET_BAD_RATE
    )

    pretty_pairwise_report = make_prettier_pairwise_report(
        pairwise_report=pairwise_report,
        dataset_size=DATASET_SIZE,
        dataset_share_threshold=0.005,
        dataset_num_bad_events=DATASET_NUM_BAD_EVENTS,
        bad_share_threshold=0.01
    )

    summary_table = (
        pretty_pairwise_report
        .sort_values(by="Bad Rate", ascending=False)
        .reset_index(drop=True)
        .head(20)
        .iloc[[0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 15, 16, 17, 19], :]
    ).reset_index(drop=True)

    summary_table = pd.concat(
        [
            summary_table,
            pretty_pairwise_report
            .sort_values(by="Bad Events", ascending=False)
            .reset_index(drop=True)
            .head(20)
            .iloc[[0, 2, 3, 5, 6, 10, 13, 14, 18], :]
        ],
        axis=0
    ).reset_index(drop=True)

    summary_table = pd.concat(
        [
            summary_table,
            pretty_pairwise_report
            .sort_values(by="Delta Bad Rate", ascending=False)
            .reset_index(drop=True)
            .head(20)
            .iloc[[0, 1, 2, 3, 4, 5, 6, 7, 12, 15, 16, 17, 18, 19], :]
        ],
        axis=0
    ).reset_index(drop=True)

    summary_table = summary_table.drop_duplicates()

    cross_segment_risk_analysis_summary = (
        summary_table
        .iloc[
            [1, 2, 3, 4, 5, 6, 7, 9, 17, 18, 21, 22, 25, 26, 27],
            [0, 1, 2, 5, 7, 8, 11, 12]
        ]
        .reset_index(drop=True)
    )

    cross_segment_risk_analysis_summary["Explanations"] = [
        "Очень высокий BR + огромное его повышение",
        "Очень высокий BR + огромное его повышение",
        "Очень высокий BR + огромное его повышение",
        "Очень высокий BR + огромное его повышение + хороший объём",
        "Очень высокий BR + неплохое его повышение",
        "Очень высокий BR + неплохое его повышение",
        "Очень высокий BR + неплохое его повышение",
        "Очень высокий BR + неплохое его повышение + хороший объём",
        "Очень большое повышение BR + очень значительный Bad Share",
        "Высокий Bad Rate + очень значительный Bad Share",
        "Очень высокий BR + очень большое повышение BR + хороший объём",
        "Высокий Bad Rate + огромное его повышение",
        "Высокий Bad Rate + значительное его повышение + хороший объём",
        "Очень высокий BR + значительное его повышение",
        "Высокий Bad Rate + значительное его повышение"
    ]

    cross_segment_risk_analysis_summary = (
        cross_segment_risk_analysis_summary
        .style
        .set_properties(
            **{
                "text-align": "left",
                "white-space": "pre-wrap"
            }
        )
        .set_table_styles(
            [{
                "selector": "th.col_heading",
                "props": [("text-align", "center")]
            }]
        )
    )

    out_path = Path("../docs/risk_analysis/cross_segment_risk_analysis_summary.png")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    dfi.export(cross_segment_risk_analysis_summary, out_path, table_conversion="matplotlib")