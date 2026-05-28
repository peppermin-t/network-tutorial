# Concept Map

These maps show how the labs connect. They are not new architecture; they are the same 10-week path with AI engineering and VPN branches made explicit.

## General Request Path

```mermaid
flowchart LR
    A[Application intent] --> B[DNS]
    B --> C[Route table]
    C --> D[Socket]
    D --> E[TCP or UDP]
    E --> F[TLS optional]
    F --> G[HTTP or application protocol]
    G --> H[Proxy or gateway]
    H --> I[Upstream]
    I --> J[Logs, trace, metrics, packets]
```

DNS decides names. The route table decides paths. TCP/UDP carries bytes or datagrams. TLS may hide HTTP content. HTTP/protocol code gives status, headers, body, and streaming behavior. Proxies and gateways add another downstream/upstream split.

## VPN Branch

```mermaid
flowchart TD
    A[Route table] --> B[Physical NIC direct path]
    A --> C[Virtual VPN interface]
    C --> D[Encrypted outer tunnel]
    D --> E[VPN gateway]
    E --> F[Target network]
    G[DNS policy] --> A
    G --> F
```

VPN is not a single layer. It changes DNS policy and routing, which then changes what TCP, TLS, and HTTP experience. On a physical NIC capture you may see the encrypted outer tunnel, not the inner HTTP request.

## Model Serving Branch

```mermaid
flowchart LR
    A[Client] --> B[Gateway / reverse proxy]
    B --> C[Model-like upstream]
    C --> D[Worker capacity / backpressure]
    C --> E[Streaming response]
    B --> F[Trace/log/metrics]
    C --> F
    D --> G[HTTP 429 or queue latency]
```

Model serving network failures are often combined failures: gateway timeout, proxy buffering, slow first token, overloaded worker queue, Docker name/port mismatch, or VPN/DNS path issues.
