from typing import Any

import httpx

DEFAULT_BACKEND_URL = "http://127.0.0.1:8000"


class BackendConnectionError(RuntimeError):
    """Raised when the frontend cannot contact the backend."""


def send_chat_message(
    message: str,
    backend_url: str = DEFAULT_BACKEND_URL,
) -> dict[str, Any]:
    """Send a chat message to the backend API."""

    endpoint = f"{backend_url.rstrip('/')}/api/v1/chat"

    try:
        response = httpx.post(
            endpoint,
            json={"message": message},
            timeout=30.0,
        )
        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise BackendConnectionError(
            "Impossibile contattare il backend di Maranello AI."
        ) from exc

    return response.json()
