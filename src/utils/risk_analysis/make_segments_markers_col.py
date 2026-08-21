import pandas as pd

from utils.risk_analysis.make_labels_by_segments_borders import make_labels


def make_segment_col_continuos_feature(
    data: pd.DataFrame,
    feature: str,
    segment_col_name: str,
    segments: list[float],
    special_values: list[float] = []
) -> list[str]:
    labels = make_labels(segments)

    data[segment_col_name] = pd.cut(
        x=data[feature],
        bins=segments,
        labels=labels,
        right=True,
        include_lowest=True
    )


    special_labels = []
    if special_values:
        for special_value in special_values:
            if pd.isna(special_value):
                label = "NaN"
            else:
                label = str(special_value)

            special_labels.append(label)

        new_categories = [
            label
            for label in special_labels
            if label not in data[segment_col_name].cat.categories
        ]

        data[segment_col_name] = (
            data[segment_col_name]
            .cat.add_categories(new_categories)
        )

        for special_value in special_values:
            if pd.isna(special_value):
                mask = data[feature].isna()
                label = "NaN"
            else:
                mask = data[feature].eq(special_value)
                label = str(special_value)

            data.loc[mask, segment_col_name] = label
    

    return labels + special_labels

def make_segment_col_count_or_cat_feature(
    data: pd.DataFrame,
    feature: str,
    segment_col_name: str,
    values: list[float],
    segments: list[float] = [],
    special_values: list[float] = []
) -> list[str]:
    values_ = values
    if segments:
        values_ = [value for value in values if value not in set(range(segments[0], segments[-1]+1))]
    
    values_labels = list(map(str, values_))
    for value, value_label in zip(values_, values_labels):
        mask = data[feature].eq(value)
        data.loc[mask, segment_col_name] = value_label

    data[segment_col_name] = data[segment_col_name].astype("category")

    segments_labels = []
    if segments:
        segments_labels = make_labels(segments)

        new_categories = [
            label
            for label in segments_labels
        ]
        data[segment_col_name] = (
            data[segment_col_name]
            .cat.add_categories(new_categories)
        )

        mask = data[feature].isin(values_)
        data.loc[~mask, segment_col_name] = pd.cut(
            x=data.loc[~mask, feature],
            bins=segments,
            labels=segments_labels,
            right=True,
            include_lowest=True
        ).astype(object)

    special_values_labels = []
    if special_values:
        special_values_labels = [
            "Nan" if pd.isna(special_value) else str(special_value)
            for special_value in special_values
        ]

        new_categories = [
            label
            for label in special_values_labels
        ]

        data[segment_col_name] = (
            data[segment_col_name]
            .cat.add_categories(new_categories)
        )        

        for special_value in special_values:
            if pd.isna(special_value):
                mask = data[feature].isna()
                label = "Nan"
            else:
                mask = data[feature].eq(special_value)
                label = str(special_value)

            data.loc[mask, segment_col_name] = label
    

    return values_labels + segments_labels + special_values_labels