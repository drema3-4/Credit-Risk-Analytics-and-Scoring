import pandas as pd
import sqlite3
from catboost import CatBoostClassifier


def add_scoring_table_in_db() -> None:
    data = pd.read_csv("data/scoring_data/data.csv")

    catboost_classifier = CatBoostClassifier()
    catboost_classifier.load_model("data/models_data/catboost_model.cbm")

    data["score"] = catboost_classifier.predict_proba(data)[:, 1]

    conn = sqlite3.connect("sql_analysis/db.db")

    data.to_sql(
        "scored_borrowers",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()