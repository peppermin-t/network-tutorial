from __future__ import annotations

import socket
import time
from contextlib import closing
from dataclasses import dataclass

from .messages import CRLF, HEADER_END, HTTPResponse, build_http_request, parse_headers, parse_http_response


@dataclass(frozen=True)
class HTTPStreamChunk:
    elapsed_ms: float
    size: int
    data: bytes


@dataclass(frozen=True)
class HTTPStreamResult:
    status_code: int
    reason: str
    headers: dict[str, str]
    chunks: list[HTTPStreamChunk]
    first_byte_ms: float | None
    total_ms: float


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


def stream_http_request(host: str, port: int, path: str = "/", timeout: float = 3.0, headers: dict[str, str] | None = None) -> HTTPStreamResult:
    raw = build_http_request("GET", path, f"{host}:{port}", headers=headers)
    started = time.perf_counter()
    first_byte_ms: float | None = None
    chunks: list[HTTPStreamChunk] = []
    with closing(socket.create_connection((host, port), timeout=timeout)) as sock:
        sock.settimeout(timeout)
        sock.sendall(raw)
        buffer = bytearray()
        while HEADER_END not in buffer:
            received = sock.recv(4096)
            if not received:
                raise ValueError("http headers incomplete")
            if first_byte_ms is None:
                first_byte_ms = _elapsed_ms(started)
            buffer.extend(received)

        head, body = bytes(buffer).split(HEADER_END, 1)
        lines = head.split(CRLF)
        _version, status, reason = lines[0].decode("ascii").split(" ", 2)
        parsed_headers = parse_headers(lines[1:])

        if parsed_headers.get("transfer-encoding", "").lower() == "chunked":
            _read_chunked_stream(sock, bytearray(body), chunks, started)
        else:
            _read_plain_stream(sock, bytearray(body), parsed_headers, chunks, started)

    return HTTPStreamResult(int(status), reason, parsed_headers, chunks, first_byte_ms, _elapsed_ms(started))


def _read_plain_stream(sock: socket.socket, body: bytearray, headers: dict[str, str], chunks: list[HTTPStreamChunk], started: float) -> None:
    expected = int(headers.get("content-length", "0"))
    if body:
        chunks.append(HTTPStreamChunk(_elapsed_ms(started), len(body), bytes(body)))
    while expected == 0 or sum(chunk.size for chunk in chunks) < expected:
        received = sock.recv(4096)
        if not received:
            break
        chunks.append(HTTPStreamChunk(_elapsed_ms(started), len(received), received))


def _read_chunked_stream(sock: socket.socket, buffer: bytearray, chunks: list[HTTPStreamChunk], started: float) -> None:
    while True:
        while CRLF not in buffer:
            received = sock.recv(4096)
            if not received:
                raise ValueError("chunk size line missing")
            buffer.extend(received)
        line_end = buffer.find(CRLF)
        size = int(bytes(buffer[:line_end]).split(b";", 1)[0], 16)
        del buffer[: line_end + len(CRLF)]
        if size == 0:
            while len(buffer) < len(CRLF):
                received = sock.recv(4096)
                if not received:
                    return
                buffer.extend(received)
            return
        while len(buffer) < size + len(CRLF):
            received = sock.recv(4096)
            if not received:
                raise ValueError("chunked body incomplete")
            buffer.extend(received)
        payload = bytes(buffer[:size])
        del buffer[: size + len(CRLF)]
        chunks.append(HTTPStreamChunk(_elapsed_ms(started), size, payload))


def _elapsed_ms(started: float) -> float:
    return round((time.perf_counter() - started) * 1000, 2)
