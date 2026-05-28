# Minimal Networking Curriculum

This tutorial covers the smallest practical network backbone an engineer needs to stop being blocked by everyday network failures.

## In Scope
- Layering: application intent to DNS, route, socket, transport, TLS, HTTP, gateway, upstream, observability.
- IP/subnet/routing: address, private range, CIDR, subnet mask, gateway, default route, more-specific route, DHCP, static IP.
- Local diagnostics: ARP, ICMP, ping, traceroute, NAT, port forwarding, firewall/security group, refused versus timeout.
- Transport: TCP, UDP, socket lifecycle, byte streams, datagrams.
- DNS: A/AAAA/CNAME, resolver, TTL, NXDOMAIN, timeout.
- HTTP: request/response, headers/body, Content-Length, status, chunked introduction.
- TLS: HTTPS, certificate validation, trust, hostname match, SNI, ALPN.
- Proxy/gateway: forward/reverse mental model, two TCP legs, timeout, retry, backpressure.
- RPC/WebSocket/streaming: request id, long-lived connection, first byte latency, token streaming.
- Docker networking: namespace, bridge, service-name DNS, host/container ports.
- VPN: virtual interface, route table, encrypted tunnel, DNS policy, full/split tunnel.
- Observability: trace id, metrics, packet capture, timing, layered evidence.
- Capstone design: topology, subnet plan, DNS naming, port exposure, traffic paths, failure checklist.

## Out of Scope
- BGP/OSPF routing depth.
- Enterprise VLAN/STP deep dive.
- Data center networking.
- Kubernetes CNI deep dive.
- HTTP/3/QUIC deep dive.
- Production firewall policy engineering.
- Offensive security, scanning, intrusion, anonymity, censorship bypass, or commercial VPN node configuration.
