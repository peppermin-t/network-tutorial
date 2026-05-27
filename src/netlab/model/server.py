from __future__ import annotations

import socket
import threading
import time
from contextlib import closing
from dataclasses import dataclass

from netlab.capacity.backpressure import BackpressureGate
from netlab.common.logging import EventLogger
from netlab.http.messages import build_http_response, parse_http_request
from netlab.observability.metrics import Metrics
from netlab.observability.trace import new_trace_id


@dataclass(frozen=True)
class GenerationConfig:
    tokens: int = 8
    token_delay: float = 0.05


def generate_tokens(prompt: str, count: int) -> list[str]:
    base = prompt.strip() or "token"
    return [f"{base}-{index + 1}" for index in range(count)]


def chunk(payload: bytes) -> bytes:
    return f"{len(payload):X}\r\n".encode("ascii") + payload + b"\r\n"


def run_model_server(host: str, port: int, max_concurrency: int = 2, token_delay: float = 0.05, tokens: int = 8) -> None:
    logger = EventLogger("model-server")
    gate = BackpressureGate(max_concurrency)
    metrics = Metrics()
    config = GenerationConfig(tokens=tokens, token_delay=token_delay)
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen()
        logger.event("listening", host=host, port=port, max_concurrency=max_concurrency, token_delay=token_delay, tokens=tokens)
        while True:
            conn, addr = server.accept()
            threading.Thread(target=_handle_model, args=(conn, addr, gate, metrics, config, logger), daemon=True).start()


def _handle_model(conn: socket.socket, addr: tuple[str, int], gate: BackpressureGate, metrics: Metrics, config: GenerationConfig, logger: EventLogger) -> None:
    decision = gate.try_acquire()
    remote = f"{addr[0]}:{addr[1]}"
    if not decision.accepted:
        with conn:
            metrics.increment("requests.rejected")
            conn.sendall(build_http_response(429, "Too Many Requests", b"capacity exceeded\n", {"Content-Type": "text/plain"}))
        logger.event("rejected", remote=remote, layer=decision.layer, status=decision.status_code)
        return

    started = time.perf_counter()
    trace_id = new_trace_id()
    try:
        with conn:
            data = conn.recv(65535)
            request = parse_http_request(data)
            metrics.increment("requests.accepted")
            if request.target.startswith("/metrics"):
                conn.sendall(build_http_response(200, "OK", metrics.render_prometheus().encode("utf-8"), {"Content-Type": "text/plain"}))
                return
            if request.target.startswith("/stream"):
                _send_stream(conn, request.target, config, trace_id)
            else:
                _send_complete(conn, request.target, config, trace_id)
            elapsed_ms = round((time.perf_counter() - started) * 1000, 3)
            logger.event("completed", remote=remote, target=request.target, trace_id=trace_id, elapsed_ms=elapsed_ms)
    finally:
        gate.release()


def _send_complete(conn: socket.socket, target: str, config: GenerationConfig, trace_id: str) -> None:
    prompt = _prompt_from_target(target)
    time.sleep(config.tokens * config.token_delay)
    body = (" ".join(generate_tokens(prompt, config.tokens)) + "\n").encode("utf-8")
    conn.sendall(build_http_response(200, "OK", body, {"Content-Type": "text/plain", "X-Trace-Id": trace_id}))


def _send_stream(conn: socket.socket, target: str, config: GenerationConfig, trace_id: str) -> None:
    headers = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/plain\r\n"
        "Transfer-Encoding: chunked\r\n"
        f"X-Trace-Id: {trace_id}\r\n"
        "Connection: close\r\n\r\n"
    ).encode("ascii")
    conn.sendall(headers)
    first_token_started = time.perf_counter()
    for token in generate_tokens(_prompt_from_target(target), config.tokens):
        time.sleep(config.token_delay)
        conn.sendall(chunk((token + "\n").encode("utf-8")))
    conn.sendall(b"0\r\n\r\n")
    _ = first_token_started


def _prompt_from_target(target: str) -> str:
    if "prompt=" not in target:
        return "token"
    return target.split("prompt=", 1)[1].split("&", 1)[0].replace("+", " ")
