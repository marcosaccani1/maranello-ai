import pandas as pd
import pytest

from app.services.analysis_service import AnalysisService


def test_calculate_defect_rate_by_returns_expected_results() -> None:
    dataframe = pd.DataFrame(
        {
            "production_line": [
                "Line 1",
                "Line 1",
                "Line 2",
                "Line 2",
            ],
            "units_produced": [100, 100, 100, 100],
            "defective_units": [2, 4, 5, 7],
            "valid_defect_data": [True, True, True, True],
        }
    )

    service = AnalysisService()

    result = service.calculate_defect_rate_by(
        dataframe,
        dimension="production_line",
    )

    assert len(result) == 2

    assert result[0].group == "Line 2"
    assert result[0].total_production == 200
    assert result[0].total_defective_units == 12
    assert result[0].defect_rate == 6.0

    assert result[1].group == "Line 1"
    assert result[1].total_production == 200
    assert result[1].total_defective_units == 6
    assert result[1].defect_rate == 3.0


def test_calculate_defect_rate_by_excludes_invalid_records() -> None:
    dataframe = pd.DataFrame(
        {
            "production_line": ["Line 1", "Line 1"],
            "units_produced": [100, 50],
            "defective_units": [5, 80],
            "valid_defect_data": [True, False],
        }
    )

    service = AnalysisService()

    result = service.calculate_defect_rate_by(
        dataframe,
        dimension="production_line",
    )

    assert len(result) == 1
    assert result[0].total_production == 100
    assert result[0].total_defective_units == 5
    assert result[0].defect_rate == 5.0


def test_calculate_defect_rate_by_excludes_missing_group_values() -> None:
    dataframe = pd.DataFrame(
        {
            "supplier_id": ["SUP-01", None],
            "units_produced": [100, 100],
            "defective_units": [3, 10],
            "valid_defect_data": [True, True],
        }
    )

    service = AnalysisService()

    result = service.calculate_defect_rate_by(
        dataframe,
        dimension="supplier_id",
    )

    assert len(result) == 1
    assert result[0].group == "SUP-01"
    assert result[0].defect_rate == 3.0


def test_calculate_defect_rate_by_rejects_unsupported_dimension() -> None:
    dataframe = pd.DataFrame(
        {
            "production_line": ["Line 1"],
            "units_produced": [100],
            "defective_units": [3],
            "valid_defect_data": [True],
        }
    )

    service = AnalysisService()

    with pytest.raises(
        ValueError,
        match="Unsupported grouping dimension",
    ):
        service.calculate_defect_rate_by(
            dataframe,
            dimension="batch_id",
        )