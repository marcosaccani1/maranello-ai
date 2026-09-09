import pandas as pd

from app.services.analysis_service import AnalysisService


def test_calculate_kpis_returns_expected_values() -> None:
    dataframe = pd.DataFrame(
        {
            "units_produced": [100, 200],
            "defective_units": [5, 10],
            "rework_units": [3, 6],
            "scrap_units": [1, 2],
            "quality_score": [95.0, 91.0],
            "downtime_minutes": [20.0, 40.0],
            "cycle_time_seconds": [120.0, 140.0],
            "valid_defect_data": [True, True],
        }
    )

    service = AnalysisService()

    result = service.calculate_kpis(dataframe)

    assert result.total_production == 300
    assert result.total_defective_units == 15
    assert result.defect_rate == 5.0
    assert result.rework_rate == 3.0
    assert result.scrap_rate == 1.0
    assert result.average_quality_score == 93.0
    assert result.average_downtime_minutes == 30.0
    assert result.average_cycle_time_seconds == 130.0


def test_calculate_kpis_excludes_invalid_defect_records_from_rate_calculations() -> None:
    dataframe = pd.DataFrame(
        {
            "units_produced": [100, 50],
            "defective_units": [5, 80],
            "rework_units": [3, 20],
            "scrap_units": [1, 10],
            "quality_score": [95.0, 85.0],
            "downtime_minutes": [20.0, 100.0],
            "cycle_time_seconds": [120.0, 200.0],
            "valid_defect_data": [True, False],
        }
    )

    service = AnalysisService()

    result = service.calculate_kpis(dataframe)

    assert result.total_production == 100
    assert result.total_defective_units == 5
    assert result.defect_rate == 5.0
    assert result.rework_rate == 3.0
    assert result.scrap_rate == 1.0

    assert result.average_quality_score == 90.0
    assert result.average_downtime_minutes == 60.0
    assert result.average_cycle_time_seconds == 160.0


def test_calculate_kpis_ignores_missing_values_when_calculating_averages() -> None:
    dataframe = pd.DataFrame(
        {
            "units_produced": [100, 100],
            "defective_units": [2, 4],
            "rework_units": [1, 2],
            "scrap_units": [0, 1],
            "quality_score": [94.0, None],
            "downtime_minutes": [30.0, None],
            "cycle_time_seconds": [120.0, None],
            "valid_defect_data": [True, True],
        }
    )

    service = AnalysisService()

    result = service.calculate_kpis(dataframe)

    assert result.average_quality_score == 94.0
    assert result.average_downtime_minutes == 30.0
    assert result.average_cycle_time_seconds == 120.0


def test_calculate_kpis_returns_none_when_average_has_no_valid_values() -> None:
    dataframe = pd.DataFrame(
        {
            "units_produced": [100],
            "defective_units": [2],
            "rework_units": [1],
            "scrap_units": [0],
            "quality_score": [None],
            "downtime_minutes": [None],
            "cycle_time_seconds": [None],
            "valid_defect_data": [True],
        }
    )

    service = AnalysisService()

    result = service.calculate_kpis(dataframe)

    assert result.average_quality_score is None
    assert result.average_downtime_minutes is None
    assert result.average_cycle_time_seconds is None


def test_calculate_kpis_handles_zero_valid_production() -> None:
    dataframe = pd.DataFrame(
        {
            "units_produced": [0],
            "defective_units": [0],
            "rework_units": [0],
            "scrap_units": [0],
            "quality_score": [95.0],
            "downtime_minutes": [20.0],
            "cycle_time_seconds": [120.0],
            "valid_defect_data": [True],
        }
    )

    service = AnalysisService()

    result = service.calculate_kpis(dataframe)

    assert result.total_production == 0
    assert result.total_defective_units == 0
    assert result.defect_rate == 0.0
    assert result.rework_rate == 0.0
    assert result.scrap_rate == 0.0