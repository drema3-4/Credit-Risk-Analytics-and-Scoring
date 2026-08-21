from utils.scoring.calc_logistic_regression_best_params import (
    calc_logistic_regression_best_params
)
from utils.scoring.calc_catboost_classifier_best_params import (
    calc_catboost_classifier_best_params
)


def calc_models_best_params() -> None:
    calc_logistic_regression_best_params()
    calc_catboost_classifier_best_params()