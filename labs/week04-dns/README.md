# Week 04 - DNS

Focus: DNS message format, A/AAAA/CNAME, UDP query, TTL cache.

## Before You Run: Concepts

- `DNS query`: name resolution before connection. See `../../docs/concepts.md#dns-query`.
- `A / AAAA / CNAME`: common record types. See `../../docs/concepts.md#a--aaaa--cname`.
- `TTL`: how long a DNS answer can be cached. See `../../docs/concepts.md#ttl`.
- `DNS timeout vs NXDOMAIN`: no answer in time versus name does not exist. See `../../docs/concepts.md#dns-timeout-vs-nxdomain`.
- `Docker Compose service name DNS`: the container version of service discovery. See `../../docs/concepts.md#docker-compose-service-name-dns`.

## If You Are Confused

- If a name resolves but connection fails, move from DNS to TCP/routing.
- If VPN changes internal names, read `DNS policy`, `split tunnel`, and `DNS leak`.

Run:

```powershell
$env:PYTHONPATH="src"
python -m netlab dns query example.com --type A --server 8.8.8.8
python labs/week04-dns/experiment.py
```

Questions:

- TTL cache 命中和过期分别会发生什么？
- NXDOMAIN、timeout、SERVFAIL 对调用方有什么区别？
- 公司内网 DNS 问题应该先看哪些信号？

Wireshark task:

- Capture `udp port 53` while running the DNS query.
- Use display filter `dns`.
- Find transaction id, query type, answer TTL, and response code.

## Systematic Template

- Concept Model: Name Resolution. A service name must become an address before connection.
- Code Lab: Build and parse DNS messages; run a UDP DNS query.
- Failure Lab: Use an unreachable DNS server or bad name; classify with `python -m netlab fault classify dns-timeout` or `dns-nxdomain`.
- Wireshark Lab: Use `dns` and inspect transaction id, rcode, answer, and TTL.
- Work Mapping: Docker service names, cloud private DNS, and internal model endpoints all depend on name resolution.
