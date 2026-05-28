# Network Debug Playbook

Use this as a first-pass triage table. The goal is to identify the likely layer before changing code or configuration.

| Symptom | Likely Layer | First Commands | Wireshark Filter | Related Lab | AI/LLM Engineering Mapping |
| ---- | ---- | ---- | ---- | ---- | ---- |
| Domain name does not resolve | DNS | `python -m netlab dns query example.com --type A`; `nslookup example.com` or `Resolve-DnsName example.com` | `dns` | Week04 | Internal model/service name cannot be found. |
| DNS timeout | DNS / Routing | Try a known resolver, note the DNS server, compare VPN on/off snapshots | `dns and not dns.flags.response` | Week04, Week11 | VPN or firewall path blocks resolver reachability. |
| NXDOMAIN | DNS | Query the exact name and check spelling/search domain | `dns.flags.rcode == 3` | Week04 | Wrong private DNS zone or missing internal record. |
| Connection refused | TCP | Confirm server is running; retry the exact host/port; `python -m netlab fault classify connection-refused` | `tcp.flags.reset == 1` | Week01, Week06 | Gateway/model process not listening or wrong port mapping. |
| Connection timeout | TCP / Routing | Check DNS result, route snapshot, and whether any SYN response appears | `tcp.analysis.retransmission or tcp.flags.syn == 1` | Week01, Week11 | No route to internal service, security group, or wrong tunnel path. |
| Read timeout | TCP / Application | Confirm connection opens, then check server logs and response timing | `tcp` | Week02, Week06 | Model accepted request but did not return bytes before deadline. |
| TLS certificate verify failed | TLS | `python -m netlab client https --host example.com`; inspect hostname and CA expectation | `tls` | Week07 | Private CA or SNI/hostname mismatch at model gateway. |
| HTTP 500 | HTTP / Application | Read status and body; run `python -m netlab fault classify http-500` | `http.response.code == 500` | Week05, Week06 | Upstream application/model worker threw an error. |
| HTTP 429 | Capacity / Backpressure | Run load summary; inspect accepted/rejected metrics | `http.response.code == 429` | Week10 | GPU worker queue or gateway rate limit is full. |
| Streaming response arrives all at once | Proxy / HTTP Streaming | Compare direct upstream `/stream` with gateway `/stream`; look at first byte timing | `http or tcp` | Week10 | Proxy buffering broke token streaming. |
| Docker container cannot reach `localhost` service | Docker Network | Check whether service is on host, same container, or another Compose service | `tcp` on published port | Week09 | Agent container points to itself instead of host/model container. |
| Host can reach service, container cannot | Docker Network / Routing | Compare host port mapping with Compose service name and container port | `tcp` plus container logs | Week09 | Wrong address scope between host and bridge network. |
| Docker service name does not resolve | Docker DNS | Run from inside the Compose network; check service name spelling | `dns` if captured in namespace | Week09 | Gateway container cannot resolve model container. |
| VPN connected but internal network unreachable | Routing / VPN | Before/after route table; check default route and specific internal routes | Usually outer tunnel traffic on physical NIC | Week11 | Authorized tunnel lacks route to lab/model subnet. |
| VPN connected but public internet behaves oddly | Routing / DNS / Policy | Compare default route, DNS server, and traceroute before/after VPN | Outer tunnel traffic or direct TCP | Week11 | Full tunnel egress policy affects public APIs/package downloads. |
| VPN connected but DNS server did not change | DNS Policy | Compare DNS server output and internal name resolution before/after VPN | `dns` | Week11 | Internal model names still query public/local resolver. |
| Ping works but HTTP stalls | Routing / MTU / TLS / HTTP | First verify DNS, TCP connect, TLS, then note route/VPN changes; treat MTU/MSS as a later hypothesis | `tcp.analysis.retransmission` | Week07, Week11 | Large TLS/HTTP payloads over VPN may expose path MTU issues. |

## Layering Rule

Classify in this order before changing anything: DNS -> routing -> TCP -> TLS -> HTTP -> proxy/gateway -> capacity -> application. A later-layer error usually means earlier layers worked enough to reach it.
