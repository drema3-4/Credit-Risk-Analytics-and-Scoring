import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from catboost import CatBoostClassifier
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score, roc_curve
from pathlib import Path


def make_catboost_classifier_vs_logistic_regression_roc_curves() -> None:
    transformed_test = pd.read_csv("data/scoring_data/transformed_test.csv")
    test = pd.read_csv("data/scoring_data/test.csv")

    X_t_test = transformed_test.drop(columns="target")
    y_t_test = transformed_test["target"]
    X_test = test.drop(columns="target")
    y_test = test["target"]

    logistic_regression = joblib.load("data/models_data/logistic_regression.joblib")
    catboost_classifier = CatBoostClassifier()
    catboost_classifier.load_model("data/models_data/catboost_model.cbm")

    logistic_score = logistic_regression.predict_proba(X_t_test)[:, 1]
    catboost_score = catboost_classifier.predict_proba(X_test)[:, 1]

    logistic_fpr, logistic_tpr, _ = roc_curve(
        y_test,
        logistic_score
    )
    catboost_fpr, catboost_tpr, _ = roc_curve(
        y_test,
        catboost_score
    )

    logistic_auc = roc_auc_score(
        y_test,
        logistic_score
    )
    catboost_auc = roc_auc_score(
        y_t_test,
        catboost_score
    )

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.plot(
        logistic_fpr,
        logistic_tpr,
        label=f"Logistic Regression (AUC = {logistic_auc:.3f})"
    )

    ax.plot(
        catboost_fpr,
        catboost_tpr,
        label=f"CatBoost (AUC = {catboost_auc:.3f})"
    )

    ax.plot(
        [0, 1],
        [0, 1],
        linestyle="--",
        label="Random classifier"
    )

    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curves — Logistic Regression vs CatBoost")
    ax.legend()
    ax.grid(alpha=0.25)

    path = Path("../docs/scoring/roc_aucs_logistic_regression_vs_catboost_classifier.png")
    path.parent.mkdir(parents=True, exist_ok=True)

    plt.savefig(path)