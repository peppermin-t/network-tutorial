# Week 06 - HTTP/1.1 Fundamentals

## Goal
Understand HTTP request/response structure on top of TCP: start line, headers, body, Content-Length, status codes, and connection close.

## Why this matters
HTTP is the interface for APIs, model gateways, RAG services, local dashboards, and most deployment health checks.

## Where this fits
Week04 explains framing. Week06 applies it to HTTP before TLS, proxying, and streaming.

## Before You Run: Concepts
Read [HTTP](../../docs/concepts.md#http), [TCP Framing](../../docs/concepts.md#tcp-framing), and [Closed, Filtered, Refused](../../docs/concepts.md#closed-filtered-refused).

## Run
Terminal 1:

```powershell
python -m netlab server http --host 127.0.0.1 --port 8080
```

Terminal 2:

```powershell
python -m netlab client http --host 127.0.0.1 --port 8080 --path /
python labs/week06-http/experiment.py
```

## Observe
- Request line, status line, headers, and body.
- Header/body separator.
- `Content-Length` and `Connection: close`.
- HTTP status is not the same kind of failure as TCP refused or timeout.

## Questions
1. How does HTTP define messages over a TCP byte stream?
2. How are headers and body separated?
3. Why does `Content-Length` matter?
4. Why is HTTP 500 not a TCP failure?
5. Why is HTTP 429 a capacity signal?

## Notes Checklist
- Paste one raw-ish HTTP request and response.
- Mark status line, headers, body, and Content-Length.
- Compare TCP failure with HTTP 500/429.
- Write one health-check interpretation rule.

## Work Mapping
This maps to API debugging, local model server calls, reverse proxy health checks, HTTP client behavior, and gateway error interpretation.

## Next Week
Week07 adds TLS and HTTPS failure modes.

