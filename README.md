# Python Network Lab Tutorial Project

`python-network-lab` is a code-driven computer networking learning lab. It starts from Python `socket` and gradually builds TCP/UDP, protocol framing, DNS, HTTP, proxy/gateway behavior, TLS, RPC/WebSocket, Docker networking, concurrency/backpressure, failure handling, observability, and packet-level verification.

## What this repo is

- This is a code-driven network learning lab.
- It is not a production network library.
- It is not a full computer networking textbook.
- It is not a VPN bypass, anonymity, censorship-circumvention, or commercial proxy tutorial.

The main path is:

```text
Application Intent
-> Name Resolution
-> Connection
-> Secure Transport
-> Application Protocol
-> Proxy/Gateway
-> Concurrency & Backpressure
-> Failure Handling
-> Observability
-> Packet-Level Verification
```

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .[dev]
python -m unittest discover -s tests -p "test_*.py"
python -m netlab --help
```

Without installing the package:

```powershell
$env:PYTHONPATH="src"
python -m netlab --help
```

## For AI/LLM Engineering Learners

This tutorial helps build network intuition for local model serving, gateway/reverse proxy behavior, HTTP streaming responses, timeout/retry/backpressure, Docker networking, and DNS/TLS/VPN-related debugging.

See [docs/ai-engineering-learning-path.md](docs/ai-engineering-learning-path.md) for the focused path.

## Fast Track

1. `labs/week01-sockets`: host/port, TCP/UDP, connection lifecycle.
2. `labs/week04-dns`: name resolution, TTL, DNS failure modes.
3. `labs/week05-http`: HTTP request/response/body and streaming foundation.
4. `labs/week06-proxy-timeout-retry`: gateway, timeout, retry, failure classification.
5. `labs/week09-container-networking`: Docker service names, bridge network, port mapping.
6. `labs/week10-capstone`: client -> gateway -> model-like upstream.
7. `labs/week11-vpn-mental-model`: optional VPN/routing/DNS mental model.

## CLI Examples

```powershell
python -m netlab server tcp-echo --host 127.0.0.1 --port 9001
python -m netlab client tcp-echo --host 127.0.0.1 --port 9001 --message "hello tcp"
python -m netlab dns query example.com --type A --server 8.8.8.8
python -m netlab server http --host 127.0.0.1 --port 8080
python -m netlab client http --host 127.0.0.1 --port 8080 --path /
python -m netlab fault classify retry-storm
python -m netlab client load-http --host 127.0.0.1 --port 8080 --requests 20 --concurrency 5
```

Model-like upstream:

```powershell
python -m netlab server model --host 127.0.0.1 --port 8090 --max-concurrency 2 --tokens 8 --token-delay 0.1
python -m netlab client http --host 127.0.0.1 --port 8090 --path /stream?prompt=local+model
```

Wireshark/TShark optional helpers:

```powershell
python -m netlab capture status
python -m netlab capture command --interface "Adapter for loopback traffic capture" --output captures/week05-http.pcapng --filter "tcp port 8080" --packets 20
```

## 10-Week Path

1. `labs/week01-sockets`: TCP/UDP echo, port, connection lifecycle.
2. `labs/week02-tcp-udp`: length prefix, packet split/sticky packets, heartbeat, timeout.
3. `labs/week03-packet-thinking`: protocol header and payload as bytes.
4. `labs/week04-dns`: DNS message, query, TTL cache.
5. `labs/week05-http`: HTTP/1.1 parser, client, server, keep-alive.
6. `labs/week06-proxy-timeout-retry`: forward/reverse proxy, timeout, retry.
7. `labs/week07-tls`: Python `ssl`, local certificate, SNI/ALPN observation.
8. `labs/week08-rpc-websocket`: JSON-RPC over HTTP, WebSocket.
9. `labs/week09-container-networking`: Docker Compose, service name DNS, bridge network.
10. `labs/week10-capstone`: observable client -> gateway -> model-like upstream system.

Week11 is an optional extension for VPN mental models. It uses read-only observation only and does not configure a VPN.

## How to use this repo

1. Run the lab.
2. Read the code path that handled the request.
3. Capture packets when Wireshark/TShark is available.
4. Inspect logs, HTTP status, headers, trace ids, and metrics.
5. Write notes using [docs/notes-template.md](docs/notes-template.md).
6. Map the observation to real engineering problems.

## Links

- [Concepts](docs/concepts.md)
- [Glossary](docs/glossary.md)
- [AI/LLM engineering learning path](docs/ai-engineering-learning-path.md)
- [Network debug playbook](docs/network-debug-playbook.md)
- [Concept map](docs/concept-map.md)
- [Further reading](docs/further-reading.md)
- [Notes template](docs/notes-template.md)
- [Wireshark workflow](docs/wireshark.md)
- [First-day capture route](docs/capture-first-day.md)

## Tooling Notes

- The main path uses only the Python standard library.
- Unit tests use `unittest` and are compatible with `pytest` discovery.
- Docker is used for Week09 and optional Week10 container experiments.
- Wireshark/TShark is useful but not required for the core code labs.
