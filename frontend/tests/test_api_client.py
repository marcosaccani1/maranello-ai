from unittest.mock import Mock, patch

import httpx
import pytest

from app.api_client import BackendConnectionError, send_chat_message


@patch("app.api_client.httpx.post")
def test_send_chat_message_returns_backend_response(
    mock_post: Mock,
) -> None:
    mock_response = Mock()
    mock_response.json.return_value = {
        "answer": "Risposta di test",
        "language": "it",
        "sources": [],
    }
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    response = send_chat_message("Messaggio di test")

    assert response == {
        "answer": "Risposta di test",
        "language": "it",
        "sources": [],
    }

    mock_post.assert_called_once_with(
        "http://127.0.0.1:8000/api/v1/chat",
        json={"message": "Messaggio di test"},
        timeout=30.0,
    )


@patch("app.api_client.httpx.post")
def test_send_chat_message_raises_custom_error(
    mock_post: Mock,
) -> None:
    mock_post.side_effect = httpx.ConnectError("Backend unavailable")

    with pytest.raises(
        BackendConnectionError,
        match="Impossibile contattare il backend",
    ):
        send_chat_message("Messaggio di test")