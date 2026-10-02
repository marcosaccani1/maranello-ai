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


def test_real_dataset_produces_valid_manufacturing_kpis(
    tmp_path: Path,
) -> None:
    repository = build_repository(tmp_path / "real_analysis.duckdb")

    result = repository.calculate_kpis()

    assert result.total_production > 0
    assert result.total_defective_units >= 0

    assert 0.0 <= result.defect_rate <= 100.0
    assert 0.0 <= result.rework_rate <= 100.0
    assert 0.0 <= result.scrap_rate <= 100.0

    assert result.average_quality_score is not None
    assert 0.0 <= result.average_quality_score <= 100.0

    assert result.average_downtime_minutes is not None
    assert result.average_downtime_minutes >= 0.0

    assert result.average_cycle_time_seconds is not None
    assert result.average_cycle_time_seconds > 0.0
