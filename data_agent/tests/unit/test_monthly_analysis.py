import pandas as pd

from app.services.analysis_service import AnalysisService


def test_calculate_monthly_trend_returns_expected_results() -> None:
    dataframe = pd.DataFrame(
        {
            "production_date": pd.to_datetime(
                [
                    "2025-01-10",
                    "2025-01-20",
                    "2025-02-05",
                    "2025-02-15",
                ]
            ),
            "units_produced": [100, 100, 100, 100],
            "defective_units": [2, 4, 5, 7],
            "quality_score": [96.0, 94.0, 92.0, 90.0],
            "downtime_minutes": [10.0, 20.0, 30.0, 50.0],
            "valid_defect_data": [True, True, True, True],
        }
    )

    service = AnalysisService()

    result = service.calculate_monthly_trend(dataframe)

    assert len(result) == 2

    january = result[0]
    february = result[1]

    assert january.period == "2025-01"
    assert january.total_production == 200
    assert january.total_defective_units == 6
    assert january.defect_rate == 3.0
    assert january.average_quality_score == 95.0
    assert january.average_downtime_minutes == 15.0

    assert february.period == "2025-02"
    assert february.total_production == 200
    assert february.total_defective_units == 12
    assert february.defect_rate == 6.0
    assert february.average_quality_score == 91.0
    assert february.average_downtime_minutes == 40.0


def test_calculate_monthly_trend_excludes_invalid_defect_records() -> None:
    dataframe = pd.DataFrame(
        {
            "production_date": pd.to_datetime(
                ["2025-01-10", "2025-01-20"]
            ),
            "units_produced": [100, 50],
            "defective_units": [5, 80],
            "quality_score": [95.0, 85.0],
            "downtime_minutes": [20.0, 100.0],
            "valid_defect_data": [True, False],
        }
    )

    service = AnalysisService()

    result = service.calculate_monthly_trend(dataframe)

    assert len(result) == 1
    assert result[0].total_production == 100
    assert result[0].total_defective_units == 5
    assert result[0].defect_rate == 5.0

    assert result[0].average_quality_score == 90.0
    assert result[0].average_downtime_minutes == 60.0


def test_calculate_monthly_trend_is_chronologically_sorted() -> None:
    dataframe = pd.DataFrame(
        {
            "production_date": pd.to_datetime(
                [
                    "2025-03-10",
                    "2025-01-10",
                    "2025-02-10",
                ]
            ),
            "units_produced": [100, 100, 100],
            "defective_units": [3, 2, 4],
            "quality_score": [94.0, 96.0, 95.0],
            "downtime_minutes": [30.0, 10.0, 20.0],
            "valid_defect_data": [True, True, True],
        }
    )

    service = AnalysisService()

    result = service.calculate_monthly_trend(dataframe)

    assert [item.period for item in result] == [
        "2025-01",
        "2025-02",
        "2025-03",
    ]


def test_calculate_monthly_trend_returns_empty_list_without_valid_dates() -> None:
    dataframe = pd.DataFrame(
        {
            "production_date": pd.Series(
                [pd.NaT, pd.NaT],
                dtype="datetime64[ns]",
            ),
            "units_produced": [100, 100],
            "defective_units": [2, 3],
            "quality_score": [95.0, 94.0],
            "downtime_minutes": [20.0, 30.0],
            "valid_defect_data": [True, True],
        }
    )

    service = AnalysisService()

    result = service.calculate_monthly_trend(dataframe)

    assert result == []