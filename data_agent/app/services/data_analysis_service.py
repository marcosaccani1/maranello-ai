from typing import Literal

from app.core.config import settings
from app.models.analysis import AnalysisResult
from app.services.chart_service import ChartService
from app.services.data_cleaner import DataCleaner
from app.services.data_loader import DataLoader
from app.services.duckdb_analysis_repository import (
    DuckDBAnalysisRepository,
)
from app.services.duckdb_dataset_store import (
    DuckDBDatasetStore,
)
from app.services.question_interpreter import QuestionInterpreter

AnalysisType = Literal[
    "global_kpis",
    "grouped_defect_rate",
    "monthly_trend",
]


class DataAnalysisService:
    def __init__(
        self,
        dataset_store: DuckDBDatasetStore | None = None,
        analysis_repository: DuckDBAnalysisRepository | None = None,
        chart_service: ChartService | None = None,
        question_interpreter: QuestionInterpreter | None = None,
    ) -> None:
        self.dataset_store = (
            dataset_store
            or DuckDBDatasetStore(
                database_path=settings.database_path,
                loader=DataLoader(
                    settings.dataset_path
                ),
                cleaner=DataCleaner(),
            )
        )

        self.analysis_repository = (
            analysis_repository
            or DuckDBAnalysisRepository(
                database_path=settings.database_path
            )
        )

        self.chart_service = (
            chart_service
            or ChartService(
                settings.charts_directory
            )
        )

        self.question_interpreter = (
            question_interpreter
            or QuestionInterpreter()
        )

    def initialize_dataset(self) -> None:
        """Ensure the persistent DuckDB dataset is available."""
        self.dataset_store.initialize()

    def analyze_question(
        self,
        question: str,
    ) -> AnalysisResult:
        plan = self.question_interpreter.interpret(
            question
        )

        return self.execute(
            analysis_type=plan.analysis_type,
            dimension=plan.dimension,
        )

    def execute(
        self,
        analysis_type: AnalysisType,
        dimension: str | None = None,
    ) -> AnalysisResult:
        self.initialize_dataset()

        if analysis_type == "global_kpis":
            return self._global_kpis()

        if analysis_type == "grouped_defect_rate":
            return self._grouped_defect_rate(
                dimension
            )

        if analysis_type == "monthly_trend":
            return self._monthly_trend()

        raise ValueError(
            f"Unsupported analysis type: {analysis_type}"
        )

    def reload_dataset(self) -> None:
        """Rebuild the persistent DuckDB dataset from the source CSV."""
        self.dataset_store.reload()

    def _global_kpis(
        self,
    ) -> AnalysisResult:
        result = (
            self.analysis_repository
            .calculate_kpis()
        )

        summary = (
            "Manufacturing performance analysis completed. "
            f"Total production was "
            f"{result.total_production:,} units with "
            f"a defect rate of {result.defect_rate:.2f}%, "
            f"a rework rate of {result.rework_rate:.2f}% "
            f"and a scrap rate of {result.scrap_rate:.2f}%."
        )

        return AnalysisResult(
            analysis_type="global_kpis",
            summary=summary,
            data=result.model_dump(),
        )

    def _grouped_defect_rate(
        self,
        dimension: str | None,
    ) -> AnalysisResult:
        if dimension is None:
            raise ValueError(
                "A grouping dimension is required for "
                "grouped defect rate analysis."
            )

        result = (
            self.analysis_repository
            .calculate_defect_rate_by(
                dimension=dimension,
            )
        )

        if not result:
            summary = (
                f"No valid data is available for "
                f"grouping by {dimension}."
            )
        else:
            highest = result[0]

            summary = (
                f"The highest defect rate by {dimension} "
                f"is {highest.group} at "
                f"{highest.defect_rate:.2f}%."
            )

        return AnalysisResult(
            analysis_type="grouped_defect_rate",
            summary=summary,
            data=[
                item.model_dump()
                for item in result
            ],
        )

    def _monthly_trend(
        self,
    ) -> AnalysisResult:
        result = (
            self.analysis_repository
            .calculate_monthly_trend()
        )

        if not result:
            return AnalysisResult(
                analysis_type="monthly_trend",
                summary=(
                    "No valid monthly trend data "
                    "is available."
                ),
                data=[],
            )

        chart_path = (
            self.chart_service
            .create_monthly_defect_rate_chart(
                result
            )
        )

        highest = max(
            result,
            key=lambda item: item.defect_rate,
        )

        lowest = min(
            result,
            key=lambda item: item.defect_rate,
        )

        summary = (
            "Monthly defect rate analysis completed. "
            f"The highest rate was "
            f"{highest.defect_rate:.2f}% in "
            f"{highest.period}, while the lowest was "
            f"{lowest.defect_rate:.2f}% in "
            f"{lowest.period}."
        )

        return AnalysisResult(
            analysis_type="monthly_trend",
            summary=summary,
            data=[
                item.model_dump()
                for item in result
            ],
            chart_url=(
                f"/charts/{chart_path.name}"
            ),
        )