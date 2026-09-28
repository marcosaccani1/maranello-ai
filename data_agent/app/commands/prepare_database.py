from app.core.config import settings
from app.services.data_cleaner import DataCleaner
from app.services.data_loader import DataLoader
from app.services.duckdb_dataset_store import DuckDBDatasetStore


def build_dataset_store() -> DuckDBDatasetStore:
    """Build the dataset store used by the preparation command."""
    return DuckDBDatasetStore(
        database_path=settings.database_path,
        loader=DataLoader(
            settings.dataset_path
        ),
        cleaner=DataCleaner(),
    )


def prepare_database() -> None:
    """Build the persistent DuckDB dataset from the source CSV."""
    dataset_store = build_dataset_store()

    dataset_store.reload()

    if not dataset_store.is_initialized():
        raise RuntimeError(
            "DuckDB dataset preparation completed "
            "without producing a valid analytical database."
        )


def main() -> None:
    """Prepare the analytical database before workers are started."""
    print(
        "Preparing Maranello AI analytical database..."
    )

    prepare_database()

    print(
        "Analytical database ready at: "
        f"{settings.database_path}"
    )


if __name__ == "__main__":
    main()
