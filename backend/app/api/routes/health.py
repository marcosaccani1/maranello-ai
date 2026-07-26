from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
def health_check() -> dict[str, str]:
    """Return the current health status of the API."""

    settings = get_settings()

    return {
        "status": "healthy",
        "service": settings.app_name,
        "environment": settings.app_env,
    }
