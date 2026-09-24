from pathlib import Path

import pytest

from app.models.analysis import (
    GroupedMetric,
    ManufacturingKPIs,
    MonthlyTrendMetric,
)
from app.services.data_analysis_service import DataAnalysisService


class FakeDatasetStore:
    def __init__(self) -> None:
        self.initialize_calls = 0
        self.reload_calls = 0

    def initialize(self) -> None:
        self.initialize_calls += 1

    def reload(self) -> None:
        self.reload_calls += 1


class FakeAnalysisRepository:
    def __init__(self) -> None:
        self.kpi_calls = 0
        self.grouped_calls: list[str] = []
        self.monthly_calls = 0

    def calculate_kpis(
        self,
    ) -> ManufacturingKPIs:
        self.kpi_calls += 1

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
        dimension: str,
    ) -> list[GroupedMetric]:
        self.grouped_calls.append(
            dimension
        )

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
    ) -> list[MonthlyTrendMetric]:
        self.monthly_calls += 1

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
    def __init__(
        self,
        output_path: Path,
    ) -> None:
        self.output_path = output_path
        self.create_calls = 0

    def create_monthly_defect_rate_chart(
        self,
        trend: list[MonthlyTrendMetric],
    ) -> Path:
        self.create_calls += 1

        return self.output_path


def build_service(
    tmp_path: Path,
) -> tuple[
    DataAnalysisService,
    FakeDatasetStore,
    FakeAnalysisRepository,
    FakeChartService,
]:
    dataset_store = FakeDatasetStore()
    analysis_repository = FakeAnalysisRepository()

    chart_service = FakeChartService(
        tmp_path
        / "monthly_defect_rate_test.png"
    )

    service = DataAnalysisService(
        dataset_store=dataset_store,
        analysis_repository=analysis_repository,
        chart_service=chart_service,
    )

    return (
        service,
        dataset_store,
        analysis_repository,
        chart_service,
    )


def test_execute_global_kpis_returns_expected_result(
    tmp_path: Path,
) -> None:
    (
        service,
        dataset_store,
        repository,
        _,
    ) = build_service(tmp_path)

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

    assert dataset_store.initialize_calls == 1
    assert repository.kpi_calls == 1


def test_execute_grouped_defect_rate_returns_expected_result(
    tmp_path: Path,
) -> None:
    (
        service,
        dataset_store,
        repository,
        _,
    ) = build_service(tmp_path)

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

    assert "Line 3" in result.summary
    assert "3.00%" in result.summary

    assert dataset_store.initialize_calls == 1

    assert repository.grouped_calls == [
        "production_line"
    ]


def test_execute_grouped_defect_rate_requires_dimension(
    tmp_path: Path,
) -> None:
    (
        service,
        dataset_store,
        repository,
        _,
    ) = build_service(tmp_path)

    with pytest.raises(
        ValueError,
        match=(
            "A grouping dimension is required"
        ),
    ):
        service.execute(
            analysis_type="grouped_defect_rate"
        )

    assert dataset_store.initialize_calls == 1
    assert repository.grouped_calls == []


def test_execute_monthly_trend_returns_chart_url(
    tmp_path: Path,
) -> None:
    (
        service,
        dataset_store,
        repository,
        chart_service,
    ) = build_service(tmp_path)

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

    assert dataset_store.initialize_calls == 1
    assert repository.monthly_calls == 1
    assert chart_service.create_calls == 1


def test_execute_raises_error_for_unsupported_analysis_type(
    tmp_path: Path,
) -> None:
    (
        service,
        dataset_store,
        _,
        _,
    ) = build_service(tmp_path)

    with pytest.raises(
        ValueError,
        match="Unsupported analysis type",
    ):
        service.execute(
            analysis_type="unsupported",
        )

    assert dataset_store.initialize_calls == 1


def test_multiple_analyses_reuse_persistent_dataset(
    tmp_path: Path,
) -> None:
    (
        service,
        dataset_store,
        repository,
        _,
    ) = build_service(tmp_path)

    service.execute(
        analysis_type="global_kpis"
    )

    service.execute(
        analysis_type="grouped_defect_rate",
        dimension="production_line",
    )

    service.execute(
        analysis_type="monthly_trend"
    )

    assert dataset_store.initialize_calls == 3
    assert repository.kpi_calls == 1

    assert repository.grouped_calls == [
        "production_line"
    ]

    assert repository.monthly_calls == 1


def test_reload_dataset_rebuilds_persistent_dataset(
    tmp_path: Path,
) -> None:
    (
        service,
        dataset_store,
        _,
        _,
    ) = build_service(tmp_path)

    service.reload_dataset()

    assert dataset_store.reload_calls == 1


def test_initialize_dataset_delegates_to_store(
    tmp_path: Path,
) -> None:
    (
        service,
        dataset_store,
        _,
        _,
    ) = build_service(tmp_path)

    service.initialize_dataset()

    assert dataset_store.initialize_calls == 1