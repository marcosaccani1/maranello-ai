from pathlib import Path

import duckdb
import pandas as pd
import pytest

from app.services.data_cleaner import DataCleaner
from app.services.data_loader import DataLoader
from app.services.duckdb_dataset_store import DuckDBDatasetStore


@pytest.fixture
def source_csv(tmp_path: Path) -> Path:
    dataset_path = tmp_path / "manufacturing.csv"

    dataframe = pd.DataFrame(
        [
            {
                "batch_id": "BATCH-001",
                "production_date": "2025-01-10",
                "plant": "Plant A",
                "production_line": " Line 1 ",
                "vehicle_model": "Model A",
                "shift": " day ",
                "units_produced": 100,
                "defective_units": 2,
                "defect_category": "Paint",
                "rework_units": 1,
                "scrap_units": 1,
                "downtime_minutes": 10.0,
                "cycle_time_seconds": 80.0,
                "quality_score": 95.0,
                "supplier_id": " SUP-01 ",
                "component_category": "Body",
                "inspection_status": "Passed",
                "temperature_c": 22.0,
                "operator_team": "Team A",
                "notes": "Valid row",
            },
            {
                "batch_id": "BATCH-002",
                "production_date": "2025-02-10",
                "plant": "Plant A",
                "production_line": "Line 2",
                "vehicle_model": "Model B",
                "shift": "NIGHT",
                "units_produced": 120,
                "defective_units": 4,
                "defect_category": "Electronics",
                "rework_units": 2,
                "scrap_units": 1,
                "downtime_minutes": 20.0,
                "cycle_time_seconds": 90.0,
                "quality_score": 105.0,
                "supplier_id": "SUP-02",
                "component_category": "Electronics",
                "inspection_status": "Review",
                "temperature_c": 23.0,
                "operator_team": "Team B",
                "notes": "Invalid quality score",
            },
        ]
    )

    dataframe.to_csv(
        dataset_path,
        index=False,
    )

    return dataset_path


@pytest.fixture
def store(
    tmp_path: Path,
    source_csv: Path,
) -> DuckDBDatasetStore:
    return DuckDBDatasetStore(
        database_path=tmp_path / "test.duckdb",
        loader=DataLoader(source_csv),
        cleaner=DataCleaner(),
    )


def test_reload_creates_persistent_database(
    store: DuckDBDatasetStore,
) -> None:
    assert store.is_initialized() is False

    store.reload()

    assert store.database_path.exists()
    assert store.is_initialized() is True


def test_reload_persists_cleaned_dataset(
    store: DuckDBDatasetStore,
) -> None:
    store.reload()

    connection = duckdb.connect(
        str(store.database_path),
        read_only=True,
    )

    try:
        rows = connection.execute(
            """
            SELECT
                batch_id,
                production_line,
                shift,
                supplier_id,
                quality_score,
                valid_defect_data
            FROM manufacturing_data
            ORDER BY batch_id
            """
        ).fetchall()
    finally:
        connection.close()

    assert rows == [
        (
            "BATCH-001",
            "Line 1",
            "Day",
            "SUP-01",
            95.0,
            True,
        ),
        (
            "BATCH-002",
            "Line 2",
            "Night",
            "SUP-02",
            None,
            True,
        ),
    ]


def test_reload_replaces_existing_dataset(
    store: DuckDBDatasetStore,
    source_csv: Path,
) -> None:
    store.reload()

    replacement = pd.read_csv(source_csv)
    replacement = replacement.iloc[[0]].copy()
    replacement.loc[
        replacement.index[0],
        "units_produced",
    ] = 250

    replacement.to_csv(
        source_csv,
        index=False,
    )

    store.reload()

    connection = duckdb.connect(
        str(store.database_path),
        read_only=True,
    )

    try:
        result = connection.execute(
            """
            SELECT
                COUNT(*),
                SUM(units_produced)
            FROM manufacturing_data
            """
        ).fetchone()
    finally:
        connection.close()

    assert result == (1, 250)


def test_reload_failure_preserves_existing_dataset(
    store: DuckDBDatasetStore,
    source_csv: Path,
) -> None:
    store.reload()

    source_csv.unlink()

    with pytest.raises(FileNotFoundError):
        store.reload()

    assert store.is_initialized() is True

    connection = duckdb.connect(
        str(store.database_path),
        read_only=True,
    )

    try:
        result = connection.execute(
            """
            SELECT COUNT(*)
            FROM manufacturing_data
            """
        ).fetchone()
    finally:
        connection.close()

    assert result == (2,)


def test_reload_requires_preparation_dependencies(
    tmp_path: Path,
) -> None:
    store = DuckDBDatasetStore(
        database_path=tmp_path / "test.duckdb",
    )

    with pytest.raises(
        RuntimeError,
        match=(
            "Dataset preparation requires both "
            "a DataLoader and a DataCleaner"
        ),
    ):
        store.reload()

    assert store.database_path.exists() is False


def test_is_initialized_returns_false_when_database_is_missing(
    tmp_path: Path,
) -> None:
    store = DuckDBDatasetStore(
        database_path=tmp_path / "missing.duckdb",
    )

    assert store.is_initialized() is False


def test_readiness_check_does_not_require_preparation_dependencies(
    store: DuckDBDatasetStore,
) -> None:
    store.reload()

    readiness_store = DuckDBDatasetStore(
        database_path=store.database_path,
    )

    assert readiness_store.loader is None
    assert readiness_store.cleaner is None
    assert readiness_store.is_initialized() is True