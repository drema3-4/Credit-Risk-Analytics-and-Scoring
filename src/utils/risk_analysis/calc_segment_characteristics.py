import pandas as pd


def cacl_segment_characteristics(
    segment: pd.DataFrame,
    dataset_size: int,
    dataset_num_bad_events: int,
    dataset_bad_rate: float
):
    size = segment.shape[0]
    dataset_share = (segment.shape[0] * 1.0)/ dataset_size
    bad_share = (segment["target"].sum() * 1.0) / dataset_num_bad_events
    bad_rate = segment["target"].mean()
    lift = bad_rate / dataset_bad_rate
    borrowers_idx = set(segment["borrower_id"].to_list())
    borrowers_t1_idx = set(
        segment.loc[segment["target"] == 1, "borrower_id"].to_list()
    )

    return [
        size,
        dataset_share,
        bad_share,
        bad_rate,
        lift,
        borrowers_idx,
        borrowers_t1_idx
    ]