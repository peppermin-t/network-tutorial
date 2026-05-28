from __future__ import annotations

import argparse
import platform
import shutil
import sys
import time

from netlab.capacity.backpressure import run_concurrent_load
from netlab.capture.tshark import build_capture_command, build_read_command, run_tshark, tshark_status
from netlab.common.retry import RetryPolicy
from netlab.dns.resolver import CachingResolver
from netlab.faults.model import classify_failure
from netlab.faults.server import run_fault_http_server
from netlab.http.client import http_request, stream_http_request
from netlab.http.server import run_http_server
from netlab.model.server import run_model_server
from netlab.observability.trace import span
from netlab.proxy.simple import run_reverse_proxy
from netlab.rpc.websocket import run_websocket_echo_server, websocket_echo_client
from netlab.sockets.echo import run_tcp_echo_server, run_udp_echo_server, tcp_echo_client, udp_echo_client
from netlab.tls.simple import https_get


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="netlab", description="Python Network Lab tutorial CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    server = subparsers.add_parser("server", help="Run local servers")
    server_sub = server.add_subparsers(dest="kind", required=True)
    _host_port(server_sub.add_parser("tcp-echo", help="Run TCP echo server"))
    _host_port(server_sub.add_parser("udp-echo", help="Run UDP echo server"))
    _host_port(server_sub.add_parser("http", help="Run minimal HTTP server"), default_port=8080)
    _host_port(server_sub.add_parser("websocket", help="Run WebSocket echo server"), default_port=8765)
    fault_http = _host_port(server_sub.add_parser("fault-http", help="Run HTTP server with injected failures"), default_port=8082)
    fault_http.add_argument("--mode", choices=["ok", "delay", "slow", "close", "500", "error"], default="delay")
    fault_http.add_argument("--delay", type=float, default=2.0)
    fault_http.add_argument("--status-code", type=int, default=500)
    model_server = _host_port(server_sub.add_parser("model", help="Run model-like upstream server"), default_port=8090)
    model_server.add_argument("--max-concurrency", type=int, default=2)
    model_server.add_argument("--token-delay", type=float, default=0.05)
    model_server.add_argument("--tokens", type=int, default=8)

    client = subparsers.add_parser("client", help="Run local clients")
    client_sub = client.add_subparsers(dest="kind", required=True)
    tcp_client = _host_port(client_sub.add_parser("tcp-echo", help="Call TCP echo server"))
    tcp_client.add_argument("--message", default="hello tcp")
    udp_client = _host_port(client_sub.add_parser("udp-echo", help="Call UDP echo server"))
    udp_client.add_argument("--message", default="hello udp")
    http_client = _host_port(client_sub.add_parser("http", help="Call HTTP server"), default_port=8080)
    http_client.add_argument("--path", default="/")
    stream_http = _host_port(client_sub.add_parser("stream-http", help="Call HTTP server and print response timing"), default_port=8080)
    stream_http.add_argument("--path", default="/")
    stream_http.add_argument("--timeout", type=float, default=3.0)
    stream_http.add_argument("--show-headers", action="store_true")
    ws_client = _host_port(client_sub.add_parser("websocket", help="Call WebSocket echo server"), default_port=8765)
    ws_client.add_argument("--message", default="hello websocket")
    https_client = client_sub.add_parser("https", help="Call public or private HTTPS endpoint")
    https_client.add_argument("--host", required=True)
    https_client.add_argument("--port", type=int, default=443)
    https_client.add_argument("--path", default="/")
    load_http = _host_port(client_sub.add_parser("load-http", help="Run concurrent HTTP load"), default_port=8080)
    load_http.add_argument("--path", default="/")
    load_http.add_argument("--requests", type=int, default=20)
    load_http.add_argument("--concurrency", type=int, default=5)
    load_http.add_argument("--timeout", type=float, default=3.0)

    dns = subparsers.add_parser("dns", help="DNS experiments")
    dns_sub = dns.add_subparsers(dest="kind", required=True)
    dns_query = dns_sub.add_parser("query", help="Query DNS over UDP")
    dns_query.add_argument("name")
    dns_query.add_argument("--type", default="A", choices=["A", "AAAA", "CNAME"])
    dns_query.add_argument("--server", default="8.8.8.8")
    dns_query.add_argument("--port", type=int, default=53)

    proxy = subparsers.add_parser("proxy", help="Proxy experiments")
    proxy_sub = proxy.add_subparsers(dest="kind", required=True)
    reverse = _host_port(proxy_sub.add_parser("reverse", help="Run reverse proxy"), default_port=8081)
    reverse.add_argument("--upstream-host", default="127.0.0.1")
    reverse.add_argument("--upstream-port", type=int, default=8080)

    trace = subparsers.add_parser("trace", help="Measure one local operation")
    trace.add_argument("name")
    trace.add_argument("--sleep", type=float, default=0.05)

    bench = subparsers.add_parser("benchmark", help="Repeated TCP echo calls")
    bench.add_argument("--host", default="127.0.0.1")
    bench.add_argument("--port", type=int, default=9001)
    bench.add_argument("--requests", type=int, default=10)
    bench.add_argument("--message", default="hello")

    capture = subparsers.add_parser("capture", help="Optional Wireshark/TShark helpers")
    capture_sub = capture.add_subparsers(dest="kind", required=True)
    capture_sub.add_parser("status", help="Check whether tshark is available")
    capture_command = capture_sub.add_parser("command", help="Print a tshark capture command")
    capture_command.add_argument("--interface", required=True)
    capture_command.add_argument("--output", required=True)
    capture_command.add_argument("--filter", default="")
    capture_command.add_argument("--packets", type=int)
    capture_read = capture_sub.add_parser("read", help="Run tshark against a capture file")
    capture_read.add_argument("pcap")
    capture_read.add_argument("--display-filter", default="")
    capture_read.add_argument("--field", action="append", default=[])

    fault = subparsers.add_parser("fault", help="Classify failure scenarios by network layer")
    fault_sub = fault.add_subparsers(dest="kind", required=True)
    fault_classify = fault_sub.add_parser("classify", help="Explain where a failure belongs")
    fault_classify.add_argument("scenario")

    subparsers.add_parser("doctor", help="Print local environment hints")

    path = subparsers.add_parser("path", help="Print recommended learning paths")
    path_sub = path.add_subparsers(dest="kind", required=True)
    path_sub.add_parser("tutorial", help="Complete Week00-Week12 tutorial path")
    path_sub.add_parser("ai", help="AI/LLM engineering fast track")
    path_sub.add_parser("design", help="Small network design path")
    path_sub.add_parser("vpn", help="VPN mental model path")

    concept = subparsers.add_parser("concept", help="Print a short concept summary")
    concept.add_argument("name")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "server":
        return _server(args)
    if args.command == "client":
        return _client(args)
    if args.command == "dns":
        return _dns(args)
    if args.command == "proxy":
        return _proxy(args)
    if args.command == "trace":
        return _trace(args)
    if args.command == "benchmark":
        return _benchmark(args)
    if args.command == "capture":
        return _capture(args)
    if args.command == "fault":
        return _fault(args)
    if args.command == "doctor":
        return _doctor()
    if args.command == "path":
        return _path(args)
    if args.command == "concept":
        return _concept(args)
    raise AssertionError(args.command)


def _host_port(parser: argparse.ArgumentParser, default_port: int = 9001) -> argparse.ArgumentParser:
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=default_port)
    return parser


def _server(args: argparse.Namespace) -> int:
    if args.kind == "tcp-echo":
        run_tcp_echo_server(args.host, args.port)
    elif args.kind == "udp-echo":
        run_udp_echo_server(args.host, args.port)
    elif args.kind == "http":
        run_http_server(args.host, args.port)
    elif args.kind == "websocket":
        run_websocket_echo_server(args.host, args.port)
    elif args.kind == "fault-http":
        run_fault_http_server(args.host, args.port, args.mode, args.delay, args.status_code)
    elif args.kind == "model":
        run_model_server(args.host, args.port, args.max_concurrency, args.token_delay, args.tokens)
    return 0


def _client(args: argparse.Namespace) -> int:
    if args.kind == "tcp-echo":
        print(tcp_echo_client(args.host, args.port, args.message.encode()).decode("utf-8", errors="replace"))
    elif args.kind == "udp-echo":
        print(udp_echo_client(args.host, args.port, args.message.encode()).decode("utf-8", errors="replace"))
    elif args.kind == "http":
        response = http_request(args.host, args.port, args.path)
        print(f"{response.status_code} {response.reason}")
        print(response.body.decode("utf-8", errors="replace"))
    elif args.kind == "stream-http":
        response = stream_http_request(args.host, args.port, args.path, timeout=args.timeout)
        print(f"status={response.status_code} {response.reason}")
        print(f"x_trace_id={response.headers.get('x-trace-id', '')}")
        print(f"first_byte_ms={response.first_byte_ms}")
        if args.show_headers:
            for key, value in sorted(response.headers.items()):
                print(f"header.{key}={value}")
        for index, chunk in enumerate(response.chunks, start=1):
            preview = chunk.data[:120].decode("utf-8", errors="replace").replace("\n", "\\n")
            print(f"chunk={index} elapsed_ms={chunk.elapsed_ms} size={chunk.size} data={preview}")
        print(f"total_ms={response.total_ms}")
    elif args.kind == "websocket":
        print(websocket_echo_client(args.host, args.port, args.message.encode()).decode("utf-8", errors="replace"))
    elif args.kind == "https":
        cipher, body = https_get(args.host, args.port, args.path)
        print(f"cipher={cipher}")
        print(body[:1000].decode("utf-8", errors="replace"))
    elif args.kind == "load-http":
        result = run_concurrent_load(
            args.requests,
            args.concurrency,
            lambda: http_request(args.host, args.port, args.path, timeout=args.timeout).status_code,
        )
        print(
            f"requests={result.total} successes={result.successes} failures={result.failures} "
            f"timeouts={result.timeouts} p50_ms={result.p50_ms} p95_ms={result.p95_ms}"
        )
    return 0


def _dns(args: argparse.Namespace) -> int:
    resolver = CachingResolver(server=args.server, port=args.port)
    for answer in resolver.query(args.name, args.type):
        print(f"{answer.name}\t{answer.ttl}\t{answer.rtype}\t{answer.value}")
    return 0


def _proxy(args: argparse.Namespace) -> int:
    if args.kind == "reverse":
        run_reverse_proxy(args.host, args.port, args.upstream_host, args.upstream_port)
    return 0


def _trace(args: argparse.Namespace) -> int:
    with span(args.name) as item:
        time.sleep(args.sleep)
    print(f"trace_id={item.trace_id} span={item.name} elapsed_ms={item.elapsed_ms} error={item.error}")
    return 0


def _benchmark(args: argparse.Namespace) -> int:
    policy = RetryPolicy(max_attempts=3, timeout_seconds=1.0, backoff_seconds=0.05)
    started = time.perf_counter()
    for _ in range(args.requests):
        policy.run(lambda: tcp_echo_client(args.host, args.port, args.message.encode(), timeout=policy.timeout_seconds))
    elapsed = time.perf_counter() - started
    print(f"requests={args.requests} elapsed_ms={elapsed * 1000:.2f} rps={args.requests / elapsed:.2f}")
    return 0


def _capture(args: argparse.Namespace) -> int:
    if args.kind == "status":
        status = tshark_status()
        print(f"available={status.available}")
        print(f"path={status.path or ''}")
        print(f"version={status.version or ''}")
        return 0 if status.available else 1
    if args.kind == "command":
        print(" ".join(build_capture_command(args.interface, args.output, args.filter, args.packets)))
        return 0
    if args.kind == "read":
        print(run_tshark(build_read_command(args.pcap, args.display_filter, args.field)), end="")
        return 0
    raise AssertionError(args.kind)


def _fault(args: argparse.Namespace) -> int:
    if args.kind == "classify":
        scenario = classify_failure(args.scenario)
        print(f"name={scenario.name}")
        print(f"layer={scenario.layer}")
        print(f"symptom={scenario.symptom}")
        print(f"wireshark_filter={scenario.wireshark_filter}")
        print(f"expected_client_result={scenario.expected_client_result}")
        return 0
    raise AssertionError(args.kind)


def _doctor() -> int:
    print(f"python={sys.version.split()[0]}")
    print(f"platform={platform.platform()}")
    print(f"tshark={'yes' if shutil.which('tshark') else 'no'}")
    print(f"docker={'yes' if shutil.which('docker') else 'no'}")
    print("wireshark=optional but useful for packet-level verification")
    print("recommended_first_lab=python -m netlab server tcp-echo --host 127.0.0.1 --port 9001")
    return 0


def _path(args: argparse.Namespace) -> int:
    if args.kind == "tutorial":
        lines = [
            "Complete tutorial path:",
            "1. Week00 - Orientation, Layering, and Tools",
            "2. Week01 - IP Addressing, Subnetting, and Routing",
            "3. Week02 - Local Network Diagnostics",
            "4. Week03 - Sockets, TCP/UDP, Host/Port, Connection Lifecycle",
            "5. Week04 - TCP Framing and Packet Thinking",
            "6. Week05 - DNS",
            "7. Week06 - HTTP/1.1 Fundamentals",
            "8. Week07 - TLS and HTTPS",
            "9. Week08 - Proxy, Gateway, Timeout, Retry",
            "10. Week09 - RPC, WebSocket, and Streaming",
            "11. Week10 - Docker and Container Networking",
            "12. Week11 - VPN and Remote Access Mental Model",
            "13. Week12 - Capstone: Network Design + Observable Service Path",
        ]
    elif args.kind == "ai":
        lines = [
            "AI/LLM engineering fast track:",
            "1. Week00: layering and request path vocabulary",
            "2. Week03: sockets, TCP/UDP, host/port",
            "3. Week05: DNS and resolver failure",
            "4. Week06: HTTP request/response foundation",
            "5. Week08: gateway, timeout, retry, failure classification",
            "6. Week09: RPC, WebSocket, streaming, first byte latency",
            "7. Week10: Docker service names, bridge network, port mapping",
            "8. Week12: client -> gateway -> model-like upstream with traces and metrics",
        ]
    elif args.kind == "design":
        lines = [
            "Small network design path:",
            "1. Week00: practical layering and observation tools",
            "2. Week01: IP, CIDR, gateway, route table, DHCP/static split",
            "3. Week02: ARP, ICMP, NAT, firewall mental models",
            "4. Week05: DNS naming and resolver behavior",
            "5. Week08: gateway boundaries, timeout, retry",
            "6. Week10: container network boundaries",
            "7. Week11: VPN route and DNS policy",
            "8. Week12: topology, subnet plan, ports, paths, observability",
        ]
    elif args.kind == "vpn":
        lines = [
            "VPN mental model path:",
            "1. Week01: route table, default route, DNS server",
            "2. Week02: local reachability, NAT, firewall symptoms",
            "3. Week05: DNS query, TTL, timeout, NXDOMAIN",
            "4. Week07: HTTPS, certificate validation, SNI",
            "5. Week10: namespaces and localhost intuition",
            "6. Week11: virtual interface, route table, DNS policy, full/split tunnel",
        ]
    else:
        raise AssertionError(args.kind)
    print("\n".join(lines))
    return 0


CONCEPT_SUMMARIES = {
    "tcp": [
        "TCP is a reliable ordered byte stream between two endpoints.",
        "Observe handshake, payload, ACKs, and teardown in Week03.",
        "TCP does not preserve application message boundaries.",
        "AI mapping: slow model response after connect is usually above TCP.",
    ],
    "dns": [
        "DNS maps names to records before a connection can be made.",
        "Observe query type, answer, TTL, timeout, and NXDOMAIN in Week05.",
        "DNS success does not prove TCP/TLS/HTTP success.",
        "AI mapping: internal model endpoints often fail first at DNS policy.",
    ],
    "http-streaming": [
        "HTTP streaming sends the response body progressively.",
        "Observe chunked responses and first byte vs total latency in Week09 and Week12.",
        "Streaming can be broken by proxy buffering.",
        "AI mapping: token streaming quality depends on prompt first chunk forwarding.",
    ],
    "proxy-buffering": [
        "Proxy buffering means a gateway reads upstream data before forwarding it.",
        "Observe direct `/stream` versus gateway `/stream` in Week12.",
        "If chunks arrive all at once, streaming has likely been buffered.",
        "AI mapping: model server streams correctly but users still see delayed output.",
    ],
    "docker-localhost": [
        "Localhost points to the current network namespace.",
        "Inside a container, localhost is the container itself.",
        "Use Compose service names for service-to-service calls.",
        "AI mapping: containerized agents often point at the wrong model endpoint.",
    ],
    "backpressure": [
        "Backpressure rejects or slows callers when capacity is exhausted.",
        "Observe HTTP 429 and p50/p95 latency in Week12.",
        "429 is a capacity signal, not a TCP failure.",
        "AI mapping: GPU workers and queues need explicit overload behavior.",
    ],
    "vpn": [
        "VPN combines virtual interface, route table, encrypted tunnel, and DNS policy.",
        "Observe route and DNS snapshots before and after VPN in Week11.",
        "Full tunnel and split tunnel change different paths.",
        "AI mapping: internal model endpoints may depend on authorized routes and DNS.",
    ],
}


def _concept(args: argparse.Namespace) -> int:
    name = args.name.strip().lower()
    summary = CONCEPT_SUMMARIES.get(name)
    if summary is None:
        print("unknown concept")
        print("available=" + ", ".join(sorted(CONCEPT_SUMMARIES)))
        return 1
    print(name)
    for line in summary:
        print(f"- {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
