from pathlib import Path

from utils.data_quality_prepare import data_quality_prepare


def prepare_analytical_dataset() -> None:
    data_path = Path("data/raw/cs-training.csv")
    output_path = Path("data/interim/borrowers.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    data_quality_prepare(data_path=data_path, out_path=output_path)