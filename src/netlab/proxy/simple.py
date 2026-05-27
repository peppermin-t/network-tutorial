from __future__ import annotations

import socket
import threading
import time
from contextlib import closing

from netlab.common.logging import EventLogger


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
    with client:
        try:
            request = client.recv(65535)
            with closing(socket.create_connection((upstream_host, upstream_port), timeout=3.0)) as upstream:
                upstream.sendall(request)
                response = bytearray()
                while True:
                    chunk = upstream.recv(4096)
                    if not chunk:
                        break
                    response.extend(chunk)
            client.sendall(response)
            logger.event("proxied", remote=remote, bytes_in=len(request), bytes_out=len(response), elapsed_ms=round((time.perf_counter() - start) * 1000, 2))
        except OSError as exc:
            logger.event("proxy_error", remote=remote, error=type(exc).__name__)
