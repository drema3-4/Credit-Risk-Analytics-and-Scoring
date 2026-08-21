import pandas as pd
from catboost import CatBoostClassifier
from pathlib import Path
import dataframe_image as dfi
import matplotlib.pyplot as plt


def observed_bad_rate_by_risk_decile(
    risk_groups: pd.DataFrame
) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))

    bars = ax.bar(
        risk_groups["risk_group"].astype(str),
        risk_groups["observed_bad_rate"] * 100
    )

    ax.bar_label(
        bars,
        labels=[
            f"{value:.1f}%"
            for value in risk_groups["observed_bad_rate"] * 100
        ],
        padding=3
    )

    ax.set_xlabel("Risk Decile")
    ax.set_ylabel("Observed Bad Rate, %")
    ax.set_title("Observed Bad Rate by Predicted Risk Decile")

    ax.grid(
        axis="y",
        alpha=0.25
    )

def make_risk_ranking_decile_table() -> None:
    test = pd.read_csv("data/scoring_data/test.csv")
    X_test = test.drop(columns="target")
    y_test = test["target"]

    catboost_classifier = CatBoostClassifier()
    catboost_classifier.load_model("data/models_data/catboost_model.cbm")

    risk_table = pd.DataFrame({
        "borrower_id": y_test.index,
        "target": y_test,
        "predicted_risk_score": catboost_classifier.predict_proba(X_test)[:, 1]
    }).sort_values(by="predicted_risk_score")

    risk_table["risk_group"] = pd.qcut(
        risk_table["predicted_risk_score"],
        q=10,
        labels=[f"D{i}" for i in range(1, 11)]
    )

    risk_groups = (
        risk_table
        .groupby("risk_group", observed=True)
        .agg(
            borrowers=("target", "size"),
            avg_predicted_risk=("predicted_risk_score", "mean"),
            observed_bad_rate=("target", "mean")
        )
        .reset_index()
    )

    path = Path("../docs/scoring/make_risk_ranking_decile_table.png")
    path.parent.mkdir(parents=True, exist_ok=True)
    dfi.export(risk_groups, path, table_conversion="matplotlib")

    observed_bad_rate_by_risk_decile(
        risk_groups=risk_groups
    )