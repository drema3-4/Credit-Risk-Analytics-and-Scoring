import pandas as pd
from statsmodels.stats.proportion import proportion_confint

from utils.risk_analysis.calc_segment_characteristics import (
    cacl_segment_characteristics
)


def calc_segments_intersection_characteristics(
    feature_1_segmented_data: pd.DataFrame,
    feature_1: str,
    segments_1: list[str],
    feature_2_segmented_data: pd.DataFrame,
    feature_2: str,
    segments_2: list[str],
    dataset_size: int,
    dataset_num_bad_events: int,
    dataset_bad_rate: float,
    result: pd.DataFrame
):
    f1sd = feature_1_segmented_data.copy(deep=True)
    f1_s_col = f"{feature_1}_segments"
    f2sd = feature_2_segmented_data.copy(deep=True)
    f2_s_col = f"{feature_2}_segments"
    
    for segment_1 in segments_1:
        s_1 = f1sd[f1sd[f1_s_col] == segment_1]
        size_1, dataset_share_1, bad_share_1, bad_rate_1, lift_1, borrowers_idx_1, borrowers_t1_idx_1 =\
            cacl_segment_characteristics(
            s_1,
            dataset_size,
            dataset_num_bad_events,
            dataset_bad_rate
        )

        for segment_2 in segments_2:
            s_2 = f2sd[f2sd[f2_s_col] == segment_2]
            size_2, dataset_share_2, bad_share_2, bad_rate_2, lift_2, borrowers_idx_2, borrowers_t1_idx_2 =\
                cacl_segment_characteristics(
                    s_2,
                    dataset_size,
                    dataset_num_bad_events,
                    dataset_bad_rate
                )

            size = len(borrowers_idx_1 & borrowers_idx_2)
            dataset_share = (size * 1.0) / dataset_size
            bad_events = len(borrowers_t1_idx_1 & borrowers_t1_idx_2)
            bad_share = (bad_events * 1.0) / dataset_num_bad_events
            bad_rate = (bad_events * 1.0) / size if size > 0 else 0
            lift = bad_rate / dataset_bad_rate

            ci_low_bad_rate, ci_high_bad_rate =\
                [0.0, 0.0] if size == 0 else proportion_confint(
                    count=bad_events,
                    nobs=size,
                    alpha=0.05,
                    method="wilson"
                )

            result.loc[ result.shape[0] ] = [
                feature_1,
                segment_1,
                feature_2,
                segment_2,
                size_1,
                size_2,
                size,
                dataset_share_1,
                dataset_share_2,
                dataset_share,
                bad_share_1,
                bad_share_2,
                bad_share,
                bad_events,
                bad_rate_1,
                bad_rate_2,
                bad_rate,
                ci_low_bad_rate,
                ci_high_bad_rate,
                lift_1,
                lift_2,
                lift
            ]