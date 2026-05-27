import unittest

from netlab.protocols.length_prefixed import LengthPrefixedProtocol


class LengthPrefixedProtocolTest(unittest.TestCase):
    def test_round_trip_across_split_chunks(self) -> None:
        protocol = LengthPrefixedProtocol()
        raw = LengthPrefixedProtocol.encode(b"hello") + LengthPrefixedProtocol.encode(b"world")

        self.assertEqual(protocol.feed(raw[:2]), [])
        self.assertEqual(protocol.feed(raw[2:7]), [])
        self.assertEqual(protocol.feed(raw[7:]), [b"hello", b"world"])

    def test_rejects_large_frame(self) -> None:
        protocol = LengthPrefixedProtocol(max_frame_size=3)
        with self.assertRaises(ValueError):
            protocol.feed(LengthPrefixedProtocol.encode(b"toolong"))


if __name__ == "__main__":
    unittest.main()
