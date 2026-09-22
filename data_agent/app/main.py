import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager, suppress

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.core.config import settings
from app.services.chart_cleanup_service import ChartCleanupService

chart_cleanup_service = ChartCleanupService(
    charts_directory=settings.charts_directory,
    retention_seconds=(
        settings.chart_retention_hours
        * 60
        * 60
    ),
)


async def run_chart_cleanup_loop() -> None:
    """Periodically remove expired generated chart files."""
    interval_seconds = (
        settings.chart_cleanup_interval_minutes
        * 60
    )

    while True:
        await asyncio.sleep(interval_seconds)
        await asyncio.to_thread(
            chart_cleanup_service.cleanup
        )


@asynccontextmanager
async def lifespan(
    app: FastAPI,
) -> AsyncIterator[None]:
    """Manage startup and shutdown resources for the Data Agent."""
    del app

    settings.charts_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    await asyncio.to_thread(
        chart_cleanup_service.cleanup
    )

    cleanup_task = asyncio.create_task(
        run_chart_cleanup_loop()
    )

    try:
        yield
    finally:
        cleanup_task.cancel()

        with suppress(asyncio.CancelledError):
            await cleanup_task


app = FastAPI(
    title="Maranello AI Data Agent",
    version="0.1.0",
    description=(
        "Python analytics microservice for "
        "Maranello AI manufacturing data."
    ),
    lifespan=lifespan,
)

settings.charts_directory.mkdir(
    parents=True,
    exist_ok=True,
)

app.mount(
    "/charts",
    StaticFiles(
        directory=settings.charts_directory
    ),
    name="charts",
)

app.include_router(
    router,
    prefix="/api",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "maranello-ai-data-agent",
        "environment": settings.environment,
    }


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": "maranello-ai-data-agent",
        "status": "running",
        "environment": settings.environment,
    }