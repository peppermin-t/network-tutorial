# AI / LLM Engineering Learning Path

Use this as a focused pass through the main tutorial when your goal is model serving, RAG, agents, local services, gateways, and deployment debugging.

## Path

### Week00 - Layering and Tools
- Learn the request path: application intent -> DNS -> route -> socket -> TCP/TLS/HTTP -> gateway -> upstream -> observability.
- Run: `python -m netlab doctor` and `python -m netlab path ai`.

### Week03 - Sockets, TCP/UDP
- Learn host, port, bind, connect, refused, and timeout vocabulary.
- Run the TCP/UDP echo labs.

### Week05 - DNS
- Learn resolver behavior, TTL, NXDOMAIN, and timeout.
- Run: `python -m netlab dns query example.com --type A`.

### Week06 - HTTP
- Learn request/response, status, headers, body, and Content-Length.
- Run the local HTTP server/client.

### Week08 - Proxy, Gateway, Timeout, Retry
- Learn client timeout, upstream timeout, gateway timeout, retry, retry storm, and 429.
- Run: `python labs/week08-proxy-timeout-retry/experiment.py`.

### Week09 - RPC, WebSocket, Streaming
- Learn request ids, long-lived connections, first byte latency, total latency, and proxy buffering.
- Run: `python labs/week09-rpc-websocket-streaming/experiment.py`.

### Week10 - Docker Networking
- Learn Compose service DNS, host/container ports, and why container localhost is not the host.
- Run Docker Compose if Docker is available.

### Week11 - VPN Remote Access
- Learn route table and DNS policy changes when remote access is involved.
- Run: `python labs/week11-vpn-remote-access/experiment.py` before and after connecting to an authorized VPN.

### Week12 - Capstone
- Run client -> gateway -> model-like upstream.
- Compare direct stream and gateway stream.
- Observe `X-Trace-Id`, metrics, 429 backpressure, and load-test timing.
- Complete one design template for a local AI service network.

## What This Helps With
- Local model endpoints that bind to the wrong interface.
- RAG services whose containers use the wrong hostname.
- Gateways that buffer token streaming.
- Retries that multiply model load.
- VPN-only internal endpoints that fail at DNS, route, TLS, or access policy.
- Small lab designs with clear subnets, names, ports, paths, and monitoring.
