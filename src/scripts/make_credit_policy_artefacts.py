import pandas as pd
from catboost import CatBoostClassifier

from utils.credit_policy.make_scenario_table import (
    make_scenario_table
)
from utils.credit_policy.plot_approved_borrowers_and_bads import (
    plot_approved_borrowers_and_bads
)
from utils.credit_policy.plot_price_and_effect_of_the_policy import (
    plot_price_and_effect_of_the_policy
)


def make_credit_policy_artefacts() -> None:
    data = pd.read_csv("data/scoring_data/test.csv")

    model = CatBoostClassifier()
    model.load_model("data/models_data/catboost_model.cbm")

    data["score"] = model.predict_proba(data.drop(columns="target"))[:, 1]
    data = data.sort_values(by="score", ascending=False).reset_index(drop=True)

    scenario_table = make_scenario_table(data)

    plot_approved_borrowers_and_bads(scenario_table)

    plot_price_and_effect_of_the_policy(scenario_table)