import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def top_logistic_regression_coefficients(
    weights_classes: pd.DataFrame
) -> None:
    top_n = 15

    top_coefficients = (
        weights_classes
        .nlargest(top_n, "weights_abs")
        .sort_values("weights")
    )

    fig, ax = plt.subplots(figsize=(9, 7))

    ax.barh(
        top_coefficients["classes"],
        top_coefficients["weights"]
    )

    ax.axvline(
        0,
        linewidth=1
    )

    ax.set_xlabel("Logistic Regression Coefficient")
    ax.set_ylabel("Feature / Segment")
    ax.set_title(f"Top {top_n} Logistic Regression Coefficients")

    ax.grid(
        axis="x",
        alpha=0.25
    )

    plt.tight_layout()

    path = Path("../docs/scoring/top_logistic_regression_coefficients.png")
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(path)