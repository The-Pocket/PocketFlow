import importlib.util
import json
import unittest
from pathlib import Path
from unittest.mock import patch

try:
    import anthropic
    import httpx2
except ImportError:
    anthropic = httpx2 = None


HELPER = (
    Path(__file__).resolve().parents[1]
    / "cookbook"
    / "pocketflow-batch"
    / "utils.py"
)


@unittest.skipUnless(anthropic and httpx2, "Batch translation example needs anthropic")
class TestBatchTranslationExample(unittest.TestCase):
    def request_translation(self, content):
        requests = []

        def respond(request):
            self.assertEqual(request.url.path, "/v1/messages")
            requests.append(json.loads(request.content))
            return httpx2.Response(
                200,
                json={
                    "id": "msg_translation",
                    "type": "message",
                    "role": "assistant",
                    "model": "claude-sonnet-5-5",
                    "content": content,
                    "stop_reason": "end_turn",
                    "stop_sequence": None,
                    "usage": {"input_tokens": 12, "output_tokens": 4},
                },
            )

        spec = importlib.util.spec_from_file_location("batch_translation_utils", HELPER)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with anthropic.Anthropic(
            api_key="test-key",
            base_url="https://example.invalid",
            http_client=httpx2.Client(transport=httpx2.MockTransport(respond)),
        ) as client:
            with patch.object(module, "Anthropic", return_value=client):
                result = module.call_llm("Translate this heading")
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0]["model"], "claude-sonnet-5-5")
        self.assertEqual(requests[0]["thinking"], {"type": "adaptive"})
        self.assertEqual(requests[0]["max_tokens"], 20000)
        self.assertEqual(
            requests[0]["messages"],
            [{"role": "user", "content": "Translate this heading"}],
        )
        return result

    def test_adaptive_thinking_can_return_text_only(self):
        self.assertEqual(
            self.request_translation([{"type": "text", "text": "# Bonjour"}]),
            "# Bonjour",
        )

    def test_concatenates_text_blocks_and_ignores_non_text(self):
        self.assertEqual(
            self.request_translation(
                [
                    {"type": "thinking", "thinking": "", "signature": "mock"},
                    {"type": "text", "text": "# Bonjour"},
                    {"type": "text", "text": "\n\nTexte"},
                ]
            ),
            "# Bonjour\n\nTexte",
        )

    def test_no_text_fails_instead_of_writing_a_blank_translation(self):
        with self.assertRaisesRegex(ValueError, "no translation text"):
            self.request_translation(
                [{"type": "thinking", "thinking": "", "signature": "mock"}]
            )
