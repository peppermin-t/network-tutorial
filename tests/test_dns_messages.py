import struct
import unittest

from netlab.dns.messages import build_query, encode_name, parse_message


class DNSMessagesTest(unittest.TestCase):
    def test_build_query_contains_question(self) -> None:
        raw = build_query("example.com", "A", transaction_id=0x1234)
        self.assertEqual(raw[:2], b"\x12\x34")
        self.assertIn(encode_name("example.com"), raw)

    def test_parse_a_answer(self) -> None:
        txid = 0x1234
        header = struct.pack("!HHHHHH", txid, 0x8180, 1, 1, 0, 0)
        question = encode_name("example.com") + struct.pack("!HH", 1, 1)
        answer = b"\xc0\x0c" + struct.pack("!HHIH", 1, 1, 60, 4) + b"\x5d\xb8\xd8\x22"
        message = parse_message(header + question + answer)

        self.assertEqual(message.rcode, 0)
        self.assertEqual(message.answers[0].value, "93.184.216.34")


if __name__ == "__main__":
    unittest.main()
