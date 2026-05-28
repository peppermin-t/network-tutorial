# Week 10 - Capstone

Focus: observable communication system: client -> gateway -> upstream.

## Before You Run: Concepts

- `Gateway`: the reverse proxy hop between client and model-like upstream. See `docs/concepts.md#gateway`.
- `HTTP streaming`: response body arrives progressively. See `docs/concepts.md#http-streaming`.
- `Proxy buffering`: buffering can turn streaming into one final response. See `docs/concepts.md#proxy-buffering`.
- `Backpressure`: reject or slow callers when capacity is full. See `docs/concepts.md#backpressure`.
- `Trace ID`: correlate client, gateway, and upstream logs. See `docs/concepts.md#trace-id`.
- `p50 / p95 latency`: median versus tail latency. See `docs/concepts.md#p50--p95-latency`.

## If You Are Confused

- If streaming becomes non-streaming through the gateway, read `chunked transfer encoding` and `proxy buffering`.
- If you see 429, classify it as Capacity, not TCP.
- If logs from client, gateway, and upstream feel disconnected, follow `X-Trace-Id`.

Run:

```powershell
$env:PYTHONPATH="src"
python -m netlab server model --host 127.0.0.1 --port 8090 --max-concurrency 2 --tokens 8 --token-delay 0.1
python -m netlab proxy reverse --host 127.0.0.1 --port 8081 --upstream-host 127.0.0.1 --upstream-port 8090
python -m netlab client http --host 127.0.0.1 --port 8090 --path /generate?prompt=direct
python -m netlab client http --host 127.0.0.1 --port 8090 --path /stream?prompt=direct
python -m netlab client http --host 127.0.0.1 --port 8081 --path /stream?prompt=capstone
python -m netlab client load-http --host 127.0.0.1 --port 8090 --path /generate?prompt=load --requests 10 --concurrency 5
python -m netlab client load-http --host 127.0.0.1 --port 8090 --path /stream?prompt=load --requests 10 --concurrency 5
python -m netlab client http --host 127.0.0.1 --port 8090 --path /metrics
python -m netlab trace capstone-request
```

Streaming check:

- Direct upstream `/stream` should produce chunked HTTP.
- Gateway `/stream` should forward chunks as they arrive instead of waiting for the full upstream body.
- Compare first byte latency and total elapsed time when `--token-delay` is visible.

Capacity check:

- `HTTP 429` means capacity/backpressure. In model serving, this maps to GPU worker limits, request queue limits, or rate limits.
- p50/p95 latency helps show when pressure affects the tail before every request fails.
- `X-Trace-Id` should appear in the response and in gateway/upstream logs.

Deliverable:

- Draw one request path from application code to socket to proxy to upstream.
- Include DNS/name resolution, TCP, HTTP, streaming, timeout, retry, capacity, TLS optional, and logging fields.
- Write the final explanation in `notes/final-review.md`.

Wireshark task:

- Capture the capstone request path and attach the relevant display filters to your final review.
- Minimum filters: `tcp`, `http`, `dns`, `tls` where applicable.
- Explain one packet-level observation that changed or corrected your mental model.

## Systematic Template

- Concept Model: Full path. Application intent flows through name resolution, connection, protocol, gateway, capacity, failure handling, observability, and packet verification.
- Code Lab: Run `client -> gateway -> model-like upstream`.
- Failure Lab: Overload model-like upstream and classify with `python -m netlab fault classify too-many-requests` or `retry-storm`.
- Wireshark Lab: Capture gateway and upstream ports; connect trace id, logs, HTTP status, and packets.
- Work Mapping: This is the same shape as cloud service calls, distributed workers, and local model serving.
