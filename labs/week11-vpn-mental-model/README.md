# Week 11 - VPN Mental Model

Focus: VPN = virtual interface + route table + encrypted tunnel + DNS policy.

This is an optional extension lab. It does not build or configure a VPN, does not provide proxy nodes or bypass instructions, and does not change system network settings. Use it only with networks and VPNs you are authorized to access.

## Before You Run: Concepts

- `VPN tunnel`: selected traffic carried through an encrypted path. See `docs/concepts.md#vpn-tunnel`.
- `Virtual interface`: software network interface used by VPN clients. See `docs/concepts.md#virtual-interface`.
- `Route table`: decides which path a destination IP uses. See `docs/concepts.md#route-table`.
- `Full tunnel`: most traffic goes through VPN. See `docs/concepts.md#full-tunnel`.
- `Split tunnel`: only selected routes go through VPN. See `docs/concepts.md#split-tunnel`.
- `DNS policy`: resolver behavior may change with VPN state. See `docs/concepts.md#dns-policy`.
- `VPN outer traffic vs inner traffic`: physical captures may show encrypted tunnel packets, not inner HTTP. See `docs/concepts.md#vpn-outer-traffic-vs-inner-traffic`.

## If You Are Confused

- If VPN changes DNS behavior, read `route table`, `full tunnel`, `split tunnel`, and `DNS policy`.
- If internal names fail but public names work, classify the symptom as DNS policy first.
- If DNS works but TCP times out, inspect route table and default route next.
- If packet capture does not show HTTP after VPN connects, remember you may be seeing outer tunnel traffic.

## Run

Before connecting to an authorized VPN:

```powershell
$env:PYTHONPATH="src"
python labs/week11-vpn-mental-model/experiment.py
```

Save the output in `notes.md` under "Before VPN snapshot". Then connect to your authorized VPN and run the same command again. Save that output under "After VPN snapshot".

## Read-Only Commands

The helper prints and attempts a small safe subset of these commands. Commands marked as optional may be slower or more environment-specific, so run them manually only if useful.

Windows / PowerShell:

```powershell
route print
ipconfig /all
nslookup example.com
tracert example.com
netstat -rn
Get-NetRoute
Get-DnsClientServerAddress
Resolve-DnsName example.com
```

Linux:

```bash
ip route
resolvectl dns
dig example.com
traceroute example.com
```

macOS:

```bash
netstat -rn
scutil --dns
dig example.com
traceroute example.com
```

## Before / After Template

- Before VPN snapshot
- After VPN snapshot
- Default route changed?
- DNS server changed?
- Internal domain resolves?
- Public domain resolves differently?
- Traceroute changed?
- Which traffic likely uses the tunnel?
- Which traffic likely does not?

## What To Learn

- VPN is not a magic switch. It changes the inputs that DNS, routing, TCP, TLS, and HTTP depend on.
- Full tunnel usually changes the default route and often DNS.
- Split tunnel usually adds specific internal routes and may still change DNS policy.
- VPN problems often present as DNS failure, TCP timeout, TLS failure, HTTP failure, or changed public egress behavior.
- On the physical NIC, packet capture usually shows VPN outer tunnel traffic. Inner traffic may be visible only on a virtual interface, depending on OS and permissions.

## Systematic Template

- Concept Model: DNS policy + route table + virtual interface + encrypted outer tunnel.
- Code Lab: Run the snapshot helper before and after VPN.
- Failure Lab: Classify the symptom without changing network settings.
- Wireshark Lab: Compare expected visibility on physical NIC versus virtual interface.
- Work Mapping: Remote lab servers, internal model serving, private package indexes, vector DBs, and company-only DNS names.
