# Week 09 - RPC, WebSocket, and Streaming

## Goal
Compare request/response HTTP, RPC, WebSocket, and HTTP streaming, with attention to request ids, long-lived connections, first byte latency, total latency, and proxy buffering.

## Why this matters
LLM token streaming, agent tool calls, dashboards, chat UIs, and event feeds all depend on choosing the right communication pattern.

## Where this fits
Week08 introduced gateway behavior. Week09 focuses on higher-level application communication styles before Docker networking.

## Before You Run: Concepts
Read [RPC](../../docs/concepts.md#rpc), [WebSocket](../../docs/concepts.md#websocket), [HTTP Streaming](../../docs/concepts.md#http-streaming), [Proxy and Gateway](../../docs/concepts.md#proxy-and-gateway), and [Observability](../../docs/concepts.md#observability).

## Run
```powershell
python labs/week09-rpc-websocket-streaming/experiment.py
```

Optional WebSocket echo:

```powershell
python -m netlab server websocket --host 127.0.0.1 --port 8765
python -m netlab client websocket --host 127.0.0.1 --port 8765 --message "hello websocket"
```

Optional streaming client against Week12 model server:

```powershell
python -m netlab client stream-http --host 127.0.0.1 --port 8090 --path /stream --show-headers
```

## Observe
- JSON-RPC request id and response.
- WebSocket frame opcode and payload.
- Long-lived connection behavior.
- First byte latency versus total latency for streaming.
- Whether chunks arrive progressively or all at once.

## Questions
1. When is plain HTTP request/response enough?
2. What does RPC add beyond HTTP transport?
3. When does WebSocket fit better than repeated HTTP requests?
4. Why are first byte latency and total latency different?
5. Why can proxy buffering break token streaming?

## Notes Checklist
- Compare HTTP, RPC, WebSocket, and streaming in one table.
- Record first byte and total latency from one stream.
- Explain request id in JSON-RPC.
- Write a proxy buffering symptom.

## Work Mapping
This maps to LLM streaming APIs, tool-call RPC, agent backends, browser dashboards, chat systems, and gateway configuration.

## Next Week
Week10 moves these services into containers and changes the meaning of localhost and DNS names.

