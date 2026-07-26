import pytest
from pydantic import ValidationError

from app.ai.providers.factory import create_llm_provider
from app.ai.providers.mock import MockLLMProvider
from app.core.config import Settings


def test_factory_creates_mock_provider() -> None:
    settings = Settings(
        llm_provider="mock",
        _env_file=None,
    )

    provider = create_llm_provider(settings)

    assert isinstance(provider, MockLLMProvider)


def test_settings_reject_unsupported_provider() -> None:
    with pytest.raises(ValidationError):
        Settings(
            llm_provider="unsupported",
            _env_file=None,
        )