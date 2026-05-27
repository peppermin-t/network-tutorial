from __future__ import annotations

import socket
import threading
from contextlib import closing

from netlab.common.logging import EventLogger

from .messages import build_http_response, parse_http_request


def run_http_server(host: str, port: int, stop_after_one: bool = False) -> None:
    logger = EventLogger("http-server")
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen()
        logger.event("listening", host=host, port=port)
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=_handle, args=(conn, addr, logger), daemon=True)
            thread.start()
            if stop_after_one:
                thread.join()
                return


def _handle(conn: socket.socket, addr: tuple[str, int], logger: EventLogger) -> None:
    remote = f"{addr[0]}:{addr[1]}"
    with conn:
        data = conn.recv(65535)
        request = parse_http_request(data)
        logger.event("request", remote=remote, method=request.method, target=request.target)
        body = f"hello from netlab http server\npath={request.target}\n".encode("utf-8")
        conn.sendall(build_http_response(200, "OK", body, {"Content-Type": "text/plain; charset=utf-8"}))
