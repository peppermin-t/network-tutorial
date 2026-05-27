# Week 04 - DNS

Focus: DNS message format, A/AAAA/CNAME, UDP query, TTL cache.

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
