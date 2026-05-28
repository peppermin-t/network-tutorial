# Week 01 - IP Addressing, Subnetting, and Routing

## Goal
Understand the local addressing and path-selection facts that every higher-level network problem depends on.

## Why this matters
If you cannot read IP, CIDR, gateway, DNS server, and route table output, Docker, VPN, proxy, and service deployment problems become guesswork.

## Where this fits
Week00 gave the map. This week covers the network layer substrate before Week02 local diagnostics and Week03 sockets.

## Before You Run: Concepts
Read [IP Address](../../docs/concepts.md#ip-address), [Private IP Range](../../docs/concepts.md#private-ip-range), [CIDR](../../docs/concepts.md#cidr), [Subnet Mask](../../docs/concepts.md#subnet-mask), [Gateway](../../docs/concepts.md#gateway), [Default Route](../../docs/concepts.md#default-route), [More-Specific Route](../../docs/concepts.md#more-specific-route), [DHCP](../../docs/concepts.md#dhcp), [Static IP](../../docs/concepts.md#static-ip), and [DNS Server vs Gateway](../../docs/concepts.md#dns-server-vs-gateway).

## Run
```powershell
python labs/week01-ip-routing-subnetting/experiment.py
```

Optional CIDR variations:

```powershell
python -c "from netlab.local.subnet import format_cidr_report; print(format_cidr_report('10.20.0.0/20'))"
```

## Observe
- Interface IP addresses and whether they are private, loopback, or public.
- Default gateway and default route.
- More-specific routes that would beat the default route.
- DNS server addresses; do not confuse them with the gateway.
- CIDR report: network address, broadcast address, usable host count, first/last usable host.

## Questions
1. What does `192.168.1.0/24` mean?
2. Why is `192.168.1.1` often the gateway?
3. How is a DNS server different from a gateway?
4. What is a default route?
5. Why does a more-specific route win over the default route?
6. How would you split DHCP and static IPs in a small lab network?

## Notes Checklist
- Paste the route table and mark the default route.
- Paste DNS server output and identify which interface it belongs to.
- Calculate one `/24`, one `/20`, and one `/30` subnet.
- Draft a DHCP/static split for a small personal lab.

## Work Mapping
This maps to designing home labs, fixing wrong-route bugs, understanding VPN route changes, and knowing why an internal service is reachable from one network but not another.

## Next Week
Week02 asks what local diagnostics prove and what they do not prove.

