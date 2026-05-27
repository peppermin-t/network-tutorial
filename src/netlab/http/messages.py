from __future__ import annotations

from dataclasses import dataclass


CRLF = b"\r\n"
HEADER_END = b"\r\n\r\n"


@dataclass(frozen=True)
class HTTPRequest:
    method: str
    target: str
    version: str
    headers: dict[str, str]
    body: bytes = b""


@dataclass(frozen=True)
class HTTPResponse:
    version: str
    status_code: int
    reason: str
    headers: dict[str, str]
    body: bytes = b""


def parse_headers(lines: list[bytes]) -> dict[str, str]:
    headers: dict[str, str] = {}
    for line in lines:
        if not line:
            continue
        if b":" not in line:
            raise ValueError(f"malformed header: {line!r}")
        key, value = line.split(b":", 1)
        headers[key.decode("ascii").strip().lower()] = value.decode("latin1").strip()
    return headers


def parse_http_request(data: bytes) -> HTTPRequest:
    head, body = _split_head_body(data)
    lines = head.split(CRLF)
    method, target, version = lines[0].decode("ascii").split(" ", 2)
    headers = parse_headers(lines[1:])
    expected = int(headers.get("content-length", "0"))
    return HTTPRequest(method, target, version, headers, body[:expected])


def parse_http_response(data: bytes) -> HTTPResponse:
    head, body = _split_head_body(data)
    lines = head.split(CRLF)
    version, status, reason = lines[0].decode("ascii").split(" ", 2)
    headers = parse_headers(lines[1:])
    if headers.get("transfer-encoding", "").lower() == "chunked":
        body = decode_chunked_body(body)
    else:
        expected = int(headers.get("content-length", str(len(body))))
        body = body[:expected]
    return HTTPResponse(version, int(status), reason, headers, body)


def build_http_request(method: str, target: str, host: str, body: bytes = b"", headers: dict[str, str] | None = None) -> bytes:
    merged = {"Host": host, "Connection": "close", **(headers or {})}
    if body:
        merged["Content-Length"] = str(len(body))
    lines = [f"{method} {target} HTTP/1.1".encode("ascii")]
    lines.extend(f"{key}: {value}".encode("latin1") for key, value in merged.items())
    return CRLF.join(lines) + HEADER_END + body


def build_http_response(status_code: int, reason: str, body: bytes, headers: dict[str, str] | None = None) -> bytes:
    merged = {"Content-Length": str(len(body)), "Connection": "close", **(headers or {})}
    lines = [f"HTTP/1.1 {status_code} {reason}".encode("ascii")]
    lines.extend(f"{key}: {value}".encode("latin1") for key, value in merged.items())
    return CRLF.join(lines) + HEADER_END + body


def decode_chunked_body(data: bytes) -> bytes:
    offset = 0
    chunks: list[bytes] = []
    while True:
        line_end = data.find(CRLF, offset)
        if line_end < 0:
            raise ValueError("chunk size line missing")
        size = int(data[offset:line_end].split(b";", 1)[0], 16)
        offset = line_end + 2
        if size == 0:
            return b"".join(chunks)
        chunks.append(data[offset : offset + size])
        offset += size + 2


def _split_head_body(data: bytes) -> tuple[bytes, bytes]:
    marker = data.find(HEADER_END)
    if marker < 0:
        raise ValueError("http headers incomplete")
    return data[:marker], data[marker + len(HEADER_END) :]
