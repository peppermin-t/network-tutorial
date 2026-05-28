# Week 08 - Proxy, Gateway, Timeout, Retry

## Goal
Understand proxy/gateway boundaries, timeout types, retries, retry storms, and layer-aware failure classification.

## Why this matters
AI/LLM services, RAG pipelines, internal APIs, and deployment gateways often fail between client and upstream, not at only one endpoint.

## Where this fits
Weeks05-07 covered DNS, HTTP, and TLS. Week08 explains what changes when a gateway sits between client and upstream.

## Before You Run: Concepts
Read [Proxy and Gateway](../../docs/concepts.md#proxy-and-gateway), [Timeout](../../docs/concepts.md#timeout), [Retry](../../docs/concepts.md#retry), [Backpressure](../../docs/concepts.md#backpressure), and [Observability](../../docs/concepts.md#observability).

## Run
```powershell
python labs/week08-proxy-timeout-retry/experiment.py
```

Optional local proxy:

```powershell
python -m netlab server http --host 127.0.0.1 --port 8080
python -m netlab proxy reverse --host 127.0.0.1 --port 8081 --upstream-host 127.0.0.1 --upstream-port 8080
python -m netlab client http --host 127.0.0.1 --port 8081 --path /
```

## Observe
- Retry succeeds for a transient failure.
- Retry multiplies work for slow operations.
- Failure classifier maps symptoms to likely layers.
- Reverse proxy creates client->gateway and gateway->upstream TCP connections.

## Questions
1. Why does a reverse proxy create two TCP connections?
2. How is gateway timeout different from client timeout?
3. Why can retry make an outage worse?
4. How would you classify DNS, TCP, TLS, HTTP, proxy, and capacity failures?
5. What evidence would you collect before increasing timeout?

## Notes Checklist
- Record transient retry attempts.
- Record slow retry risk.
- Classify at least four failure scenarios.
- Draw client -> gateway -> upstream.

## Work Mapping
This maps to API gateways, reverse proxies, model gateways, LLM retry policies, rate limits, overloaded upstreams, and incident debugging.

## Next Week
Week09 applies these ideas to RPC, WebSocket, and streaming behavior.

