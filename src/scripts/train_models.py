import json
from sklearn.linear_model import LogisticRegression
from catboost import CatBoostClassifier
import pandas as pd
import joblib
from pathlib import Path

from utils.scoring.evaluate_ranking import (
    evaluate_ranking
)
from utils.scoring.plot_logistic_regression_coefficients import (
    top_logistic_regression_coefficients
)


def train_models() -> None:
    with open("data/models_data/logistic_regression_best_params.json", "r", encoding="utf-8") as f:
        logistic_regression_best_params = json.load(f)
    with open("data/models_data/catboost_classifier_best_params.json", "r", encoding="utf-8") as f:
        catboost_classifier_best_params = json.load(f)

    transformed_train = pd.read_csv("data/scoring_data/transformed_train.csv")
    transformed_test = pd.read_csv("data/scoring_data/transformed_test.csv")
    X_t_train = transformed_train.drop(columns="target")
    y_t_train = transformed_train["target"]
    X_t_test = transformed_test.drop(columns="target")
    y_t_test = transformed_test["target"]

    train = pd.read_csv("data/scoring_data/train.csv")
    test = pd.read_csv("data/scoring_data/test.csv")
    X_train = train.drop(columns="target")
    y_train = train["target"]
    X_test= test.drop(columns="target")
    y_test = test["target"]

    logistic_regression = LogisticRegression(
        **logistic_regression_best_params,
        max_iter=1000,
        random_state=42
    )
    catboost_classifier = CatBoostClassifier(
        **catboost_classifier_best_params,
        random_strength=1,
        loss_function="Logloss",
        random_seed=42,
        verbose=False,
        thread_count=1
    )

    logistic_regression.fit(X_t_train, y_t_train)
    catboost_classifier.fit(X_train, y_train)

    log_reg_path = Path("data/models_data/logistic_regression.joblib")
    log_reg_path.parent.mkdir(parents=True, exist_ok=True)
    catboost_path = Path("data/models_data/catboost_model.cbm")
    catboost_path.parent.mkdir(parents=True, exist_ok=True)
    
    joblib.dump(logistic_regression, log_reg_path)
    catboost_classifier.save_model(catboost_path)

    baseline_model_metrics = evaluate_ranking(
        model=logistic_regression,
        X=X_t_test,
        y=y_t_test
    )
    challenger_model_metrics = evaluate_ranking(
        model=catboost_classifier,
        X=X_test,
        y=y_test
    )

    baseline_model_metrics_path = Path("data/models_data/baseline_model_metrics.json")
    baseline_model_metrics_path.parent.mkdir(parents=True, exist_ok=True)
    challenger_model_metrics_path = Path("data/models_data/challenger_model_metrics.json")
    challenger_model_metrics_path.parent.mkdir(parents=True, exist_ok=True)

    with open(baseline_model_metrics_path, "w", encoding="utf-8") as f:
        json.dump(baseline_model_metrics, f, indent=4, ensure_ascii=False)
    with open(challenger_model_metrics_path, "w", encoding="utf-8") as f:
        json.dump(challenger_model_metrics, f, indent=4, ensure_ascii=False)

    weights_classes = pd.DataFrame({
        "classes": X_t_train.columns,
        "weights_abs": list(map(abs, logistic_regression.coef_[0])),
        "weights": logistic_regression.coef_[0]
    }).sort_values(by="weights_abs", ascending=False).reset_index(drop=True)
    top_logistic_regression_coefficients(weights_classes=weights_classes)