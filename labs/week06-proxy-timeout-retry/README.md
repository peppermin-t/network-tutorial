# Week 06 - Proxy, Timeout, Retry

Focus: reverse proxy, upstream latency, retry policy, connection reuse thinking.

## Before You Run: Concepts

- `Forward proxy vs reverse proxy`: which side the proxy represents. See `docs/concepts.md#forward-proxy-vs-reverse-proxy`.
- `Gateway`: the controlled hop between client and upstream. See `docs/concepts.md#gateway`.
- `Upstream timeout`: the gateway waited too long on a dependency. See `docs/concepts.md#upstream-timeout`.
- `Retry`: useful for transient failures but dangerous under overload. See `docs/concepts.md#retry`.
- `Retry storm`: retries multiplying load. See `docs/concepts.md#retry-storm`.

## If You Are Confused

- If a request reaches the gateway but not the upstream, compare downstream and upstream TCP connections.
- If retry seems always good, read `retry storm` and `backpressure`.
- If a model endpoint is slow, separate connect timeout, read timeout, upstream timeout, and gateway timeout.

Run:

```powershell
$env:PYTHONPATH="src"
python -m netlab server http --host 127.0.0.1 --port 8080
python -m netlab proxy reverse --host 127.0.0.1 --port 8081 --upstream-host 127.0.0.1 --upstream-port 8080
python -m netlab client http --host 127.0.0.1 --port 8081 --path /via-proxy
python -m netlab server fault-http --host 127.0.0.1 --port 8082 --mode delay --delay 5
python -m netlab server fault-http --host 127.0.0.1 --port 8082 --mode slow --delay 0.5
python -m netlab server fault-http --host 127.0.0.1 --port 8082 --mode close
python -m netlab server fault-http --host 127.0.0.1 --port 8082 --mode 500
python -m netlab client http --host 127.0.0.1 --port 8082 --path /slow
python labs/week06-proxy-timeout-retry/experiment.py
```

Failure modes to classify:

```powershell
python -m netlab fault classify connection-refused
python -m netlab fault classify read-timeout
python -m netlab fault classify upstream-slow
python -m netlab fault classify retry-storm
python -m netlab fault classify http-500
python -m netlab fault classify too-many-requests
```

Timeout mapping:

- Connect timeout: the TCP connection could not be established in budget.
- Read timeout: the connection exists, but response bytes did not arrive in budget.
- Upstream timeout: the gateway timed out while waiting for upstream.
- Gateway timeout: the client sees the gateway's failure response or connection close.
- Retry risk: retrying slow model generation can multiply GPU worker pressure.

Questions:

- timeout 应该设置在连接、读取还是整个请求？
- 哪些错误适合 retry？哪些不适合？
- proxy 日志里至少要有哪些字段？

Wireshark task:

- Capture `tcp port 8080 or tcp port 8081`.
- Compare client -> proxy and proxy -> upstream connections.
- Verify that reverse proxy creates a separate upstream TCP connection.

## Systematic Template

- Concept Model: Proxy/Gateway -> Failure Handling. A gateway owns both downstream and upstream behavior.
- Code Lab: Run reverse proxy and retry experiment.
- Failure Lab: Point proxy at a slow or closed upstream; classify with `python -m netlab fault classify upstream-slow`.
- Wireshark Lab: Compare downstream and upstream TCP connections.
- Work Mapping: API gateways, service clients, and model serving frontends all make timeout/retry decisions here.
