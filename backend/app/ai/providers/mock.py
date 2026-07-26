from app.ai.providers.base import BaseLLMProvider


class MockLLMProvider(BaseLLMProvider):
    """Deterministic provider used during development and automated tests."""

    def generate(self, message: str) -> str:
        """Return a predictable response without calling an external LLM."""

        return (
            "Maranello AI ha ricevuto correttamente il tuo messaggio: "
            f'"{message}"'
        )