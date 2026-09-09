from pathlib import Path
from uuid import uuid4

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from app.models.analysis import MonthlyTrendMetric


class ChartService:
    def __init__(self, output_directory: Path) -> None:
        self.output_directory = output_directory
        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def create_monthly_defect_rate_chart(
        self,
        trend: list[MonthlyTrendMetric],
    ) -> Path:
        if not trend:
            raise ValueError(
                "Monthly trend data cannot be empty."
            )

        periods = [item.period for item in trend]
        defect_rates = [
            item.defect_rate for item in trend
        ]

        figure, axis = plt.subplots(
            figsize=(10, 6),
        )

        axis.plot(
            periods,
            defect_rates,
            marker="o",
        )

        axis.set_title(
            "Monthly Manufacturing Defect Rate"
        )
        axis.set_xlabel("Month")
        axis.set_ylabel("Defect Rate (%)")

        axis.grid(
            visible=True,
            alpha=0.3,
        )

        axis.tick_params(
            axis="x",
            rotation=45,
        )

        figure.tight_layout()

        filename = (
            f"monthly_defect_rate_{uuid4().hex}.png"
        )

        output_path = (
            self.output_directory / filename
        )

        figure.savefig(
            output_path,
            dpi=150,
            bbox_inches="tight",
        )

        plt.close(figure)

        return output_path