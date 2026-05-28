# Week 00 - Orientation, Layering, and Tools

## Goal
Build the learning map before writing sockets: what layer to suspect, what tool to use, and how to keep notes that turn experiments into engineering intuition.

## Why this matters
Most network debugging gets stuck because DNS, routing, TCP, TLS, HTTP, proxy, and application failures are mixed together. This week gives you the vocabulary to separate them.

## Where this fits
This is the entry point for the whole tutorial. Week01 starts the concrete foundation with IP, routing, and subnetting.

## Before You Run: Concepts
Read [Orientation / Layering](../../docs/concepts.md#orientation--layering), [Observability](../../docs/concepts.md#observability), and [Network Design](../../docs/concepts.md#network-design).

## Run
```powershell
python -m netlab doctor
python -m netlab path tutorial
python -m netlab capture status
```

If TShark is installed, print a capture command without running it:

```powershell
python -m netlab capture command --interface "YOUR_INTERFACE" --output captures/week00.pcapng --filter "tcp port 9001" --packets 20
```

## Observe
- `doctor` output: Python version, platform, optional TShark/Docker availability.
- Tutorial path: how Week00-Week12 builds from local network facts to capstone design.
- Capture command shape: interface, capture filter, output file, packet limit.
- No command in this week should modify network settings.

## Questions
1. In `application intent -> DNS -> route -> socket -> TCP/UDP -> TLS -> HTTP -> proxy/gateway -> upstream`, which layers are visible to code?
2. Which layers can fail before the application server receives anything?
3. What is the difference between logs, metrics, command output, and packet capture evidence?
4. What would you write down after every lab so the result is reusable later?

## Notes Checklist
- Your current OS, Python version, and whether TShark/Docker are available.
- A one-line definition of each practical layer in your own words.
- Your preferred packet capture interface, if known.
- Three network problems you want this tutorial to make easier.

## Work Mapping
This week maps to first-response debugging: deciding whether a broken model endpoint, internal service, proxy, Docker app, or VPN resource is failing at name resolution, path selection, transport, encryption, protocol, gateway, capacity, or application logic.

## Next Week
Week01 turns the map into concrete local facts: IP address, subnet, gateway, route table, and DNS server.

