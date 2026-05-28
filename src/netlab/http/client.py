from __future__ import annotations

import socket
from contextlib import closing

from .messages import HTTPResponse, build_http_request, parse_http_response


def http_request(host: str, port: int, path: str = "/", timeout: float = 3.0, headers: dict[str, str] | None = None) -> HTTPResponse:
    raw = build_http_request("GET", path, f"{host}:{port}", headers=headers)
    with closing(socket.create_connection((host, port), timeout=timeout)) as sock:
        sock.settimeout(timeout)
        sock.sendall(raw)
        data = bytearray()
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data.extend(chunk)
    return parse_http_response(bytes(data))
