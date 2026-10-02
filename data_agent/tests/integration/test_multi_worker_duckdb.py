import multiprocessing
from pathlib import Path
from queue import Empty

import pandas as pd

from app.services.data_cleaner import DataCleaner
from app.services.data_loader import DataLoader
from app.services.duckdb_analysis_repository import (
    DuckDBAnalysisRepository,
)
from app.services.duckdb_dataset_store import DuckDBDatasetStore

WORKER_COUNT = 3
WORKER_TIMEOUT_SECONDS = 10


def run_read_only_worker(
    database_path: str,
    start_event,
    result_queue,
) -> None:
    """Read the prepared DuckDB database from an isolated worker process."""
    start_event.wait()

    try:
        repository = DuckDBAnalysisRepository(Path(database_path))
        result = repository.calculate_kpis()

        result_queue.put(
            (
                "ok",
                result.total_production,
                result.total_defective_units,
                result.defect_rate,
            )
        )
    except Exception as exc:
        result_queue.put(
            (
                "error",
                type(exc).__name__,
                str(exc),
            )
        )


def create_source_csv(
    dataset_path: Path,
) -> None:
    """Create an isolated source dataset for the multi-worker test."""
    dataframe = pd.DataFrame(
        [
            {
                "batch_id": "BATCH-001",
                "production_date": "2025-01-10",
                "plant": "Plant A",
                "production_line": "Line 1",
                "vehicle_model": "Model A",
                "shift": "Day",
                "units_produced": 100,
                "defective_units": 2,
                "defect_category": "Paint",
                "rework_units": 1,
                "scrap_units": 0,
                "downtime_minutes": 10.0,
                "cycle_time_seconds": 80.0,
                "quality_score": 95.0,
                "supplier_id": "SUP-01",
                "component_category": "Body",
                "inspection_status": "Passed",
                "temperature_c": 22.0,
                "operator_team": "Team A",
                "notes": "Worker test row 1",
            },
            {
                "batch_id": "BATCH-002",
                "production_date": "2025-01-11",
                "plant": "Plant A",
                "production_line": "Line 2",
                "vehicle_model": "Model B",
                "shift": "Night",
                "units_produced": 200,
                "defective_units": 6,
                "defect_category": "Electronics",
                "rework_units": 2,
                "scrap_units": 1,
                "downtime_minutes": 20.0,
                "cycle_time_seconds": 90.0,
                "quality_score": 90.0,
                "supplier_id": "SUP-02",
                "component_category": "Electronics",
                "inspection_status": "Review",
                "temperature_c": 23.0,
                "operator_team": "Team B",
                "notes": "Worker test row 2",
            },
        ]
    )

    dataframe.to_csv(
        dataset_path,
        index=False,
    )


def test_multiple_workers_read_database_only_after_preparation(
    tmp_path: Path,
) -> None:
    dataset_path = tmp_path / "manufacturing.csv"
    database_path = tmp_path / "multi_worker.duckdb"

    create_source_csv(dataset_path)

    dataset_store = DuckDBDatasetStore(
        database_path=database_path,
        loader=DataLoader(dataset_path),
        cleaner=DataCleaner(),
    )

    dataset_store.reload()

    assert dataset_store.is_initialized() is True

    context = multiprocessing.get_context("spawn")
    start_event = context.Event()
    result_queue = context.Queue()

    workers = [
        context.Process(
            target=run_read_only_worker,
            args=(
                str(database_path),
                start_event,
                result_queue,
            ),
        )
        for _ in range(WORKER_COUNT)
    ]

    try:
        for worker in workers:
            worker.start()

        start_event.set()

        results = []

        for _ in range(WORKER_COUNT):
            try:
                results.append(result_queue.get(timeout=WORKER_TIMEOUT_SECONDS))
            except Empty as exc:
                raise AssertionError("Timed out waiting for a worker result.") from exc

        for worker in workers:
            worker.join(timeout=WORKER_TIMEOUT_SECONDS)

        assert all(worker.exitcode == 0 for worker in workers)

        assert (
            results
            == [
                (
                    "ok",
                    300,
                    8,
                    2.67,
                )
            ]
            * WORKER_COUNT
        )
    finally:
        for worker in workers:
            if worker.is_alive():
                worker.terminate()

            worker.join(timeout=WORKER_TIMEOUT_SECONDS)

        result_queue.close()
        result_queue.join_thread()
