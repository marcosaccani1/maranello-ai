from pathlib import Path

import duckdb
import pytest

from app.services.duckdb_analysis_repository import (
    DuckDBAnalysisRepository,
)


@pytest.fixture
def database_path(tmp_path: Path) -> Path:
    path = tmp_path / "analytics.duckdb"

    connection = duckdb.connect(str(path))

    try:
        connection.execute(
            """
            CREATE TABLE manufacturing_data (
                batch_id VARCHAR,
                production_date TIMESTAMP,
                plant VARCHAR,
                production_line VARCHAR,
                vehicle_model VARCHAR,
                shift VARCHAR,
                units_produced BIGINT,
                defective_units BIGINT,
                defect_category VARCHAR,
                rework_units BIGINT,
                scrap_units BIGINT,
                downtime_minutes DOUBLE,
                cycle_time_seconds DOUBLE,
                quality_score DOUBLE,
                supplier_id VARCHAR,
                component_category VARCHAR,
                inspection_status VARCHAR,
                temperature_c DOUBLE,
                operator_team VARCHAR,
                notes VARCHAR,
                valid_defect_data BOOLEAN
            )
            """
        )

        connection.execute(
            """
            INSERT INTO manufacturing_data VALUES
            (
                'BATCH-001',
                '2025-01-10',
                'Plant A',
                'Line 1',
                'Model A',
                'Day',
                100,
                2,
                'Paint',
                1,
                1,
                10.0,
                80.0,
                95.0,
                'SUP-01',
                'Body',
                'Passed',
                22.0,
                'Team A',
                'Row 1',
                TRUE
            ),
            (
                'BATCH-002',
                '2025-01-20',
                'Plant A',
                'Line 2',
                'Model B',
                'Night',
                200,
                6,
                'Electronics',
                3,
                1,
                20.0,
                90.0,
                90.0,
                'SUP-02',
                'Electronics',
                'Review',
                23.0,
                'Team B',
                'Row 2',
                TRUE
            ),
            (
                'BATCH-003',
                '2025-02-10',
                'Plant A',
                'Line 1',
                'Model A',
                'Day',
                100,
                200,
                'Paint',
                10,
                5,
                30.0,
                100.0,
                NULL,
                'SUP-01',
                'Body',
                'Review',
                24.0,
                'Team A',
                'Invalid defect row',
                FALSE
            )
            """
        )
    finally:
        connection.close()

    return path


@pytest.fixture
def repository(
    database_path: Path,
) -> DuckDBAnalysisRepository:
    return DuckDBAnalysisRepository(database_path)


def create_edge_case_repository(
    tmp_path: Path,
    rows_sql: str,
) -> DuckDBAnalysisRepository:
    path = tmp_path / "edge_cases.duckdb"

    connection = duckdb.connect(str(path))

    try:
        connection.execute(
            """
            CREATE TABLE manufacturing_data (
                batch_id VARCHAR,
                production_date TIMESTAMP,
                plant VARCHAR,
                production_line VARCHAR,
                vehicle_model VARCHAR,
                shift VARCHAR,
                units_produced BIGINT,
                defective_units BIGINT,
                defect_category VARCHAR,
                rework_units BIGINT,
                scrap_units BIGINT,
                downtime_minutes DOUBLE,
                cycle_time_seconds DOUBLE,
                quality_score DOUBLE,
                supplier_id VARCHAR,
                component_category VARCHAR,
                inspection_status VARCHAR,
                temperature_c DOUBLE,
                operator_team VARCHAR,
                notes VARCHAR,
                valid_defect_data BOOLEAN
            )
            """
        )

        connection.execute(
            f"""
            INSERT INTO manufacturing_data
            {rows_sql}
            """
        )
    finally:
        connection.close()

    return DuckDBAnalysisRepository(path)


def test_calculate_kpis_uses_valid_defect_rows_for_rates(
    repository: DuckDBAnalysisRepository,
) -> None:
    result = repository.calculate_kpis()

    assert result.total_production == 300
    assert result.total_defective_units == 8
    assert result.defect_rate == 2.67
    assert result.rework_rate == 1.33
    assert result.scrap_rate == 0.67
    assert result.average_quality_score == 92.5
    assert result.average_downtime_minutes == 20.0
    assert result.average_cycle_time_seconds == 90.0


def test_calculate_kpis_ignores_null_values_in_averages(
    tmp_path: Path,
) -> None:
    repository = create_edge_case_repository(
        tmp_path,
        """
        VALUES
        (
            'BATCH-001',
            '2025-01-10',
            'Plant A',
            'Line 1',
            'Model A',
            'Day',
            100,
            2,
            'Paint',
            1,
            0,
            30.0,
            120.0,
            94.0,
            'SUP-01',
            'Body',
            'Passed',
            22.0,
            'Team A',
            'Valid values',
            TRUE
        ),
        (
            'BATCH-002',
            '2025-01-11',
            'Plant A',
            'Line 1',
            'Model A',
            'Day',
            100,
            4,
            'Paint',
            2,
            1,
            NULL,
            NULL,
            NULL,
            'SUP-01',
            'Body',
            'Passed',
            22.0,
            'Team A',
            'Missing averages',
            TRUE
        )
        """,
    )

    result = repository.calculate_kpis()

    assert result.average_quality_score == 94.0
    assert result.average_downtime_minutes == 30.0
    assert result.average_cycle_time_seconds == 120.0


def test_calculate_kpis_returns_none_when_averages_have_no_values(
    tmp_path: Path,
) -> None:
    repository = create_edge_case_repository(
        tmp_path,
        """
        VALUES
        (
            'BATCH-001',
            '2025-01-10',
            'Plant A',
            'Line 1',
            'Model A',
            'Day',
            100,
            2,
            'Paint',
            1,
            0,
            NULL,
            NULL,
            NULL,
            'SUP-01',
            'Body',
            'Passed',
            22.0,
            'Team A',
            'Missing averages',
            TRUE
        )
        """,
    )

    result = repository.calculate_kpis()

    assert result.average_quality_score is None
    assert result.average_downtime_minutes is None
    assert result.average_cycle_time_seconds is None


def test_calculate_kpis_handles_zero_valid_production(
    tmp_path: Path,
) -> None:
    repository = create_edge_case_repository(
        tmp_path,
        """
        VALUES
        (
            'BATCH-001',
            '2025-01-10',
            'Plant A',
            'Line 1',
            'Model A',
            'Day',
            0,
            0,
            'Paint',
            0,
            0,
            20.0,
            120.0,
            95.0,
            'SUP-01',
            'Body',
            'Passed',
            22.0,
            'Team A',
            'Zero production',
            TRUE
        )
        """,
    )

    result = repository.calculate_kpis()

    assert result.total_production == 0
    assert result.total_defective_units == 0
    assert result.defect_rate == 0.0
    assert result.rework_rate == 0.0
    assert result.scrap_rate == 0.0


def test_calculate_defect_rate_by_groups_and_sorts(
    repository: DuckDBAnalysisRepository,
) -> None:
    result = repository.calculate_defect_rate_by(
        "production_line"
    )

    assert [item.group for item in result] == [
        "Line 2",
        "Line 1",
    ]

    assert result[0].total_production == 200
    assert result[0].total_defective_units == 6
    assert result[0].defect_rate == 3.0

    assert result[1].total_production == 100
    assert result[1].total_defective_units == 2
    assert result[1].defect_rate == 2.0


def test_calculate_defect_rate_by_excludes_null_groups(
    tmp_path: Path,
) -> None:
    repository = create_edge_case_repository(
        tmp_path,
        """
        VALUES
        (
            'BATCH-001',
            '2025-01-10',
            'Plant A',
            'Line 1',
            'Model A',
            'Day',
            100,
            3,
            'Paint',
            1,
            0,
            20.0,
            120.0,
            95.0,
            'SUP-01',
            'Body',
            'Passed',
            22.0,
            'Team A',
            'Known supplier',
            TRUE
        ),
        (
            'BATCH-002',
            '2025-01-11',
            'Plant A',
            'Line 1',
            'Model A',
            'Day',
            100,
            10,
            'Paint',
            2,
            1,
            20.0,
            120.0,
            95.0,
            NULL,
            'Body',
            'Passed',
            22.0,
            'Team A',
            'Missing supplier',
            TRUE
        )
        """,
    )

    result = repository.calculate_defect_rate_by(
        "supplier_id"
    )

    assert len(result) == 1
    assert result[0].group == "SUP-01"
    assert result[0].total_production == 100
    assert result[0].total_defective_units == 3
    assert result[0].defect_rate == 3.0


def test_calculate_defect_rate_by_rejects_unknown_dimension(
    repository: DuckDBAnalysisRepository,
) -> None:
    with pytest.raises(
        ValueError,
        match="Unsupported grouping dimension",
    ):
        repository.calculate_defect_rate_by(
            "arbitrary_sql"
        )


def test_calculate_monthly_trend_is_ordered(
    repository: DuckDBAnalysisRepository,
) -> None:
    result = repository.calculate_monthly_trend()

    assert [item.period for item in result] == [
        "2025-01",
        "2025-02",
    ]

    january = result[0]

    assert january.total_production == 300
    assert january.total_defective_units == 8
    assert january.defect_rate == 2.67
    assert january.average_quality_score == 92.5
    assert january.average_downtime_minutes == 15.0

    february = result[1]

    assert february.total_production == 0
    assert february.total_defective_units == 0
    assert february.defect_rate == 0.0
    assert february.average_quality_score is None
    assert february.average_downtime_minutes == 30.0


def test_calculate_monthly_trend_returns_empty_without_valid_dates(
    tmp_path: Path,
) -> None:
    repository = create_edge_case_repository(
        tmp_path,
        """
        VALUES
        (
            'BATCH-001',
            NULL,
            'Plant A',
            'Line 1',
            'Model A',
            'Day',
            100,
            2,
            'Paint',
            1,
            0,
            20.0,
            120.0,
            95.0,
            'SUP-01',
            'Body',
            'Passed',
            22.0,
            'Team A',
            'Missing date',
            TRUE
        )
        """,
    )

    result = repository.calculate_monthly_trend()

    assert result == []


def test_repository_requires_existing_database(
    tmp_path: Path,
) -> None:
    repository = DuckDBAnalysisRepository(
        tmp_path / "missing.duckdb"
    )

    with pytest.raises(
        FileNotFoundError,
        match="DuckDB database not found",
    ):
        repository.calculate_kpis()