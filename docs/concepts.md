# Concepts

Each concept is intentionally small: mental model, why it matters, what to observe, common confusion, and related week.

## Orientation / Layering
- Mental model: application intent becomes DNS, route lookup, socket call, TCP/UDP, optional TLS, HTTP/proxy/gateway, upstream behavior, then logs/metrics/packets.
- Why it matters: it stops you from debugging every symptom at the application layer.
- Observe: command output, route/DNS state, client errors, HTTP status, trace ids, metrics, packet capture.
- Common confusion: treating "network issue" as one layer.
- Related week: Week00.

## IP Address
- Mental model: an IP address identifies an interface or endpoint at the network layer.
- Why it matters: every route, subnet, gateway, and service binding depends on it.
- Observe: `ipconfig /all`, `ip addr`, `ifconfig`.
- Common confusion: public/private address does not say whether a service is listening.
- Related week: Week01.

## Private IP Range
- Mental model: RFC1918-style private IPv4 ranges are used inside local networks and usually need NAT for internet access.
- Why it matters: home labs, Docker bridges, and VPNs mostly use private ranges.
- Observe: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`.
- Common confusion: private does not mean secure by itself.
- Related week: Week01.

## CIDR
- Mental model: `192.168.1.0/24` means the first 24 bits identify the network.
- Why it matters: CIDR controls subnet size and route specificity.
- Observe: network address, broadcast address, usable hosts.
- Common confusion: `/24` is not a port or host count.
- Related week: Week01.

## Subnet Mask
- Mental model: another way to express which IP bits are network bits.
- Why it matters: it determines local versus routed destinations.
- Observe: `/24` equals `255.255.255.0` for IPv4.
- Common confusion: mask and gateway are different roles.
- Related week: Week01.

## Network Address
- Mental model: the first address of an IPv4 subnet, identifying the subnet itself.
- Why it matters: it appears in route tables and subnet plans.
- Observe: `192.168.1.0` in `192.168.1.0/24`.
- Common confusion: it is usually not assigned to a normal host.
- Related week: Week01.

## Broadcast Address
- Mental model: the last IPv4 address in many subnets, used for broadcast delivery.
- Why it matters: it affects usable host count.
- Observe: `192.168.1.255` in `192.168.1.0/24`.
- Common confusion: IPv6 does not use broadcast the same way.
- Related week: Week01.

## Gateway
- Mental model: the next hop used to reach addresses outside the local subnet.
- Why it matters: wrong gateway means the path starts wrong.
- Observe: default gateway in OS network output.
- Common confusion: gateway forwards packets; DNS server answers names.
- Related week: Week01.

## Default Route
- Mental model: fallback route when no more-specific route matches.
- Why it matters: most internet traffic uses it.
- Observe: `0.0.0.0/0`, `default via`, or route print default entry.
- Common confusion: default route is not always the route for VPN/internal subnets.
- Related week: Week01.

## More-Specific Route
- Mental model: the route with the longest matching prefix wins.
- Why it matters: VPN and Docker often add specific routes that beat default route.
- Observe: route entries with narrower prefixes than `0.0.0.0/0`.
- Common confusion: metric matters after prefix specificity.
- Related week: Week01.

## DHCP
- Mental model: automatic assignment of IP settings.
- Why it matters: clients need IP, gateway, DNS server, and lease behavior.
- Observe: DHCP enabled and lease fields in OS output.
- Common confusion: DHCP is not DNS.
- Related week: Week01.

## Static IP
- Mental model: manually planned address assignment.
- Why it matters: servers, NAS, gateways, and lab infrastructure need stable addresses.
- Observe: address outside DHCP pool but inside subnet.
- Common confusion: static IP must still fit route/subnet/gateway plan.
- Related week: Week01.

## DNS Server vs Gateway
- Mental model: DNS server translates names; gateway forwards packets.
- Why it matters: both are often set by DHCP but solve different problems.
- Observe: resolver addresses and default gateway separately.
- Common confusion: `8.8.8.8` can be DNS server, not your gateway.
- Related week: Week01 and Week05.

## ARP
- Mental model: local IPv4 neighbor resolution from IP address to MAC address.
- Why it matters: it proves local link-layer neighbor knowledge, not HTTP success.
- Observe: `arp -a` or `ip neigh`.
- Common confusion: ARP is local subnet only.
- Related week: Week02.

## ICMP, Ping, and Traceroute
- Mental model: ICMP and TTL behavior can test reachability and path shape.
- Why it matters: it gives path evidence below TCP/HTTP.
- Observe: ping replies, loss, latency, traceroute hops.
- Common confusion: ping blocked does not prove HTTP blocked, and ping success does not prove HTTP works.
- Related week: Week02.

## NAT
- Mental model: a device rewrites addresses/ports so private hosts can share another address.
- Why it matters: it explains home internet access and why inbound access is special.
- Observe: private source inside, public source outside.
- Common confusion: NAT is not a firewall, though devices often combine them.
- Related week: Week02.

## Port Forwarding
- Mental model: explicit inbound mapping from an external port to an internal host/port.
- Why it matters: it exposes internal services and changes security assumptions.
- Observe: router/cloud rule maps external -> internal.
- Common confusion: forwarding a port does not secure the service.
- Related week: Week02 and Week12.

## Firewall / Security Group
- Mental model: policy deciding whether traffic is allowed, rejected, or dropped.
- Why it matters: it can mimic service failure.
- Observe: timeout/drop versus refused/reject signals where available.
- Common confusion: this tutorial observes policy symptoms; it does not change policy.
- Related week: Week02 and Week12.

## Closed, Filtered, Refused
- Mental model: closed/refused means a host responded that no service accepts the connection; filtered often means no useful reply.
- Why it matters: refused and timeout imply different next checks.
- Observe: client exception, timing, packet response if captured.
- Common confusion: HTTP 500 is not refused; TCP already worked.
- Related week: Week02 and Week03.

## Socket
- Mental model: OS API endpoint used by application code to send/receive network data.
- Why it matters: service code reaches the network through sockets.
- Observe: bind, listen, accept, connect, send, recv.
- Common confusion: socket is not the same as TCP; UDP uses sockets too.
- Related week: Week03.

## TCP
- Mental model: reliable ordered byte stream between endpoints.
- Why it matters: most APIs, HTTP, TLS, RPC, and proxies ride on it.
- Observe: handshake, retransmission, payload, close.
- Common confusion: TCP does not preserve application messages.
- Related week: Week03 and Week04.

## UDP
- Mental model: connectionless datagrams with message boundaries but no reliability guarantee.
- Why it matters: DNS commonly uses UDP; some real-time protocols use UDP.
- Observe: datagram send/receive, no handshake.
- Common confusion: UDP can be correct when the protocol handles loss/retry.
- Related week: Week03 and Week05.

## TCP Framing
- Mental model: applications define message boundaries over a byte stream.
- Why it matters: partial reads and sticky packets are normal.
- Observe: length-prefix, delimiter, HTTP headers/body.
- Common confusion: one send is not one recv.
- Related week: Week04.

## Packet Thinking
- Mental model: separate headers from payload at each layer.
- Why it matters: packet capture becomes readable.
- Observe: Ethernet/IP/TCP headers and application bytes.
- Common confusion: packet boundary and application message boundary are different.
- Related week: Week04.

## DNS
- Mental model: resolver asks for records such as A, AAAA, or CNAME.
- Why it matters: no address means no connection attempt to the intended service.
- Observe: answer, TTL, NXDOMAIN, timeout.
- Common confusion: DNS success does not prove TCP/TLS/HTTP success.
- Related week: Week05.

## HTTP
- Mental model: request/response protocol with start line, headers, body, and status.
- Why it matters: APIs and model services expose behavior through HTTP.
- Observe: method, path, status, headers, body, `Content-Length`, chunking.
- Common confusion: HTTP 500/429 are application/protocol outcomes, not TCP failures.
- Related week: Week06.

## TLS
- Mental model: encrypted session negotiated after TCP and before HTTPS data.
- Why it matters: certificate, hostname, SNI, and trust failures happen before HTTP status.
- Observe: certificate validation, cipher, SNI, ALPN.
- Common confusion: SNI is in TLS; Host header is in HTTP.
- Related week: Week07.

## Proxy and Gateway
- Mental model: an intermediary accepts downstream traffic and makes upstream requests.
- Why it matters: failures can occur at either leg or inside gateway policy.
- Observe: client->gateway and gateway->upstream connections, status, timeout, trace id.
- Common confusion: reverse proxy is not just a transparent pipe.
- Related week: Week08.

## Timeout
- Mental model: a deadline for connect, read, upstream work, or whole request.
- Why it matters: timeout location determines the next fix.
- Observe: connect timeout, read timeout, gateway timeout, total latency.
- Common confusion: increasing timeout can hide capacity problems.
- Related week: Week08.

## Retry
- Mental model: repeat a failed operation under a policy.
- Why it matters: retry helps transient errors but can amplify load.
- Observe: attempts, backoff, final result, upstream work duplication.
- Common confusion: retrying non-idempotent or slow work can be harmful.
- Related week: Week08.

## Backpressure
- Mental model: service rejects or slows callers when capacity is exhausted.
- Why it matters: AI/model systems need explicit overload behavior.
- Observe: HTTP 429, queue depth, p95 latency, failure rate.
- Common confusion: 429 is a capacity signal, not a network outage.
- Related week: Week08 and Week12.

## RPC
- Mental model: remote call pattern usually adding method, params, and request id over a transport.
- Why it matters: tool calls and internal services often look like RPC.
- Observe: method, params, id, result/error.
- Common confusion: RPC can use HTTP but is a different application abstraction.
- Related week: Week09.

## WebSocket
- Mental model: long-lived bidirectional message channel after an HTTP upgrade.
- Why it matters: interactive UIs and agents may need bidirectional updates.
- Observe: handshake, frame opcode, payload, connection lifetime.
- Common confusion: WebSocket is not the same as HTTP chunked streaming.
- Related week: Week09.

## HTTP Streaming
- Mental model: response body arrives progressively, often with chunked encoding.
- Why it matters: LLM token streaming depends on first bytes moving quickly.
- Observe: first byte latency, chunk timing, total latency.
- Common confusion: a proxy can buffer chunks and make streaming appear broken.
- Related week: Week09 and Week12.

## Docker Networking
- Mental model: containers have their own network namespaces and Compose DNS.
- Why it matters: localhost and ports mean different things inside containers.
- Observe: service names, host port mapping, container port, bridge network.
- Common confusion: `localhost` inside a container is not the host.
- Related week: Week10.

## VPN
- Mental model: virtual interface plus route table plus encrypted tunnel plus DNS policy.
- Why it matters: remote access changes paths and name resolution.
- Observe: route table, DNS servers, virtual adapters, full/split tunnel clues.
- Common confusion: VPN connected does not prove every internal service is reachable.
- Related week: Week11.

## Observability
- Mental model: combine logs, metrics, traces, command output, and packets.
- Why it matters: layer-aware evidence prevents guesswork.
- Observe: trace id, status, latency, p50/p95, packet filters.
- Common confusion: one signal rarely proves every layer.
- Related week: Week00 and Week12.

## Network Design
- Mental model: topology, subnets, names, ports, access boundaries, paths, and monitoring.
- Why it matters: a small network that is not written down becomes hard to debug.
- Observe: diagrams, subnet table, DNS plan, port exposure table, failure checklist.
- Common confusion: design is not only drawing devices; it includes operations and failure assumptions.
- Related week: Week12.
