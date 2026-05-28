# Week 11 - VPN and Remote Access Mental Model

## Goal
Understand VPN as virtual interface plus route table plus encrypted tunnel plus DNS policy, without configuring or bypassing anything.

## Why this matters
Remote access often changes both where packets go and which resolver answers names. A connected VPN does not automatically prove internal services are reachable.

## Where this fits
Week01 route/DNS facts, Week05 DNS, Week07 TLS, and Week10 namespace thinking all combine here.

## Before You Run: Concepts
Read [VPN](../../docs/concepts.md#vpn), [Default Route](../../docs/concepts.md#default-route), [More-Specific Route](../../docs/concepts.md#more-specific-route), [DNS](../../docs/concepts.md#dns), and [TLS](../../docs/concepts.md#tls).

## Run
```powershell
python labs/week11-vpn-remote-access/experiment.py
```

Optional workflow: run it before and after connecting to an authorized VPN, then compare route and DNS snapshots. Do not modify settings from this tutorial.

## Observe
- Route table changes: full tunnel versus split tunnel clues.
- DNS server or resolver policy changes.
- Virtual adapter/interface presence.
- Outer encrypted tunnel traffic versus inner application traffic.
- MTU/MSS as a later hypothesis, not a first guess.

## Questions
1. Why can VPN change DNS and route table behavior?
2. What is the difference between full tunnel and split tunnel?
3. Why can an internal domain still fail after VPN connects?
4. Why might physical-interface capture not show inner HTTP?
5. When would MTU/MSS become a hypothesis?

## Notes Checklist
- Paste before/after route table snapshots if available.
- Paste before/after DNS snapshots if available.
- Identify full-tunnel or split-tunnel clues.
- Write a remote-access failure checklist.

## Work Mapping
This maps to company VPNs, home lab remote access, internal AI services, private DNS zones, certificate names, and debugging "VPN connected but service unreachable."

## Next Week
Week12 combines design, gateway, streaming, metrics, traces, load, and failure checklists.

