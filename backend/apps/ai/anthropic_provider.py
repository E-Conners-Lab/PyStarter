"""AI provider: Anthropic API by default, or any OpenAI-compatible local server."""

import logging
from typing import Any

from django.conf import settings

logger = logging.getLogger(__name__)

FALLBACK_MESSAGE = "Sorry, I'm having trouble generating a response right now. Please try again."
MAX_OUTPUT_TOKENS = 1024


def _first_text(blocks: list[Any]) -> str:
    """Return the first text block of an Anthropic response, or '' if there is none."""
    for block in blocks:
        if getattr(block, "type", None) == "text":
            return block.text
    return ""


class AnthropicProvider:
    def __init__(self) -> None:
        self.model: str = settings.ANTHROPIC_MODEL
        base_url: str = settings.ANTHROPIC_BASE_URL

        if base_url:
            # Local LLM via OpenAI-compatible API (Ollama, LM Studio, etc.)
            try:
                from openai import OpenAI
            except ImportError:
                logger.error("openai package required for local LLM support: pip install openai")
                raise
            self.client = OpenAI(api_key=settings.ANTHROPIC_API_KEY or "not-needed", base_url=base_url)
            self._use_openai = True
        else:
            import anthropic

            self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            self._use_openai = False

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        try:
            if self._use_openai:
                return self._generate_openai(system_prompt, user_prompt)
            return self._generate_anthropic(system_prompt, user_prompt)
        except Exception:
            # Full traceback goes to the server log; the caller gets a generic message (SEC-11).
            logger.exception("AI provider error (model=%s)", self.model)
            return FALLBACK_MESSAGE

    def _generate_openai(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=MAX_OUTPUT_TOKENS,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content or FALLBACK_MESSAGE

    def _generate_anthropic(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=MAX_OUTPUT_TOKENS,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        if response.stop_reason == "refusal":
            logger.warning("AI provider refused request (model=%s)", self.model)
            return FALLBACK_MESSAGE
        return _first_text(response.content) or FALLBACK_MESSAGE
