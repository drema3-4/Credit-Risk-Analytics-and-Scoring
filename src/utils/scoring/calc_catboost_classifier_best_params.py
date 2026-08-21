from catboost import CatBoostClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
import pandas as pd
import optuna
import json
from pathlib import Path

def calc_catboost_classifier_best_params() -> None:
    def objective(trial):
        model = CatBoostClassifier(
            iterations=trial.suggest_int(
                "iterations",
                300,
                700,
                step=100
            ),

            learning_rate=trial.suggest_float(
                "learning_rate",
                0.02,
                0.08,
                log=True
            ),

            depth=trial.suggest_int(
                "depth",
                4,
                7
            ),

            l2_leaf_reg=trial.suggest_float(
                "l2_leaf_reg",
                3,
                12,
                log=True
            ),

            auto_class_weights=trial.suggest_categorical(
                "auto_class_weights",
                [None, "SqrtBalanced"]
            ),

            random_strength=1,

            loss_function="Logloss",
            random_seed=42,
            verbose=False,
            thread_count=1
        )

        cv = StratifiedKFold(
            n_splits=5,
            shuffle=True,
            random_state=42
        )

        scores = cross_val_score(
            model,
            X,
            y,
            cv=cv,
            scoring="roc_auc",
            n_jobs=-1
        )

        return scores.mean()

    train = pd.read_csv("data/scoring_data/train.csv")

    X = train.drop(columns="target")
    y = train["target"]

    study = optuna.create_study(direction="maximize")

    study.optimize(
        objective,
        n_trials=20
    )

    best_params = study.best_params

    path = Path("data/models_data/catboost_classifier_best_params.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(best_params, f, indent=4, ensure_ascii=False)