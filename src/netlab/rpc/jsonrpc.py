from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class JSONRPCRequest:
    method: str
    params: Any
    id: int | str | None


def encode_request(method: str, params: Any = None, request_id: int | str = 1) -> bytes:
    return json.dumps({"jsonrpc": "2.0", "method": method, "params": params, "id": request_id}).encode("utf-8")


def decode_request(data: bytes) -> JSONRPCRequest:
    payload = json.loads(data.decode("utf-8"))
    if payload.get("jsonrpc") != "2.0":
        raise ValueError("unsupported jsonrpc version")
    return JSONRPCRequest(payload["method"], payload.get("params"), payload.get("id"))


def handle_request(data: bytes, methods: dict[str, Callable[[Any], Any]]) -> bytes:
    request = decode_request(data)
    try:
        result = methods[request.method](request.params)
        response = {"jsonrpc": "2.0", "result": result, "id": request.id}
    except Exception as exc:
        response = {"jsonrpc": "2.0", "error": {"code": -32000, "message": str(exc)}, "id": request.id}
    return json.dumps(response).encode("utf-8")
