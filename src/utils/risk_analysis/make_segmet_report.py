import pandas as pd
import numpy as np
from pathlib import Path
from statsmodels.stats.proportion import proportion_confint
import dataframe_image as dfi

from utils.risk_analysis.make_segments_border import make_values
from utils.risk_analysis.make_segments_markers_col import (
    make_segment_col_continuos_feature,
    make_segment_col_count_or_cat_feature
)


COLUMNS_SEGMENT_REPORT = [
    "segment",
    "clients",
    "dataset_share",
    "dataset_bad_rate",
    "bad_count",
    "bad_share",
    "bad_rate",
    "ci_low",
    "ci_high",
    "delta_bad_rate_pp",
    "lift"
]


def make_segment_report_continuos_feature(
    data: pd.DataFrame,
    feature: str,
    segments: list[float],
    special_values: list[float],
    out_path: str,
    target_feature: str
) -> None:
    """
    Создаёт таблицу отчёта сегментного анализа и сохраняет его.

    Args:
        data: датасет.
        feature: наименование признака, сегментация которого будет оцениваться.
        segments: список границ сегментов, на который будет разбиваться признак.
        special_values: специальные значения, под которые нужно выделить сегменты.
        out_path: путь, по которому нужно сохранить таблицу.
        target_feature: наименования целевой переменной.
    """
    df = data.copy(deep=True)

    segment_col_name = f"{feature}_segments"

    df_size = df.shape[0] * 1.0
    df_bad_count = df[target_feature].sum()
    df_bad_rate = df[target_feature].mean()    

    segment_report = pd.DataFrame(columns=COLUMNS_SEGMENT_REPORT)

    labels = make_segment_col_continuos_feature(
        data=df,
        feature=feature,
        segment_col_name=segment_col_name,
        segments=segments,
        special_values=special_values
    )

    for label in labels:
        segment = df.loc[
            df[segment_col_name] == label
        ]

        clients = segment.shape[0]
        dataset_share = clients / df_size
        bad_count = segment[target_feature].sum()
        bad_rate = segment[target_feature].mean()
        ci_low, ci_high = proportion_confint(
            count=bad_count,
            nobs=clients,
            alpha=0.05,
            method="wilson"
        )
        delta_bad_rate_pp = round((bad_rate - df_bad_rate) * 100, 4)
        lift = round(bad_rate / df_bad_rate, 4)
        bad_share = round(bad_count / df_bad_count, 4)

        segment_report.loc[ segment_report.shape[0] ] = [
            label,
            clients,
            dataset_share,
            df_bad_rate,
            bad_count,
            bad_share,
            bad_rate,
            ci_low,
            ci_high,
            delta_bad_rate_pp,
            lift
        ]

    path = Path(f"data/segmented_data/{feature}.csv")
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path)

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    dfi.export(segment_report, out_path, table_conversion="matplotlib")

def make_segment_report_count_or_cat_feature(
    data: pd.DataFrame,
    feature: str,
    segments: list[float],
    special_values: list[float],
    out_path: str,
    target_feature: str
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Создаёт таблицу отчёта сегментного анализа и сохраняет его.

    Args:
        data: датасет.
        feature: наименование признака, сегментация которого будет оцениваться.
        segments: список границ сегментов, на который будет разбиваться признак.
        special_values: специальные значения, под которые нужно выделить сегменты.
        out_path: путь, по которому нужно сохранить таблицу.
        target_feature: наименования целевой переменной.
    """
    df = data.copy(deep=True)

    segment_col_name = f"{feature}_segments"

    df_size = df.shape[0] * 1.0
    df_bad_count = df[target_feature].sum()
    df_bad_rate = df[target_feature].mean()    

    segment_report = pd.DataFrame(columns=COLUMNS_SEGMENT_REPORT)

    values = make_values(
        data=df,
        feature=feature,
        special_values=special_values,
        segments=segments
    )
    
    segment_col_name = f"{feature}_segments"
    labels = make_segment_col_count_or_cat_feature(
        data=df,
        feature=feature,
        segment_col_name=segment_col_name,
        values=values,
        segments=segments,
        special_values=special_values
    )
    labels = sorted(
        labels,
        key=lambda x: (
            int(x[1: x.index(",")])
            if 
                x.__contains__("]")
            else 
            np.inf if x == "Nan" else eval(x)
        )
    )

    for label in labels:
        segment = df.loc[
            df[segment_col_name] == label
        ]

        clients = segment.shape[0]
        dataset_share = clients / df_size
        bad_count = segment[target_feature].sum()
        bad_rate = segment[target_feature].mean()
        ci_low, ci_high = proportion_confint(
            count=bad_count,
            nobs=clients,
            alpha=0.05,
            method="wilson"
        )
        delta_bad_rate_pp = round((bad_rate - df_bad_rate) * 100, 4)
        lift = round(bad_rate / df_bad_rate, 4)
        bad_share = round(bad_count / df_bad_count, 4)

        segment_report.loc[ segment_report.shape[0] ] = [
            label,
            clients,
            dataset_share,
            df_bad_rate,
            bad_count,
            bad_share,
            bad_rate,
            ci_low,
            ci_high,
            delta_bad_rate_pp,
            lift
        ]

    path = Path(f"data/segmented_data/{feature}.csv")
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path)

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    dfi.export(segment_report, out_path, table_conversion="matplotlib")