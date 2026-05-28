# Network Debug Playbook

Use this as `symptom -> likely layer -> first check -> related week`.

| Symptom | Likely layer | First check | Related week |
| --- | --- | --- | --- |
| Cannot resolve name | DNS | Query the name; confirm resolver/DNS server | Week05 |
| DNS timeout | DNS/path/firewall | Compare DNS server reachability and VPN/Docker policy | Week05, Week11 |
| NXDOMAIN | DNS data | Check spelling, search domain, intended internal zone | Week05 |
| No route / wrong route | Routing | Inspect route table and default/more-specific routes | Week01, Week11 |
| Ping works but HTTP fails | TCP/TLS/HTTP/app | Try TCP/HTTP client; check port and status | Week02, Week06 |
| Connection refused | TCP/listener | Confirm server process bind host/port | Week03 |
| Connection timeout | Route/firewall/drop | Check route, security group/firewall symptoms, wrong address | Week02 |
| TLS certificate verify failed | TLS | Check hostname, CA trust, SNI, certificate chain | Week07 |
| HTTP 500 | Application/upstream | Read response body/logs/trace id | Week06, Week08 |
| HTTP 429 | Capacity/backpressure | Check concurrency, load result, retry policy | Week08, Week12 |
| Streaming buffered | Proxy/gateway | Compare direct stream vs gateway stream chunk timing | Week09, Week12 |
| Docker localhost confusion | Docker namespace | Replace container localhost with service name or host gateway plan | Week10 |
| Docker service name failure | Docker DNS/network | Confirm services share Compose network | Week10 |
| VPN connected but internal service unreachable | Route/DNS/firewall/TLS | Compare before/after routes, DNS, endpoint name, certificate | Week11 |
| VPN connected but DNS unchanged | VPN DNS policy | Check resolver configuration after connect | Week11 |
| MTU/MSS suspected | Path/tunnel edge | Consider only after DNS/TCP/TLS basics; look for stalls/fragmentation symptoms | Week11 |

## Layer Order
1. Name: does the name resolve to the expected address?
2. Route: would packets go through the expected interface/gateway/tunnel?
3. Transport: does TCP connect or UDP exchange data?
4. TLS: does certificate and hostname validation succeed?
5. HTTP/RPC: is the protocol response meaningful?
6. Gateway: is the proxy changing status, timeout, headers, or streaming?
7. Capacity: are 429, p95 latency, queue, or retries the real issue?
8. Application: does upstream logic return an error after all network layers work?
