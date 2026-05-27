# Knowledge Map

Use this as the long-term index for concepts and failures.

```text
Networked Request
  Application Intent
    target host
    port
    protocol
    timeout budget
    retry policy
  Name Resolution
    DNS timeout
    NXDOMAIN
    TTL/cache
    internal service name
  Connection
    TCP handshake
    connection refused
    reset
    read timeout
    UDP datagram boundary
  Secure Transport
    TLS handshake
    certificate verification
    SNI
  Application Protocol
    HTTP headers/body
    status code
    chunked response
    WebSocket upgrade
    RPC request id
  Proxy/Gateway
    downstream connection
    upstream connection
    timeout
    retry
    trace id propagation
  Concurrency & Backpressure
    max concurrency
    queueing
    429
    p50/p95 latency
    retry storm
  Observability
    logs
    metrics
    trace id
    Wireshark capture
```
