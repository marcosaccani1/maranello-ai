import uvicorn

from app.commands.prepare_database import prepare_database
from app.core.config import settings

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8001


def resolve_worker_count() -> int:
    """Return the configured number of Data Agent worker processes."""
    return settings.data_agent_workers


def start_data_agent() -> None:
    """Prepare DuckDB once, then start the Data Agent workers."""
    worker_count = resolve_worker_count()

    print("Preparing Maranello AI analytical database before worker startup...")

    prepare_database()

    print(
        "Analytical database preparation completed. "
        f"Starting {worker_count} Data Agent worker(s)..."
    )

    uvicorn.run(
        "app.main:app",
        host=DEFAULT_HOST,
        port=DEFAULT_PORT,
        workers=worker_count,
    )


def main() -> None:
    """Run the automated Data Agent startup sequence."""
    start_data_agent()


if __name__ == "__main__":
    main()
