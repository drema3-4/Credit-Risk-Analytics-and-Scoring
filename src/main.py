from scripts.prepare_analytical_dataset import (
    prepare_analytical_dataset,
)
from scripts.make_dataset_db import (
    make_dataset_db
)


def main() -> None:
    prepare_analytical_dataset()
    make_dataset_db()


if __name__ == "__main__":
    main()