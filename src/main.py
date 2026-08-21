import optuna
import warnings

from scripts.prepare_analytical_dataset import (
    prepare_analytical_dataset,
)
from scripts.make_db import (
    make_db
)
from scripts.make_risk_analysis_artefacts import (
    make_reports_risk_analysis,
    make_plots_risk_analysis
)
from scripts.make_risk_factor_summary import (
    make_risk_factor_summary
)
from scripts.make_cross_segment_risk_analysis import (
    make_cross_segment_risk_analysis
)
from scripts.make_scoring_data import (
    make_scoring_data
)
from scripts.calc_models_best_params import (
    calc_models_best_params
)
from scripts.train_models import (
    train_models
)
from scripts.make_catboost_classifier_vs_logistic_regression_roc_curves import (
    make_catboost_classifier_vs_logistic_regression_roc_curves
)
from scripts.make_models_metrics import (
    make_models_metrics
)
from scripts.make_risk_ranking_decile_table import (
    make_risk_ranking_decile_table
)
from scripts.add_scoring_table_in_db import (
    add_scoring_table_in_db
)

optuna.logging.disable_default_handler()
warnings.filterwarnings("ignore")


def main() -> None:
    print("1. prepare analytical dataset")
    prepare_analytical_dataset()
    print("2. make db")
    make_db()
    print("3. make reports risk analysis")
    make_reports_risk_analysis()
    print("4. make plots risk analysis")
    make_plots_risk_analysis()
    print("5. make risk factor summary")
    make_risk_factor_summary()
    print("6. make cross segments risk analysis")
    make_cross_segment_risk_analysis()
    print("7. make scoring data")
    make_scoring_data()
    print("8. calc models best params")
    # calc_models_best_params()
    print("9. train models")
    train_models()
    print("10. make catboost classifier vs logistic regression roc curves")
    make_catboost_classifier_vs_logistic_regression_roc_curves()
    print("11. make models metrics")
    make_models_metrics()
    print("12. make risk ranking decile table")
    make_risk_ranking_decile_table()
    print("13. add scoring table in db")
    add_scoring_table_in_db()

if __name__ == "__main__":
    main()