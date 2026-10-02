from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[3]
ENV_FILE = PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    service_name: str = "maranello-ai-data-agent"
    environment: str = "development"

    project_root: Path = PROJECT_ROOT

    dataset_path: Path = PROJECT_ROOT / "data" / "manufacturing_quality_data.csv"

    database_path: Path = PROJECT_ROOT / "data" / "manufacturing_quality.duckdb"

    charts_directory: Path = PROJECT_ROOT / "data_agent" / "generated_charts"

    data_agent_workers: int = Field(
        default=1,
        gt=0,
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
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
