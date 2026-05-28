import unittest
import socket
import threading

from netlab.capacity.backpressure import BackpressureGate
from netlab.common.logging import EventLogger
from netlab.http.messages import build_http_request, parse_http_response
from netlab.model.server import GenerationConfig, _handle_model, chunk, generate_tokens
from netlab.observability.metrics import Metrics


class ModelServerTest(unittest.TestCase):
    def test_generate_tokens_uses_prompt_prefix(self) -> None:
        self.assertEqual(generate_tokens("local model", 3), ["local model-1", "local model-2", "local model-3"])

    def test_chunk_encodes_http_chunk(self) -> None:
        self.assertEqual(chunk(b"hello"), b"5\r\nhello\r\n")

    def test_rejected_request_preserves_trace_id(self) -> None:
        server_sock, client_sock = socket.socketpair()
        gate = BackpressureGate(max_concurrency=1)
        held = gate.try_acquire()
        self.assertTrue(held.accepted)
        thread = threading.Thread(
            target=_handle_model,
            args=(server_sock, ("127.0.0.1", 50000), gate, Metrics(), GenerationConfig(), EventLogger("test-model")),
        )
        thread.start()
        try:
            client_sock.sendall(build_http_request("GET", "/generate", "localhost", headers={"X-Trace-Id": "trace-test"}))
            data = client_sock.recv(4096)
        finally:
            client_sock.close()
            gate.release()
        thread.join(timeout=1.0)

        response = parse_http_response(data)
        self.assertEqual(response.status_code, 429)
        self.assertEqual(response.headers["x-trace-id"], "trace-test")


if __name__ == "__main__":
    unittest.main()
