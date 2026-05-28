# Week 02 - Local Network Diagnostics: ARP, ICMP, NAT, Firewall

## Goal
Learn why "the network is reachable" and "the application works" are different claims.

## Why this matters
Ping, ARP, traceroute, refused connections, timeouts, NAT, and firewall policy each prove different things. This week prevents false conclusions.

## Where this fits
Week01 described addresses and routes. Week02 adds local diagnostic signals before Week03 opens sockets.

## Before You Run: Concepts
Read [ARP](../../docs/concepts.md#arp), [ICMP, Ping, and Traceroute](../../docs/concepts.md#icmp-ping-and-traceroute), [NAT](../../docs/concepts.md#nat), [Port Forwarding](../../docs/concepts.md#port-forwarding), [Firewall / Security Group](../../docs/concepts.md#firewall--security-group), and [Closed, Filtered, Refused](../../docs/concepts.md#closed-filtered-refused).

## Run
```powershell
python labs/week02-local-network-diagnostics/experiment.py
```

Optional manual traceroute from the printed command list is allowed, but keep it read-only.

## Observe
- ARP or neighbor table entries: local IP-to-MAC mappings.
- Loopback ping result: ICMP to your own machine.
- Whether traceroute is skipped by default and why it is only path evidence.
- The distinction between no route, timeout, refused, and HTTP failure.

## Questions
1. Why does ping success not prove HTTP success?
2. What is the difference between connection refused and timeout?
3. How does NAT let private hosts initiate public connections?
4. Why is port forwarding a security boundary decision?
5. How can you distinguish firewall/security-group blocking from an app that is not listening?

## Notes Checklist
- Paste ARP/neighbor output.
- Write one example of each: ICMP success, TCP refused, TCP timeout, HTTP error.
- Draw the NAT mental model for laptop -> router -> internet.
- List what you are not allowed to change in this tutorial.

## Work Mapping
This maps to debugging "server is down" reports, cloud security group mistakes, home router port forwarding confusion, and VPN routes that exist but still cannot reach a service.

## Next Week
Week03 opens TCP and UDP sockets so you can see application code enter the network stack.

