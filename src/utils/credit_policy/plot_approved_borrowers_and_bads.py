import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def plot_approved_borrowers_and_bads(
    scenario_table: pd.DataFrame
) -> None:
    reject_rate = (
        scenario_table["Scenario"]
        .str.replace("reject ", "", regex=False)
        .astype(float)
        * 100
    )

    approved_borrowers_share = (
        scenario_table["Approved Borrowers"]
        / scenario_table["All Borrowers"]
        * 100
    )

    approved_bads_share = (
        scenario_table["Approved Bads"]
        / scenario_table["Bads"]
        * 100
    )

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.plot(
        reject_rate,
        approved_borrowers_share,
        marker="o",
        linewidth=2,
        label="Approved Borrowers"
    )

    ax.plot(
        reject_rate,
        approved_bads_share,
        marker="o",
        linewidth=2,
        label="Approved Bads"
    )

    ax.set_xlabel("Reject Rate, %")
    ax.set_ylabel("Remaining Population, %")
    ax.set_title(
        "Approved Borrowers vs Approved Bads"
    )

    ax.set_xticks(reject_rate)
    ax.legend()
    ax.grid(alpha=0.25)

    plt.tight_layout()

    out_path = Path("../docs/credit_policy/plot_approved_borrowers_and_bads.png")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path)