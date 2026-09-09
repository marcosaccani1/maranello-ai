from pathlib import Path

import pandas as pd
import pytest

from app.models.analysis import (
    GroupedMetric,
    ManufacturingKPIs,
    MonthlyTrendMetric,
)
from app.services.data_analysis_service import DataAnalysisService


class FakeLoader:
    def __init__(self, dataframe: pd.DataFrame) -> None:
        self.dataframe = dataframe

    def load(self) -> pd.DataFrame:
        return self.dataframe.copy()


class FakeCleaner:
    def clean(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        return dataframe.copy()


class FakeAnalysisService:
    def calculate_kpis(
        self,
        dataframe: pd.DataFrame,
    ) -> ManufacturingKPIs:
        return ManufacturingKPIs(
            total_production=1000,
            total_defective_units=20,
            defect_rate=2.0,
            rework_rate=1.0,
            scrap_rate=0.5,
            average_quality_score=95.0,
            average_downtime_minutes=30.0,
            average_cycle_time_seconds=85.0,
        )

    def calculate_defect_rate_by(
        self,
        dataframe: pd.DataFrame,
        dimension: str,
    ) -> list[GroupedMetric]:
        return [
            GroupedMetric(
                group="Line 3",
                total_production=500,
                total_defective_units=15,
                defect_rate=3.0,
            ),
            GroupedMetric(
                group="Line 1",
                total_production=500,
                total_defective_units=5,
                defect_rate=1.0,
            ),
        ]

    def calculate_monthly_trend(
        self,
        dataframe: pd.DataFrame,
    ) -> list[MonthlyTrendMetric]:
        return [
            MonthlyTrendMetric(
                period="2025-01",
                total_production=500,
                total_defective_units=8,
                defect_rate=1.6,
                average_quality_score=96.0,
                average_downtime_minutes=25.0,
            ),
            MonthlyTrendMetric(
                period="2025-02",
                total_production=500,
                total_defective_units=12,
                defect_rate=2.4,
                average_quality_score=94.0,
                average_downtime_minutes=35.0,
            ),
        ]


class FakeChartService:
    def __init__(self, output_path: Path) -> None:
        self.output_path = output_path

    def create_monthly_defect_rate_chart(
        self,
        trend: list[MonthlyTrendMetric],
    ) -> Path:
        return self.output_path


def build_service(
    tmp_path: Path,
) -> DataAnalysisService:
    dataframe = pd.DataFrame(
        {
            "example": [1],
        }
    )

    chart_path = (
        tmp_path
        / "monthly_defect_rate_test.png"
    )

    return DataAnalysisService(
        loader=FakeLoader(dataframe),
        cleaner=FakeCleaner(),
        analysis_service=FakeAnalysisService(),
        chart_service=FakeChartService(
            chart_path
        ),
    )


def test_execute_global_kpis_returns_expected_result(
    tmp_path: Path,
) -> None:
    service = build_service(tmp_path)

    result = service.execute(
        analysis_type="global_kpis"
    )

    assert result.analysis_type == "global_kpis"
    assert result.chart_url is None

    assert result.data[
        "total_production"
    ] == 1000

    assert result.data[
        "total_defective_units"
    ] == 20

    assert result.data["defect_rate"] == 2.0
    assert result.data["rework_rate"] == 1.0
    assert result.data["scrap_rate"] == 0.5

    assert "1,000 units" in result.summary
    assert "2.00%" in result.summary


def test_execute_grouped_defect_rate_returns_expected_result(
    tmp_path: Path,
) -> None:
    service = build_service(tmp_path)

    result = service.execute(
        analysis_type="grouped_defect_rate",
        dimension="production_line",
    )

    assert (
        result.analysis_type
        == "grouped_defect_rate"
    )

    assert result.chart_url is None
    assert len(result.data) == 2

    assert result.data[0]["group"] == "Line 3"
    assert result.data[0]["defect_rate"] == 3.0

    assert (
        "Line 3"
        in result.summary
    )

    assert (
        "3.00%"
        in result.summary
    )


def test_execute_grouped_defect_rate_requires_dimension(
    tmp_path: Path,
) -> None:
    service = build_service(tmp_path)

    with pytest.raises(
        ValueError,
        match=(
            "A grouping dimension is required"
        ),
    ):
        service.execute(
            analysis_type="grouped_defect_rate"
        )


def test_execute_monthly_trend_returns_chart_url(
    tmp_path: Path,
) -> None:
    service = build_service(tmp_path)

    result = service.execute(
        analysis_type="monthly_trend"
    )

    assert result.analysis_type == "monthly_trend"

    assert result.chart_url == (
        "/charts/"
        "monthly_defect_rate_test.png"
    )

    assert len(result.data) == 2

    assert (
        "2.40% in 2025-02"
        in result.summary
    )

    assert (
        "1.60% in 2025-01"
        in result.summary
    )


def test_execute_raises_error_for_unsupported_analysis_type(
    tmp_path: Path,
) -> None:
    service = build_service(tmp_path)

    with pytest.raises(
        ValueError,
        match="Unsupported analysis type",
    ):
        service.execute(
            analysis_type="unsupported",
        )