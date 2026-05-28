import socket
import threading
import time
import unittest
from contextlib import closing

from netlab.common.logging import EventLogger
from netlab.http.messages import build_http_request
from netlab.model.server import chunk
from netlab.proxy.simple import _ensure_trace_id_header, _proxy_once, _trace_id_from_request


def _free_port() -> int:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


class ProxyStreamingTest(unittest.TestCase):
    def test_trace_header_is_added_when_missing(self) -> None:
        request = build_http_request("GET", "/stream", "localhost")

        updated = _ensure_trace_id_header(request, "trace-1")

        self.assertEqual(_trace_id_from_request(updated), "trace-1")

    def test_trace_header_is_preserved_when_present(self) -> None:
        request = build_http_request("GET", "/stream", "localhost", headers={"X-Trace-Id": "client-trace"})

        updated = _ensure_trace_id_header(request, "new-trace")

        self.assertEqual(_trace_id_from_request(updated), "client-trace")

    def test_proxy_forwards_first_stream_chunk_before_complete_body(self) -> None:
        upstream_port = _free_port()
        upstream_seen = {}

        def upstream_server() -> None:
            with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as server:
                server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server.bind(("127.0.0.1", upstream_port))
                server.listen(1)
                conn, _ = server.accept()
                with conn:
                    upstream_seen["request"] = conn.recv(4096)
                    conn.sendall(
                        b"HTTP/1.1 200 OK\r\n"
                        b"Content-Type: text/plain\r\n"
                        b"Transfer-Encoding: chunked\r\n"
                        b"Connection: close\r\n\r\n"
                        + chunk(b"first\n")
                    )
                    time.sleep(0.25)
                    conn.sendall(chunk(b"second\n") + b"0\r\n\r\n")

        server_thread = threading.Thread(target=upstream_server)
        server_thread.start()

        client_sock, proxy_sock = socket.socketpair()
        proxy_thread = threading.Thread(
            target=_proxy_once,
            args=(proxy_sock, ("127.0.0.1", 50001), "127.0.0.1", upstream_port, EventLogger("test-proxy")),
        )
        proxy_thread.start()

        try:
            client_sock.settimeout(0.15)
            client_sock.sendall(build_http_request("GET", "/stream", "localhost", headers={"X-Trace-Id": "stream-trace"}))
            first = client_sock.recv(4096)

            self.assertIn(b"first\n", first)
            self.assertNotIn(b"second\n", first)
            self.assertIn(b"X-Trace-Id: stream-trace", upstream_seen["request"])
        finally:
            client_sock.close()

        proxy_thread.join(timeout=1.0)
        server_thread.join(timeout=1.0)


if __name__ == "__main__":
    unittest.main()
