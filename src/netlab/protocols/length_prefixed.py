from __future__ import annotations

import struct


class LengthPrefixedProtocol:
    """A tiny TCP-friendly framing protocol: 4-byte big-endian length + payload."""

    def __init__(self, max_frame_size: int = 16 * 1024 * 1024) -> None:
        self.max_frame_size = max_frame_size
        self._buffer = bytearray()

    @staticmethod
    def encode(message: bytes) -> bytes:
        return struct.pack("!I", len(message)) + message

    def feed(self, data: bytes) -> list[bytes]:
        self._buffer.extend(data)
        messages: list[bytes] = []
        while True:
            if len(self._buffer) < 4:
                return messages
            length = struct.unpack("!I", self._buffer[:4])[0]
            if length > self.max_frame_size:
                raise ValueError(f"frame too large: {length}")
            if len(self._buffer) < 4 + length:
                return messages
            payload = bytes(self._buffer[4 : 4 + length])
            del self._buffer[: 4 + length]
            messages.append(payload)
