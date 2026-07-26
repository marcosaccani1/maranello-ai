import pytest
from pydantic import ValidationError

from app.ai.providers.factory import create_llm_provider
from app.ai.providers.mock import MockLLMProvider
from app.core.config import Settings


def test_factory_creates_configured_mock_provider() -> None:
    settings = Settings(
        llm_provider="mock",
        llm_model="configured-mock-model",
        _env_file=None,
    )

    provider = create_llm_provider(settings)
    response = provider.generate("Messaggio di test")

    assert isinstance(provider, MockLLMProvider)
    assert response.model == "configured-mock-model"


def test_settings_reject_unsupported_provider() -> None:
    with pytest.raises(ValidationError):
        Settings(
            llm_provider="unsupported",
            _env_file=None,
        )