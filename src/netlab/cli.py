from __future__ import annotations

import argparse
import sys
import time

from netlab.capacity.backpressure import run_concurrent_load
from netlab.capture.tshark import build_capture_command, build_read_command, run_tshark, tshark_status
from netlab.common.retry import RetryPolicy
from netlab.dns.resolver import CachingResolver
from netlab.faults.model import classify_failure
from netlab.faults.server import run_fault_http_server
from netlab.http.client import http_request
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


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
