from app.commands.prepare_database import prepare_database
from app.core.config import settings
from app.services.duckdb_analysis_repository import (
    DuckDBAnalysisRepository,
)


def build_repository() -> DuckDBAnalysisRepository:
    prepare_database()

    return DuckDBAnalysisRepository(
        settings.database_path
    )


def test_real_dataset_grouped_analysis_returns_expected_dimensions() -> None:
    repository = build_repository()

    production_lines = repository.calculate_defect_rate_by(
        "production_line"
    )
    shifts = repository.calculate_defect_rate_by(
        "shift"
    )
    suppliers = repository.calculate_defect_rate_by(
        "supplier_id"
    )
    components = repository.calculate_defect_rate_by(
        "component_category"
    )

    assert len(production_lines) == 4
    assert len(shifts) == 3
    assert len(suppliers) == 12
    assert len(components) == 6


def test_real_dataset_grouped_analysis_is_sorted_by_defect_rate() -> None:
    repository = build_repository()

    results = repository.calculate_defect_rate_by(
        "production_line"
    )

    defect_rates = [
        item.defect_rate
        for item in results
    ]

    assert defect_rates == sorted(
        defect_rates,
        reverse=True,
    )