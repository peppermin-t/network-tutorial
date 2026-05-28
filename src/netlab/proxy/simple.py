from __future__ import annotations

import socket
import threading
import time
from contextlib import closing

from netlab.common.logging import EventLogger
from netlab.http.messages import HEADER_END, build_http_response
from netlab.observability.trace import new_trace_id


UPSTREAM_TIMEOUT_SECONDS = 3.0


def run_reverse_proxy(host: str, port: int, upstream_host: str, upstream_port: int) -> None:
    logger = EventLogger("reverse-proxy")
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen()
        logger.event("listening", host=host, port=port, upstream=f"{upstream_host}:{upstream_port}")
        while True:
            conn, addr = server.accept()
            threading.Thread(target=_proxy_once, args=(conn, addr, upstream_host, upstream_port, logger), daemon=True).start()


def _proxy_once(client: socket.socket, addr: tuple[str, int], upstream_host: str, upstream_port: int, logger: EventLogger) -> None:
    start = time.perf_counter()
    remote = f"{addr[0]}:{addr[1]}"
    response_started = False
    with client:
        try:
            request = client.recv(65535)
            if not request:
                return
            trace_id = _trace_id_from_request(request) or new_trace_id()
            request = _ensure_trace_id_header(request, trace_id)
            with closing(socket.create_connection((upstream_host, upstream_port), timeout=UPSTREAM_TIMEOUT_SECONDS)) as upstream:
                upstream.settimeout(UPSTREAM_TIMEOUT_SECONDS)
                upstream.sendall(request)
                bytes_out = 0
                first_byte_ms: float | None = None
                while True:
                    chunk = upstream.recv(4096)
                    if not chunk:
                        break
                    if first_byte_ms is None:
                        first_byte_ms = round((time.perf_counter() - start) * 1000, 2)
                    response_started = True
                    client.sendall(chunk)
                    bytes_out += len(chunk)
            logger.event(
                "proxied",
                remote=remote,
                trace_id=trace_id,
                bytes_in=len(request),
                bytes_out=bytes_out,
                first_byte_ms=first_byte_ms,
                elapsed_ms=round((time.perf_counter() - start) * 1000, 2),
            )
        except socket.timeout as exc:
            if not response_started:
                client.sendall(
                    build_http_response(
                        504,
                        "Gateway Timeout",
                        b"upstream timeout\n",
                        {"Content-Type": "text/plain"},
                    )
                )
            logger.event("proxy_timeout", remote=remote, error=type(exc).__name__, elapsed_ms=round((time.perf_counter() - start) * 1000, 2))
        except OSError as exc:
            logger.event("proxy_error", remote=remote, error=type(exc).__name__, elapsed_ms=round((time.perf_counter() - start) * 1000, 2))


def _trace_id_from_request(request: bytes) -> str | None:
    head_end = request.find(HEADER_END)
    if head_end < 0:
        return None
    for line in request[:head_end].split(b"\r\n")[1:]:
        if b":" not in line:
            continue
        key, value = line.split(b":", 1)
        if key.strip().lower() == b"x-trace-id":
            trace_id = value.decode("latin1").strip()
            return trace_id or None
    return None


def _ensure_trace_id_header(request: bytes, trace_id: str) -> bytes:
    if _trace_id_from_request(request):
        return request
    head_end = request.find(HEADER_END)
    if head_end < 0:
        return request
    return request[:head_end] + f"\r\nX-Trace-Id: {trace_id}".encode("ascii") + request[head_end:]
