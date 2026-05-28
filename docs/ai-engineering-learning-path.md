# AI/LLM Engineering Learning Path

This path uses the existing tutorial to build network debugging intuition for local model serving, RAG services, agents, gateways, Docker networking, and remote/internal endpoints.

## Fast Track: Core Labs

### Week01 Sockets

- Why this matters for AI/LLM engineering: every local model server, vector DB, gateway, and tool server starts as a reachable host and port.
- What to run: TCP echo, UDP echo, and a closed-port call.
- What to observe: TCP handshake, UDP no-handshake behavior, connection refused.
- What to write in notes: host, port, server bind address, client target, packet sequence.
- Real-world mapping: "my agent cannot reach local model server" starts here.

### Week04 DNS

- Why this matters for AI/LLM engineering: internal model names, service discovery, Docker service names, and VPN-only domains all depend on resolution.
- What to run: `python -m netlab dns query example.com --type A --server 8.8.8.8` and the Week04 experiment.
- What to observe: query type, answer, TTL, timeout versus NXDOMAIN.
- What to write in notes: resolver used, answer records, TTL, failure classification.
- Real-world mapping: "works by IP but not by name" and "VPN connected but internal name fails".

### Week05 HTTP

- Why this matters for AI/LLM engineering: model APIs, embedding APIs, vector DB APIs, and gateway APIs usually expose HTTP first.
- What to run: local HTTP server/client and parser experiment.
- What to observe: request line, status line, headers, body, `Content-Length`, chunked response concepts.
- What to write in notes: exact path, status code, headers that affected parsing.
- Real-world mapping: "HTTP 500/429 is not a TCP failure" and "body framing decides when a response is complete".

### Week06 Proxy, Timeout, Retry

- Why this matters for AI/LLM engineering: gateways, agent tool routers, and service clients own timeout/retry behavior.
- What to run: reverse proxy, fault HTTP server modes, retry experiment.
- What to observe: downstream connection, separate upstream connection, connect timeout, read timeout, slow upstream, retry amplification.
- What to write in notes: which layer failed first and whether retry helped or added load.
- Real-world mapping: "gateway timeout", "retry storm", and "slow model worker".

### Week09 Container Networking

- Why this matters for AI/LLM engineering: local AI stacks often run gateway, model, database, and UI in containers.
- What to run: Docker Compose lab when Docker is available.
- What to observe: service name DNS, bridge network, host port versus container port, container `localhost`.
- What to write in notes: from-host address, from-container address, and one wrong address that fails.
- Real-world mapping: "container cannot reach localhost model server" or "service name works only inside Compose".

### Week10 Capstone

- Why this matters for AI/LLM engineering: it models client -> gateway -> model-like upstream with streaming, trace id, metrics, capacity, and 429.
- What to run: direct upstream `/generate`, direct upstream `/stream`, gateway `/stream`, load test, metrics.
- What to observe: first byte latency, total latency, chunk forwarding, `X-Trace-Id`, 429 under load, p50/p95.
- What to write in notes: request path, trace id through components, whether streaming stayed streaming through the gateway.
- Real-world mapping: "LLM streaming got buffered by proxy" and "GPU worker capacity caused 429".

## Optional Extension

### Week07 TLS

- Why this matters: HTTPS model APIs fail differently from plain TCP/HTTP.
- Run: `python -m netlab client https --host example.com --port 443 --path /`.
- Observe: certificate validation, SNI, ALPN/cipher, encrypted application data.
- Notes: separate TCP connect success from TLS verification failure.
- Mapping: private CA, wrong hostname, ingress certificate mismatch.

### Week08 RPC/WebSocket

- Why this matters: tools and agents often use structured RPC or long-lived WebSocket sessions.
- Run: JSON-RPC and WebSocket echo experiments.
- Observe: framing, request id, persistent connection behavior.
- Notes: where protocol framing sits above TCP.
- Mapping: streaming tool sessions and agent control channels.

### Week11 VPN Mental Model

- Why this matters: remote lab servers and internal model services often require authorized VPN routes and DNS policy.
- Run: `python labs/week11-vpn-mental-model/experiment.py` before and after connecting to an authorized VPN.
- Observe: route table, default route, DNS server, traceroute changes.
- Notes: classify each change as DNS, routing, TCP, TLS, HTTP, or capacity.
- Mapping: "VPN connected but internal model endpoint still fails".

## Suggested Study Loop

1. Read the small concept sections for the lab.
2. Run the command exactly once in the happy path.
3. Capture or inspect logs for one concrete signal.
4. Inject one failure.
5. Write the layer classification in notes before trying fixes.
