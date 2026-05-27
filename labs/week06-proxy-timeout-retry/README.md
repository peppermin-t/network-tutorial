# Week 06 - Proxy, Timeout, Retry

Focus: reverse proxy, upstream latency, retry policy, connection reuse thinking.

Run:

```powershell
$env:PYTHONPATH="src"
python -m netlab server http --host 127.0.0.1 --port 8080
python -m netlab proxy reverse --host 127.0.0.1 --port 8081 --upstream-host 127.0.0.1 --upstream-port 8080
python -m netlab client http --host 127.0.0.1 --port 8081 --path /via-proxy
python -m netlab server fault-http --host 127.0.0.1 --port 8082 --mode delay --delay 5
python -m netlab client http --host 127.0.0.1 --port 8082 --path /slow
python labs/week06-proxy-timeout-retry/experiment.py
```

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
