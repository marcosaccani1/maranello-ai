class AIProviderError(RuntimeError):
    """Base error raised when an AI provider cannot generate a response."""


class AIProviderConfigurationError(AIProviderError):
    """Raised when an AI provider is not configured correctly."""


class AIProviderRequestError(AIProviderError):
    """Raised when an external provider request fails."""
