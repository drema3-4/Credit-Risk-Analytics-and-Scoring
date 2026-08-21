from scripts.prepare_analytical_dataset import (
    prepare_analytical_dataset,
)
from scripts.make_raw_data_db import (
    make_raw_data_db
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


def main() -> None:
    prepare_analytical_dataset()
    make_raw_data_db()
    make_reports_risk_analysis()
    make_plots_risk_analysis()
    make_risk_factor_summary()
    make_cross_segment_risk_analysis()


if __name__ == "__main__":
    main()