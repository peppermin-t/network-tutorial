# Python Network Lab Tutorial

## What this is
- A code-driven, lightweight computer networking tutorial.
- Built for engineers with programming background.
- Focused on practical layering, commands, packets, logs, and small-network design.
- Not a full textbook.
- Not network engineer certification training.
- Not a VPN/proxy bypass tutorial.

## Why this exists
This repo rebuilds practical networking foundations for general engineering and AI/LLM engineering work: local services, Docker stacks, RAG systems, model gateways, VPN remote access, deployment debugging, and observable service paths.

## Tutorial Path
- [Week00 - Orientation, Layering, and Tools](labs/week00-orientation/README.md)
- [Week01 - IP Addressing, Subnetting, and Routing](labs/week01-ip-routing-subnetting/README.md)
- [Week02 - Local Network Diagnostics](labs/week02-local-network-diagnostics/README.md)
- [Week03 - Sockets, TCP/UDP](labs/week03-sockets-tcp-udp/README.md)
- [Week04 - TCP Framing and Packet Thinking](labs/week04-tcp-framing-packet-thinking/README.md)
- [Week05 - DNS](labs/week05-dns/README.md)
- [Week06 - HTTP/1.1 Fundamentals](labs/week06-http/README.md)
- [Week07 - TLS and HTTPS](labs/week07-tls-https/README.md)
- [Week08 - Proxy, Gateway, Timeout, Retry](labs/week08-proxy-timeout-retry/README.md)
- [Week09 - RPC, WebSocket, and Streaming](labs/week09-rpc-websocket-streaming/README.md)
- [Week10 - Docker and Container Networking](labs/week10-container-networking/README.md)
- [Week11 - VPN and Remote Access Mental Model](labs/week11-vpn-remote-access/README.md)
- [Week12 - Capstone: Network Design + Observable Service Path](labs/week12-capstone-network-design/README.md)

## How to Study
1. Read the linked concepts.
2. Run the lab.
3. Observe command output, logs, headers, metrics, timing, and optional packets.
4. Answer the questions.
5. Write `notes.md`.
6. Finish with the Week12 design template.

## Quick Start
```powershell
python -m pip install -e .
python -m netlab doctor
python -m netlab path tutorial
python -m unittest discover -s tests -p "test_*.py"
```

## CLI Examples
```powershell
python -m netlab concept tcp
python -m netlab path ai
python -m netlab path design
python -m netlab server tcp-echo --host 127.0.0.1 --port 9001
python -m netlab client tcp-echo --host 127.0.0.1 --port 9001
python -m netlab client stream-http --host 127.0.0.1 --port 8090 --path /stream --show-headers
```

## Docs
- [Tutorial Map](docs/tutorial-map.md)
- [Minimal Networking Curriculum](docs/minimal-networking-curriculum.md)
- [Concepts](docs/concepts.md)
- [Glossary](docs/glossary.md)
- [Network Debug Playbook](docs/network-debug-playbook.md)
- [Network Design Template](docs/network-design-template.md)
- [Concept Map](docs/concept-map.md)
- [Further Reading](docs/further-reading.md)
