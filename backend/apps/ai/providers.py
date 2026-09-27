"""AI provider abstraction layer."""

from typing import Protocol


class AIProvider(Protocol):
    def generate(self, system_prompt: str, user_prompt: str) -> str: ...


def get_provider() -> AIProvider:
    from .anthropic_provider import AnthropicProvider

    return AnthropicProvider()
