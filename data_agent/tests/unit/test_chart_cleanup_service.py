import os
from pathlib import Path

import pytest

from app.services.chart_cleanup_service import (
    ChartCleanupService,
)


def create_chart(
    path: Path,
    modified_time: float,
) -> None:
    path.write_bytes(b"chart")

    os.utime(
        path,
        (
            modified_time,
            modified_time,
        ),
    )


def test_cleanup_removes_expired_generated_charts(
    tmp_path: Path,
) -> None:
    current_time = 100_000.0
    retention_seconds = 3_600.0

    expired_chart = (
        tmp_path
        / "monthly_defect_rate_expired.png"
    )

    recent_chart = (
        tmp_path
        / "monthly_defect_rate_recent.png"
    )

    create_chart(
        expired_chart,
        current_time
        - retention_seconds
        - 1,
    )

    create_chart(
        recent_chart,
        current_time
        - retention_seconds
        + 1,
    )

    service = ChartCleanupService(
        charts_directory=tmp_path,
        retention_seconds=retention_seconds,
    )

    removed = service.cleanup(
        current_time=current_time
    )

    assert removed == 1
    assert not expired_chart.exists()
    assert recent_chart.exists()


def test_cleanup_preserves_unmanaged_png_files(
    tmp_path: Path,
) -> None:
    current_time = 100_000.0

    unmanaged_chart = (
        tmp_path
        / "unmanaged_chart.png"
    )

    create_chart(
        unmanaged_chart,
        current_time - 100_000,
    )

    service = ChartCleanupService(
        charts_directory=tmp_path,
        retention_seconds=3_600,
    )

    removed = service.cleanup(
        current_time=current_time
    )

    assert removed == 0
    assert unmanaged_chart.exists()


def test_cleanup_returns_zero_for_missing_directory(
    tmp_path: Path,
) -> None:
    charts_directory = (
        tmp_path
        / "missing"
    )

    service = ChartCleanupService(
        charts_directory=charts_directory,
        retention_seconds=3_600,
    )

    assert service.cleanup() == 0


def test_cleanup_rejects_non_positive_retention(
    tmp_path: Path,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "Chart retention must be greater than zero"
        ),
    ):
        ChartCleanupService(
            charts_directory=tmp_path,
            retention_seconds=0,
        )