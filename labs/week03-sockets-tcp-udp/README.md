# Week 03 - Sockets, TCP/UDP, Host/Port, Connection Lifecycle

## Goal
Use sockets to connect application code to TCP and UDP, and understand host, port, bind, listen, accept, connect, and connection lifecycle.

## Why this matters
Most service deployment, local model serving, gateway, and agent tooling problems eventually reduce to "which process is listening on which host/port, and from where?"

## Where this fits
Week01/02 explain where packets can go. Week03 shows how code asks the OS to send them.

## Before You Run: Concepts
Read [Socket](../../docs/concepts.md#socket), [TCP](../../docs/concepts.md#tcp), [UDP](../../docs/concepts.md#udp), and [Closed, Filtered, Refused](../../docs/concepts.md#closed-filtered-refused).

## Run
Terminal 1:

```powershell
python -m netlab server tcp-echo --host 127.0.0.1 --port 9001
```

Terminal 2:

```powershell
python -m netlab client tcp-echo --host 127.0.0.1 --port 9001 --message "hello tcp"
python -m netlab server udp-echo --host 127.0.0.1 --port 9002
```

Terminal 3:

```powershell
python -m netlab client udp-echo --host 127.0.0.1 --port 9002 --message "hello udp"
python labs/week03-sockets-tcp-udp/experiment.py
```

## Observe
- Server logs: bind/listen/receive/send behavior.
- Client output: echoed bytes.
- TCP failure if the server is not running: usually refused.
- UDP has no connection handshake.
- Optional packet capture: TCP handshake for TCP echo; UDP datagrams for UDP echo.

## Questions
1. What does a socket identify in your program?
2. What is the difference between bind and connect?
3. What changes between TCP and UDP echo behavior?
4. Why does connection refused usually mean a host replied?
5. How did Week01 route facts decide the path before the socket call?

## Notes Checklist
- Commands used for TCP and UDP.
- Observed success and failure outputs.
- One Wireshark/TShark filter you tried or would try.
- A short lifecycle summary for TCP and UDP.

## Work Mapping
This maps to local services, model servers, dev servers, bind address mistakes, port collisions, and client libraries that hide socket behavior.

## Next Week
Week04 explains why TCP delivers bytes, not complete application messages.

