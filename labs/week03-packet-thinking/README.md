# Week 03 - Packet Thinking

Focus: protocol headers, payload, offsets, byte order, parser failure modes.

Run:

```powershell
$env:PYTHONPATH="src"
python labs/week03-packet-thinking/experiment.py
```

Questions:

- Ethernet、IP、TCP headers 各自负责什么？
- 为什么网络字节序通常是 big-endian？
- parser 应该如何处理 truncated packet？

## Systematic Template

- Concept Model: Packet-Level Verification. This week exists to make captures readable.
- Code Lab: Parse a small synthetic Ethernet -> IPv4 -> TCP frame.
- Failure Lab: Truncate the byte array and observe parser failure.
- Wireshark Lab: Identify source/destination address, port, flags, and payload in a real capture.
- Work Mapping: You only need enough packet structure to verify where a cloud/distributed call failed.
