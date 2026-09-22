import time
from pathlib import Path


class ChartCleanupService:
    """Remove generated chart files older than the configured retention."""

    def __init__(
        self,
        charts_directory: Path,
        retention_seconds: float,
    ) -> None:
        if retention_seconds <= 0:
            raise ValueError(
                "Chart retention must be greater than zero."
            )

        self.charts_directory = charts_directory
        self.retention_seconds = retention_seconds

    def cleanup(
        self,
        current_time: float | None = None,
    ) -> int:
        """Delete expired generated PNG charts and return the removal count."""
        if not self.charts_directory.exists():
            return 0

        now = (
            current_time
            if current_time is not None
            else time.time()
        )

        removed_files = 0

        for path in self.charts_directory.glob(
            "monthly_defect_rate_*.png"
        ):
            if not path.is_file():
                continue

            age_seconds = (
                now
                - path.stat().st_mtime
            )

            if age_seconds <= self.retention_seconds:
                continue

            try:
                path.unlink()
            except FileNotFoundError:
                continue

            removed_files += 1

        return removed_files