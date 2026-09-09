from pathlib import Path

import pytest

from app.models.analysis import MonthlyTrendMetric
from app.services.chart_service import ChartService


def test_create_monthly_defect_rate_chart_creates_png(
    tmp_path: Path,
) -> None:
    trend = [
        MonthlyTrendMetric(
            period="2025-01",
            total_production=1000,
            total_defective_units=20,
            defect_rate=2.0,
            average_quality_score=95.0,
            average_downtime_minutes=30.0,
        ),
        MonthlyTrendMetric(
            period="2025-02",
            total_production=1200,
            total_defective_units=36,
            defect_rate=3.0,
            average_quality_score=94.0,
            average_downtime_minutes=35.0,
        ),
    ]

    service = ChartService(
        output_directory=tmp_path,
    )

    output_path = (
        service.create_monthly_defect_rate_chart(
            trend
        )
    )

    assert output_path.exists()
    assert output_path.is_file()
    assert output_path.suffix == ".png"
    assert output_path.stat().st_size > 0


def test_create_monthly_defect_rate_chart_uses_unique_filenames(
    tmp_path: Path,
) -> None:
    trend = [
        MonthlyTrendMetric(
            period="2025-01",
            total_production=1000,
            total_defective_units=20,
            defect_rate=2.0,
            average_quality_score=95.0,
            average_downtime_minutes=30.0,
        )
    ]

    service = ChartService(
        output_directory=tmp_path,
    )

    first_path = (
        service.create_monthly_defect_rate_chart(
            trend
        )
    )

    second_path = (
        service.create_monthly_defect_rate_chart(
            trend
        )
    )

    assert first_path != second_path
    assert first_path.exists()
    assert second_path.exists()


def test_create_monthly_defect_rate_chart_rejects_empty_data(
    tmp_path: Path,
) -> None:
    service = ChartService(
        output_directory=tmp_path,
    )

    with pytest.raises(
        ValueError,
        match="Monthly trend data cannot be empty",
    ):
        service.create_monthly_defect_rate_chart([])