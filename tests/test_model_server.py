import unittest

from netlab.model.server import chunk, generate_tokens


class ModelServerTest(unittest.TestCase):
    def test_generate_tokens_uses_prompt_prefix(self) -> None:
        self.assertEqual(generate_tokens("local model", 3), ["local model-1", "local model-2", "local model-3"])

    def test_chunk_encodes_http_chunk(self) -> None:
        self.assertEqual(chunk(b"hello"), b"5\r\nhello\r\n")


if __name__ == "__main__":
    unittest.main()
