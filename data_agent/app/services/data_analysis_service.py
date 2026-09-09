from typing import Literal

import pandas as pd

from app.core.config import settings
from app.models.analysis import AnalysisResult
from app.services.analysis_service import AnalysisService
from app.services.chart_service import ChartService
from app.services.data_cleaner import DataCleaner
from app.services.data_loader import DataLoader
from app.services.question_interpreter import QuestionInterpreter

AnalysisType = Literal[
    "global_kpis",
    "grouped_defect_rate",
    "monthly_trend",
]


class DataAnalysisService:
    def __init__(
        self,
        loader: DataLoader | None = None,
        cleaner: DataCleaner | None = None,
        analysis_service: AnalysisService | None = None,
        chart_service: ChartService | None = None,
        question_interpreter: QuestionInterpreter | None = None,
    ) -> None:
        self.loader = loader or DataLoader(
            settings.dataset_path
        )
        self.cleaner = cleaner or DataCleaner()
        self.analysis_service = (
            analysis_service or AnalysisService()
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
        dataframe = self.loader.load()
        cleaned = self.cleaner.clean(dataframe)

        if analysis_type == "global_kpis":
            return self._global_kpis(cleaned)

        if analysis_type == "grouped_defect_rate":
            return self._grouped_defect_rate(
                cleaned,
                dimension,
            )

        if analysis_type == "monthly_trend":
            return self._monthly_trend(cleaned)

        raise ValueError(
            f"Unsupported analysis type: {analysis_type}"
        )

    def _global_kpis(
        self,
        dataframe: pd.DataFrame,
    ) -> AnalysisResult:
        result = self.analysis_service.calculate_kpis(
            dataframe
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
        dataframe: pd.DataFrame,
        dimension: str | None,
    ) -> AnalysisResult:
        if dimension is None:
            raise ValueError(
                "A grouping dimension is required for "
                "grouped defect rate analysis."
            )

        result = (
            self.analysis_service
            .calculate_defect_rate_by(
                dataframe,
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
        dataframe: pd.DataFrame,
    ) -> AnalysisResult:
        result = (
            self.analysis_service
            .calculate_monthly_trend(
                dataframe
            )
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