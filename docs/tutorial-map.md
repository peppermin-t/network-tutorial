# Tutorial Map

## Overview

| Week | Goal | Concepts | Experiment | Afterward you can |
| --- | --- | --- | --- | --- |
| Week00 | Build the map and tooling workflow | layering, observability | doctor/path/capture status | choose a likely layer before debugging |
| Week01 | Read IP, subnet, gateway, route, DNS facts | IP, CIDR, gateway, route, DHCP | local read-only snapshot + CIDR helper | explain a route table and plan a subnet |
| Week02 | Separate reachability from application success | ARP, ICMP, NAT, firewall | ARP/ping/traceroute suggestions | distinguish refused, timeout, HTTP error |
| Week03 | Use sockets for TCP and UDP | socket, TCP, UDP | echo clients/servers | reason about host/port and bind/connect |
| Week04 | Understand framing and packet structure | TCP framing, packet thinking | length-prefix + packet parser | avoid send/recv boundary mistakes |
| Week05 | Resolve names and interpret DNS outcomes | DNS, TTL, NXDOMAIN, timeout | DNS query builder/client | know what DNS proves and does not prove |
| Week06 | Read HTTP/1.1 messages | HTTP, Content-Length | HTTP parser/client/server | separate HTTP status from transport failure |
| Week07 | Add TLS/HTTPS failure modes | TLS, CA, SNI, ALPN | Python SSL client | separate TCP, TLS, and HTTP failures |
| Week08 | Reason through gateways and retries | proxy, timeout, retry, backpressure | retry/fault classifier/proxy | diagnose gateway and capacity symptoms |
| Week09 | Compare RPC, WebSocket, streaming | RPC, WebSocket, streaming | JSON-RPC/WebSocket/stream client | choose a communication pattern |
| Week10 | Understand container paths | Docker networking, Compose DNS | Compose gateway/upstream | avoid localhost and port mapping errors |
| Week11 | Model VPN remote access | VPN, routes, DNS policy | read-only before/after snapshot | explain full/split tunnel behavior |
| Week12 | Design and observe a service path | design, observability, streaming | model-like upstream + design template | produce a small network design and failure checklist |

## Recommended Pace
- Fast pass: one week per day, run only core commands, write short notes.
- Careful pass: two or three sessions per week: concepts, lab, notes.
- Debug-driven pass: jump to the symptom in `network-debug-playbook.md`, then return to the related week.

## Study Loop
1. Read the week README and linked concepts.
2. Run the experiment.
3. Observe output, logs, headers, timing, metrics, and optional packet capture.
4. Answer the week questions.
5. Update `notes.md`.
6. Reuse the playbook when a real failure appears.
