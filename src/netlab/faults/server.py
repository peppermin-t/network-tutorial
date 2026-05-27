from __future__ import annotations

import socket
import threading
import time
from contextlib import closing

from netlab.common.logging import EventLogger
from netlab.http.messages import build_http_response, parse_http_request


def run_fault_http_server(host: str, port: int, mode: str = "delay", delay: float = 2.0, status_code: int = 500) -> None:
    logger = EventLogger("fault-http-server")
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen()
        logger.event("listening", host=host, port=port, mode=mode, delay=delay, status_code=status_code)
        while True:
            conn, addr = server.accept()
            threading.Thread(target=_handle_fault, args=(conn, addr, mode, delay, status_code, logger), daemon=True).start()


def _handle_fault(conn: socket.socket, addr: tuple[str, int], mode: str, delay: float, status_code: int, logger: EventLogger) -> None:
    remote = f"{addr[0]}:{addr[1]}"
    with conn:
        data = conn.recv(65535)
        if not data:
            return
        request = parse_http_request(data)
        logger.event("request", remote=remote, mode=mode, target=request.target)
        if mode == "close":
            return
        if mode in {"delay", "slow"}:
            time.sleep(delay)
            body = f"delayed {delay:.3f}s\n".encode("utf-8")
            conn.sendall(build_http_response(200, "OK", body, {"Content-Type": "text/plain"}))
            return
        if mode in {"500", "error"}:
            conn.sendall(build_http_response(status_code, "Injected Error", b"injected error\n", {"Content-Type": "text/plain"}))
            return
        conn.sendall(build_http_response(200, "OK", b"ok\n", {"Content-Type": "text/plain"}))
