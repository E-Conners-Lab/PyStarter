"""Tests for the Anthropic-backed AI provider and its default model pin."""

import os
import re
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase, override_settings

from apps.ai.anthropic_provider import FALLBACK_MESSAGE, AnthropicProvider
from config.settings.base import DEFAULT_ANTHROPIC_MODEL, _env_str

# Snapshot IDs retire; aliases track the current model. Never pin a snapshot as the default.
DATED_SNAPSHOT = re.compile(r"-\d{8}$")
KNOWN_RETIRED_PREFIXES = ("claude-3", "claude-sonnet-4-", "claude-opus-4-0", "claude-opus-4-1")

PROVIDER_SETTINGS = dict(
    ANTHROPIC_API_KEY="test-key", ANTHROPIC_BASE_URL="", ANTHROPIC_MODEL="claude-opus-5"
)


def _response(blocks, stop_reason="end_turn"):
    return SimpleNamespace(content=blocks, stop_reason=stop_reason)


def _text(text):
    return SimpleNamespace(type="text", text=text)


class DefaultModelTest(SimpleTestCase):
    def test_default_is_an_alias_not_a_dated_snapshot(self):
        self.assertIsNone(DATED_SNAPSHOT.search(DEFAULT_ANTHROPIC_MODEL))

    def test_default_is_not_a_retired_family(self):
        self.assertFalse(DEFAULT_ANTHROPIC_MODEL.startswith(KNOWN_RETIRED_PREFIXES))


class ModelEnvResolutionTest(SimpleTestCase):
    """docker compose passes `${ANTHROPIC_MODEL:-}` through as an *empty string*, so the
    var is set-but-blank in the container. A plain os.environ.get(name, default) never
    reaches the default there, and the empty model went out on the wire (v1.0.5 bug)."""

    def _resolve(self, **env):
        with patch.dict(os.environ, env, clear=False):
            return _env_str("ANTHROPIC_MODEL", DEFAULT_ANTHROPIC_MODEL)

    def test_unset_falls_back_to_default(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("ANTHROPIC_MODEL", None)
            self.assertEqual(
                _env_str("ANTHROPIC_MODEL", DEFAULT_ANTHROPIC_MODEL), DEFAULT_ANTHROPIC_MODEL
            )

    def test_blank_falls_back_to_default(self):
        self.assertEqual(self._resolve(ANTHROPIC_MODEL=""), DEFAULT_ANTHROPIC_MODEL)

    def test_whitespace_only_falls_back_to_default(self):
        self.assertEqual(self._resolve(ANTHROPIC_MODEL="   "), DEFAULT_ANTHROPIC_MODEL)

    def test_explicit_value_wins(self):
        self.assertEqual(self._resolve(ANTHROPIC_MODEL="claude-haiku-4-5"), "claude-haiku-4-5")

    def test_surrounding_whitespace_is_stripped(self):
        self.assertEqual(self._resolve(ANTHROPIC_MODEL=" claude-haiku-4-5\n"), "claude-haiku-4-5")


@override_settings(**PROVIDER_SETTINGS)
class AnthropicProviderTest(SimpleTestCase):
    def _provider(self, response=None, side_effect=None):
        client = MagicMock()
        client.messages.create.return_value = response
        client.messages.create.side_effect = side_effect
        with patch("anthropic.Anthropic", return_value=client):
            provider = AnthropicProvider()
        return provider, client

    def test_uses_configured_model(self):
        provider, client = self._provider(_response([_text("hint")]))
        provider.generate("sys", "user")
        self.assertEqual(client.messages.create.call_args.kwargs["model"], "claude-opus-5")

    def test_returns_first_text_block_even_after_thinking(self):
        thinking = SimpleNamespace(type="thinking", thinking="")
        provider, _ = self._provider(_response([thinking, _text("the hint")]))
        self.assertEqual(provider.generate("sys", "user"), "the hint")

    def test_refusal_returns_fallback(self):
        provider, _ = self._provider(_response([], stop_reason="refusal"))
        self.assertEqual(provider.generate("sys", "user"), FALLBACK_MESSAGE)

    def test_api_error_returns_fallback_not_exception(self):
        provider, _ = self._provider(side_effect=RuntimeError("model not found"))
        self.assertEqual(provider.generate("sys", "user"), FALLBACK_MESSAGE)

    def test_never_sends_an_empty_model(self):
        """The v1.0.5 regression: model="" reached the API and every hint 400'd."""
        provider, client = self._provider(_response([_text("hint")]))
        provider.generate("sys", "user")
        self.assertTrue(client.messages.create.call_args.kwargs["model"].strip())
