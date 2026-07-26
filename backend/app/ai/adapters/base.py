"""Abstract contracts for provider-specific prompt adapters."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from app.ai.prompts.models import Prompt

AdapterOutputT = TypeVar("AdapterOutputT")


class PromptAdapter(ABC, Generic[AdapterOutputT]):
    """Convert internal prompts into provider-specific request structures."""

    @abstractmethod
    def adapt(self, prompt: Prompt) -> AdapterOutputT:
        """Convert a domain prompt into a provider-specific representation.

        Args:
            prompt: Provider-independent prompt domain model.

        Returns:
            A provider-specific request representation.
        """
        raise NotImplementedError
