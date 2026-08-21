import pandas as pd
import numpy as np


def make_segments_continuos_feature(
    data: pd.DataFrame,
    feature: str,
    special_values: list[float] = []
) -> list[float]:
    mask = data[feature].isin(special_values)
    feature = data.loc[~mask, feature]

    super_segments = np.unique(
        np.quantile(
            a=feature,
            q=[0.0, 0.005, 0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99, 0.995, 1.0]
        )
    ).tolist()

    segments = []
    for i in range(len(super_segments)-1):
        left = super_segments[i]
        right = super_segments[i+1]

        mask = (left <= feature) & (feature <= right)

        segments.extend(
            np.quantile(
                a=feature[mask],
                q=np.linspace(0, 1, 4)
            ).tolist()
        )

    segments = list(
        map(
            lambda x: round(x, 2),
            segments
        )
    )
    segments.extend([min(feature), max(feature)])
    segments = sorted(
        np.unique(segments).tolist()
    )
    
    return segments

def make_values(
    data: pd.DataFrame,
    feature: str,
    special_values: list[float] = [],
    segments: list[float] = []
) -> list[float]:
    mask = data[feature].isin(special_values + segments)
    feature = data.loc[~mask, feature]

    values = sorted(feature.unique().tolist())
    
    return values