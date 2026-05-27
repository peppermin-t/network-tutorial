# Wireshark and TShark Workflow

Wireshark is optional, but strongly recommended after Week 1. The code labs teach how to build network behavior; packet capture teaches how to verify what actually crossed the network boundary.

Install Wireshark from the official site and include the command-line tool TShark during installation. After installation, reopen PowerShell and verify:

```powershell
tshark --version
python -m netlab capture status
```

If `tshark` is not found, add the Wireshark install directory to `PATH`.

## Core Loop

Use this loop for every lab:

1. Start the server.
2. Start a capture with a narrow capture filter.
3. Run the client or experiment.
4. Stop capture.
5. Open the `.pcapng` in Wireshark or summarize it with TShark.
6. Write the observation into that week’s `notes.md`.

## Useful Filters

Capture filters decide what gets written:

```text
tcp port 9001
udp port 9002
tcp port 8080
tcp port 8765
udp port 53
host 127.0.0.1
```

Display filters decide what Wireshark shows:

```text
tcp.port == 9001
udp.port == 9002
http
dns
tls
websocket
tcp.analysis.retransmission
tcp.flags.syn == 1
```

## CLI Helpers

Check installation:

```powershell
$env:PYTHONPATH="src"
python -m netlab capture status
```

Generate a capture command:

```powershell
python -m netlab capture command --interface "Adapter for loopback traffic capture" --output captures/week05-http.pcapng --filter "tcp port 8080" --packets 20
```

Read selected fields from an existing capture:

```powershell
python -m netlab capture read captures/week05-http.pcapng --display-filter http --field frame.time_relative --field ip.src --field tcp.srcport --field http.request.method
```

## Windows Notes

On Windows, loopback capture usually requires the Npcap loopback adapter. In Wireshark, look for an interface named similar to `Adapter for loopback traffic capture`.

If loopback capture is awkward, use Docker labs or capture traffic to a real remote host such as DNS or HTTPS. Keep filters narrow so the capture is readable.
