import logging

import anthropic
from django.conf import settings

logger = logging.getLogger(__name__)


class AnthropicProvider:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = settings.ANTHROPIC_MODEL

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
            )
            return response.content[0].text
        except anthropic.APIError as e:
            logger.error(f"Anthropic API error: {e}")
            return "Sorry, I'm having trouble generating a response right now. Please try again."
