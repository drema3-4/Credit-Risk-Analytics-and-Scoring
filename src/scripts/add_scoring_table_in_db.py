import pandas as pd
import sqlite3
from catboost import CatBoostClassifier


def add_scoring_table_in_db() -> None:
    data = pd.read_csv("data/scoring_data/data.csv")

    data["borrower_id"] = list(range(1, data.shape[0]+1))

    catboost_classifier = CatBoostClassifier()
    catboost_classifier.load_model("data/models_data/catboost_model.cbm")

    data["score"] = catboost_classifier.predict_proba(data)[:, 1]

    conn = sqlite3.connect("sql_analysis/db.db")

    data[["borrower_id", "score"]].to_sql(
        "borrowers_score",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()