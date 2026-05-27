# Lab Template

Every weekly lab uses the same structure so the project remains systematic.

## Concept Model

Where this week fits in the request path:

```text
Application Intent
-> Name Resolution
-> Connection
-> Secure Transport
-> Application Protocol
-> Proxy/Gateway
-> Concurrency & Backpressure
-> Failure Handling
-> Observability
-> Packet-Level Verification
```

## Code Lab

Run the smallest Python implementation that demonstrates the concept.

## Failure Lab

Trigger at least one failure and classify it with:

```powershell
python -m netlab fault classify <scenario>
```

## Wireshark Lab

Capture only the traffic needed for the concept. Keep capture filters narrow and write the display filter in `notes.md`.

## Work Mapping

Map the concept back to cloud services, distributed calls, or local model serving. The scenario is evidence for the concept, not the organizing principle.
