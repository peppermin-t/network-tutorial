# Week 01 - Socket Basics

Focus: TCP/UDP echo, host, port, blocking calls, connection lifecycle.

## Before You Run: Concepts

- `Host / Port`: the address and application endpoint you are trying to reach. See `docs/concepts.md#host--port`.
- `Socket`: the Python API for network I/O. See `docs/concepts.md#socket`.
- `TCP handshake`: what happens before TCP carries bytes. See `docs/concepts.md#tcp-handshake`.
- `UDP`: datagrams without TCP connection setup. See `docs/concepts.md#udp`.
- `Connection refused`: a reachable host rejected a closed TCP port. See `docs/concepts.md#connection-refused`.

## If You Are Confused

- If you do not understand why UDP has no `accept`, read `UDP` and `connection lifecycle`.
- If a closed port fails immediately, compare `connection refused` with `timeout`.
- If Docker or VPN later changes what `localhost` means, come back to `localhost / 127.0.0.1 / loopback`.

Run:

```powershell
$env:PYTHONPATH="src"
python -m netlab server tcp-echo --host 127.0.0.1 --port 9001
python -m netlab client tcp-echo --host 127.0.0.1 --port 9001 --message "hello tcp"
python -m netlab server udp-echo --host 127.0.0.1 --port 9002
python -m netlab client udp-echo --host 127.0.0.1 --port 9002 --message "hello udp"
```

Questions:

- TCP client exit 时 server 看到什么？
- UDP 为什么没有 accept？
- 同一个端口为什么不能同时被两个 server 监听？

Wireshark task:

- Capture `tcp port 9001` and observe SYN, SYN/ACK, ACK, payload, FIN.
- Capture `udp port 9002` and compare it with TCP: no handshake, no connection teardown.
- Write the packet sequence into `notes.md`.

## Systematic Template

- Concept Model: Connection. Application intent becomes a socket call to a host and port.
- Code Lab: Run TCP and UDP echo clients/servers.
- Failure Lab: Call a closed port and classify it with `python -m netlab fault classify connection-refused`.
- Wireshark Lab: Use `tcp.port == 9001` and `udp.port == 9002`.
- Work Mapping: Every cloud service, distributed worker, and local model server still starts with a reachable host/port.
