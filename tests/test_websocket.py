import unittest

from netlab.rpc.websocket import accept_key, decode_frame, encode_frame


class WebSocketTest(unittest.TestCase):
    def test_accept_key_known_vector(self) -> None:
        self.assertEqual(accept_key("dGhlIHNhbXBsZSBub25jZQ=="), "s3pPLMBiTxaQ9kYGzzhZRbK+xOo=")

    def test_masked_frame_round_trip(self) -> None:
        frame = encode_frame(b"hello", mask=True)
        opcode, payload, used = decode_frame(frame)

        self.assertEqual(opcode, 1)
        self.assertEqual(payload, b"hello")
        self.assertEqual(used, len(frame))


if __name__ == "__main__":
    unittest.main()
