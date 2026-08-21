import pandas as pd
import json
from pathlib import Path
import dataframe_image as dfi


def make_models_metrics() -> None:
    with open("data/models_data/baseline_model_metrics.json", "r", encoding="utf-8") as f:
        baseline_model_metrics = json.load(f)
    with open("data/models_data/challenger_model_metrics.json", "r", encoding="utf-8") as f:
        challenger_model_metrics = json.load(f)

    models_metrics = pd.DataFrame(columns=["model", "ROC-AUC", "Gini", "KS", "PR-AUC"])

    models_metrics.loc[ models_metrics.shape[0] ] = [
        "Logistic Regression",
        baseline_model_metrics["roc_auc"],
        baseline_model_metrics["gini"],
        baseline_model_metrics["ks"],
        baseline_model_metrics["pr_auc"]
    ]

    models_metrics.loc[ models_metrics.shape[0] ] = [
        "CatBoost Classifier",
        challenger_model_metrics["roc_auc"],
        challenger_model_metrics["gini"],
        challenger_model_metrics["ks"],
        challenger_model_metrics["pr_auc"]
    ]

    models_metrics.loc[ models_metrics.shape[0] ] = [
        "Delta PP",
        (challenger_model_metrics["roc_auc"] - baseline_model_metrics["roc_auc"]) * 100,
        (challenger_model_metrics["gini"] - baseline_model_metrics["gini"]) * 100,
        (challenger_model_metrics["ks"] - baseline_model_metrics["ks"]) * 100,
        (challenger_model_metrics["pr_auc"] - baseline_model_metrics["pr_auc"]) * 100
    ]

    path = Path("../docs/scoring/models_metrics_vs.png")
    path.parent.mkdir(parents=True, exist_ok=True)
    dfi.export(models_metrics, path, table_conversion="matplotlib")