import pandas as pd

from utils.scoring.make_labels import (
    make_labels
)


def make_segments_cols(
    data: pd.DataFrame,
    feature: str,
    segments: list[float],
    special_values: list[int] = []
) -> pd.DataFrame:
    df = data.copy(deep=True)

    labels = make_labels(segments)

    segment_col_name = f"{feature}_segments"

    df[segment_col_name] = pd.cut(
        x=df[feature].dropna(),
        labels=labels,
        bins=segments,
        right=True,
        include_lowest=True
    )

    special_labels = []
    if special_values:
        for special_value in special_values:
            label = str(special_value)

            special_labels.append(label)

        new_categories = [
            label
            for label in special_labels
            if label not in df[segment_col_name].cat.categories
        ]

        df[segment_col_name] = (
            df[segment_col_name]
            .cat.add_categories(new_categories)
        )

        for special_value in special_values:
            mask = df[feature].eq(special_value)
            label = str(special_value)

            df.loc[mask, segment_col_name] = label

    cols = pd.get_dummies(
        df[segment_col_name],
        prefix=f"{feature}"
    )

    return cols