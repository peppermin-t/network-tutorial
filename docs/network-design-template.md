# Network Design Template

## Goal
What should this network make possible?

## Topology
Draw devices/services and links. Include router, clients, servers, containers, VPN users, and gateways.

```text

```

## Subnet Plan
| Subnet | Purpose | Gateway | Notes |
| --- | --- | --- | --- |
| | | | |

## DHCP / Static Assignment
| Range / Address | Owner | Dynamic or static | Reason |
| --- | --- | --- | --- |
| | | | |

## DNS Naming
| Name | Target | Resolver/source | Notes |
| --- | --- | --- | --- |
| | | | |

## Service Table
| Service | Host/container | Listen address | Port | Protocol |
| --- | --- | --- | --- | --- |
| | | | | |

## Port Exposure Table
| Port | Exposed to | Internal target | Why exposed | Risk |
| --- | --- | --- | --- | --- |
| | | | | |

## Traffic Paths
Write paths such as `laptop -> gateway -> model upstream` and mark DNS, route, TCP, TLS, HTTP, proxy, and upstream.

## Security / Access Assumptions
Who can reach what? Which services are internal-only? What requires VPN?

## Failure Checklist
- DNS:
- Route:
- TCP:
- TLS:
- HTTP/RPC:
- Proxy/gateway:
- Capacity:
- Application:

## Observability Plan
What logs, metrics, traces, packet captures, and command snapshots would you collect?

## Tradeoffs
What did you keep simple, and what risk did that accept?
