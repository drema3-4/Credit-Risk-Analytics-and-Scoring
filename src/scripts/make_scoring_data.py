import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path
import numpy as np

from utils.scoring.prepare_dataset import (
    prepare_dataset
)


BASE_PATH = "data/scoring_data"

FEATURES = [
    "revolving_utilization",
    "age",
    "num_30_59_days_late",
    "debt_ratio",
    "monthly_income",
    "num_open_credit_lines",
    "num_90_days_late",
    "num_real_estate_loans",
    "num_60_89_days_late",
    "num_dependents"
]

SEGMENTS = [
    [0.0, 0.2, 0.4, 0.5, 0.7, 1.0, 2.0, 5.0, np.inf],
    [0.0, 22.0, 30.0, 45.0, 55.0, 75.0, np.inf],
    [1, 2, np.inf],
    [0.0, 0.1, 0.7, 1.0, 4.0, np.inf],
    [0.0, 900.0, 3000.0, 4500.0, 6500.0, 13000.0, np.inf],
    [1, 2, np.inf],
    [1, 2, np.inf],
    [1, 3, np.inf],
    [1, 2, np.inf],
    [1, 2, np.inf]
]

SPECIAL_VALUES = [
    [],
    [],
    [0, 96, 98],
    [0],
    [],
    [0],
    [0, 96, 98],
    [0],
    [0, 96, 98],
    [0]
]


def make_scoring_data() -> None:
    data = pd.read_csv("data/interim/borrowers.csv")

    train_idx, test_idx = train_test_split(
        data.index,
        test_size=0.1,
        shuffle=True,
        random_state=42,
        stratify=data["target"]
    )

    train = data.loc[train_idx]
    test = data.loc[test_idx]

    transformed_train = prepare_dataset(
        data=train,
        features=FEATURES,
        segmentss=SEGMENTS,
        special_valuess=SPECIAL_VALUES
    )
    transformed_test = prepare_dataset(
        data=test,
        features=FEATURES,
        segmentss=SEGMENTS,
        special_valuess=SPECIAL_VALUES
    )

    train.fillna(-1)
    test.fillna(-1)
    data.fillna(-1)

    path = Path(BASE_PATH + "/")
    path.mkdir(parents=True, exist_ok=True)

    train_path = Path(f"{BASE_PATH}/train.csv")
    test_path = Path(f"{BASE_PATH}/test.csv")
    transformed_train_path = Path(f"{BASE_PATH}/transformed_train.csv")
    transformed_test_path = Path(f"{BASE_PATH}/transformed_test.csv")
    data_path = Path(f"{BASE_PATH}/data.csv")

    train.to_csv(train_path, index=False)
    test.to_csv(test_path, index=False)
    transformed_train.to_csv(transformed_train_path, index=False)
    transformed_test.to_csv(transformed_test_path, index=False)
    data.to_csv(data_path, index=False)