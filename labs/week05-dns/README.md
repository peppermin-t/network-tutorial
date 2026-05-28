# Week 05 - DNS

## Goal
Understand DNS query/answer behavior and why name resolution success is only the first step in a service request.

## Why this matters
Internal services, Docker Compose names, VPN domains, model gateways, and remote deployments often fail before TCP starts because the name did not resolve as expected.

## Where this fits
Week04 covered message parsing. DNS is the first application protocol in the request path and a preview of Docker/VPN naming behavior.

## Before You Run: Concepts
Read [DNS](../../docs/concepts.md#dns), [DNS Server vs Gateway](../../docs/concepts.md#dns-server-vs-gateway), [Timeout](../../docs/concepts.md#timeout), and [Docker Networking](../../docs/concepts.md#docker-networking).

## Run
```powershell
python labs/week05-dns/experiment.py
python -m netlab dns query example.com --type A
```

If public UDP DNS is blocked in your environment, record the timeout instead of changing system DNS.

## Observe
- Query bytes built by the lab.
- A/AAAA/CNAME answers and TTL values.
- Difference between NXDOMAIN and timeout.
- DNS success does not prove TCP, TLS, HTTP, or proxy success.

## Questions
1. What exactly does successful DNS resolution prove?
2. What does it not prove?
3. Why can TTL make service migration look random?
4. How are NXDOMAIN and timeout different?
5. Why do Docker and VPN often change DNS behavior?

## Notes Checklist
- Query at least one A record and one AAAA or CNAME when available.
- Record answer TTLs.
- Write one example where DNS succeeds but HTTP still fails.
- Write one Docker/VPN DNS hypothesis for later weeks.

## Work Mapping
This maps to internal API names, model endpoint names, service discovery, stale DNS caches, and VPN-only domains.

## Next Week
Week06 shows how HTTP defines requests and responses on top of TCP byte streams.

