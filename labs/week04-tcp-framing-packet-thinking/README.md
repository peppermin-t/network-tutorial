# Week 04 - TCP Framing and Packet Thinking

## Goal
Understand that TCP is a byte stream, UDP preserves datagram boundaries, and application protocols need explicit framing.

## Why this matters
Sticky packets, partial reads, streaming bugs, and broken protocol parsers all come from assuming one `send` equals one `recv`.

## Where this fits
Week03 introduced sockets. Week04 builds the protocol thinking required for DNS, HTTP, RPC, and streaming.

## Before You Run: Concepts
Read [TCP Framing](../../docs/concepts.md#tcp-framing), [Packet Thinking](../../docs/concepts.md#packet-thinking), [TCP](../../docs/concepts.md#tcp), and [UDP](../../docs/concepts.md#udp).

## Run
```powershell
python labs/week04-tcp-framing-packet-thinking/experiment.py
```

## Observe
- A length-prefixed protocol receiving partial bytes and emitting messages only when complete.
- Two encoded messages arriving through arbitrary feed boundaries.
- Ethernet/IP/TCP header fields separated from payload.
- Why packet capture evidence and application message evidence are related but not identical.

## Questions
1. Why does TCP not guarantee one send maps to one recv?
2. Why does an application protocol need message boundaries?
3. What are the tradeoffs between length-prefix and delimiter framing?
4. What do heartbeat and timeout solve?
5. Which fields are header, and which bytes are payload?

## Notes Checklist
- Draw a byte stream with two messages split across three reads.
- Compare length-prefix and delimiter framing.
- Record one example of partial read and sticky packet thinking.
- Write your rule for when to add timeout and heartbeat.

## Work Mapping
This maps to custom protocols, log streaming, model token streams, websocket frames, and any TCP service that sends multiple logical messages.

## Next Week
Week05 moves from raw framing to name resolution with DNS messages and resolver behavior.

