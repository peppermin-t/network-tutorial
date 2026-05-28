import socket
import threading
import time
import unittest
from contextlib import closing

from netlab.http.client import stream_http_request
from netlab.model.server import chunk


def _free_port() -> int:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


class StreamHttpClientTest(unittest.TestCase):
    def test_stream_http_reports_trace_and_chunk_timings(self) -> None:
        port = _free_port()

        def server() -> None:
            with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as listener:
                listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                listener.bind(("127.0.0.1", port))
                listener.listen(1)
                conn, _ = listener.accept()
                with conn:
                    conn.recv(4096)
                    conn.sendall(
                        b"HTTP/1.1 200 OK\r\n"
                        b"Content-Type: text/plain\r\n"
                        b"Transfer-Encoding: chunked\r\n"
                        b"X-Trace-Id: stream-test\r\n"
                        b"Connection: close\r\n\r\n"
                        + chunk(b"first\n")
                    )
                    time.sleep(0.03)
                    conn.sendall(chunk(b"second\n") + b"0\r\n\r\n")

        thread = threading.Thread(target=server)
        thread.start()

        result = stream_http_request("127.0.0.1", port, "/stream", timeout=1.0)
        thread.join(timeout=1.0)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.headers["x-trace-id"], "stream-test")
        self.assertIsNotNone(result.first_byte_ms)
        self.assertEqual([chunk.data for chunk in result.chunks], [b"first\n", b"second\n"])
        self.assertGreaterEqual(result.chunks[1].elapsed_ms, result.chunks[0].elapsed_ms)
        self.assertGreaterEqual(result.total_ms, result.first_byte_ms or 0)


if __name__ == "__main__":
    unittest.main()
