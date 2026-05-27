# Week 02 - TCP Byte Stream vs UDP Datagram

Focus: length-prefixed messages, partial reads, sticky packets, heartbeat, timeout.

Run:

```powershell
$env:PYTHONPATH="src"
python labs/week02-tcp-udp/experiment.py
```

Questions:

- 为什么 TCP 需要应用层 framing？
- `feed()` 为什么可能返回 0、1 或多个消息？
- UDP 一次 `recvfrom` 和一次 `sendto` 的边界关系是什么？

Wireshark task:

- Capture a TCP echo call and inspect whether one application message maps cleanly to one TCP segment.
- Use display filter `tcp.port == 9001`.
- Record whether packet boundaries and application message boundaries are the same.

## Systematic Template

- Concept Model: Connection -> Application Protocol. TCP provides bytes, not messages.
- Code Lab: Feed split length-prefixed frames and observe when complete messages appear.
- Failure Lab: Send partial frames or set a short read timeout; classify with `python -m netlab fault classify read-timeout`.
- Wireshark Lab: Compare application message boundaries with TCP segment boundaries.
- Work Mapping: Streaming APIs and model token output need explicit framing or protocol rules.
