import json
import unittest

from netlab.rpc.jsonrpc import decode_request, encode_request, handle_request


class JSONRPCTest(unittest.TestCase):
    def test_request_round_trip(self) -> None:
        request = decode_request(encode_request("echo", {"message": "hi"}, 7))

        self.assertEqual(request.method, "echo")
        self.assertEqual(request.id, 7)

    def test_handle_request(self) -> None:
        response = handle_request(encode_request("echo", "hi", 1), {"echo": lambda params: params})

        self.assertEqual(json.loads(response)["result"], "hi")


if __name__ == "__main__":
    unittest.main()
