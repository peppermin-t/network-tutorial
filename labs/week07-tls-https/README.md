# Week 07 - TLS and HTTPS

## Goal
Understand TLS after TCP and before HTTP application data: certificate validation, CA trust, hostname matching, SNI, ALPN, and encrypted payloads.

## Why this matters
HTTPS can fail after TCP connects but before any HTTP status exists. That distinction is essential for APIs, gateways, VPN resources, and internal certificates.

## Where this fits
Week06 covered HTTP in cleartext. Week07 wraps it in TLS before Week08 proxy/gateway behavior.

## Before You Run: Concepts
Read [TLS](../../docs/concepts.md#tls), [HTTP](../../docs/concepts.md#http), [DNS](../../docs/concepts.md#dns), and [Closed, Filtered, Refused](../../docs/concepts.md#closed-filtered-refused).

## Run
```powershell
python labs/week07-tls-https/experiment.py
python -m netlab client https --host example.com --path /
```

## Observe
- Cipher negotiated by Python `ssl`.
- Certificate validation behavior.
- SNI uses the connection hostname; HTTP `Host` is inside the encrypted request.
- Packet capture can show IPs, ports, handshake metadata, SNI in many TLS 1.2/1.3 cases, and encrypted application data, but not HTTP body plaintext.

## Questions
1. Why can TCP connect but TLS still fail?
2. How is certificate verification failure different from HTTP 500?
3. How are SNI and HTTP Host different?
4. What does TLS hide from packet capture?
5. What does TLS not hide?

## Notes Checklist
- Record cipher and endpoint used.
- Write a failure ladder: DNS -> TCP -> TLS -> HTTP.
- Explain SNI vs Host in your own words.
- List what packet capture can and cannot show.

## Work Mapping
This maps to HTTPS APIs, corporate/internal certificates, reverse proxies, model gateways with TLS termination, and certificate mismatch debugging.

## Next Week
Week08 introduces proxies, gateways, timeouts, retries, and failure classification.

