from __future__ import annotations

import socket
import ssl
from contextlib import closing

from netlab.http.messages import build_http_request, parse_http_response


def https_get(host: str, port: int = 443, path: str = "/", timeout: float = 5.0) -> tuple[str, bytes]:
    context = ssl.create_default_context()
    with closing(socket.create_connection((host, port), timeout=timeout)) as raw:
        with context.wrap_socket(raw, server_hostname=host) as sock:
            cipher = sock.cipher()[0] if sock.cipher() else "unknown"
            sock.sendall(build_http_request("GET", path, host))
            data = bytearray()
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                data.extend(chunk)
    return cipher, parse_http_response(bytes(data)).body
