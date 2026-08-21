import pandas as pd


def make_prettier_pairwise_report(
    pairwise_report: pd.DataFrame,
    dataset_size: int,
    dataset_share_threshold: float,
    dataset_num_bad_events: int,
    bad_share_threshold: float
) -> pd.DataFrame:
    pairwise_report = pairwise_report.copy(deep=True)

    dataset_share_threshold = dataset_size * dataset_share_threshold
    bad_share_threshold = dataset_num_bad_events * bad_share_threshold

    pairwise_report = pairwise_report.query(
        f"(Size > {dataset_share_threshold}) &"
        f"(`Bad Events` > {bad_share_threshold})"
    )
    pairwise_report = pairwise_report.query("(`Lift 1` < Lift) & (`Lift 2` < Lift)")

    pairwise_report["Expected Share"] =\
        pairwise_report["Dataset Share 1"] * pairwise_report["Dataset Share 2"] * 1.0
    pairwise_report["Overlap Ratio"] = pairwise_report.apply(
        lambda x: True if x["Dataset Share"] * 1.0 / x["Expected Share"] > 1.0 else False,
        axis=1
    )
    pairwise_report["Features"] = pairwise_report.apply(
        lambda x: f"{x["Feature 1"]}\n{x["Feature 2"]}",
        axis=1
    )
    pairwise_report["Segments"] = pairwise_report.apply(
        lambda x: f"{x["Segment 1"]}\n{x["Segment 2"]}",
        axis=1
    )
    pairwise_report["Min Parent Size"] = pairwise_report[["Size 1", "Size 2"]].min(axis=1)
    pairwise_report["Retention From Smaller Parent"] = pairwise_report.apply(
        lambda x: x["Size"] * 1.0 / x["Min Parent Size"],
        axis=1
    )
    pairwise_report["Max Parent Bad Rate"] = pairwise_report[["Bad Rate 1", "Bad Rate 2"]].max(axis=1)
    pairwise_report["Delta Bad Rate"] = pairwise_report["Bad Rate"] - pairwise_report["Max Parent Bad Rate"]
    pairwise_report["Max Parent Lift"] = pairwise_report[["Lift 1", "Lift 2"]].max(axis=1)
    pairwise_report["Delta Lift"] = pairwise_report["Lift"] - pairwise_report["Max Parent Lift"]

    pairwise_report = pairwise_report[
        [
            "Features",
            "Segments",
            "Size",
            "Overlap Ratio",
            "Retention From Smaller Parent",
            "Dataset Share",
            "Bad Events",
            "Bad Share",
            "Bad Rate",
            "CI Low",
            "CI High",
            "Delta Bad Rate",
            "Lift",
            "Delta Lift"
        ]
    ]

    return pairwise_report