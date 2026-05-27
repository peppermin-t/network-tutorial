# Week 08 - RPC and WebSocket

Focus: JSON-RPC over request/response, WebSocket handshake, frame boundary, heartbeat.

Run:

```powershell
$env:PYTHONPATH="src"
python labs/week08-rpc-websocket/experiment.py
python -m netlab server websocket --host 127.0.0.1 --port 8765
python -m netlab client websocket --host 127.0.0.1 --port 8765 --message "hello ws"
```

Questions:

- RPC 的 method、params、id 分别解决什么问题？
- WebSocket 为什么先发 HTTP Upgrade？
- 长连接里的心跳和业务消息如何区分？

Wireshark task:

- Capture `tcp port 8765`.
- Use display filter `http or websocket`.
- Observe the HTTP Upgrade handshake, then compare WebSocket frames with JSON-RPC request/response.

## Systematic Template

- Concept Model: Application Protocol -> Long-Lived Communication. RPC and WebSocket define message identity and streaming boundaries.
- Code Lab: Run JSON-RPC and WebSocket echo.
- Failure Lab: Close the WebSocket server during a client call; classify with `python -m netlab fault classify server-close`.
- Wireshark Lab: Use `http or websocket` and inspect Upgrade plus frames.
- Work Mapping: Streaming dashboards, agents, and token streams need long-lived connection discipline.
