import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def plot_price_and_effect_of_the_policy(
    scenario_table: pd.DataFrame
) -> None:
    reject_rate = (
        scenario_table["Scenario"]
        .str.replace("reject ", "", regex=False)
        .astype(float)
        * 100
    )

    plt.figure(figsize=(16, 5))

    plt.subplot(1, 2, 1)
    plt.bar(
        reject_rate,
        scenario_table["All Borrowers"],
        width=3.5,
        alpha=0.35,
        label="All Borrowers"
    )
    plt.bar(
        reject_rate,
        scenario_table["Approved Borrowers"],
        width=2.2,
        label="Approved Borrowers"
    )
    plt.xlabel("Reject Rate, %")
    plt.ylabel("Borrowers")
    plt.title(
        "All Borrowers vs Approved Borrowers"
    )
    plt.xticks(reject_rate)
    plt.legend()
    plt.grid(axis="y", alpha=0.25)

    plt.subplot(1, 2, 2)
    plt.bar(
        reject_rate,
        scenario_table["Bads"],
        width=3.5,
        alpha=0.35,
        label="All Bads"
    )
    plt.bar(
        reject_rate,
        scenario_table["Approved Bads"],
        width=2.2,
        label="Approved Bads"
    )
    plt.xlabel("Reject Rate, %")
    plt.ylabel("Bad Borrowers")
    plt.title(
        "All Bads vs Approved Bads"
    )
    plt.xticks(reject_rate)
    plt.legend()
    plt.grid(axis="y", alpha=0.25)

    plt.tight_layout()

    out_path = Path("../docs/credit_policy/plot_approved_borrowers_and_bads.png")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path)