# Week 12 - Capstone: Network Design + Observable Service Path

## Goal
Combine the tutorial into two outcomes: run an observable client -> gateway -> model-like upstream path, and design a small network with subnets, names, ports, paths, access assumptions, and monitoring.

## Why this matters
The point is not memorizing protocols. The point is explaining a real service path, collecting evidence, and designing a small network you can operate.

## Where this fits
This is the final synthesis of Week00-Week11.

## Before You Run: Concepts
Read [Network Design](../../docs/concepts.md#network-design), [Observability](../../docs/concepts.md#observability), [Proxy and Gateway](../../docs/concepts.md#proxy-and-gateway), [HTTP Streaming](../../docs/concepts.md#http-streaming), and [Backpressure](../../docs/concepts.md#backpressure).

## Run
Part A, observable service path:

```powershell
python -m netlab server model --host 127.0.0.1 --port 8090 --max-concurrency 2 --token-delay 0.05 --tokens 8
python -m netlab proxy reverse --host 127.0.0.1 --port 8081 --upstream-host 127.0.0.1 --upstream-port 8090
python -m netlab client http --host 127.0.0.1 --port 8090 --path /generate
python -m netlab client stream-http --host 127.0.0.1 --port 8090 --path /stream --show-headers
python -m netlab client stream-http --host 127.0.0.1 --port 8081 --path /stream --show-headers
python -m netlab client load-http --host 127.0.0.1 --port 8090 --path /generate --requests 20 --concurrency 5
python labs/week12-capstone-network-design/experiment.py
```

Part B, design one network using [the template](../../docs/network-design-template.md):

- Home / personal lab network.
- Small AI/R&D lab network.
- Docker-based local AI service network.

Use the partial sample below as a depth reference. Your own answer can be shorter, but it should still name subnets, services, ports, paths, access assumptions, and checks.

### Partial Sample: Small AI/R&D Lab Network

Goal: one laptop and one workstation can use an internal model gateway; the GPU server, vector DB, and admin UI stay private; remote access requires authorized VPN.

Topology:

```text
internet
  -> home/office router
  -> 10.20.0.0/24 lab LAN
       -> laptop 10.20.0.50 DHCP
       -> workstation 10.20.0.60 DHCP
       -> gpu-server 10.20.0.10 static
            -> model-gateway :8080
            -> model-upstream :8090 internal-only
            -> vector-db :6333 internal-only
            -> admin-ui :3000 internal-only or VPN-only
       -> vpn users 10.30.0.0/24 routed to selected lab services
```

Subnet plan:

| Subnet | Purpose | Gateway | Notes |
| --- | --- | --- | --- |
| `10.20.0.0/24` | Lab LAN | `10.20.0.1` | Main trusted lab network |
| `10.30.0.0/24` | VPN clients | VPN gateway | Route only required lab prefixes |

Service and exposure sketch:

| Service | Address/name | Port | Exposure |
| --- | --- | --- | --- |
| model gateway | `model.lab.local` / `10.20.0.10` | `8080` | LAN and authorized VPN |
| model upstream | container/internal name | `8090` | gateway only |
| vector DB | `vectordb.internal` | `6333` | gateway/RAG service only |
| admin UI | `admin.lab.local` | `3000` | LAN or VPN-only |

Traffic paths:

- Laptop -> DNS `model.lab.local` -> route to `10.20.0.10` -> TCP `8080` -> HTTP -> gateway -> upstream model.
- Remote user -> VPN DNS policy -> VPN route -> `10.20.0.10:8080` -> gateway -> upstream model.
- Gateway -> vector DB stays internal; do not publish vector DB to the internet.

Failure checklist:

- DNS: does `model.lab.local` resolve differently on LAN and VPN?
- Route: does VPN add a route to `10.20.0.0/24` or only selected hosts?
- TCP: does `10.20.0.10:8080` connect, and do internal-only ports refuse/drop from clients?
- TLS/HTTP: if HTTPS is added, does certificate hostname match `model.lab.local`?
- Proxy/gateway: does gateway preserve streaming chunks and `X-Trace-Id`?
- Capacity: does overload return 429 instead of unbounded latency?
- Observability: collect gateway logs, upstream metrics, trace id, p95 latency, and one packet capture when behavior is unclear.

## Observe
- `X-Trace-Id` across service path where available.
- Direct generate response and direct stream timing.
- Gateway stream timing and whether chunks are buffered.
- Metrics and load-test result, including 429 backpressure.
- Your topology diagram, subnet plan, DNS names, port exposure table, traffic paths, failure checklist, and monitoring plan.

## Questions
1. Which evidence proves DNS, TCP, HTTP, gateway, upstream, and capacity behavior?
2. Where would you put a trace id?
3. Which services should be internal-only?
4. What would you monitor first?
5. Which failure checklist would you use before changing configs?
6. What tradeoff did your network design make?

## Notes Checklist
- Paste direct and gateway stream timing.
- Paste metrics and load result.
- Complete one network design template.
- Write a layer-by-layer failure checklist for your design.

## Work Mapping
This maps directly to personal labs, Docker AI stacks, model gateways, RAG services, remote access plans, and production-style debugging habits at small scale.

## Next Week
There is no next week. Re-run selected weeks when a real network problem appears, then update your notes with evidence.
