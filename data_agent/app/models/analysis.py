from typing import Any, Literal

from pydantic import BaseModel, Field


class ManufacturingKPIs(BaseModel):
    total_production: int
    total_defective_units: int
    defect_rate: float
    rework_rate: float
    scrap_rate: float
    average_quality_score: float | None
    average_downtime_minutes: float | None
    average_cycle_time_seconds: float | None


class GroupedMetric(BaseModel):
    group: str
    total_production: int
    total_defective_units: int
    defect_rate: float


class MonthlyTrendMetric(BaseModel):
    period: str
    total_production: int
    total_defective_units: int
    defect_rate: float
    average_quality_score: float | None
    average_downtime_minutes: float | None


class AnalysisRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=1000,
    )


class AnalysisResult(BaseModel):
    analysis_type: Literal[
        "global_kpis",
        "grouped_defect_rate",
        "monthly_trend",
    ]
    summary: str
    data: Any
    chart_url: str | None = None


class AnalysisResponse(BaseModel):
    success: bool
    result: AnalysisResult | None = None
    error: str | None = None