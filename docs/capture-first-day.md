# First Day With Wireshark

This is the recommended first-day path after installing Wireshark and TShark.

## 0. Verify

```powershell
$env:PYTHONPATH="src"
python -m netlab capture status
```

If unavailable, reopen PowerShell. If it still fails, add the Wireshark install directory to `PATH`.

On Windows loopback traffic, select the Npcap loopback adapter in Wireshark. Its name is usually similar to `Adapter for loopback traffic capture`.

## 1. TCP Handshake

Terminal 1:

```powershell
$env:PYTHONPATH="src"
python -m netlab server tcp-echo --host 127.0.0.1 --port 9001
```

Wireshark capture filter:

```text
tcp port 9001
```

Terminal 2:

```powershell
python -m netlab client tcp-echo --host 127.0.0.1 --port 9001 --message "hello tcp"
```

Display filter:

```text
tcp.port == 9001
```

Observe: SYN, SYN/ACK, ACK, payload, FIN/ACK.

## 2. UDP Has No Connection

Terminal 1:

```powershell
python -m netlab server udp-echo --host 127.0.0.1 --port 9002
```

Capture filter:

```text
udp port 9002
```

Terminal 2:

```powershell
python -m netlab client udp-echo --host 127.0.0.1 --port 9002 --message "hello udp"
```

Observe: one datagram out, one datagram back, no handshake.

## 3. DNS

Capture filter:

```text
udp port 53
```

Command:

```powershell
python -m netlab dns query example.com --type A --server 8.8.8.8
```

Display filter:

```text
dns
```

Observe: transaction id, query type, response code, answer TTL.

## 4. HTTP

Terminal 1:

```powershell
python -m netlab server http --host 127.0.0.1 --port 8080
```

Capture filter:

```text
tcp port 8080
```

Terminal 2:

```powershell
python -m netlab client http --host 127.0.0.1 --port 8080 --path /hello
```

Display filter:

```text
http
```

Observe: request line, response status, headers, body.

## 5. Proxy Path

Terminal 1:

```powershell
python -m netlab server http --host 127.0.0.1 --port 8080
```

Terminal 2:

```powershell
python -m netlab proxy reverse --host 127.0.0.1 --port 8081 --upstream-host 127.0.0.1 --upstream-port 8080
```

Capture filter:

```text
tcp port 8080 or tcp port 8081
```

Terminal 3:

```powershell
python -m netlab client http --host 127.0.0.1 --port 8081 --path /via-proxy
```

Observe: client-to-proxy and proxy-to-upstream are two separate TCP connections.

## What To Write In Notes

For each capture, write:

- command used
- capture filter
- display filter
- packet sequence
- one concept the capture made concrete
- one question to investigate later
