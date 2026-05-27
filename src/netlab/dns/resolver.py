from __future__ import annotations

import socket
import time
from dataclasses import dataclass

from .messages import DNSAnswer, build_query, parse_message


@dataclass
class CacheEntry:
    expires_at: float
    answers: list[DNSAnswer]


class CachingResolver:
    def __init__(self, server: str = "8.8.8.8", port: int = 53, timeout: float = 3.0) -> None:
        self.server = server
        self.port = port
        self.timeout = timeout
        self._cache: dict[tuple[str, str], CacheEntry] = {}

    def query(self, name: str, qtype: str = "A") -> list[DNSAnswer]:
        key = (name.rstrip(".").lower(), qtype.upper())
        now = time.time()
        entry = self._cache.get(key)
        if entry and entry.expires_at > now:
            return entry.answers
        answers = query_dns(name, qtype, self.server, self.port, self.timeout)
        ttl = min((answer.ttl for answer in answers), default=0)
        if ttl > 0:
            self._cache[key] = CacheEntry(now + ttl, answers)
        return answers


def query_dns(name: str, qtype: str = "A", server: str = "8.8.8.8", port: int = 53, timeout: float = 3.0) -> list[DNSAnswer]:
    query = build_query(name, qtype)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(timeout)
        sock.sendto(query, (server, port))
        data, _ = sock.recvfrom(4096)
    message = parse_message(data)
    if message.rcode != 0:
        raise OSError(f"dns rcode={message.rcode}")
    return [answer for answer in message.answers if answer.rtype == qtype.upper()]
