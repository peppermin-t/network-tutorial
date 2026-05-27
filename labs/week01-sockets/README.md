# Week 01 - Socket Basics

Focus: TCP/UDP echo, host, port, blocking calls, connection lifecycle.

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
