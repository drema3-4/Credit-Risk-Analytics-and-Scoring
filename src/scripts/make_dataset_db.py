import sqlite3
import pandas as pd


def make_dataset_db() -> None:
    dataset = pd.read_csv("data/interim/borrowers.csv")

    dataset["borrower_id"] = list(range(dataset.shape[0]))

    conn = sqlite3.connect("sql_analysis/borrowers.db")

    dataset.to_sql(
        "borrowers",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()