from __future__ import annotations

from dataclasses import dataclass


FAILURE_LAYERS = {
    "dns-timeout": "DNS",
    "dns-nxdomain": "DNS",
    "connection-refused": "TCP",
    "connect-timeout": "TCP/Routing",
    "read-timeout": "TCP/Application",
    "tls-verify-failed": "TLS",
    "http-500": "HTTP",
    "upstream-slow": "Proxy/Application",
    "gateway-timeout": "Proxy/Application",
    "retry-storm": "Capacity",
    "server-close": "TCP/Application",
    "too-many-requests": "Capacity",
}


@dataclass(frozen=True)
class FailureScenario:
    name: str
    layer: str
    symptom: str
    wireshark_filter: str
    expected_client_result: str


def classify_failure(name: str) -> FailureScenario:
    normalized = name.strip().lower()
    layer = FAILURE_LAYERS.get(normalized)
    if layer is None:
        raise ValueError(f"unknown failure scenario: {name}")
    symptoms = {
        "dns-timeout": "DNS query has no timely response.",
        "dns-nxdomain": "DNS response says the name does not exist.",
        "connection-refused": "TCP SYN receives RST because nothing is listening.",
        "connect-timeout": "TCP SYN or route path does not complete before deadline.",
        "read-timeout": "Connection opens, but response bytes arrive too late.",
        "tls-verify-failed": "TCP connects, then TLS certificate validation fails.",
        "http-500": "HTTP response is syntactically valid but application failed.",
        "upstream-slow": "Gateway connects to upstream but waits too long.",
        "gateway-timeout": "Client receives a gateway-level timeout while the upstream path is slow or unavailable.",
        "retry-storm": "Retries multiply load after a dependency slows or fails.",
        "server-close": "Peer closes before a complete application response.",
        "too-many-requests": "Server rejects excess concurrency with 429.",
    }
    filters = {
        "DNS": "dns",
        "TCP": "tcp.flags.reset == 1 or tcp.analysis.retransmission",
        "TCP/Routing": "tcp.analysis.retransmission or tcp.flags.syn == 1",
        "TCP/Application": "tcp",
        "TLS": "tls",
        "HTTP": "http",
        "Proxy/Application": "http or tcp",
        "Capacity": "http.response.code == 429 or tcp",
    }
    results = {
        "dns-timeout": "resolver timeout",
        "dns-nxdomain": "name resolution error",
        "connection-refused": "ConnectionRefusedError",
        "connect-timeout": "TimeoutError during connect",
        "read-timeout": "TimeoutError or socket.timeout",
        "tls-verify-failed": "certificate verify failed",
        "http-500": "HTTP 500 response",
        "upstream-slow": "gateway timeout or client timeout",
        "gateway-timeout": "HTTP 504 or gateway closes connection after upstream wait",
        "retry-storm": "retry-amplified latency and more failed requests",
        "server-close": "empty or truncated response",
        "too-many-requests": "HTTP 429 response",
    }
    return FailureScenario(normalized, layer, symptoms[normalized], filters[layer], results[normalized])
