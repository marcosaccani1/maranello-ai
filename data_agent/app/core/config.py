from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    service_name: str = "maranello-ai-data-agent"
    environment: str = "development"

    project_root: Path = Path(__file__).resolve().parents[3]

    dataset_path: Path = (
        project_root
        / "data"
        / "manufacturing_quality_data.csv"
    )

    database_path: Path = (
        project_root
        / "data"
        / "manufacturing_quality.duckdb"
    )

    charts_directory: Path = (
        project_root
        / "data_agent"
        / "generated_charts"
    )

    chart_retention_hours: float = Field(
        default=24.0,
        gt=0,
    )

    chart_cleanup_interval_minutes: float = Field(
        default=60.0,
        gt=0,
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()