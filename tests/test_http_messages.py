import unittest

from netlab.http.messages import build_http_request, build_http_response, parse_http_request, parse_http_response


class HTTPMessagesTest(unittest.TestCase):
    def test_request_round_trip(self) -> None:
        raw = build_http_request("POST", "/items", "example.test", b"abc", {"X-Trace-Id": "t1"})
        request = parse_http_request(raw)

        self.assertEqual(request.method, "POST")
        self.assertEqual(request.target, "/items")
        self.assertEqual(request.headers["host"], "example.test")
        self.assertEqual(request.headers["x-trace-id"], "t1")
        self.assertEqual(request.body, b"abc")

    def test_response_round_trip(self) -> None:
        raw = build_http_response(200, "OK", b"hello")
        response = parse_http_response(raw)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.body, b"hello")

    def test_chunked_response(self) -> None:
        raw = b"HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n5\r\nhello\r\n0\r\n\r\n"
        response = parse_http_response(raw)

        self.assertEqual(response.body, b"hello")


if __name__ == "__main__":
    unittest.main()
