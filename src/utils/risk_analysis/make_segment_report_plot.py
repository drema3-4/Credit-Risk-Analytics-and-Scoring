import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

from utils.risk_analysis.make_segments_border import (
    make_segments_continuos_feature,
    make_values
)
from utils.risk_analysis.make_segments_markers_col import (
    make_segment_col_continuos_feature,
    make_segment_col_count_or_cat_feature
)


def plot_prebin_bad_rate_continuos_feature(
    data: pd.DataFrame,
    feature: str,
    segments: list[float],
    special_values: list[float],
    out_path: str,
    target_feature: str
) -> None:
    """
    Создаёт и сохраняет график сегментов признака и их связи с targetом.

    Args:
        data: датасет.
        feature: наименование признака, связь которого будет оцениваться.
        segments: список сегментов.
        special_values: специальные значения, под которые нужно выделить сегменты.
        out_path: путь, по которому нужно сохранить график.
        target_feature: наименования целевой переменной.
    """
    df = data.copy(deep=True)
    avg_bad_pct = df[target_feature].mean() * 100

    if not segments:
        segments = make_segments_continuos_feature(
            data=df,
            feature=feature,
            special_values=special_values
        )

    segment_col_name = f"{feature}_segments"
    _ = make_segment_col_continuos_feature(
        data=df,
        feature=feature,
        segment_col_name=segment_col_name,
        segments=segments,
        special_values=special_values
    )

    summary = (
        df
        .groupby(by=segment_col_name)
        .agg(
            count=(target_feature, "size"),
            bad_rate=(target_feature, "mean")
        )
        .reset_index()
    )
    summary["bad_pct"] = summary["bad_rate"] * 100

    plt.figure(figsize=(14, 4))

    ax = sns.barplot(
        data=summary,
        x=segment_col_name,
        y="bad_pct"
    )
    ax.bar_label(
        ax.containers[0],
        labels=summary["count"],
        padding=3,
        rotation=90
    )

    ax.axhline(
        y=avg_bad_pct,
        linestyle='--',
        color='red',
        linewidth=1.5,
        label='dataset bad rate'
    )
    ax.legend()

    plt.title(f"Доля target = 1 по группам {feature}")
    plt.xlabel(f"{feature}")
    plt.ylabel("Процент target = 1")
    plt.xticks(rotation=90)
    plt.grid(axis="y", alpha=0.3)

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path)

def plot_prebin_bad_rate_count_or_cat_feature(
    data: pd.DataFrame,
    feature: str,
    segments: list[float],
    special_values: list[float],
    out_path: str,
    target_feature: str
) -> None:
    """
    Создаёт и сохраняет график сегментов признака и их связи с targetом.

    Args:
        data: датасет.
        feature: наименование признака, связь которого будет оцениваться.
        segments: список сегментов.
        special_values: специальные значения, под которые нужно выделить сегменты.
        out_path: путь, по которому нужно сохранить график.
        target_feature: наименования целевой переменной.
    """
    df = data.copy(deep=True)
    avg_bad_pct = df[target_feature].mean() * 100

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

    summary = (
        df
        .groupby(by=segment_col_name)
        .agg(
            count=(target_feature, "size"),
            bad_rate=(target_feature, "mean")
        )
        .reset_index()
    )
    summary["bad_pct"] = summary["bad_rate"] * 100
    summary[segment_col_name] = pd.Categorical(
        summary[segment_col_name],
        categories=labels,
        ordered=True
    )
    summary = (
        summary
        .sort_values(segment_col_name)
        .reset_index(drop=True)
    )

    plt.figure(figsize=(14, 4))

    ax = sns.barplot(
        data=summary,
        x=segment_col_name,
        y="bad_pct"
    )
    ax.bar_label(
        ax.containers[0],
        labels=summary["count"],
        padding=3,
        rotation=90
    )

    ax.axhline(
        y=avg_bad_pct,
        linestyle='--',
        color='red',
        linewidth=1.5,
        label='dataset bad rate'
    )
    ax.legend()

    plt.title(f"Доля target = 1 по группам {feature}")
    plt.xlabel(f"{feature}")
    plt.ylabel("Процент target = 1")
    plt.xticks(rotation=90)
    plt.grid(axis="y", alpha=0.3)

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path)