import pandas as pd

from utils.risk_analysis.calc_segments_intersection_characteristics import (
    calc_segments_intersection_characteristics
)


COLS = [
    "Feature 1",
    "Segment 1",
    "Feature 2",
    "Segment 2",
    "Size 1",
    "Size 2",
    "Size",
    "Dataset Share 1",
    "Dataset Share 2",
    "Dataset Share",
    "Bad Share 1",
    "Bad Share 2",
    "Bad Share",
    "Bad Events",
    "Bad Rate 1",
    "Bad Rate 2",
    "Bad Rate",
    "CI Low",
    "CI High",
    "Lift 1",
    "Lift 2",
    "Lift"
]

def make_pairwise_segments_analysis(
    features_segmented_datas: list[pd.DataFrame],
    features: list[str],
    segments: list[list[str]],
    dataset_size: int,
    dataset_num_bad_events: int,
    dataset_bad_rate: float
) -> pd.DataFrame:
    pairwise_segments_report = pd.DataFrame(columns=COLS)
    
    num_features = len(features_segmented_datas)
    for i in range(num_features - 1):
        feature_1_segmented_data = features_segmented_datas[i]
        feature_1 = features[i]
        segments_1 = segments[i]

        for j in range(i+1, num_features):
            feature_2_segmented_data = features_segmented_datas[j]
            feature_2 = features[j]
            segments_2 = segments[j]

            calc_segments_intersection_characteristics(
                feature_1_segmented_data=feature_1_segmented_data,
                feature_1=feature_1,
                segments_1=segments_1,
                feature_2_segmented_data=feature_2_segmented_data,
                feature_2=feature_2,
                segments_2=segments_2,
                dataset_size=dataset_size,
                dataset_num_bad_events=dataset_num_bad_events,
                dataset_bad_rate=dataset_bad_rate,
                result=pairwise_segments_report
            )

    return pairwise_segments_report