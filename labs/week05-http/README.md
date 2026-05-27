# Week 05 - HTTP/1.1

Focus: request line, status line, headers, body, content-length, chunked response.

Run:

```powershell
$env:PYTHONPATH="src"
python -m netlab server http --host 127.0.0.1 --port 8080
python -m netlab client http --host 127.0.0.1 --port 8080 --path /hello
python labs/week05-http/experiment.py
```

Questions:

- HTTP parser 怎么知道 header 结束？
- body 长度由谁决定？
- keep-alive 为什么会影响 server 读取策略？

Wireshark task:

- Capture `tcp port 8080` while calling the local HTTP server.
- Use display filter `http`.
- Identify request line, status line, `Content-Length`, and payload bytes.

## Systematic Template

- Concept Model: Application Protocol. HTTP turns byte streams into requests, headers, status, and body.
- Code Lab: Run the minimal HTTP server/client and parse headers/body.
- Failure Lab: Run `python -m netlab server fault-http --mode 500 --port 8082` and classify with `python -m netlab fault classify http-500`.
- Wireshark Lab: Use `http` and inspect request line, status line, and body.
- Work Mapping: Most cloud APIs and local inference endpoints expose this layer first.
