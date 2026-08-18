from scripts.prepare_analytical_dataset import (
    prepare_analytical_dataset,
)
from scripts.make_raw_data_db import (
    make_raw_data_db
)


def main() -> None:
    prepare_analytical_dataset()
    make_raw_data_db()


if __name__ == "__main__":
    main()