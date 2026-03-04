import logging

from django.conf import settings

logger = logging.getLogger(__name__)


class AnthropicProvider:
    def __init__(self):
        self.model = settings.ANTHROPIC_MODEL
        base_url = settings.ANTHROPIC_BASE_URL

        if base_url:
            # Local LLM via OpenAI-compatible API (Ollama, LM Studio, etc.)
            try:
                from openai import OpenAI

                self.client = OpenAI(
                    api_key=settings.ANTHROPIC_API_KEY or "not-needed",
                    base_url=base_url,
                )
                self._use_openai = True
            except ImportError:
                logger.error("openai package required for local LLM support: pip install openai")
                raise
        else:
            # Anthropic API
            import anthropic

            self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            self._use_openai = False

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        try:
            if self._use_openai:
                response = self.client.chat.completions.create(
                    model=self.model,
                    max_tokens=1024,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                )
                return response.choices[0].message.content
            else:
                import anthropic

                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=1024,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_prompt}],
                )
                return response.content[0].text
        except Exception as e:
            logger.error(f"AI provider error: {e}")
            return "Sorry, I'm having trouble generating a response right now. Please try again."
