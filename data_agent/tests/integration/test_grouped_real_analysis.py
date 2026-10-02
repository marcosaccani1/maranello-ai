from pathlib import Path

from app.core.config import settings
from app.services.data_cleaner import DataCleaner
from app.services.data_loader import DataLoader
from app.services.duckdb_analysis_repository import (
    DuckDBAnalysisRepository,
)
from app.services.duckdb_dataset_store import DuckDBDatasetStore


def build_repository(
    database_path: Path,
) -> DuckDBAnalysisRepository:
    dataset_store = DuckDBDatasetStore(
        database_path=database_path,
        loader=DataLoader(settings.dataset_path),
        cleaner=DataCleaner(),
    )

    dataset_store.reload()

    assert dataset_store.is_initialized()

    return DuckDBAnalysisRepository(database_path)


def test_real_dataset_grouped_analysis_returns_expected_dimensions(
    tmp_path: Path,
) -> None:
    repository = build_repository(tmp_path / "grouped_dimensions.duckdb")

    production_lines = repository.calculate_defect_rate_by("production_line")
    shifts = repository.calculate_defect_rate_by("shift")
    suppliers = repository.calculate_defect_rate_by("supplier_id")
    components = repository.calculate_defect_rate_by("component_category")

    assert len(production_lines) == 4
    assert len(shifts) == 3
    assert len(suppliers) == 12
    assert len(components) == 6


def test_real_dataset_grouped_analysis_is_sorted_by_defect_rate(
    tmp_path: Path,
) -> None:
    repository = build_repository(tmp_path / "grouped_sorting.duckdb")

    results = repository.calculate_defect_rate_by("production_line")

    defect_rates = [item.defect_rate for item in results]

    assert defect_rates == sorted(
        defect_rates,
        reverse=True,
    )
