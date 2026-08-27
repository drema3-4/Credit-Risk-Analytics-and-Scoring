import pandas as pd
from pathlib import Path
import dataframe_image as dfi


def make_scenario_table(
    data: pd.DataFrame,
    quantiles: list[float] = [1.00, 0.95, 0.90, 0.85, 0.80, 0.75, 0.70]
) -> pd.DataFrame:
    scenario_tables = pd.DataFrame(columns=[
        "Scenario",
        "All Borrowers",
        "Approved Borrowers",
        "Approved Bad Rate",
        "Bads",
        "Approved Bads",
        "Rejected Bads",
        "Reject Bad Rate",
        "Bad Capture Rate"
    ])

    dataset_size = data.shape[0] * 1.0
    dataset_num_bads = data["target"].sum() * 1.0

    for reject_rate in quantiles:
        reject = data.query(f"score > {data["score"].quantile(reject_rate)}")
        approved = data.query(f"score <= {data["score"].quantile(reject_rate)}")

        approved_borrowers = approved.shape[0]
        approved_num_bads = approved["target"].sum() * 1.0
        approved_bad_rate = approved_num_bads / approved_borrowers

        reject_borrowers = reject.shape[0]
        reject_num_bads = reject["target"].sum() * 1.0
        reject_bad_rate = (
            reject_num_bads / reject_borrowers
            if reject_borrowers > 0
            else float("nan")
        )

        bad_capture_rate = reject_num_bads / dataset_num_bads

        scenario_tables.loc[ scenario_tables.shape[0] ] = [
            f"reject {1.0 - reject_rate:.2f}",
            int(dataset_size),
            approved_borrowers,
            approved_bad_rate,
            int(dataset_num_bads),
            approved_num_bads,
            reject_num_bads,
            reject_bad_rate,
            bad_capture_rate
        ]

    scenario_tables["Additional Rejected Bad Borrowers"] = (
        scenario_tables["Bad Capture Rate"].diff()
    )

    out_path = Path("../docs/credit_policy/scenario_tables.png")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    dfi.export(scenario_tables, out_path, table_conversion="matplotlib")

    return scenario_tables