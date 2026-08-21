import pandas as pd

from utils.scoring.make_segments_col import (
    make_segments_cols
)


def prepare_dataset(
    data: pd.DataFrame,
    features: list[str],
    segmentss: list[list[float]],
    special_valuess: list[list[float]]
) -> pd.DataFrame:
    df = data.copy(deep=True)

    for feature, segments, special_values in zip(
        features,
        segmentss,
        special_valuess
    ):
        cols = make_segments_cols(
            data=df,
            feature=feature,
            segments=segments,
            special_values=special_values
        )

        df = df.drop(columns=feature)
        df = pd.concat([df, cols], axis=1)

    return df