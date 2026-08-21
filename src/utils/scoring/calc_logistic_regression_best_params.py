from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
import pandas as pd
import optuna
import json
from pathlib import Path

def calc_logistic_regression_best_params() -> None:
    def objective(trial):
        C = trial.suggest_float(
            "C",
            1e-3,
            10,
            log=True
        )

        class_weight = trial.suggest_categorical(
            "class_weight",
            [None, "balanced"]
        )

        model = LogisticRegression(
            solver="lbfgs",
            penalty="l2",
            C=C,
            class_weight=class_weight,
            max_iter=1000,
            random_state=42
        )

        cv = StratifiedKFold(
            n_splits=5,
            shuffle=True,
            random_state=42
        )

        score = cross_val_score(
            model,
            X,
            y,
            cv=cv,
            scoring="roc_auc",
            n_jobs=-1
        ).mean()

        return score

    transformed_train = pd.read_csv("data/scoring_data/transformed_train.csv")

    X = transformed_train.drop(columns="target")
    y = transformed_train["target"]

    study = optuna.create_study(direction="maximize")

    study.optimize(
        objective,
        n_trials=20
    )

    best_params = study.best_params

    path = Path("data/models_data/logistic_regression_best_params.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(best_params, f, indent=4, ensure_ascii=False)