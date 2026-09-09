from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.core.config import settings

app = FastAPI(
    title="Maranello AI Data Agent",
    version="0.1.0",
    description=(
        "Python analytics microservice for "
        "Maranello AI manufacturing data."
    ),
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