from __future__ import annotations

import base64
import hashlib
import os
import socket
import struct
import threading
from contextlib import closing

from netlab.common.logging import EventLogger


GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"


def accept_key(client_key: str) -> str:
    digest = hashlib.sha1((client_key + GUID).encode("ascii")).digest()
    return base64.b64encode(digest).decode("ascii")


def encode_frame(payload: bytes, opcode: int = 1, mask: bool = False) -> bytes:
    first = 0x80 | opcode
    length = len(payload)
    if length < 126:
        header = struct.pack("!BB", first, (0x80 if mask else 0) | length)
    elif length <= 0xFFFF:
        header = struct.pack("!BBH", first, (0x80 if mask else 0) | 126, length)
    else:
        header = struct.pack("!BBQ", first, (0x80 if mask else 0) | 127, length)
    if not mask:
        return header + payload
    key = os.urandom(4)
    masked = bytes(byte ^ key[i % 4] for i, byte in enumerate(payload))
    return header + key + masked


def decode_frame(data: bytes) -> tuple[int, bytes, int]:
    if len(data) < 2:
        raise ValueError("websocket frame too short")
    first, second = data[0], data[1]
    opcode = first & 0x0F
    masked = bool(second & 0x80)
    length = second & 0x7F
    offset = 2
    if length == 126:
        length = struct.unpack("!H", data[offset : offset + 2])[0]
        offset += 2
    elif length == 127:
        length = struct.unpack("!Q", data[offset : offset + 8])[0]
        offset += 8
    key = b""
    if masked:
        key = data[offset : offset + 4]
        offset += 4
    payload = data[offset : offset + length]
    if len(payload) < length:
        raise ValueError("websocket payload truncated")
    if masked:
        payload = bytes(byte ^ key[i % 4] for i, byte in enumerate(payload))
    return opcode, payload, offset + length


def run_websocket_echo_server(host: str, port: int, stop_after_one: bool = False) -> None:
    logger = EventLogger("websocket-server")
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen()
        logger.event("listening", host=host, port=port)
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=_handle_ws, args=(conn, addr, logger), daemon=True)
            thread.start()
            if stop_after_one:
                thread.join()
                return


def websocket_echo_client(host: str, port: int, message: bytes, timeout: float = 3.0) -> bytes:
    key = base64.b64encode(os.urandom(16)).decode("ascii")
    request = (
        f"GET / HTTP/1.1\r\nHost: {host}:{port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n"
    ).encode("ascii")
    with closing(socket.create_connection((host, port), timeout=timeout)) as sock:
        sock.settimeout(timeout)
        sock.sendall(request)
        response = sock.recv(4096)
        if b"101 Switching Protocols" not in response:
            raise OSError(f"websocket handshake failed: {response!r}")
        sock.sendall(encode_frame(message, mask=True))
        data = sock.recv(4096)
    _opcode, payload, _used = decode_frame(data)
    return payload


def _handle_ws(conn: socket.socket, addr: tuple[str, int], logger: EventLogger) -> None:
    remote = f"{addr[0]}:{addr[1]}"
    with conn:
        request = conn.recv(4096).decode("latin1")
        key = ""
        for line in request.split("\r\n"):
            if line.lower().startswith("sec-websocket-key:"):
                key = line.split(":", 1)[1].strip()
        if not key:
            return
        response = (
            "HTTP/1.1 101 Switching Protocols\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Accept: {accept_key(key)}\r\n\r\n"
        ).encode("ascii")
        conn.sendall(response)
        data = conn.recv(65535)
        opcode, payload, _used = decode_frame(data)
        logger.event("frame", remote=remote, opcode=opcode, bytes=len(payload))
        conn.sendall(encode_frame(payload))
